import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from configuracion.views_persona import login, login_in_whit_email,restore_password_email,restore_password_send_code_email,change_password_email
from unittest import TestCase
from configuracion.config import Query_db
from faker import Faker
from configuracion.code_redi import Redis

faker = Faker()

class Pass(TestCase):

    def test_restore_password_user(self):
        email = "*******"
        
        device_id = 961
        
        otp_restore_pass = restore_password_send_code_email(device_id,email)
        response_otp = otp_restore_pass.json()
        print(response_otp)
        status_ = response_otp["status"]
        message_ = response_otp["message"]
        self.assertEqual(status_,200)
        self.assertEqual(message_,"email_sent")
        #print(otp_restore_pass.json())

        otp = Redis.validacion_password(device_id,email)
        #print(otp)
        
        new_password = "Pablito."+ str(faker.random_number(digits=2))
        print(f"new_pass_restore = {new_password}")
        restore_pass = restore_password_email(device_id,email,otp,new_password,new_password)
        body_restore = restore_pass.json()
        #print(restore_pass.json())
        status = body_restore["status"]
        message = body_restore["message"]
        self.assertEqual(status,200,"No se restore password")
        self.assertEqual(message,"new_password_set")
        
        login_new = login_in_whit_email(email,new_password)
        assert "token" in login_new, "no se logeo correctamente"
        print(login_new)

    
    def test_change_password_user(self):
        email = "*******"
        password = "*******"
        log = login_in_whit_email(email,password)
        token = log["token"]

        new_password = "Pablito."+ str(faker.random_number(digits=2))
        print(f"new_pass_change = {new_password}")
        change_password = change_password_email(token,password,new_password,new_password)
        body_change = change_password.json()
        status = body_change["status"]
        message = body_change["message"]
        self.assertEqual(status,200,"No se restore password")
        self.assertEqual(message,"new_password_set")

        login_new = login_in_whit_email(email,new_password)
        assert "token" in login_new, "no se logeo correctamente"
        print(login_new)


    def test_restore_password_with_already_password_exist_in_database(self):
        email ="*******"
        
        device_id = 961
        
        otp_restore_pass = restore_password_send_code_email(device_id,email)
        response_otp = otp_restore_pass.json()
        print(response_otp)
        status_ = response_otp["status"]
        message_ = response_otp["message"]
        self.assertEqual(status_,200)
        self.assertEqual(message_,"email_sent")
        #print(otp_restore_pass.json())

        otp = Redis.validacion_password(device_id,email)
        #print(otp)
        
        #new_password = "Pablito."+ str(faker.random_number(digits=2))
        #print(f"new_pass_restore = {new_password}")
        password_exist = "Pablito.244"
        restore_pass = restore_password_email(device_id,email,otp,password_exist,password_exist)
        body_restore = restore_pass.json()
        print(restore_pass.json())
        status = body_restore["code"]
        message = body_restore["message"]
        self.assertEqual(status,400)
        self.assertEqual(message,"InvalidCredentialsException: Invalid Credentials")
        
        # login_new = login_in_whit_email(email,password_exist)
        # assert "token" in login_new, "no se logeo correctamente"
        # print(login_new)


    def test_restore_password_email_mayuscula(self):
        email = "*******"
        
        device_id = 961
        
        otp_restore_pass = restore_password_send_code_email(device_id,email)
        response_otp = otp_restore_pass.json()
        print(response_otp)
        status_ = response_otp["status"]
        message_ = response_otp["message"]
        self.assertEqual(status_,200)
        self.assertEqual(message_,"email_sent")
        #print(otp_restore_pass.json())

        otp = Redis.validacion_password(device_id,email)
        #print(otp)
        
        new_password = "Pablito."+ str(faker.random_number(digits=2))
        print(f"new_pass_restore = {new_password}")
        restore_pass = restore_password_email(device_id,email,otp,new_password,new_password)
        body_restore = restore_pass.json()
        #print(restore_pass.json())
        status = body_restore["status"]
        message = body_restore["message"]
        self.assertEqual(status,200,"No se restore password")
        self.assertEqual(message,"new_password_set")
        
        login_new = login_in_whit_email(email,new_password)
        assert "token" in login_new, "no se logeo correctamente"
        print(login_new)


        
    
    

    
