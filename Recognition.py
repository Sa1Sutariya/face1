import os
from scipy.spatial.distance import cosine
import numpy as np
import cv2
import mtcnn
from keras.models import load_model
from utils import get_face, load_json, get_encode, l2_normalizer
from flask import jsonify
import logging

encoder_model = 'facenet_keras.h5'
encodings_path = 'encodings.json'
test_img_path = os.path.join(os.getcwd(), 'picture_out.jpg')
test_res_path = 'picture_out.jpg'

recognition_t = 0.3
required_size = (160, 160)
encoding_dict = load_json(encodings_path)
face_detector = mtcnn.MTCNN()
face_encoder = load_model(encoder_model)
face_encoder._make_predict_function()
path = os.path.join(os.getcwd(), 'picture_out.jpg')

def Recognition (test_img_path):
    img = cv2.imread(test_img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_detector.detect_faces(img_rgb)
    if not results:
        return jsonify({'face_name' : 'Face Not Detect'})
        
    for res in results:
        face, pt_1, pt_2 = get_face(img_rgb, res['box'])
        encode = get_encode(face_encoder, face, required_size)
        encode = l2_normalizer.transform(np.expand_dims(encode, axis=0))[0]

        name = 'Unknown'
        distance = float("inf")

        for db_name, db_encode in encoding_dict.items():
            dist = cosine(db_encode, encode)
            if dist < recognition_t and dist < distance:
                name = db_name
                distance = dist
        return jsonify({'face_name' : name})
