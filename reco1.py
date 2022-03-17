from scipy.spatial.distance import cosine
import numpy as np
import cv2
import mtcnn
from keras.models import load_model
import keras
import tensorflow as tf
from utils import get_face, plt_show, get_encode, load_pickle, l2_normalizer
from flask import jsonify


encoder_model = 'facenet_keras.h5'
people_dir = 'data/people'
encodings_path = 'encodings.pkl'
# test_img_path = 'data/test/IMG_20160620_165511.jpg'
# test_img_path = 'Newfolder/picture_out.jpg'
test_res_path = 'Newfolder/picture_out1.jpg'

config = tf.ConfigProto(
device_count={'GPU': 1},
intra_op_parallelism_threads=1,
allow_soft_placement=True
)

config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.6

session = tf.Session(config=config)
keras.backend.set_session(session)

# model = load_model(encoder_model)

recognition_t = 0.3
required_size = (160, 160)

encoding_dict = load_pickle(encodings_path)
face_detector = mtcnn.MTCNN()
face_encoder = load_model(encoder_model)
face_encoder._make_predict_function()

def reco (test_img_path):
    img = cv2.imread(test_img_path)
    # plt_show(img)
    # height, width, channels = img.shape
    # print (height, width)
    # graph = tf.get_default_graph()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_detector.detect_faces(img_rgb)
    if not results:
        return jsonify({'face_name' : 'Face Not Detect'})
        # return 'Face Not Detect'
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
        # return name
    # return cv2.imwrite(test_res_path, img)

    # plt_show(img)

# reco(test_img_path)
