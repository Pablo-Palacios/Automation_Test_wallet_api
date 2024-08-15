from locust import HttpUser, task, between

"""
Locust for load tests, now its configured for two users, one to request the list of clients and a client in particular and one client to get his own data
to run do cd backend/testing, and then on the console > locust then open http://localhost:8089 for the graphic UI and start the tests 

"""

admin_email = "agent@diglo.com"
user_email = "puigdiuca@gmail.com"

clients_endpoint = "clients"


class AgentUser(HttpUser):
    once = False
    wait_time = between(0.5, 1)
    headers = {
            "email": admin_email
        }
    # def on_start(self):
    #     self.login()

    # def login(self):
        

    #     # Send a POST request to the login endpoint
    #     response = self.client.post("/login", {"user_email":admin_email},headers=headers,)

    #     # Check if the login was successful (you may need to adjust this based on your application's response)
    #     if response.status_code == 200:
    #         print("Login successful")
    #         # Set the flag to indicate that the user is logged in
    #         self.logged_in = True
    #         session_cookies = response.cookies.get_dict()
    #         print(response.headers)
    #         print(session_cookies)

    @task
    def list_clients(self):
                self.client.get(f"/{clients_endpoint}/list?page=0&size=10&order[]=name&order[]=asc&filters[name]=&filters[action]=all", headers=self.headers)
    @task
    def get_client(self):
                self.client.get(f"/{clients_endpoint}/w-706",headers=self.headers)


class ClientUser(HttpUser):

    headers = {
                "email": user_email
            }
    @task
    def get_me(self):
                self.client.get(f"/{clients_endpoint}/me",headers=self.headers)