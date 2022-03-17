from flask_sqlalchemy import SQLAlchemy
import sqlite3

db = SQLAlchemy()
db1 = SQLAlchemy()


# Function that initializes the db and creates the tables
def db_init(app):
    db.init_app(app)

    # Creates the tables if the db doesnt already exist
    with app.app_context():
        db.create_all()

def db_init1(app):
    db1.init_app(app)

    # Creates the tables if the db doesnt already exist
    with app.app_context():
        db1.create_all()

# def fetch_data():
#     counter = 1
#     # os.chdir("/Users/soumilshah/IdeaProjects/Youtube/images")
#     conn = sqlite3.connect("img.db")
#     cursor = conn.cursor()

#     data = cursor.execute("""SELECT * FROM my_table""")
#     for x in data.fetchall():
#         print(x[1])
#         with open("{}.png".format(counter),"wb") as f:
#             f.write(x[1])
#             counter= counter + 1


#     conn.commit()
#     cursor.close()
#     conn.close()
