from db import db, db1


# class Img(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     img = db.Column(db.String(50))
#     name = db.Column(db.LargeBinary)
#     # mimetype = db.Column(db.Text, nullable=False)

class Img1(db1.Model):
    id1 = db1.Column(db1.Integer, primary_key=True)
    # img = db.Column(db.Text, nullable=False)
    img1 = db1.Column(db1.Text, unique=True, nullable=False)
    name1 = db1.Column(db1.Text, nullable=False)
    mimetype1 = db1.Column(db1.Text, nullable=False)

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # img = db.Column(db.Text, nullable=False)
    img = db.Column(db.Text, unique=False, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
