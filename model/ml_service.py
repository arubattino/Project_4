import time
import settings
import redis
import json
import numpy as np
import os


from tensorflow.keras.applications  import resnet50
from tensorflow.keras.preprocessing import image


# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.


db = redis.Redis(
    host= settings.REDIS_IP,
    port= settings.REDIS_PORT,
    db= settings.REDIS_DB_ID
)

# Load your ML model and assign to variable `model`
model = resnet50.ResNet50(include_top=True, weights="imagenet")


def predict(image_name):
   
    var = image.load_img(os.path.join(settings.UPLOAD_FOLDER, image_name), 
                                target_size=(224, 224))

    imagetoarray = image.img_to_array(var)

    imagetoarray = np.expand_dims(imagetoarray, axis=0)

    imagetoarray = resnet50.preprocess_input(imagetoarray)

    predictions = model.predict(imagetoarray)

    res = resnet50.decode_predictions(predictions, top=1)

    clas = str(res[0][0][1])

    sco = round(float(res[0][0][2]), 4)


    return clas, sco


def classify_process():
    
    while True:
        #   1. Take a new job from Redis
        _, msg = db.brpop("tp")

        msg = json.loads(msg)
        
        #   2. Run model on provided data
        pred_class, pred_score = predict(msg["image_name"])

        #   3. Store the model prediction in a dict with the following form:
        #      {
        #         "prediction": str,
        #         "score": float,
        #      }
        dic = {"prediction": pred_class,
                "score": pred_score}

        #   4. Store the results in Redis using the original job id as a key so that the API

        dic = db.set(msg["id"], json.dumps(dic))

        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    print("Launching ML service...")
    classify_process()
