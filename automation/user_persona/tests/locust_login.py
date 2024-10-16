import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import time
from locust import HttpUser,task,between, LoadTestShape
from configuracion.views_persona import https,Endpoints
from configuracion.main import password
import itertools

# COMANDOS
# locust -f locust_login.py 
# locust -f your_script.py --headless --run-time 100s
# locust -f your_script.py --headless -u 20 -r 0.2 --run-time 100s


users_dev =[
	{
		"email" : "tinahernandezdev@movilcash.com"
	},
	{
		"email" : "brianmedinadev@movilcash.com"
	},
	{
		"email" : "kellyfitzpatrickdev@movilcash.com"
	},
	{
		"email" : "nicholasjacksondev@movilcash.com"
	},
	{
		"email" : "robertdavisdev@movilcash.com"
	},
	{
		"email" : "kennethsilvadev@movilcash.com"
	},
	{
		"email" : "justinowendev@movilcash.com"
	},
	{
		"email" : "sarahreynoldsdev@movilcash.com"
	},
	{
		"email" : "jeffreyfoxdev@movilcash.com"
	},
	{
		"email" : "emmamejiadev@movilcash.com"
	},
	{
		"email" : "coryjonesdev@movilcash.com"
	},
	{
		"email" : "catherinedavenportdev@movilcash.com"
	},
	{
		"email" : "michaelschmittdev@movilcash.com"
	},
	{
		"email" : "angelicaclarkdev@movilcash.com"
	},
	{
		"email" : "tonyphillipsdev@movilcash.com"
	},
	{
		"email" : "michaeldavisdev@movilcash.com"
	},
	{
		"email" : "meganjohnsondev@movilcash.com"
	},
	{
		"email" : "geralddennisdev@movilcash.com"
	},
	{
		"email" : "suzannemcdanieldev@movilcash.com"
	},
	{
		"email" : "jenniferrogersdev@movilcash.com"
	},
	{
		"email" : "amandaspearsdev@movilcash.com"
	},
	{
		"email" : "garycollinsdev@movilcash.com"
	},
	{
		"email" : "sarahtrujillodev@movilcash.com"
	},
	{
		"email" : "sarahdominguezdev@movilcash.com"
	},
	{
		"email" : "elizabethwelchdev@movilcash.com"
	},
	{
		"email" : "marcusstewartdev@movilcash.com"
	},
	{
		"email" : "tammybrandtdev@movilcash.com"
	},
	{
		"email" : "gregorywilliamsdev@movilcash.com"
	},
	{
		"email" : "brianfoxdev@movilcash.com"
	},
	{
		"email" : "brianparkerdev@movilcash.com"
	},
	{
		"email" : "madisonwatsondev@movilcash.com"
	},
	{
		"email" : "jeffreyhaneydev@movilcash.com"
	},
	{
		"email" : "donnawallsdev@movilcash.com"
	},
	{
		"email" : "taramolinadev@movilcash.com"
	},
	{
		"email" : "michellebarnettdev@movilcash.com"
	},
	{
		"email" : "ethanalexanderdev@movilcash.com"
	},
	{
		"email" : "leroysmithdev@movilcash.com"
	},
	{
		"email" : "rhondamathewsdev@movilcash.com"
	},
	{
		"email" : "robertsmithdev@movilcash.com"
	},
	{
		"email" : "meredithgregorydev@movilcash.com"
	},
	{
		"email" : "albertgomezdev@movilcash.com"
	},
	{
		"email" : "melissamejiadev@movilcash.com"
	},
	{
		"email" : "brandyfarmerdev@movilcash.com"
	},
	{
		"email" : "michaelbradleydev@movilcash.com"
	},
	{
		"email" : "davidlopezdev@movilcash.com"
	},
	{
		"email" : "aaronsmithdev@movilcash.com"
	},
	{
		"email" : "timothyarnolddev@movilcash.com"
	},
	{
		"email" : "clintonedwardsdev@movilcash.com"
	},
	{
		"email" : "edwardjonesdev@movilcash.com"
	},
	{
		"email" : "jessicahansondev@movilcash.com"
	},
	{
		"email" : "angelashortdev@movilcash.com"
	},
	{
		"email" : "joseowendev@movilcash.com"
	},
	{
		"email" : "robertsextondev@movilcash.com"
	},
	{
		"email" : "haleymooredev@movilcash.com"
	},
	{
		"email" : "pablomartinpalacios27@gmail.com"
	},
	{
		"email" : "jermainemurraydev@movilcash.com"
	},
	{
		"email" : "carolyncasedev@movilcash.com"
	},
	{
		"email" : "colehodgedev@movilcash.com"
	},
	{
		"email" : "donnareyesdev@movilcash.com"
	}
]

user_iteration = itertools.cycle(users_dev) 

class QuickStart(HttpUser):
    wait_time = between(5,5)

    def on_start(self):
        """Esta función se ejecuta al iniciar la sesión de cada usuario"""
        user = next(user_iteration)
        self.email =  user["email"]
        self.password = password  
        self.login_user()  

    @task
    def login_user(self):
        """Función de login para el usuario actual"""
        body_login = {
            "account": {
                "type": "person"
            },
            "element": {
                "email": f"{self.email}",  
                "password": f"{self.password}", 
                "deviceTag": "",
                "deviceModel": "mobile",
                "coordinates": "-31.392779639214137,-64.18016506749302"
            }
        }
        response = self.client.post(https + Endpoints.login_post, json=body_login)
        print(f"Usuario {self.email} status_code: {response.status_code}")
        print(response.json())
        return response

    
class MyLoadTestShape(LoadTestShape):
    total_time = 100

    def tick(self):
        run_time = self.get_run_time()

        if run_time < 100:
            user_count = int(run_time//5) + 1
            
            if user_count < 20:
                user_count = 20
            return (user_count,5)
        elif run_time >= 100:
            return (0,0)
        else:
            return None

