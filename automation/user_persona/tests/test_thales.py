import sys
import os

from faker import Faker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from configuracion.code_redi import Redis
from img_thales.back_img import get_back_leo,get_back_img,get_back_dni_vencido,get_back_menor
from img_thales.front_img import get_front_dni_vencido,get_front_img,get_front_menor,get_leo_front
from img_thales.face_img import get_face_leo,get_face_img,get_face_2_img
from img_thales.dni_2011 import front_white_image,back_white_image
from img_thales.licencia_img import get_front_licencia,get_back_licencia
from configuracion.views_persona import biometric_validate_frist_step,biometric_validate_second_step,biometric_validate_third_step, onboarding_validate_code_otp_email, onboarding_validate_code_otp_sms, onboarding_validate_cuil, onboarding_validate_send_email, onboarding_validate_send_sms
import time
from img_thales.img_agustin_bruno import get_back_dni_agus,get_front_dni_agus
from configuracion.conf_logs import setup_logger
from unittest import TestCase
from configuracion.main import email,device_id

faker = Faker()
phone = int("351" + str(faker.random_number(digits=6)) + "1")


def onboarding():
            
            #email= "robertgood@movilcash.com"
            ## REGISTER EMAIL 

            dic = {}
            print(email)
            register_email = onboarding_validate_send_email(device_id,email)
            response_email = register_email.json()
            

            # # # # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email,code)
            response_code_email = email_code.json()
        
            # # # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()

            # #  VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
            

            # # VALIDATE CUIT 
            
            cuil_ = int("20" + str(faker.random_number(digits=8)) + "1")
            
            # #cuil_ = "27220623748"
            # #cuil_ = "20295533871"
            # #cuil_ = "20418099691"
            validate_cuit = onboarding_validate_cuil(device_id,cuil_)
            body_cuit = validate_cuit.json()
            device_id_validate = body_cuit["data"]["deviceId"]
            cuil_validate = body_cuit["data"]["cuil"]

            

            dic = {"cuil":cuil_validate, "device_id":device_id_validate}

            return dic



