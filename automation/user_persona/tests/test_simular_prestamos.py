import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from configuracion.views_persona import get_balance_banking,get_capital_banking,product_offers_banking,simulate_offers_banking,installment_plan_banking,cash_out_business_banking,transaction_status_banking,contract_loands_channels_banking,login
from configuracion.conf_logs import setup_logger
from configuracion.main import email,password

from unittest import TestCase


# LOGIN 
def login_in():
        email_ = "*******"
        password_ = "*******"
       
        login_user = login(email_, password_)
        response_login = login_user.json()
        
        dic = {}

        if "data" in response_login:
                data = response_login["data"]
                client = response_login["data"]["client"]
                assert "document_number" in client
                assert "commerce_id" in client
                assert "cvu" in client
                cvu = client["cvu"]
                assert "birth_date" in client
                assert "name" in client
                name = client["name"]
                assert "last_name" in client
                assert "alias" in client
                alias = client["alias"]
                assert "cuil" in client
                cuil = client["cuil"]
                #assert "email" in client
                token = data["token"]

                dic = {"token":token, "alias":alias, "cvu": cvu,"email":email_,"cuil":cuil,"name":name}

        return dic

class Prestamo(TestCase):
        
    def test_loan_simulator(self):
        login_data = login_in()
        token = login_data["token"]
    
        step_1 = get_balance_banking(token)
        print(step_1)

