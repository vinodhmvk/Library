from flask_table import Table, Col, LinkCol
 
class Results(Table):
    id = Col('Id', show=False)
    lender = Col('Lender')
    book_name = Col('Book Name')
    author = Col('Author of the Book')
    genre = Col('Genre')
    summary = Col('Summary')
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