from locust import HttpUser, task, between



class UserBehavior(HttpUser):

    wait_time = between(0.5,5)
    min_wait = 500
    max_wait = 5000
    
    @task(1)
    def index(self):
        self.client.get('http://localhost/')

    
    @task(10)
    def press_page(self):
        with open("dog.jpeg","rb") as image:
            self.client.post("http://localhost/predict", files={'file':image})