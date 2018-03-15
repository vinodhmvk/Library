import pandas as pd
import numpy as np
from app import app, db
#from db_setup import init_db, db_session
from forms import BookSearchForm, BookForm, Borrow
from flask import flash, render_template, request, redirect, url_for
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
from sqlalchemy import Column, Date, Integer, String

login = LoginManager()
login.init_app(app)
login.login_view = 'login'

from datetime import datetime
from tables import Results, MyBooks, Borrowed_Books, df_MyBooks
from models import User, Book, Book_History
from login import LoginForm
from werkzeug.urls import url_parse

#init_db()
@app.route('/', methods=['GET', 'POST'])
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

last_search = BookSearchForm(search='')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    search = BookSearchForm(request.form)
    last_search = search
    if request.method == 'POST':
        return search_results(search)
 
    return render_template('index.html', form=search)
 

@app.route('/results')
def search_results(search = None):
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
def mybooks():
    results = []
    qry = db.session.query(Book).filter(
        Book.lender.contains(current_user.username))

    results = qry.all()
 
    if not results:
        flash("Sorry, You don't have books. Please add the books you want to lend in New Book")
        return redirect('/index')
    else:
        # display results
        table = MyBooks(results)
        table.border = True
        return render_template('mybooks.html', table=table)

@app.route('/borrowed_books')
@login_required
def borrowed_books():
    results = []
    qry = db.session.query(Book_History).filter(
        Book_History.borrower.contains(current_user.username)
        &(Book_History.status.contains('Borrowed')))

    results = qry.all()
 
    if not results:
        flash("You have not borrowed any books at this point")
        return redirect('/index')
    else:
        # display results
        books = []
        for book_his in results:
            books.append(db.session.query(Book).filter(
                Book.id==book_his.book_id).first())
        table = Borrowed_Books(books)
        table.border = True
        return render_template('borrowed_books.html', table=table)

@app.route('/lended_books')
@login_required
def Lended_books():
    results = []
    qry = db.session.query(Book).filter(
        Book.lender.contains(current_user.username)
        &(Book.current_status.contains('Borrowed')))

    results = qry.all()
 
    if not results:
        flash("No Books of has been borrowed at this point")
        return redirect('/index')
    else:
        # display results
        table = Borrowed_Books(results)
        table.border = True
        return render_template('borrowed_books.html', table=table)

def add_book_history(book, user, book_status):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    book_history = Book_History(book_id=book.id,
        book_name = book.book_name, borrowee = current_user, 
        status = book_status, borrow_time=datetime.utcnow())
    db.session.add(book_history)
    db.session.commit() 
    if book_status == 'Added':
        book.current_status = 'Avaiable'
    else:
        book.current_status = book_status +" by " + current_user.username.upper()
    db.session.commit() 

@app.route('/borrow/<int:id>', methods=['GET', 'POST'])
@login_required
def borrow(id):
    qry = db.session.query(Book).filter(
                Book.id==id)
    book = qry.first()
    book_history_qry = db.session.query(Book_History).filter(
                    Book_History.book_id.contains(book.id))
    book_history = book_history_qry.all()
    borrowed_book_qry = db.session.query(Book_History).filter(
                    (Book_History.book_id.contains(book.id))&
                    (Book_History.status.contains('Borrowed'))) 
    borrowed_book = borrowed_book_qry.first()    
    if borrowed_book:
        if book.lender == current_user.username:      
            if request.method == 'POST':
                borrowed_book.status='Returned'
                borrowed_book.borrow_time=datetime.utcnow()
                db.session.add(borrowed_book)
                db.session.commit()
                book.current_status = 'Avaiable'
                db.session.commit() 
                flash('Book is made available for others to borrow')
                return redirect('/mybooks')
            message = """If {} has returned the book press the Returned 
                button to make it Available""".format(borrowed_book.borrower.upper())
            return render_template('borrow.html', key='Returned', message = message)
        else:
            flash(borrowed_book.book_name+' has been already Borrowed by ' + borrowed_book.borrower.upper())
            return search_results(last_search)

    else:
        if book.lender == current_user.username or book_history is None:
            flash('At Present No one has borrowed this book')
            return redirect('/mybooks')  
        else:  
            if request.method == 'POST': 
                add_book_history(book, current_user, 'Borrowed') 
                      
                flash('Collect the book from '+book.lender.upper())
                return redirect('/index')
            message = """Press the borrow button and collect the 
                    book from {}""".format(book.lender.upper())
            return render_template('borrow.html', key='Borrow', message = message)

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
        add_book_history(book, current_user, 'Added')
        #save_changes(book, form, new=True)
        flash('Book added successfully!')
        return redirect('/mybooks')
    return render_template('new_book.html', form=form)

def save_changes(book, form, user, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    login = LoginForm()
    book.lendee = current_user
    book.book_name = form.book_name.data
    book.author = form.author.data
    book.genre = form.genre.data
    book.summary = form.summary.data

 
    if new:
        # Add the new book to the database
        db.session.add(book)
 
    # commit the data to the database
    db.session.commit()

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
            save_changes(book, form, current_user)

            flash('Book updated successfully!')
            return redirect('/mybooks')
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
            return redirect('/mybooks')
        return render_template('delete_book.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)

if __name__ == '__main__':
    app.run()