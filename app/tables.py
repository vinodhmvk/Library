import pandas as pd
import numpy as np
from flask_table import Table, Col, LinkCol
 
class Results(Table):
    id = Col('Id', show=False)
    lender = Col('Lender')
    book_name = Col('Book Name')
    author = Col('Author of the Book')
    genre = Col('Genre')
    summary = Col('Summary')
    borrow = LinkCol('Borrow', 'borrow', url_kwargs=dict(id='id'))
    current_status = Col('Status')
    #edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
    #delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='id'))

class MyBooks(Table):
    id = Col('Id', show=False)
    lender = Col('Lender')
    book_name = Col('Book Name')
    author = Col('Author of the Book')
    genre = Col('Genre')
    summary = Col('Summary')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='id'))
    status = LinkCol('Returned', 'borrow', url_kwargs=dict(id='id'))
    current_status = Col('Status')

class Borrowed_Books(Table):
    id = Col('Id', show=False)
    lender = Col('Lender')
    book_name = Col('Book Name')
    author = Col('Author of the Book')
    genre = Col('Genre')
    summary = Col('Summary')

def df_MyBooks(Results):
    heads=['Lender', 'Book Name', 'Author of the Book', 'Genre', 'Summary']
    df_list = []
    for book in Results:
        temp_list = [book.lender,book.book_name,book.author,book.genre,book.summary]
        df_list.append(temp_list)
    return pd.DataFrame(df_list, columns=heads)

