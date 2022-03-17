from pickle import FALSE
from matplotlib import image
import numpy as np
import werkzeug
from flask import Flask, request, send_file, render_template, Response, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from db import db_init, db, db_init1, db1
from model import Img, Img1
from io import BytesIO
import socket
# from reco1 import reco
import json
import cv2
# from prepare_data import addpd
# server_socket = socket.socket()
# server_socket.bind(('0.0.0.0', 4000))
# server_socket.listen(0)
# connection = server_socket.accept()[0].makefile('rb')
app = Flask(__name__)
# db_init(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db_init(app)

app1 = Flask(__name__)

app1.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img1.sqlite3'
app1.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db_init1(app1)

@app.route('/', methods=['GET', 'POST'])
def upload1():
    return "as.,xnvkx.cvnxfas"

@app.route('/upload', methods=['GET','POST'])
def upload(): 
    if(request.method == 'POST'):
        imagefile = request.files['image']
        print(imagefile)
        if not imagefile:
            print('No pic uploaded!')
            return 'No pic uploaded!', 400

        filename = secure_filename(imagefile.filename)
        # filename1 = werkzeug.utils.secure_filename(imagefile.filename)
        # imagefile.save("./data/" + filename1)
        mimetype = imagefile.mimetype
        if not filename or not mimetype:
            print('No pic uploaded!')
            return 'Bad upload!', 400

        img = Img(img=imagefile.read(), name=filename, mimetype=mimetype)
        # imagefile.save(r'C:\Users\sutar\Downloads\Face-master\_03_facenet_keras\Newfolder' + filename)
        try:

            db.session.add(img)
            db.session.commit()
            rows = Img.query.filter().count()
            print(rows)
            print('Img Uploaded!')
            return get_img(rows)
            # return 'Img Uploaded!', 200
        except:
            # rows = Img.query.filter().count()
            # print(rows)
            print('Img Fail!')    
            return 'Img Fail!'
                #     return jsonify({
            #     "message":  "asfas"
            # })  
# @app.route('/asd')    
# def get_img():
#     pass

@app.route('/add', methods=['GET','POST'])
def add():
    if(request.method == 'POST'):
        imagefile_add = request.files['image']
        print(imagefile_add)
        # addig = imagefile_add.read()
        if not imagefile_add:
            print('No pic uploaded!')
            return 'No pic uploaded!', 400

        filename_add = secure_filename(imagefile_add.filename)
        # filename_add = werkzeug.utils.secure_filename(imagefile_add.filename)
        # imagefile.save("./data/" + filename1)
        mimetype_add = imagefile_add.mimetype
        if not filename_add or not mimetype_add:
            print('No pic uploaded!')
            return 'Bad upload!', 400

        img_add = Img(img=imagefile_add.read(), name=filename_add, mimetype=mimetype_add)
        # imagefile_add.save(filename_add)
        path1 = r'C:\Users\sutar\Downloads\Face-master\_03_facenet_keras\Newfolder'+ filename_add
        try:

            db.session.add(img_add)
            db.session.commit()
            print('Img Uploaded!')
        # addpd(path1,filename_add)
        # print('Img Uploaded!')
            return 'Img Uploaded!', 200 
        except :
            print('Img Fail!') 
            # return 'Img Fail!', 400
                #     return jsonify({
            #     "message":  "asfas"
            # })

@app.route('/<upload_id>', methods=['GET', 'POST'])    
def get_img(upload_id): 
    upload = Img.query.filter_by(id=upload_id).first()
    # path = r'C:\Users\sutar\Downloads\Face-master\_03_facenet_keras\Newfolder'
    from PIL import Image
    vb = BytesIO(upload.img)
    # xc = send_file(BytesIO(upload.img), attachment_filename=upload.name, as_attac hment=True )
    # with open('picture_out.jpg', 'wb') as f:
    # vb.write(connection.read(vb))
    vb.seek(0)
    img1=Image.open(vb)
    image = np.asarray(bytearray(vb.read()), dtype="uint8")
    image = cv2.imdecode(img1, cv2.IMREAD_COLOR)
    cv2.imwrite("result.jpg", image)
    img1.save('picture_out.jpg')
    path = 'C:/Users/sutar/Downloads/Face-master/_03_facenet_keras/picture_out.jpg'
    # return reco(path)
 
@app.route('/Totalname', methods=['GET', 'POST'])    
def get_img1():
    data =['Savan','Ravi','rakesh','akshay','hiren','rahul']
    return (json.dumps(data)) 

if __name__ == "__main__":
    app.run(debug=False, threaded=False, port=4000)
    # app.run()
