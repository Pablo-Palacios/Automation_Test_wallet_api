import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from faker import Faker
import uuid
from configuracion.views_comercio import onboarding_validate_send_email, onboarding_validate_cuil,onboarding_validate_code_otp_email, onboarding_validate_send_sms, onboarding_validate_code_otp_sms, create_user, login_comercio, pin
from configuracion.views_comercio import biometric_validate_frist_step,biometric_validate_second_step,biometric_validate_third_step,validate_commerce,confirm_commerce,confirm_commerce_otp,login_comercio_otp
from configuracion.views_persona import login,login_in_whit_email
from img_thales.dni_pass import back_dni_user,front_dni_user,face_img_user
from img_thales.dni_luis_2011 import get_front_dni_2011,get_back_dni_2011
from img_thales.dni_gus import get_front_dni_gus,get_back_dni_gus
from img_thales.front_img import get_front_img,get_leo_front,get_front_menor,get_front_dni_vencido
from img_thales.back_img import get_back_leo,get_back_img,get_back_menor,get_back_dni_vencido
from img_thales.face_img import get_face_img,get_face_leo
from img_thales.dni_fail import get_back_fail_id,get_face_fail,get_front_fail_id
from img_thales.img_agustin_bruno import get_back_dni_agus,get_front_dni_agus
from unittest import TestCase
from configuracion.config import Query_db
import time
from configuracion.main import email, password, cuil, device_id,name,last_name
from configuracion.code_redi import Redis
from configuracion.conf_logs import setup_logger


faker = Faker()
phone = int("351" + str(faker.random_number(digits=6)) + "1")


