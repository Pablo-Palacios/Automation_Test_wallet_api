import requests
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from configuracion.views_persona import login_v1, p2p_send, transfer_external_send_cvu,login,transfer_external_send_alias,get_balance
from configuracion.config import Query_db
from configuracion.main import password
from unittest import TestCase
from configuracion.lib import cbu_random
import threading
import os
from queue import Queue

https = ('HTTPS_DEV')


device_id = ""
# LOGIN 
def login_in():
        
        email_last = "*******"
        password_ = "*******"
        login_user = login(email_last, password_)
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

                dic = {"token":token, "alias":alias, "cvu": cvu,"email":email_last,"cuil":cuil,"name":name}

        return dic


class Case(TestCase):
    
    def test_login_user_invalid(self):
        email_fail = "*******"
        password_ = "*******"

        response_login = login(email_fail, password_)
        body_login = response_login.json()
        print(body_login)
        if body_login:
            mjs = body_login["message"]
            if mjs == "AttributeError: 'NoneType' object has no attribute 'user_id'":
                 self.fail("Falla mensaje de usuario incorrecto")



        
    def test_login_password_invalid(self):
        email_ ="*******"
        password_ = "*******"

        response_login = login(email_, password_)
        body_login_ = response_login.json()
        
        mjs_email = body_login_["message"]
            


        email_fail = "*******"
        password_ = "*******"

        response_login = login(email_fail, password_)
        body_login = response_login.json()
       
        mjs_pass = body_login["message"]
            


        mjs = "InvalidCredentialsException: Invalid credentials"
        if mjs_pass != mjs_email:
            self.fail(f"Los mensajes son diferentres. {mjs_pass} - {mjs_email}")
        else:
            self.assertEqual(mjs,mjs_pass)
            self.assertEqual(mjs,mjs_email)






    def test_login_user_migrate_v1(self):
        cuil_ = "*******"
        pin_ = "*******"

        log_v1 = login_v1(cuil_, pin_)
        body_log_v1 = log_v1.json()
        print(body_log_v1)

        mjs_email = body_log_v1["message"]
            

        cuil_ = "*******"
        pin_ = "*******"

        log_v1 = login_v1(cuil_, pin_)
        _log_v1 = log_v1.json()
        
        mjs_pass = _log_v1["message"]
            
        mjs = "InvalidCredentialsException: Invalid credentials"

        if mjs_pass != mjs_email:
            self.fail(f"Los mensajes son diferentres. {mjs_pass} - {mjs_email}")
        else:
            self.assertEqual(mjs,mjs_pass)
            self.assertEqual(mjs,mjs_email)

        


    def test_transf_to_my_account_p2p(self):
        log = login_in()
        token = log["token"]
        email = log["email"]

        amount = 20

        transf = p2p_send(token, email,amount)
        print(transf)
        if transf:
            status = transf["trx_status"]

            if status == "done":
                 self.fail("Fallo el test, la cuenta se transfiere a si misma en p2p")
                
        #     code = transf["code"]
        #     description = transf["description"]
        #     self.assertEqual(code, 409)
        #     self.assertEqual(description, "You can't send money to yourself")

    
    def test_transf_to_my_account_send_cvu(self):
        log = login_in()
        token = log["token"]
        cvu = log["cvu"]

        balance_old = get_balance(token)
        print(f"balance old: {balance_old}")
        
        transf = transfer_external_send_cvu(token,cvu,ammount=10)
        print(transf.json())

        balance_new = get_balance(token)
        print(f"balance new: {balance_new}")
        # if transf:
        #     code = transf["code"]
        #     description = transf["description"]
        #     self.assertEqual(code, 409)
        #     self.assertEqual(description, "You can't send money to yourself")
        

    def test_transf_to_my_account_send_alias(self):
        log = login_in()
        token = log["token"]
        alias = log["alias"]

        balance_old = get_balance(token)
        print(f"balance old: {balance_old}")

        transf = transfer_external_send_alias(token,alias,ammount=100.55)
        print(transf.json())

        balance_new = get_balance(token)
        print(f"balance new: {balance_new}")



