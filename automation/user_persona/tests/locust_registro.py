import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import time
from locust import HttpUser,task,between, LoadTestShape
from configuracion.views_persona import https,Endpoints
from configuracion.main import password
import itertools

class TestRegisterLocust(HttpUser):
    wait_time = between(5,5)

    def on_start(self):
        pass