class Thales(TestCase):
        
    def setUp(self):
            #config el logger
            self.logger = setup_logger()

    def test_a_all_steps_success(self):
            data_user = onboarding()
            cuil = "20418099691"
            device_id_ = data_user["device_id"]
        
            self.logger.info("Runing test: Biometric_validate_frist_step")
            front_dni = biometric_validate_frist_step(device_id_,cuil,get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            
            # # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_second_step_pegada directa")
            back_dni = biometric_validate_second_step(device_id_,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")
            
            # time.sleep(15)
            self.logger.info("Runing test: Biometric_validate_third_step")
            face_img = biometric_validate_third_step(device_id_,get_face_img())
            self.logger.info(f"third_step: {face_img}")
            #print(f"Biometric third_step: {face_img}")
            status_step_3 = face_img["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_3,True,"No paso el step 3")

            hashs = face_img["data"]["approvedHash"]

            if hashs == None or hashs == '':
                self.fail("No se genero el hashs!!")


    def test_b_fail_step_1_and_pass(self):
            data_user = onboarding()
            cuil ="20303918520"
            device_id_ = data_user["device_id"]
        
            self.logger.info("Runing test: test_fail_step_1_and_pass")
            front_dni = biometric_validate_frist_step(device_id_,cuil,get_back_leo())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            #self.assertEqual(status_step_1,False,"No paso el step 1")
            if status_step_1 == False:
                time.sleep(5)
                self.logger.info("Biometric_validate_frist_step_second_try")
                front_dni = biometric_validate_frist_step(device_id_,cuil,get_leo_front())
                #print(front_dni)
                log_front_dni = front_dni.json()
                self.logger.info(f"first_step: {log_front_dni}")
                #print(f"Biometric first_step: {log_front_dni}")
                status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
                self.assertEqual(status_step_1,True,"No paso el step 1")

                self.logger.info("Biometric_validate_second_step")
                back_dni = biometric_validate_second_step(device_id_,get_back_leo())
                self.logger.info(f"second_step: {back_dni}")
                #print(f"Biometric second_step: {back_dni}")
                status_step_2 = back_dni["data"]["biometricStatus"]["status"]
                self.assertEqual(status_step_2,True,"No paso el step 2")
                
                # time.sleep(15)
                self.logger.info("Biometric_validate_third_step")
                face_img = biometric_validate_third_step(device_id_,get_face_leo())
                self.logger.info(f"third_step: {face_img}")
                #print(f"Biometric third_step: {face_img}")
                status_step_3 = face_img["data"]["biometricStatus"]["status"]
                self.assertEqual(status_step_3,True,"No paso el step 3")

                hashs = face_img["data"]["approvedHash"]

                if hashs == None or hashs == '':
                    self.fail("No se genero el hashs!!")
                    
            else:
                self.fail("step 1 no fallo")


    def test_c_fail_step_2_and_pass(self):
            data_user = onboarding()
            cuil = "20418099691"
            device_id_ = data_user["device_id"]
        
            self.logger.info("Runing test: test_fail_step_2_and_pass")
            front_dni = biometric_validate_frist_step(device_id_,cuil,get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            self.logger.info("Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id_,get_front_img())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            #self.assertEqual(status_step_2,True,"No paso el step 2")
            if status_step_2 == False:
                time.sleep(5)
                
                self.logger.info("Biometric_validate_second_step_second_try")
                back_dni = biometric_validate_second_step(device_id_,get_back_img())
                self.logger.info(f"second_step: {back_dni}")
                #print(f"Biometric second_step: {back_dni}")
                status_step_2 = back_dni["data"]["biometricStatus"]["status"]
                self.assertEqual(status_step_2,True,"No paso el step 2")
                
                # time.sleep(15)
                self.logger.info("Biometric_validate_third_step")
                face_img = biometric_validate_third_step(device_id_,get_face_img())
                self.logger.info(f"third_step: {face_img}")
                #print(f"Biometric third_step: {face_img}")
                status_step_3 = face_img["data"]["biometricStatus"]["status"]
                self.assertEqual(status_step_3,True,"No paso el step 3")

                hashs = face_img["data"]["approvedHash"]

                if hashs == None or hashs == '':
                    self.fail("No se genero el hashs!!")
                
            else:
                self.fail("step 2 no fallo")


    def test_d_fail_step_3_and_pass(self):
            data_user = onboarding()
            cuil = "20418099691"
            device_id_ = data_user["device_id"]
        
            self.logger.info("Runing test: test_fail_step_3_and_pass")
            self.logger.info("Biometric_validate_first_step")
            front_dni = biometric_validate_frist_step(device_id_,cuil,get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            self.logger.info("Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id_,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")


            self.logger.info("Biometric_validate_third_step_second_try")
            face_img = biometric_validate_third_step(device_id_,get_face_leo())
            self.logger.info(f"third_step: {face_img}")
            #print(f"Biometric third_step: {face_img}")
            status_step_3 = face_img["data"]["biometricStatus"]["status"]
            #self.assertEqual(status_step_3,True,"No paso el step 3")
        
            if status_step_3 == False:
                time.sleep(5)
                
                self.logger.info("Biometric_validate_third_step")
                face_img = biometric_validate_third_step(device_id_,get_face_img())
                self.logger.info(f"third_step: {face_img}")
                #print(f"Biometric third_step: {face_img}")
                status_step_3 = face_img["data"]["biometricStatus"]["status"]
                self.assertEqual(status_step_3,True,"No paso el step 3")

                hashs = face_img["data"]["approvedHash"]

                if hashs == None or hashs == '':
                    self.fail("No se genero el hashs!!")
                
            else:
                self.fail("step 3 no fallo")


    def test_e_fail_step_1_attemps_2_and_pass(self):
            data_user = onboarding()
            cuil = "20418099691"
            device_id_ = data_user["device_id"]
        
            self.logger.info("Runing test: test_fail_step_1_attemps_2_and_pass")
            self.logger.info("Biometric_validate_first_step")
            front_dni = biometric_validate_frist_step(device_id_,cuil,get_back_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            #self.assertEqual(status_step_1,True,"No paso el step 1")
            if status_step_1 == False:
                time.sleep(5)

                self.logger.info("Biometric_validate_first_step_second_try_fail")
                front_dni = biometric_validate_frist_step(device_id_,cuil,get_back_img())
                #print(front_dni)
                log_front_dni = front_dni.json()
                self.logger.info(f"first_step: {log_front_dni}")
                #print(f"Biometric first_step: {log_front_dni}")
                status_step_1= log_front_dni["data"]["biometricStatus"]["status"]

                if status_step_1 == False:
                    time.sleep(5)

                    self.logger.info("Biometric_validate_first_step_third_try")
                    front_dni = biometric_validate_frist_step(device_id_,cuil,get_front_img())
                    #print(front_dni)
                    log_front_dni = front_dni.json()
                    self.logger.info(f"first_step: {log_front_dni}")
                    #print(f"Biometric first_step: {log_front_dni}")
                    status_step_1= log_front_dni["data"]["biometricStatus"]["status"]


                    self.logger.info("Biometric_validate_second_step")
                    back_dni = biometric_validate_second_step(device_id_,get_back_img())
                    self.logger.info(f"second_step: {back_dni}")
                    #print(f"Biometric second_step: {back_dni}")
                    status_step_2 = back_dni["data"]["biometricStatus"]["status"]
                    self.assertEqual(status_step_2,True,"No paso el step 2")


                    self.logger.info("Biometric_validate_third_step_second_try")
                    face_img = biometric_validate_third_step(device_id_,get_face_img())
                    self.logger.info(f"third_step: {face_img}")
                    #print(f"Biometric third_step: {face_img}")
                    status_step_3 = face_img["data"]["biometricStatus"]["status"]
                    self.assertEqual(status_step_3,True,"No paso el step 3")

                    hashs = face_img["data"]["approvedHash"]

                    if hashs == None or hashs == '':
                        self.fail("No se genero el hashs!!")


                else:
                    self.fail("step 1 no fallo, attemps 2")
                
            else:
                self.fail("step 1 no fallo, attemps 1")


    def test_f_fail_step_2_attemps_2_and_pass(self):
            data_user = onboarding()
            cuil = "20418099691"
            device_id_ = data_user["device_id"]
        
            self.logger.info("Runing test: test_fail_step_2_attemps_2_and_pass")
            self.logger.info("Biometric_validate_first_step")
            front_dni = biometric_validate_frist_step(device_id_,cuil,get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            
            self.logger.info("Biometric_validate_second_step_attemps_0")
            back_dni = biometric_validate_second_step(device_id_,get_front_img())
            self.logger.info(f"second_step: {back_dni}")
                    #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
                #self.assertEqual(status_step_2,True,"No paso el step 2")

        
            if status_step_2 == False:
                time.sleep(5)

                self.logger.info("Biometric_validate_second_step_attemps_1")
                back_dni = biometric_validate_second_step(device_id_,get_front_img())
                self.logger.info(f"second_step: {back_dni}")
                    #print(f"Biometric second_step: {back_dni}")
                status_step_2 = back_dni["data"]["biometricStatus"]["status"]
                #self.assertEqual(status_step_2,True,"No paso el step 2")

                if status_step_2 == False:
                    time.sleep(5)

                    self.logger.info("Biometric_validate_second_step_2")
                    back_dni = biometric_validate_second_step(device_id_,get_back_img())
                    self.logger.info(f"second_step: {back_dni}")
                    #print(f"Biometric second_step: {back_dni}")
                    status_step_2 = back_dni["data"]["biometricStatus"]["status"]
                    self.assertEqual(status_step_2,True,"No paso el step 2")


                    self.logger.info("Biometric_validate_third_step")
                    face_img = biometric_validate_third_step(device_id_,get_face_img())
                    self.logger.info(f"third_step: {face_img}")
                    #print(f"Biometric third_step: {face_img}")
                    status_step_3 = face_img["data"]["biometricStatus"]["status"]
                    self.assertEqual(status_step_3,True,"No paso el step 3")

                    hashs = face_img["data"]["approvedHash"]

                    if hashs == None or hashs == '':
                        self.fail("No se genero el hashs!!")

                else:
                    self.fail("step 2 no fallo, attemps 2")
                
            else:
                self.fail("step 2 no fallo, attemps 1")

     
    def test_g_fail_step_3_attemps_2_and_pass(self):
            
             
            data_user = onboarding()
            cuil = "20418099691"
            device_id_ = data_user["device_id"]
        
            self.logger.info("Runing test: test_fail_step_23_attemps_2_and_pass")
            self.logger.info("Biometric_validate_first_step")
            front_dni = biometric_validate_frist_step(device_id_,cuil,get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")

            
            self.logger.info("Biometric_validate_second_step_attemps_0")
            back_dni = biometric_validate_second_step(device_id_,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
                    #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
                #self.assertEqual(status_step_2,True,"No paso el step 2")
            
            self.logger.info("Biometric_validate_third_step_attemps_0")
            face_img = biometric_validate_third_step(device_id_,get_face_leo())
            self.logger.info(f"third_step: {face_img}")
                    #print(f"Biometric third_step: {face_img}")
            status_step_3 = face_img["data"]["biometricStatus"]["status"]
            #self.assertEqual(status_step_3,True,"No paso el step 3")

        
            if status_step_3 == False:
                time.sleep(5)

                self.logger.info("Biometric_validate_third_step_attemps_1")
                face_img = biometric_validate_third_step(device_id_,get_face_leo())
                self.logger.info(f"third_step: {face_img}")
                        #print(f"Biometric third_step: {face_img}")
                status_step_3 = face_img["data"]["biometricStatus"]["status"]
                #self.assertEqual(status_step_3,True,"No paso el step 3")

                if status_step_3 == False:
                    time.sleep(5)

                
                    self.logger.info("Biometric_validate_third_step_attemps_2")
                    face_img = biometric_validate_third_step(device_id_,get_face_img())
                    self.logger.info(f"third_step: {face_img}")
                    #print(f"Biometric third_step: {face_img}")
                    status_step_3 = face_img["data"]["biometricStatus"]["status"]
                    self.assertEqual(status_step_3,True,"No paso el step 3")

                    hashs = face_img["data"]["approvedHash"]

                    if hashs == None or hashs == '':
                        self.fail("No se genero el hashs!!")


                else:
                    self.fail("step 3 no fallo, attemps 2")
                
            else:
                self.fail("step 3 no fallo, attemps 1")


    def test_h_fail_step_1_all_attemps_and_eliminate_contex(self):
            data_user = onboarding()
            cuil = "20418099691"
            device_id_ = data_user["device_id"]
        
            self.logger.info("Runing test: test_fail_step_1_all_attemps_and_eliminate_contex")
            self.logger.info("Biometric_validate_first_step_attepms_0")
            front_dni = biometric_validate_frist_step(device_id_,cuil,get_back_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            #self.assertEqual(status_step_1,True,"No paso el step 1")
            if status_step_1 == False:
                time.sleep(3)
                self.logger.info("Biometric_validate_first_step_attepms_1")
                front_dni = biometric_validate_frist_step(device_id_,cuil,get_back_img())
                #print(front_dni)
                log_front_dni = front_dni.json()
                self.logger.info(f"first_step: {log_front_dni}")
                #print(f"Biometric first_step: {log_front_dni}")
                status_step_1= log_front_dni["data"]["biometricStatus"]["status"]

                if status_step_1 == False:
                    time.sleep(3)
                    self.logger.info("Biometric_validate_first_step_attepms_2")
                    front_dni = biometric_validate_frist_step(device_id_,cuil,get_back_img())
                    #print(front_dni)
                    log_front_dni = front_dni.json()
                    self.logger.info(f"first_step: {log_front_dni}")
                    #print(f"Biometric first_step: {log_front_dni}")
                    #status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
                    self.assertEqual(front_dni["code"],400)
                    self.assertEqual(front_dni["message"],'InternalError: available attempts exhausted')
                else:
                        self.fail("step 1 no fallo, attemps 2")
                
            else:
                self.fail("step 1 no fallo, attemps 1")

                    


    
    def test_i_fail_step_2_all_attemps_and_eliminate_contex(self):
            data_user = onboarding()
            cuil = "20418099691"
            device_id_ = data_user["device_id"]
        
            self.logger.info("Runing test: test_fail_step_2_all_attemps_and_eliminate_contex")
            self.logger.info("Biometric_validate_first_step")
            front_dni = biometric_validate_frist_step(device_id_,cuil,get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")


            self.logger.info("Biometric_validate_second_step_attemps_0")
            back_dni = biometric_validate_second_step(device_id_,get_front_img())
            self.logger.info(f"second_step: {back_dni}")
                    #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
                #self.assertEqual(status_step_2,True,"No paso el step 2")
            if status_step_2 == False:
                time.sleep(3)
                self.logger.info("Biometric_validate_second_step_attemps_1")
                back_dni = biometric_validate_second_step(device_id_,get_front_img())
                self.logger.info(f"second_step: {back_dni}")
                        #print(f"Biometric second_step: {back_dni}")
                status_step_2 = back_dni["data"]["biometricStatus"]["status"]

                if status_step_2 == False:
                    time.sleep(3)
                    self.logger.info("Biometric_validate_second_step_attemps_2")
                    back_dni = biometric_validate_second_step(device_id_,get_front_img())
                    self.logger.info(f"second_step: {back_dni}")
                            #print(f"Biometric second_step: {back_dni}")
                   # status_step_2 = back_dni["data"]["biometricStatus"]["status"]
                    self.assertEqual(back_dni["code"],400)
                    self.assertEqual(back_dni["message"],'InternalError: available attempts exhausted')

                else:
                    self.fail("step 2 no fallo, attemps 2")
                
            else:
                self.fail("step 2 no fallo, attemps 1")


    
    def test_j_fail_step_3_all_attemps_and_eliminate_contex(self):
            data_user = onboarding()
            cuil = "20418099691"
            device_id_ = data_user["device_id"]
        
            self.logger.info("Runing test: test_fail_step_3_all_attemps_and_eliminate_contex")
            self.logger.info("Biometric_validate_first_step")
            front_dni = biometric_validate_frist_step(device_id_,cuil,get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")


            self.logger.info("Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id_,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")


            self.logger.info("Biometric_validate_third_step_attemps_0")
            face_img = biometric_validate_third_step(device_id_,get_face_leo())
            self.logger.info(f"third_step: {face_img}")
                    #print(f"Biometric third_step: {face_img}")
            status_step_3 = face_img["data"]["biometricStatus"]["status"]

            if status_step_3 == False:
                time.sleep(3)
                self.logger.info("Biometric_validate_third_step_attemps_1")
                face_img = biometric_validate_third_step(device_id_,get_face_leo())
                self.logger.info(f"third_step: {face_img}")
                        #print(f"Biometric third_step: {face_img}")
                status_step_3 = face_img["data"]["biometricStatus"]["status"]


                if status_step_3 == False:
                    time.sleep(3)
                    self.logger.info("Biometric_validate_third_step_attemps_2")
                    face_img = biometric_validate_third_step(device_id_,get_face_leo())
                    self.logger.info(f"third_step: {face_img}")
                            #print(f"Biometric third_step: {face_img}")
                    self.assertEqual(face_img["code"],400)
                    self.assertEqual(face_img["message"],'InternalError: available attempts exhausted')

                else:
                    self.fail("step 3 no fallo, attemps 2")
                
            else:
                self.fail("step 3 no fallo, attemps 1")

    
    def test_k_dni_vencido_black_list(self):
            data_user = onboarding()
            cuil = "20418099691"
            device_id_ = data_user["device_id"]
        
            self.logger.info("Runing test: test_dni_vencido_black_list")
            self.logger.info("Biometric_validate_first_step")
            front_dni = biometric_validate_frist_step(device_id_,cuil,get_front_dni_vencido())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,False,"paso el step 1")


            self.logger.info("Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id_,get_back_dni_vencido())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            #status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(back_dni["message"],'Endpoint request timed out',"paso el step 2")



    
    def test_m_dni_ejemplar_2011(self):
            data_user = onboarding()
            cuil = ""
            device_id_ = data_user["device_id"]
        
            self.logger.info("Runing test: test_dni_ejemplar_2011")
            self.logger.info("Biometric_validate_first_step")
            front_dni = biometric_validate_frist_step(device_id_,cuil,front_white_image)
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")


            self.logger.info("Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id_,back_white_image)
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_2,True,"No paso el step 2")



    def test_n_dni_menor_edad(self):
            data_user = onboarding()
            cuil = "20558351080"
            device_id_ = data_user["device_id"]
        
            self.logger.info("Runing test: test_dni_ejemplar_2011")
            self.logger.info("Biometric_validate_first_step")
            front_dni = biometric_validate_frist_step(device_id_,cuil,get_front_menor())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")


            self.logger.info("Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id_,get_back_menor())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            #status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(back_dni["code"],400,"paso el step 2")
    

    def test_l_licencia_conducir(self):
            data_user = onboarding()
            cuil = "20418099691"
            device_id_ = data_user["device_id"]
        
            self.logger.info("Runing test: test_dni_ejemplar_2011")
            self.logger.info("Biometric_validate_first_step")
            front_dni = biometric_validate_frist_step(device_id_,cuil,get_front_licencia())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            #status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(front_dni.status_code,400,"paso el step 1")
            #self.assertEqual(front_dni["message"],'InternalError: all retries fail: 3')
        

        #     self.logger.info("Biometric_validate_second_step")
        #     back_dni = biometric_validate_second_step(device_id_,get_back_licencia())
        #     self.logger.info(f"second_step: {back_dni}")
        #     #print(f"Biometric second_step: {back_dni}")
        #     status_step_2 = back_dni["data"]["biometricStatus"]["status"]
        #     self.assertEqual(status_step_2,False,"No paso el step 2")

    def test_fail_cuil(self):
            data_user = onboarding()
            cuil = data_user["cuil"]
            device_id_ = data_user["device_id"]
        
            self.logger.info("Runing test: test_dni_ejemplar_2011")
            self.logger.info("Biometric_validate_first_step")
            front_dni = biometric_validate_frist_step(device_id_,cuil,get_front_img())
            #print(front_dni)
            log_front_dni = front_dni.json()
            self.logger.info(f"first_step: {log_front_dni}")
            #print(f"Biometric first_step: {log_front_dni}")
            status_step_1= log_front_dni["data"]["biometricStatus"]["status"]
            self.assertEqual(status_step_1,True,"No paso el step 1")


            self.logger.info("Biometric_validate_second_step")
            back_dni = biometric_validate_second_step(device_id_,get_back_img())
            self.logger.info(f"second_step: {back_dni}")
            #print(f"Biometric second_step: {back_dni}")
            #status_step_2 = back_dni["data"]["biometricStatus"]["status"]
            
            self.assertEqual(back_dni["code"],400,"paso el step 2")
            self.assertEqual(back_dni["message"], "InternalError: The CUIL is not correct")

    # def test_picture_front_dni(self):
    #     pass

    # def test_picture_back_dni(self):
    #     pass

    # def test_picture_face(self):
    #     pass

    # def test_picture_face_ia(self):
    #     pass

    