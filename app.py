import os
from flask import Flask, request
from werkzeug.utils import secure_filename
from db import db_init, db
from model import Img, Img1
from PIL import Image
from io import BytesIO
from Recognition import Recognition
import json
from prepare_data import Prepare_data
# import logging 
# 
# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.debug)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(os.getcwd(), 'img.sqlite3')
app.config['SQLALCHEMY_BINDS'] = {'db2': 'sqlite:///' + os.path.join(os.getcwd(), 'img1.sqlite3'),
                                  }
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db_init(app)


@app.route('/', methods=['GET', 'POST'])
def upload1():
    return "as.,xnvkx.cvnxfas"


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if(request.method == 'POST'):
        imagefile = request.files['image']
        print(imagefile)
        if not imagefile:
            print('No pic uploaded!')
            return 'No pic uploaded!', 400

        filename = secure_filename(imagefile.filename)
        mimetype = imagefile.mimetype
        if not filename or not mimetype:
            print('No pic uploaded!')
            return 'Bad upload!', 400

        img = Img(img=imagefile.read(), name=filename, mimetype=mimetype)
        try:

            db.session.add(img)
            db.session.commit()
            rows = Img.query.filter().count()
            print(rows)
            print('Img Uploaded!')
            return get_img(rows)
        except:
            print('Img Fail!')
            return 'Img Fail!'


@app.route('/add', methods=['GET', 'POST'])
def add():
    if(request.method == 'POST'):
        imagefile_add1 = request.files['image']
        print(imagefile_add1)
        if not imagefile_add1:
            print('No pic uploaded!')
            return 'No pic uploaded!', 400

        filename_add1 = secure_filename(imagefile_add1.filename)
        print(filename_add1)
        mimetype_add1 = imagefile_add1.mimetype
        if not filename_add1 or not mimetype_add1:
            print('No pic uploaded!')
            return 'Bad upload!', 400

        img_add1 = Img1(img=imagefile_add1.read(),
                        name=filename_add1, mimetype=mimetype_add1)
        path1 = os.path.join(os.getcwd(), filename_add1)
        print(path1)
        try:
            db.session.add(img_add1)
            db.session.commit()
            print('Img Uploaded!')
            get_img12(filename_add1)
            return 'Img Uploaded!', 200
        except:
            db.session.rollback()
            print('Img Fail!')
            return 'Img Fail!', 400


def get_img12(upload_id1):
    v = 0
    upload1 = Img1.query.filter_by(id=upload_id1).first()
    upload = Img1.query.filter(Img1.name.like(upload_id1)).all()
    print(len(upload))
    cv = []
    for i in range(0, len(upload)):
        xc = str(upload[i])
        print(xc)
        update_name = xc.replace("<Img1 ", "")
        update_name1 = int(update_name.replace(">", ""))
        cv.append(update_name1)
        print(type(update_name1))
        print(cv)
    update_name = upload_id1.replace(".jpg", "")
    print(update_name)
    try:
        os.mkdir(update_name)
    except OSError as error:
        print(error)

    for i in cv:
        upload1 = Img1.query.filter_by(id=i).first()
        vb1 = BytesIO(upload1.img)
        img2 = Image.open(vb1)
        v = v+1
        path12 = os.path.join(os.getcwd(), update_name)
        img2.save(os.path.join(path12, f"savan{v}.jpg"))

    update_name = upload_id1.replace(".jpg", "")
    print(update_name)

    return Prepare_data(path12, update_name)


def get_img(upload_id):
    upload = Img.query.filter_by(id=upload_id).first()
    from PIL import Image
    vb = BytesIO(upload.img)
    img1 = Image.open(vb)
    img1.save(os.path.join(os.getcwd(), 'picture_out.jpg'))
    path = os.path.join(os.getcwd(), 'picture_out.jpg')
    return Recognition(path)


@app.route('/Totalname', methods=['GET', 'POST'])
def get_img1():
    with open('sample.json', 'r') as openfile:
        json_object = json.load(openfile)
    return (json.dumps(json_object))


if __name__ == "__main__":
    app.run()
    # app.run(debug=False   , threaded=False, port=4000)
