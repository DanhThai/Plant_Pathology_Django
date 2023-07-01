import cv2
import numpy as np
from tensorflow.keras.models import load_model

class PlantDiseases():
    def __init__(self, path):
        self.model = load_model(path)

    def predict(self, image_url, w = 224, h = 224, score = 0.8):
        # image_url = './media/predicts/image_predict.jpg'
        img = cv2.imread(image_url)
        img = np.asarray(img)/255.0
        
        img = cv2.resize(img, (w, h)).astype(np.float32)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        img = img.reshape((1, w, h, 3))
        result = self.model.predict(img)
        idx = np.argmax(result, axis=1)[0]
        print('predict score class {}: {}'.format(idx, result[0, idx]))
        return idx + 1 if result[0, idx] > score else 0
