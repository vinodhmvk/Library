

"""
Book_History = db.Table("book_history",
            db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
            db.Column('book_name', db.Integer, db.ForeignKey('books.book_name')),
            db.Column('borrower', db.Integer, db.ForeignKey('users.username')),
            db.Column('status', db.String(140)),
            db.Column('borrow_time', db.DateTime, index=True, default=datetime.utcnow))


class Lender(db.Model):
    __tablename__ = "lenders"
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
"""
USER_DICT = {'varun':'vnathan@kabbage.com',
        'ravi':'rchahar@kabbage.com',
        'nitin':'nrawat@kabbage.com'}
for name, mailid in USER_DICT.items():
    u = User(username=name, email=mailid)
    u.set_password(name)
    db.session.add(u)
    db.session.commit()