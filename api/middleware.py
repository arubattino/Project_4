import time
import settings
import redis
import uuid
import json

# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.

db = redis.Redis(
    host= settings.REDIS_IP,
    port= settings.REDIS_PORT,
    db= settings.REDIS_DB_ID
)


def model_predict(image_name):
    
    # Assign an unique ID for this job and add it to the queue.

    job_id = str(uuid.uuid4())

    job_data = {"id":job_id, "image_name":image_name}#None

    job_data_str = json.dumps(job_data)

    # Send the job to the model service using Redis
    # Hint: Using Redis `rpush()` function should be enough to accomplish this.
    
    db.rpush(settings.REDIS_QUEUE, job_data_str)
    
    while True:
        # Attempt to get model predictions using job_id
        # Hint: Investigate how can we get a value using a key from Redis

        output = db.get(job_data['id'])

        if output != None:
            output = json.loads(output)

            db.delete(job_data['id'])
            break

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)

    return output['prediction'], output['score']
