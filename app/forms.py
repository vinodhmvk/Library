from wtforms import Form, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class BookSearchForm(Form):
    choices = [('Lender', 'Lender'),
                ('Book Name', 'Book Name'),
               ('Author', 'Author'),
               ('Genre', 'Genre')]
    select = SelectField('Search for Books:', choices=choices)
    search = StringField('')

class BookForm(Form):
    lender = StringField('Lender')
    book_name = StringField('Book Name', validators=[DataRequired()])
    author = StringField('Author of the Book', validators=[DataRequired()])
    genre = StringField('Genre')
    summary = StringField('Summary of the Book')
    
class Borrow(Form):
    borrow = SubmitField(label='Change')
