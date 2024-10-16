import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from faker import Faker
import uuid
from configuracion.views_persona import onboarding_validate_send_email, onboarding_validate_cuil,onboarding_validate_code_otp_email, onboarding_validate_send_sms, onboarding_validate_code_otp_sms, create_user, login, pin
from configuracion.views_persona import biometric_validate_frist_step,biometric_validate_second_step,biometric_validate_third_step,login_v1
from configuracion.lib import device_models, provincias_arg
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
from configuracion.main import email, password, cuil, device_id,name,last_name,last_name_2,email_2,last_name_6,last_name_3,last_name_4,last_name_5,last_name_7,last_name_9,last_name_10,last_name_8,last_name_11,last_name_12,last_name_13
from configuracion.code_redi import Redis
from configuracion.conf_logs import setup_logger


faker = Faker()



class Auth(TestCase):
    def setUp(self):
         #config el logger
         self.logger = setup_logger()

    def test_raro_onboarding_success(self):
            email_2 = faker.first_name().lower() + str(faker.random_number(digits=4))+"@movilcash.com"
            phone = int("351" + str(faker.random_number(digits=6)) + "1")
            device_id = faker.random_number(digits=5)


            print(email_2)
            register_email = onboarding_validate_send_email(device_id,email_2)
            response_email = register_email.json()
            #print(response_email)

            if "data" in response_email:
                message = response_email["message"]
                self.assertEqual(message, "email_sent")
                status = response_email["status"]
                self.assertEqual(status, 200)


            # # # # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email_2,code)
            response_code_email = email_code.json()
            #print(response_code_email)
            if "data" in response_code_email:
                validate = response_code_email["data"]["emailValidated"]
                self.assertEqual(validate, True,"No se valido el email")
                status = response_code_email["status"]
                self.assertEqual(status, 200)

            

            # # # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()
            #print(response_sms)

            if "data" in response_sms:
                message = response_sms["message"]
                self.assertEqual(message, "sms_sent")
                status = response_sms["status"]
                self.assertEqual(status, 200)


            # #  VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
            #print(response_code_sms)
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
            #print(body_cuit)
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
            cuil = "20418099691"

            self.logger.info("Runing test: Biometric_validate_frist_step")
            front_dni = biometric_validate_frist_step(device_id,int(cuil),get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            

            # # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")
            
            # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_third_step")
            face_img = biometric_validate_third_step(device_id,get_face_img())
            self.logger.info(f"third_step: {face_img}")
            #print(f"Biometric third_step: {face_img}")
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

            request_create_user = create_user(email_2,name,last_name_2,password,cuil_,dni,phone,device_id,hashs)
            body_create_user = request_create_user.json()
            print(body_create_user)
            if "status" in body_create_user:
                code = body_create_user["status"]["status_code"] 
                self.assertEqual(code, 201)


            log = login(email_2,password)
            log_body = log.json()
            alias=log_body["data"]["client"]["alias"]
            print(f"name: {last_name_2}")
            print(f"alias en db: {alias}")

    def test_raro1_onboarding_success(self):
            
            email_2 = faker.first_name().lower() + str(faker.random_number(digits=4))+"@movilcash.com"
            phone = int("351" + str(faker.random_number(digits=6)) + "1")
            device_id = faker.random_number(digits=5)
            ## REGISTER EMAIL 
            print(email_2)
            register_email = onboarding_validate_send_email(device_id,email_2)
            response_email = register_email.json()
            #print(response_email)

            if "data" in response_email:
                message = response_email["message"]
                self.assertEqual(message, "email_sent")
                status = response_email["status"]
                self.assertEqual(status, 200)


            # # # # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email_2,code)
            response_code_email = email_code.json()
            #print(response_code_email)
            if "data" in response_code_email:
                validate = response_code_email["data"]["emailValidated"]
                self.assertEqual(validate, True,"No se valido el email")
                status = response_code_email["status"]
                self.assertEqual(status, 200)

            

            # # # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()
            #print(response_sms)

            if "data" in response_sms:
                message = response_sms["message"]
                self.assertEqual(message, "sms_sent")
                status = response_sms["status"]
                self.assertEqual(status, 200)


            # #  VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
            #print(response_code_sms)
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
            #print(body_cuit)
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
            cuil = "20418099691"

            self.logger.info("Runing test: Biometric_validate_frist_step")
            front_dni = biometric_validate_frist_step(device_id,int(cuil),get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            

            # # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")
            
            # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_third_step")
            face_img = biometric_validate_third_step(device_id,get_face_img())
            self.logger.info(f"third_step: {face_img}")
            #print(f"Biometric third_step: {face_img}")
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

            request_create_user = create_user(email_2,name,last_name_3,password,cuil_,dni,phone,device_id,hashs)
            body_create_user = request_create_user.json()
            print(body_create_user)
            if "status" in body_create_user:
                code = body_create_user["status"]["status_code"] 
                self.assertEqual(code, 201)


            log = login(email_2,password)
            log_body = log.json()
            alias=log_body["data"]["client"]["alias"]
            print(f"name: {last_name_3}")
            print(f"alias en db: {alias}")

    def test_raro2_onboarding_success(self):
            
            email_2 = faker.first_name().lower() + str(faker.random_number(digits=4))+"@movilcash.com"
            phone = int("351" + str(faker.random_number(digits=6)) + "1")
            device_id = faker.random_number(digits=5)
            print(email_2)
            register_email = onboarding_validate_send_email(device_id,email_2)
            response_email = register_email.json()
            #print(response_email)

            if "data" in response_email:
                message = response_email["message"]
                self.assertEqual(message, "email_sent")
                status = response_email["status"]
                self.assertEqual(status, 200)


            # # # # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email_2,code)
            response_code_email = email_code.json()
            #print(response_code_email)
            if "data" in response_code_email:
                validate = response_code_email["data"]["emailValidated"]
                self.assertEqual(validate, True,"No se valido el email")
                status = response_code_email["status"]
                self.assertEqual(status, 200)

            

            # # # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()
            #print(response_sms)

            if "data" in response_sms:
                message = response_sms["message"]
                self.assertEqual(message, "sms_sent")
                status = response_sms["status"]
                self.assertEqual(status, 200)


            # #  VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
            #print(response_code_sms)
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
            #print(body_cuit)
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
            cuil = "20418099691"

            self.logger.info("Runing test: Biometric_validate_frist_step")
            front_dni = biometric_validate_frist_step(device_id,int(cuil),get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            

            # # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")
            
            # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_third_step")
            face_img = biometric_validate_third_step(device_id,get_face_img())
            self.logger.info(f"third_step: {face_img}")
            #print(f"Biometric third_step: {face_img}")
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

            request_create_user = create_user(email_2,name,last_name_4,password,cuil_,dni,phone,device_id,hashs)
            body_create_user = request_create_user.json()
            print(body_create_user)
            if "status" in body_create_user:
                code = body_create_user["status"]["status_code"] 
                self.assertEqual(code, 201)


            log = login(email_2,password)
            log_body = log.json()
            alias=log_body["data"]["client"]["alias"]
            print(f"name: {last_name_4}")
            print(f"alias en db: {alias}")

    def test_raro3_onboarding_success(self):
            
            email_2 = faker.first_name().lower() + str(faker.random_number(digits=4))+"@movilcash.com"
            phone = int("351" + str(faker.random_number(digits=6)) + "1")
            device_id = faker.random_number(digits=5) 
            print(email_2)
            register_email = onboarding_validate_send_email(device_id,email_2)
            response_email = register_email.json()
            #print(response_email)

            if "data" in response_email:
                message = response_email["message"]
                self.assertEqual(message, "email_sent")
                status = response_email["status"]
                self.assertEqual(status, 200)


            # # # # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email_2,code)
            response_code_email = email_code.json()
            #print(response_code_email)
            if "data" in response_code_email:
                validate = response_code_email["data"]["emailValidated"]
                self.assertEqual(validate, True,"No se valido el email")
                status = response_code_email["status"]
                self.assertEqual(status, 200)

            

            # # # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()
            #print(response_sms)

            if "data" in response_sms:
                message = response_sms["message"]
                self.assertEqual(message, "sms_sent")
                status = response_sms["status"]
                self.assertEqual(status, 200)


            # #  VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
            #print(response_code_sms)
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
            #print(body_cuit)
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
            cuil = "20418099691"

            self.logger.info("Runing test: Biometric_validate_frist_step")
            front_dni = biometric_validate_frist_step(device_id,int(cuil),get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
           # print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            

            # # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
           # print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")
            
            # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_third_step")
            face_img = biometric_validate_third_step(device_id,get_face_img())
            self.logger.info(f"third_step: {face_img}")
            #print(f"Biometric third_step: {face_img}")
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

            request_create_user = create_user(email_2,name,last_name_5,password,cuil_,dni,phone,device_id,hashs)
            body_create_user = request_create_user.json()
            print(body_create_user)
            if "status" in body_create_user:
                code = body_create_user["status"]["status_code"] 
                self.assertEqual(code, 201)


            log = login(email_2,password)
            log_body = log.json()
            alias=log_body["data"]["client"]["alias"]
            print(f"name: {last_name_5}")
            print(f"alias en db: {alias}")
  
    def test_raro4_onboarding_success(self):
            
            email_2 = faker.first_name().lower() + str(faker.random_number(digits=4))+"@movilcash.com"
            phone = int("351" + str(faker.random_number(digits=6)) + "1")
            device_id = faker.random_number(digits=5) 
            print(email_2)
            register_email = onboarding_validate_send_email(device_id,email_2)
            response_email = register_email.json()
            #print(response_email)

            if "data" in response_email:
                message = response_email["message"]
                self.assertEqual(message, "email_sent")
                status = response_email["status"]
                self.assertEqual(status, 200)


            # # # # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email_2,code)
            response_code_email = email_code.json()
            #print(response_code_email)
            if "data" in response_code_email:
                validate = response_code_email["data"]["emailValidated"]
                self.assertEqual(validate, True,"No se valido el email")
                status = response_code_email["status"]
                self.assertEqual(status, 200)

            

            # # # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()
            #print(response_sms)

            if "data" in response_sms:
                message = response_sms["message"]
                self.assertEqual(message, "sms_sent")
                status = response_sms["status"]
                self.assertEqual(status, 200)


            # #  VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
            #print(response_code_sms)
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
            #print(body_cuit)
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
            cuil = "20418099691"

            self.logger.info("Runing test: Biometric_validate_frist_step")
            front_dni = biometric_validate_frist_step(device_id,int(cuil),get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            

            # # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")
            
            # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_third_step")
            face_img = biometric_validate_third_step(device_id,get_face_img())
            self.logger.info(f"third_step: {face_img}")
            #print(f"Biometric third_step: {face_img}")
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

            request_create_user = create_user(email_2,name,last_name_5,password,cuil_,dni,phone,device_id,hashs)
            body_create_user = request_create_user.json()
            print(body_create_user)
            if "status" in body_create_user:
                code = body_create_user["status"]["status_code"] 
                self.assertEqual(code, 201)


            log = login(email_2,password)
            log_body = log.json()
            alias=log_body["data"]["client"]["alias"]
            print(f"name: {last_name_5}")
            print(f"alias en db: {alias}")

    def test_raro5_onboarding_success(self):
            
            email_2 = faker.first_name().lower() + str(faker.random_number(digits=4))+"@movilcash.com"
            phone = int("351" + str(faker.random_number(digits=6)) + "1")
            device_id = faker.random_number(digits=5)
            print(email_2)
            register_email = onboarding_validate_send_email(device_id,email_2)
            response_email = register_email.json()
            #print(response_email)

            if "data" in response_email:
                message = response_email["message"]
                self.assertEqual(message, "email_sent")
                status = response_email["status"]
                self.assertEqual(status, 200)


            # # # # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email_2,code)
            response_code_email = email_code.json()
            #print(response_code_email)
            if "data" in response_code_email:
                validate = response_code_email["data"]["emailValidated"]
                self.assertEqual(validate, True,"No se valido el email")
                status = response_code_email["status"]
                self.assertEqual(status, 200)

            

            # # # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()
            #print(response_sms)

            if "data" in response_sms:
                message = response_sms["message"]
                self.assertEqual(message, "sms_sent")
                status = response_sms["status"]
                self.assertEqual(status, 200)


            # #  VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
            #print(response_code_sms)
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
            #print(body_cuit)
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
            cuil = "20418099691"

            self.logger.info("Runing test: Biometric_validate_frist_step")
            front_dni = biometric_validate_frist_step(device_id,int(cuil),get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            

            # # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")
            
            # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_third_step")
            face_img = biometric_validate_third_step(device_id,get_face_img())
            self.logger.info(f"third_step: {face_img}")
            #print(f"Biometric third_step: {face_img}")
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

            request_create_user = create_user(email_2,name,last_name_6,password,cuil_,dni,phone,device_id,hashs)
            body_create_user = request_create_user.json()
            print(body_create_user)
            if "status" in body_create_user:
                code = body_create_user["status"]["status_code"] 
                self.assertEqual(code, 201)


            log = login(email_2,password)
            log_body = log.json()
            alias=log_body["data"]["client"]["alias"]
            print(f"name: {last_name_6}")
            print(f"alias en db: {alias}")

    def test_raro6_onboarding_success(self):
            
            email_2 = faker.first_name().lower() + str(faker.random_number(digits=4))+"@movilcash.com"
            phone = int("351" + str(faker.random_number(digits=6)) + "1")
            device_id = faker.random_number(digits=5) 
            print(email_2)
            register_email = onboarding_validate_send_email(device_id,email_2)
            response_email = register_email.json()
            #print(response_email)

            if "data" in response_email:
                message = response_email["message"]
                self.assertEqual(message, "email_sent")
                status = response_email["status"]
                self.assertEqual(status, 200)


            # # # # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email_2,code)
            response_code_email = email_code.json()
            #print(response_code_email)
            if "data" in response_code_email:
                validate = response_code_email["data"]["emailValidated"]
                self.assertEqual(validate, True,"No se valido el email")
                status = response_code_email["status"]
                self.assertEqual(status, 200)

            

            # # # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()
            #print(response_sms)

            if "data" in response_sms:
                message = response_sms["message"]
                self.assertEqual(message, "sms_sent")
                status = response_sms["status"]
                self.assertEqual(status, 200)


            # #  VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
            #print(response_code_sms)
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
            #print(body_cuit)
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
            cuil = "20418099691"

            self.logger.info("Runing test: Biometric_validate_frist_step")
            front_dni = biometric_validate_frist_step(device_id,int(cuil),get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            

            # # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")
            
            # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_third_step")
            face_img = biometric_validate_third_step(device_id,get_face_img())
            self.logger.info(f"third_step: {face_img}")
            #print(f"Biometric third_step: {face_img}")
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

            request_create_user = create_user(email_2,name,last_name_7,password,cuil_,dni,phone,device_id,hashs)
            body_create_user = request_create_user.json()
            print(body_create_user)
            if "status" in body_create_user:
                code = body_create_user["status"]["status_code"] 
                self.assertEqual(code, 201)


            log = login(email_2,password)
            log_body = log.json()
            alias=log_body["data"]["client"]["alias"]
            print(f"name: {last_name_7}")
            print(f"alias en db: {alias}")

    def test_raro7_onboarding_success(self):
            
            email_2 = faker.first_name().lower() + str(faker.random_number(digits=4))+"@movilcash.com"
            phone = int("351" + str(faker.random_number(digits=6)) + "1")
            device_id = faker.random_number(digits=5) 
            print(email_2)
            register_email = onboarding_validate_send_email(device_id,email_2)
            response_email = register_email.json()
            #print(response_email)

            if "data" in response_email:
                message = response_email["message"]
                self.assertEqual(message, "email_sent")
                status = response_email["status"]
                self.assertEqual(status, 200)


            # # # # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email_2,code)
            response_code_email = email_code.json()
            #print(response_code_email)
            if "data" in response_code_email:
                validate = response_code_email["data"]["emailValidated"]
                self.assertEqual(validate, True,"No se valido el email")
                status = response_code_email["status"]
                self.assertEqual(status, 200)

            

            # # # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()
            #print(response_sms)

            if "data" in response_sms:
                message = response_sms["message"]
                self.assertEqual(message, "sms_sent")
                status = response_sms["status"]
                self.assertEqual(status, 200)


            # #  VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
            #print(response_code_sms)
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
            #print(body_cuit)
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
            cuil = "20418099691"

            self.logger.info("Runing test: Biometric_validate_frist_step")
            front_dni = biometric_validate_frist_step(device_id,int(cuil),get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            

            # # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")
            
            # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_third_step")
            face_img = biometric_validate_third_step(device_id,get_face_img())
            self.logger.info(f"third_step: {face_img}")
            #print(f"Biometric third_step: {face_img}")
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

            request_create_user = create_user(email_2,name,last_name_8,password,cuil_,dni,phone,device_id,hashs)
            body_create_user = request_create_user.json()
            print(body_create_user)
            if "status" in body_create_user:
                code = body_create_user["status"]["status_code"] 
                self.assertEqual(code, 201)


            log = login(email_2,password)
            log_body = log.json()
            alias=log_body["data"]["client"]["alias"]
            print(f"name: {last_name_8}")
            print(f"alias en db: {alias}")

    def test_raro8_onboarding_success(self):
            
            email_2 = faker.first_name().lower() + str(faker.random_number(digits=4))+"@movilcash.com"
            phone = int("351" + str(faker.random_number(digits=6)) + "1")
            device_id = faker.random_number(digits=5) 
            print(email_2)
            register_email = onboarding_validate_send_email(device_id,email_2)
            response_email = register_email.json()
            #print(response_email)

            if "data" in response_email:
                message = response_email["message"]
                self.assertEqual(message, "email_sent")
                status = response_email["status"]
                self.assertEqual(status, 200)


            # # # # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email_2,code)
            response_code_email = email_code.json()
          #3print(response_code_email)
            if "data" in response_code_email:
                validate = response_code_email["data"]["emailValidated"]
                self.assertEqual(validate, True,"No se valido el email")
                status = response_code_email["status"]
                self.assertEqual(status, 200)

            

            # # # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()
            
            #print(response_sms)

            if "data" in response_sms:
                message = response_sms["message"]
                self.assertEqual(message, "sms_sent")
                status = response_sms["status"]
                self.assertEqual(status, 200)


            # #  VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
            #print(response_code_sms)
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
            #print(body_cuit)
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
            cuil = "20418099691"

            self.logger.info("Runing test: Biometric_validate_frist_step")
            front_dni = biometric_validate_frist_step(device_id,int(cuil),get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
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
            #print(f"Biometric third_step: {face_img}")
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

            request_create_user = create_user(email_2,name,last_name_9,password,cuil_,dni,phone,device_id,hashs)
            body_create_user = request_create_user.json()
            print(body_create_user)
            if "status" in body_create_user:
                code = body_create_user["status"]["status_code"] 
                self.assertEqual(code, 201)


            log = login(email_2,password)
            log_body = log.json()
            alias=log_body["data"]["client"]["alias"]
            print(f"name: {last_name_9}")
            print(f"alias en db: {alias}")

    def test_raro9_onboarding_success(self):
            
            email_2 = faker.first_name().lower() + str(faker.random_number(digits=4))+"@movilcash.com"
            phone = int("351" + str(faker.random_number(digits=6)) + "1")
            device_id = faker.random_number(digits=5)
            print(email_2)
            register_email = onboarding_validate_send_email(device_id,email_2)
            response_email = register_email.json()
            #print(response_email)

            if "data" in response_email:
                message = response_email["message"]
                self.assertEqual(message, "email_sent")
                status = response_email["status"]
                self.assertEqual(status, 200)


            # # # # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email_2,code)
            response_code_email = email_code.json()
            #print(response_code_email)
            if "data" in response_code_email:
                validate = response_code_email["data"]["emailValidated"]
                self.assertEqual(validate, True,"No se valido el email")
                status = response_code_email["status"]
                self.assertEqual(status, 200)

            

            # # # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()
            #print(response_sms)

            if "data" in response_sms:
                message = response_sms["message"]
                self.assertEqual(message, "sms_sent")
                status = response_sms["status"]
                self.assertEqual(status, 200)


            # #  VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
            #print(response_code_sms)
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
            #print(body_cuit)
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
            cuil = "20418099691"

            self.logger.info("Runing test: Biometric_validate_frist_step")
            front_dni = biometric_validate_frist_step(device_id,int(cuil),get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            

            # # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")
            
            # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_third_step")
            face_img = biometric_validate_third_step(device_id,get_face_img())
            self.logger.info(f"third_step: {face_img}")
            #print(f"Biometric third_step: {face_img}")
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

            request_create_user = create_user(email_2,name,last_name_10,password,cuil_,dni,phone,device_id,hashs)
            body_create_user = request_create_user.json()
            print(body_create_user)
            if "status" in body_create_user:
                code = body_create_user["status"]["status_code"] 
                self.assertEqual(code, 201)


            log = login(email_2,password)
            log_body = log.json()
            alias=log_body["data"]["client"]["alias"]
            print(f"name: {last_name_10}")
            print(f"alias en db: {alias}")

    def test_raro10_onboarding_success(self):
            
            email_2 = faker.first_name().lower() + str(faker.random_number(digits=4))+"@movilcash.com"
            phone = int("351" + str(faker.random_number(digits=6)) + "1")
            device_id = faker.random_number(digits=5) 
            print(email_2)
            register_email = onboarding_validate_send_email(device_id,email_2)
            response_email = register_email.json()
            #print(response_email)

            if "data" in response_email:
                message = response_email["message"]
                self.assertEqual(message, "email_sent")
                status = response_email["status"]
                self.assertEqual(status, 200)


            # # # # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email_2,code)
            response_code_email = email_code.json()
            #print(response_code_email)
            if "data" in response_code_email:
                validate = response_code_email["data"]["emailValidated"]
                self.assertEqual(validate, True,"No se valido el email")
                status = response_code_email["status"]
                self.assertEqual(status, 200)

            

            # # # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()
            #print(response_sms)

            if "data" in response_sms:
                message = response_sms["message"]
                self.assertEqual(message, "sms_sent")
                status = response_sms["status"]
                self.assertEqual(status, 200)


            # #  VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
           # print(response_code_sms)
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
            #print(body_cuit)
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
            cuil = "20418099691"

            self.logger.info("Runing test: Biometric_validate_frist_step")
            front_dni = biometric_validate_frist_step(device_id,int(cuil),get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            

            # # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")
            
            # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_third_step")
            face_img = biometric_validate_third_step(device_id,get_face_img())
            self.logger.info(f"third_step: {face_img}")
            #print(f"Biometric third_step: {face_img}")
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

            request_create_user = create_user(email_2,name,last_name_11,password,cuil_,dni,phone,device_id,hashs)
            body_create_user = request_create_user.json()
            #print(body_create_user)
            if "status" in body_create_user:
                code = body_create_user["status"]["status_code"] 
                self.assertEqual(code, 201)


            log = login(email_2,password)
            log_body = log.json()
            alias=log_body["data"]["client"]["alias"]
            print(f"name: {last_name_11}")
            print(f"alias en db: {alias}")
    
    def test_raro11_onboarding_success(self): 
            email_2 = faker.first_name().lower() + str(faker.random_number(digits=4))+"@movilcash.com"
            phone = int("351" + str(faker.random_number(digits=6)) + "1")
            device_id = faker.random_number(digits=5) 
            print(email_2)
            register_email = onboarding_validate_send_email(device_id,email_2)
            response_email = register_email.json()
            #print(response_email)

            if "data" in response_email:
                message = response_email["message"]
                self.assertEqual(message, "email_sent")
                status = response_email["status"]
                self.assertEqual(status, 200)


            # # # # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email_2,code)
            response_code_email = email_code.json()
            #print(response_code_email)
            if "data" in response_code_email:
                validate = response_code_email["data"]["emailValidated"]
                self.assertEqual(validate, True,"No se valido el email")
                status = response_code_email["status"]
                self.assertEqual(status, 200)

            

            # # # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()
            #print(response_sms)

            if "data" in response_sms:
                message = response_sms["message"]
                self.assertEqual(message, "sms_sent")
                status = response_sms["status"]
                self.assertEqual(status, 200)


            # #  VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
            #print(response_code_sms)
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
            #print(body_cuit)
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
            cuil = "20418099691"

            self.logger.info("Runing test: Biometric_validate_frist_step")
            front_dni = biometric_validate_frist_step(device_id,int(cuil),get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            

            # # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")
            
            # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_third_step")
            face_img = biometric_validate_third_step(device_id,get_face_img())
            self.logger.info(f"third_step: {face_img}")
            #print(f"Biometric third_step: {face_img}")
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

            request_create_user = create_user(email_2,name,last_name_12,password,cuil_,dni,phone,device_id,hashs)
            body_create_user = request_create_user.json()
            print(body_create_user)
            if "status" in body_create_user:
                code = body_create_user["status"]["status_code"] 
                self.assertEqual(code, 201)


            log = login(email_2,password)
            log_body = log.json()
            alias=log_body["data"]["client"]["alias"]
            print(f"name: {last_name_12}")
            print(f"alias en db: {alias}")

    def test_raro12_onboarding_success(self):
            email_2 = faker.first_name().lower() + str(faker.random_number(digits=4))+"@movilcash.com"
            phone = int("351" + str(faker.random_number(digits=6)) + "1")
            device_id = faker.random_number(digits=5)
            print(email_2)
            register_email = onboarding_validate_send_email(device_id,email_2)
            response_email = register_email.json()
            #print(response_email)

            if "data" in response_email:
                message = response_email["message"]
                self.assertEqual(message, "email_sent")
                status = response_email["status"]
                self.assertEqual(status, 200)


            # # # # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email_2,code)
            response_code_email = email_code.json()
            #print(response_code_email)
            if "data" in response_code_email:
                validate = response_code_email["data"]["emailValidated"]
                self.assertEqual(validate, True,"No se valido el email")
                status = response_code_email["status"]
                self.assertEqual(status, 200)

            

            # # # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()
            #print(response_sms)

            if "data" in response_sms:
                message = response_sms["message"]
                self.assertEqual(message, "sms_sent")
                status = response_sms["status"]
                self.assertEqual(status, 200)


            # #  VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
            #print(response_code_sms)
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
           # print(body_cuit)
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
            cuil = "20418099691"

            self.logger.info("Runing test: Biometric_validate_frist_step")
            front_dni = biometric_validate_frist_step(device_id,int(cuil),get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
           # print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            

            # # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
           # print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")
            
            # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_third_step")
            face_img = biometric_validate_third_step(device_id,get_face_img())
            self.logger.info(f"third_step: {face_img}")
           # print(f"Biometric third_step: {face_img}")
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

            request_create_user = create_user(email_2,name,last_name_13,password,cuil_,dni,phone,device_id,hashs)
            body_create_user = request_create_user.json()
            print(body_create_user)
            if "status" in body_create_user:
                code = body_create_user["status"]["status_code"] 
                self.assertEqual(code, 201)


            log = login(email_2,password)
            log_body = log.json()
            alias=log_body["data"]["client"]["alias"]
            print(f"name: {last_name_13}")
            print(f"alias en db: {alias}")