class Auth(TestCase):
    def setUp(self):
         #config el logger
         self.logger = setup_logger()

    def test_a_onboarding_success(self):
            
            #email= "robertgood@movilcash.com"
            ## REGISTER EMAIL 
            print(email)
            register_email = onboarding_validate_send_email(device_id,email)
            response_email = register_email.json()
            print(response_email)

            if "data" in response_email:
                message = response_email["message"]
                self.assertEqual(message, "email_sent")
                status = response_email["status"]
                self.assertEqual(status, 200)


            # # # # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email,code)
            response_code_email = email_code.json()
            print(response_code_email)
            if "data" in response_code_email:
                validate = response_code_email["data"]["emailValidated"]
                self.assertEqual(validate, True,"No se valido el email")
                status = response_code_email["status"]
                self.assertEqual(status, 200)

            

            # # # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()
            print(response_sms)

            if "data" in response_sms:
                message = response_sms["message"]
                self.assertEqual(message, "sms_sent")
                status = response_sms["status"]
                self.assertEqual(status, 200)


            # #  VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
            print(response_code_sms)
            if "data" in response_code_sms:
                validate = response_code_sms["data"]["smsValidated"]
                self.assertEqual(validate, True,"No se valido el email")
                status = response_code_sms["status"]
                self.assertEqual(status, 200)
   

            # # VALIDATE CUIT 
            
            cuil_ = int("20" + str(faker.random_number(digits=8)) + "1")
            #cuil_= 20243169624
            #cuil_ = "27220623748"
            #cuil_ = "20295533871"
            #cuil_ = "20418099691"
            validate_cuit = onboarding_validate_cuil(device_id,int(cuil_))
            body_cuit = validate_cuit.json()
            print(body_cuit)
            if "data" in body_cuit:
                validate = body_cuit["data"]["cuilValidated"]
                self.assertEqual(validate, True,"No se valido el cuil")
                user_validate = body_cuit["data"]["userValidated"]
                self.assertEqual(user_validate, True,"No se valido el usuario")
                status = response_code_sms["status"]
                self.assertEqual(status, 200)

            # # # # THALES 
           
            # #device_id = "14567"
            # #cuil = "20558351080"
            # #cuil_leo = "20303918520"
            cuil = "'************'"

            self.logger.info("Runing test: Biometric_validate_frist_step")
            front_dni = biometric_validate_frist_step(device_id,int(cuil),get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            

            # # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
            print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")
            
            # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_third_step")
            face_img = biometric_validate_third_step(device_id,get_face_img())
            self.logger.info(f"third_step: {face_img}")
            print(f"Biometric third_step: {face_img}")
            status_step_3 =face_img["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_3,True,"No paso el step 3")

            hashs = face_img["data"]["approvedHash"]
            dni = face_img["data"]["userData"]["document_number"]

            if hashs == None or hashs == '':
                self.fail("No se genero el hashs!!")

            # # # # # CREATE USER
            cont_cuil = str(cuil_)
                        
            if len(cont_cuil) == 10:
                self.fail(f"fallo creacion de cuil: {cont_cuil}")

            request_create_user = create_user(email,name,last_name,password,cuil_,dni,phone,device_id,hashs)
            body_create_user = request_create_user.json()
            print(body_create_user)
            if "status" in body_create_user:
                code = body_create_user["status"]["status_code"] 
                self.assertEqual(code, 201)

    

    def test_login_comercio(self):
            self.logger.info("Test running: test_login_comercio")
            # cuit = 33810754225
            # email_ = 'peraltapablito822@gmail.com'
            # password_ = "Compablo12."
            # device_ = "1234"
            cuit = '************'
            email_ = '************'
            password_ = '************'
            device_ = "1234"
            
            
            request_login = login_comercio(cuit,email_, password_,device_)
            response_login = request_login.json()
            print(response_login)
            status = response_login["status"]["status_code"]
            if status == 401:
                user_id = Query_db.get_user_id_email(email_)
                 #device_new = faker.random_number(digits=6)
                code_otp = Redis.validacion_otp_login(user_id,device_)
                #print(code_otp)
                login_new = login_comercio_otp(cuit,email_,password_,device_,code_otp)
                response_login = login_new.json()
                
            else:
                 pass
            
            self.logger.info(f"response: {response_login}")
            
            if "data" in response_login:
                data = response_login["data"]
                client = response_login["data"]["client"]
                assert "client_id" in client
                
                assert "user_id" in client
                assert "document_number" in client
                assert "commerce_id" in client
                assert "cvu" in client
                cvu = client["cvu"]
                assert "birth_date" in client
                assert "name" in client
                assert "last_name" in client
                assert "alias" in client
                assert "commerce_id" in client
                assert "balance_id" in client
                assert "commerce" in client
                assert "role" in client
                assert "branches" in client
                alias = client["alias"]
                assert "cuil" in client
                cuil = client["cuil"]
                assert "token" in data

    def test_login_comercio_supervisor(self):
            cuit = '************'
            email_ = '************'
            password_ = '************'
            device__ = ""
            
            request_login = login_comercio(cuit,email_, password_,device__)
            response_login = request_login.json()
            print(response_login)
            status = response_login["status"]["status_code"]
            self.assertEqual(status,200)
            role = response_login["data"]["client"]["role"]
            self.assertEqual(role,"supervisor")


    def test_login_comercio_cajero(self):
            cuit = '************'
            email_ = '************'
            password_ = '************'
            device__ = ""

            request_login = login_comercio(cuit,email_, password_,device__)
            response_login = request_login.json()
            print(response_login)
            status = response_login["status"]["status_code"]
            self.assertEqual(status,200)
            role = response_login["data"]["client"]["role"]
            self.assertEqual(role,"cashier")

    # def test_login_comercio_sin_device(self):
    #         cuit = 33810754225
    #         email_ = 'martinpalacios561@gmail.com'
    #         password_ = "Compablo12."
    #         device_ = "123"

    #         log = login_comercio_sin_device(cuit,email_,password_)
    #         print(log.json())

    def test_login_comercio_migrado(self):
            self.logger.info("Test running: test_login_comercio")
            cuit = '************'
            email_ = '************'
            password_ = '************'
            request_login = login_comercio(cuit,email_, password_)

            response_login = request_login.json()
            self.logger.info(f"response: {response_login}")
            print(response_login)
            if "data" in response_login:
                data = response_login["data"]
                client = response_login["data"]["client"]
                assert "client_id" in client
                
                assert "user_id" in client
                assert "document_number" in client
                assert "commerce_id" in client
                assert "cvu" in client
                cvu = client["cvu"]
                assert "birth_date" in client
                assert "name" in client
                assert "last_name" in client
                assert "alias" in client
                assert "commerce_id" in client
                assert "balance_id" in client
                assert "commerce" in client
                assert "role" in client
                assert "branches" in client
                alias = client["alias"]
                assert "cuil" in client
                cuil = client["cuil"]
                assert "token" in data

    def test_login_monotributista(self):
            self.logger.info("Test running: test_login_monotributista")
            
            email_ = '************'
            password_ = '************'
            request_login = login(email_, password_)

            response_login = request_login.json()
            print(response_login)
            self.logger.info(f"response: {response_login}")
            if "data" in response_login:
                data = response_login["data"]
                client = response_login["data"]["client"]
                assert "client_id" in client
                assert "user_id" in client
                assert "document_number" in client
                assert "commerce_id" in client
                assert "cvu" in client
                cvu = client["cvu"]
                assert "birth_date" in client
                assert "name" in client
                assert "last_name" in client
                assert "alias" in client
                assert "commerce_id" in client
                assert "balance_id" in client
                assert "commerce" in client
                assert "role" in client
                alias = client["alias"]
                assert "cuil" in client
                cuil = client["cuil"]
                assert "token" in data
                
    def test_login_fail_monotributista(self):
            self.logger.info("Test running: test_login_fail_monotributista")
            email_ = '************'
            password_ = '************'
            request_login_1 = login(email_, password_)
            response_login_ = request_login_1.json()
            self.logger.info(f"response: {response_login_}")
            print(response_login_)
            mjs = response_login_["message"]

            email = '************'
            password = '************'
            request_login_2 = login(email, password)
            response_login = request_login_2.json()
            self.logger.info(f"response: {response_login}")
            print(response_login)
            mjs_ = response_login["message"]
            
            if mjs != mjs_:
                 self.fail(f"""Fallaron message diferentes:
                                - fail_email: {mjs}
                                - fail_password: {mjs_} """)
            else:
                print("Los mensajes coinciden")


    def test_login_fail_comercios(self):
            self.logger.info("Test running: test_login_fail_comercios")
            cuit = '************'
            email = '************'
            password = '************'
            request_login_1 = login_comercio(cuit,email,password)
            response_login_1 = request_login_1.json()
            print(response_login_1)
            self.logger.info(f"response_fail_cuil: {response_login_1}")
            message_1 = response_login_1["message"]

            cuit_ = '************'
            email_ = '************'
            password_ = '************'
            request_login_2 = login_comercio(cuit_,email_, password_)
            response_login_2 = request_login_2.json()
            print(response_login_2)
            self.logger.info(f"response_fail_email: {response_login_2}")
            message_2 = response_login_2["message"]

            cuit__ = '************'
            email__ = '************'
            password__ = '************'
            request_login_3 = login_comercio(cuit__,email__, password__)
            response_login_3 = request_login_3.json()
            self.logger.info(f"response_fail_password: {response_login_3}")
            print(response_login_3)
            message_3 = response_login_3["message"]

            mjs = 'InvalidCredentialsException: Invalid credentials'

            if message_1 != mjs:
                self.fail(f"fallo en el fail_cuil: {message_1}") 
            elif message_2 != mjs:
                self.fail(f"fallo en el fail_email: {message_2}") 
            elif message_3 != mjs:
                self.fail(f"fallo en el fail_cuil: {message_3}") 
            else:
                 print("Los mjs son los mismos en los 3 casos")

    