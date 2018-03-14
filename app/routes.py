from app import app, db
from db_setup import init_db, db_session
from forms import BookSearchForm, BookForm
from flask import flash, render_template, request, redirect, url_for
from flask_login import LoginManager, logout_user, login_required, login_user, current_user

login = LoginManager()
login.init_app(app)
login.login_view = 'login'

from tables import Results, MyBooks
from models import User, Book, Lender, Book_History
from login import LoginForm
from werkzeug.urls import url_parse

init_db()

@app.route('/login', methods=['GET', 'POST'])
def login():
    #if current_user.is_authenticated:
    #    return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        if user.check_password(form.password.data):
            return redirect(url_for('index'))
        #next_page = request.args.get('next')
        #if not next_page or url_parse(next_page).netloc != '':
        #    next_page = url_for('index')
        #return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    search = BookSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
 
    return render_template('index.html', form=search)
 
 
@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
 
    if search_string:
        if search.data['select'] == 'Lender':
            qry = db.session.query(Book).filter(
                    Book.lender.contains(search_string))
            results = qry.all()        
        elif search.data['select'] == 'Book Name':
            qry = db.session.query(Book).filter(
                    Book.book_name.contains(search_string))
            results = qry.all()
        elif search.data['select'] == 'Author':
            qry = db.session.query(Book).filter(
                Book.author.contains(search_string))
            results = qry.all()
        elif search.data['select'] == 'Genre':
            qry = db.session.query(Book).filter(
                Book.genre.contains(search_string))
            results = qry.all()
        else:
            qry = db.session.query(Book)
            results = qry.all()
    else:
        qry = db.session.query(Book)
        results = qry.all()
 
    if not results:
        flash('No results found!')
        return redirect('/index')
    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)

@app.route('/mybooks')
@login_required
def mybooks(search):
    results = []
    qry = db.session.query(Book).filter(
        Book.lender.contains(current_user.username.data))

    results = qry.all()
 
    if not results:
        flash("Sorry, You haven't added. Please add the books you want to lend in Add book")
        return redirect('/index')
    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('mybooks.html', table=table)


def save_changes(book, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    login = LoginForm()
    book.lender = form.lender.data
    book.book_name = form.book_name.data
    book.author = form.author.data
    book.genre = form.genre.data
    book.summary = form.summary.data

 
    if new:
        # Add the new book to the database
        db.session.add(book)
 
    # commit the data to the database
    db.session.commit()

@app.route('/new_book', methods=['GET', 'POST'])
@login_required
def new_book():
    """
    Add a new book
    """
    form = BookForm(request.form)
    if request.method == 'POST' and form.validate():
        # save the book
        book = Book(book_name=form.book_name.data, 
            author = form.author.data, genre = form.genre.data,
            summary = form.summary.data, lendee=current_user)
        db.session.add(book)
        db.session.commit()
        #save_changes(book, form, new=True)
        flash('Book added successfully!')
        return redirect('/index')
    return render_template('new_book.html', form=form)
 
@app.route('/item/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    qry = db.session.query(Book).filter(
                Book.id==id)
    book = qry.first()
 
    if book:
        form = BookForm(formdata=request.form, obj=book)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(book, form)
            flash('Book updated successfully!')
            return redirect('/')
        return render_template('edit_book.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    """
    Delete the item in the database that matches the specified
    id in the URL
    """
    qry = db.session.query(Book).filter(
        Book.id==id)
    book = qry.first()
 
    if book:
        form = BookForm(formdata=request.form, obj=book)
        if request.method == 'POST' and form.validate():
            # delete the item from the database
            db.session.delete(book)
            db.session.commit()
 
            flash('Book deleted successfully!')
            return redirect('/index')
        return render_template('delete_book.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)

if __name__ == '__main__':
    app.run()