from faker import Faker
import uuid
from views import onboarding_validate_send_email, onboarding_validate_cuil,onboarding_validate_code_otp_email, onboarding_validate_send_sms, onboarding_validate_code_otp_sms, create_user, login, pin, first
from automation.lib.lib import device_models, provincias_arg
from unittest import TestCase
from automation.database.config import Query_db

from automation.lib.main import email, password, phone, cuit, device_id
from automation.decode.code_redi import Redis


faker = Faker()
    
class Auth(TestCase):
    def test_a_onboarding_success(self):
            
            # REGISTER EMAIL 
            print(email)
            #print(device_id)
            register_email = onboarding_validate_send_email(device_id,email)
            response_email = register_email.json()
            print(response_email)

            if "data" in response_email:
                message = response_email["message"]
                self.assertEqual(message, "email_sent")
                status = response_email["status"]
                self.assertEqual(status, 200)


            # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email,code)
            response_code_email = email_code.json()
            print(response_code_email)
            if "data" in response_code_email:
                message = response_code_email["message"]
                self.assertEqual(message, "email_validated")
                status = response_code_email["status"]
                self.assertEqual(status, 200)

            

            # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()
            #print(response_sms)

            if "data" in response_sms:
                message = response_sms["message"]
                self.assertEqual(message, "sms_sent")
                status = response_sms["status"]
                self.assertEqual(status, 200)


            # VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
            print(response_code_sms)
            if "data" in response_code_sms:
                 message = response_code_sms["message"]
                 self.assertEqual(message, "user_validated")
                 status = response_code_sms["status"]
                 self.assertEqual(status, 200)
   

            #THALES 

            

            # VALIDATE CUIT 
            validate_cuit = onboarding_validate_cuil(device_id,cuit)
            body_cuit = validate_cuit.json()
            if "data" in body_cuit:
                 message = response_code_sms["message"]
                 self.assertEqual(message, "user_validated")
                 status = response_code_sms["status"]
                 self.assertEqual(status, 200)

            # CREATE USER
        
            request_create_user = create_user(email,password, cuit, phone, device_models())
            body_create_user = request_create_user.json()
            if "status" in body_create_user:
                code = body_create_user["status"]["status_code"] 
                self.assertEqual(code, 201)


            
           

           

    def test_login_success(self):
            email_ = 'carolfinley@gmail.com'
            request_login = login(email_, password)

           #print(request_login.json())

            response_login = request_login.json()
            print(response_login)
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
                #assert token in data
                #token = data["token"]
                #assert "message" in client
                #assert "status" in client
                cont_cuil = str(cuil)
                        
                if len(cont_cuil) > 11 or len(cont_cuil) == 12:
                            print("fail cuil, mal formulado")
                else:
                            print(f"se genero bien el cuil: {len(cont_cuil)}")

    #         try:
    #             for item in response_login:
    #                 if item and 'response' in item:
    #                     response_content = item["response"]
    #                     sessions = response_content["sessions"]
    #                     assert "token" in sessions
    #                     client = response_content["client"]
    #                     assert "document_number" in client
    #                     assert "cvu" in client
    #                     cvu = client["cvu"]
    #                     assert "birth_date" in client
    #                     assert "name" in client
    #                     assert "last_name" in client
    #                     assert "alias" in client
    #                     alias = client["alias"]
    #                     assert "cuil" in client
    #                     cuil = client["cuil"]
    #                     assert "email" in client
    #                     token = sessions["token"]

    #                     print(first)
    #                     print(email)
    #                     print(cuil)
    #                     cont_cuil = str(cuil)
                        
    #                     if len(cont_cuil) > 11 or len(cont_cuil) == 12:
    #                         print("fail cuil, mal formulado")
    #                     else:
    #                         print(f"se genero bien el cuil: {len(cont_cuil)}")
    #                     alias_db = Query_db.get_alias_user_with_email(email)
    #                     cvu_db = Query_db.get_cvu_user_with_email(email)
    #                     #print(cvu_db)
    #                     #print(alias_db)
    #                     if alias_db == '' or cvu_db == '':
    #                         print("campo alias y cvu vacios")
                    
    #                     else:

    #                         print(f"""Alias Y cvu registrados correcto. \n
    #                         Coinciden en db. \n
    #                         - {cvu_db}
    #                         - {alias_db}""") 

    #                     pin_access_ok = pin(token)
    #                     assert pin_access_ok.status_code, 200 
    #                     response_pin_access = pin_access_ok.json()
    #                     #print(response_pin_access)

    #                     for item in response_pin_access:
    #                         if item and 'response' in item:
    #                             response_content = item["response"]
    #                             assert "date" in response_content
    #                             assert "id" in response_content
    #                             assert "status" in response_content
    #                             status = response_content["status"]
    #                             assert status, "status del token en false"
    #         except ValueError as E:
    #             self.fail(f"Error: {E}")
