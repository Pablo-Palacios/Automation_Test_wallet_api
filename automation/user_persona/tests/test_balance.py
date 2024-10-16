from configuracion.views_persona import paid_balance_activate,paid_balance_deativate, paid_balance_status, login
from unittest import TestCase
from api_back.mc_automation_qa.pruebas_v2.configuracion.main import password
from api_back.mc_automation_qa.pruebas_v2.configuracion.conf_logs import setup_logger
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


def login_in():
        email_last = "*******"
        login_user = login(email_last, password)
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
                assert "last_name" in client
                assert "alias" in client
                alias = client["alias"]
                assert "cuil" in client
                cuil = client["cuil"]
                #assert "email" in client
                token = data["token"]

                dic = {"token":token, "alias":alias, "cvu": cvu,"email":email_last}

        return dic


class Paid(TestCase):
    def setUp(self):
         #config el logger
         self.logger = setup_logger()

    def test_get_status_paid_balance(self):
        self.logger.info("Running test: test_get_status_paid_balance")
        login_data = login_in()
        token = login_data["token"]
        status_paid = paid_balance_status(token)
        body_status_paid = status_paid.json()
        status = body_status_paid["status"]["status_code"]
        self.assertEqual(status,200)
        #print(body_status_paid)

    def test_get_status_if_paid_is_activate(self):
        self.logger.info("Running test: test_get_status_if_paid_is_activate")
        login_data = login_in()
        token = login_data["token"]
        status_paid = paid_balance_activate(token)
        body_status_paid = status_paid.json()
        self.logger.info(f"Activate Paid Balance: {body_status_paid}")
        #print(body_status_paid)
        status = body_status_paid["status"]["status_code"]
        if status == 200:
            status_paid = paid_balance_status(token)
            body_status_paid = status_paid.json()
            self.logger.info(f"status paid balance actual: {body_status_paid}")
            #print(f"status paid balance actual: {body_status_paid}")
            boolean_paid_balance = body_status_paid["data"]["is_paid_balance"]
            self.assertEqual(boolean_paid_balance, True,"No coincide el status")

    def test_get_status_if_paid_is_deactivate(self):
        self.logger.info("Running test: test_get_status_if_paid_is_desactivate")
        login_data = login_in()
        token = login_data["token"]
        status_paid = paid_balance_deativate(token)
        body_status_paid = status_paid.json()
        self.logger.info(f"Desactivate Paid Balance: {body_status_paid}")
        #print(body_status_paid)
        status = body_status_paid["status"]["status_code"]
        if status == 200:
            status_paid = paid_balance_status(token)
            body_status_paid = status_paid.json()
            self.logger.info(f"status paid balance actual: {body_status_paid}")
            boolean_paid_balance = body_status_paid["data"]["is_paid_balance"]
            self.assertEqual(boolean_paid_balance, False,"No coincide el status")
