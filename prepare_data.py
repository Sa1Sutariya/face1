import ast
import json
import os
import numpy as np
import cv2
import mtcnn
from keras.models import load_model
from utils import get_face, l2_normalizer, load_json, normalize

class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
# hyper-parameters
encoder_model = 'facenet_keras.h5'

encodings_path = os.path.join(os.getcwd(), 'encodings.json')
required_size = (160, 160)

face_detector = mtcnn.MTCNN()
face_encoder = load_model(encoder_model)

encoding_dict = dict()

def Prepare_data(img_path,person_name):
    for person_name1 in os.listdir(img_path):
        person_dir = os.path.join(img_path, person_name1)

    encodes = []
    img = cv2.imread(person_dir)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_detector.detect_faces(img_rgb)
    if results:
        res = max(results, key=lambda b: b['box'][2] * b['box'][3])
        face, _, _ = get_face(img_rgb, res['box'])

        face = normalize(face)
        face = cv2.resize(face, required_size)
        encode = face_encoder.predict(np.expand_dims(face, axis=0))[0]
        encodes.append(encode)

    if encodes:
        encode = np.sum(encodes, axis=0)
        encode = l2_normalizer.transform(np.expand_dims(encode, axis=0))[0]
        encoding_dict[person_name] = encode

    for key in encoding_dict.keys():
        with open('sample.json', 'r') as openfile:
            json_object = json.load(openfile)
        json_object.append(key)
        asd= list(set(json_object))
        json_string = json.dumps(asd, indent = 4)
        with open("sample.json", "w") as outfile:
            outfile.write(json_string)

    for person_name1 in os.listdir(img_path):
        person_dir = os.path.join(img_path, person_name1)  
        try:
            os.remove(person_dir) 
        except:
            pass
    os.rmdir(img_path)        
       
    json_object = json.dumps(load_json(encodings_path),cls=NumpyArrayEncoder)
    Con_Dict = ast.literal_eval(json_object)
    Con_Dict.update(encoding_dict)
    json_update = json.dumps(Con_Dict,cls=NumpyArrayEncoder)

    with open(encodings_path, "w") as outfile:
        outfile.write(json_update) 
        outfile.close()   

