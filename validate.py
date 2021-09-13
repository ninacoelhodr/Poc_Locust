from locust import HttpUser, task, constant, SequentialTaskSet


class MyScript(SequentialTaskSet):

    @task
    def get_xml(self):
        result = self.client.get("/xml", name="XML")
        print(result)

    @task
    def get_json(self):
        expected_response = "Wake up to WonderWidgets!"

        with self.client.get("/json", catch_response=True, name="JSON") as response:
            result = True if expected_response in response.text else False  
            print(self.get_json.__name__, result)  
            response.success()
   
    @task
    def get_failure(self):
        expected_response = 404
        with self.client.get("/status/404", catch_response=True, name="HTTP 404") as response:
            if response.status_code == expected_response:
                response.failure("Got 404!")
            else:
                response.success()


class MyLoadTest(HttpUser):
    host = "https://httpbin.org"
    wait_time = constant(1)
    tasks = [MyScript]