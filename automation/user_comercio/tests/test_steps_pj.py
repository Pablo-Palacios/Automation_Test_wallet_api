import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from configuracion.conf_logs import setup_logger_commers
from faker import Faker
from unittest import TestCase
from configuracion.views_comercio import branch_create,checkout_create,representative_create,login_comercio,login_in_whit_email,login_in_whit_email_comercio,create_commerce_pf,validate_commerce,confirm_commerce,confirm_commerce_otp,login_comercio_otp
from configuracion.views_comercio import branch_delete,branch_update,checkout_delete,checkout_update,representative_delete,representative_update,checkout_detail
from configuracion.config import Query_db
from configuracion.code_redi import Redis
import time

dict_roles = {"1":"legal_representative","2":"attorney","3":"attorney"}


faker = Faker()

class Steps(TestCase):
    def test_create_commerce(self):
        
        dni = faker.random_number(digits=8)
        if dni > 8:
             dni = faker.random_number(digits=8)
        cuit = int("33" + str(dni) + "5")
        device_id = faker.random_number(digits=8)
        name = faker.first_name().lower()
        last_name = faker.last_name().lower() + "qacomm"
        email = last_name + "@movilcash.com"
        #email = "pmpmatador@gmail.com"
        phone_ = int("351" + str(faker.random_number(digits=6)) + "1")

        password = "Compablo12."
        new_name = "comer "+faker.last_name().lower() + " test"
        new_commerce = validate_commerce(new_name,cuit,phone_,dni,name,last_name,email,password)
        body_commerce = new_commerce.json()
        print(body_commerce)
        print(f"email comercio = {email}")
        token_commerce = body_commerce["token"]

        if token_commerce:
            confirm_commer = confirm_commerce(token_commerce,cuit)
            body_confirm = confirm_commer.json()
            print(body_confirm)
            status = body_confirm["status"]["status_code"]
            message = body_confirm["message"]
            self.assertEqual(status,401,f"status: {status}")
            #self.assertEqual(message,"OTP Required")
            code = Redis.validacion_token(token_commerce)
            commerce_otp = confirm_commerce_otp(token_commerce,cuit,code)
            body_comerce_otp = commerce_otp.json()
            print(body_comerce_otp)
            assert 'commerce_id' in body_comerce_otp
            assert 'commercial_name' in body_comerce_otp
            assert 'cuit' in body_comerce_otp
            assert 'cvu' in body_comerce_otp
            assert 'alias' in body_comerce_otp
            assert 'balance_id' in body_comerce_otp
            assert 'commercial_activity_afip' in body_comerce_otp
            assert 'branches' in body_comerce_otp
            cvu = body_comerce_otp["cvu"]
            alias = body_comerce_otp["alias"]
            cuit_ = body_comerce_otp["cuit"]
            if cuit_ == 10 or cuit_ == 9:
                 self.fail(f"Se genero un cuit menor a 11. {cuit_}")

            if cvu is not None and alias is not None:
                 self.fail(f"Fallo creacion comercio, cvu y alias creados: cvu: {cvu} - alias: {alias}")
            else:
                pass

    def test_create_commerce_with_cuit_exist(self):
        phone = int("351" + str(faker.random_number(digits=6)) + "1")

        dni = faker.random_number(digits=8)
        if dni > 8:
             dni = faker.random_number(digits=8)
        cuit = int("33" + str(dni) + "5")
        device_id = faker.random_number(digits=8)
        name = faker.first_name().lower()
        last_name = faker.last_name().lower() + "qacomm"
        email = last_name + "@movilcash.com"
        password = "Compablo12."
        new_name = "comer "+faker.last_name().lower() + " test"
        new_commerce = validate_commerce(new_name,cuit,phone,dni,name,last_name,email,password)
        body_commerce = new_commerce.json()
        print(body_commerce)
        status = body_commerce["status"]["status_code"]
        message = body_commerce["message"]
        self.assertEqual(status,400,f"status dife: {status}")
    
    def test_create_commerce_with_email_exist(self):
        phone = int("351" + str(faker.random_number(digits=6)) + "1")

        dni = faker.random_number(digits=8)
        if dni > 8:
             dni = faker.random_number(digits=8)
        cuit = int("33" + str(dni) + "5")
        device_id = faker.random_number(digits=8)
        name = faker.first_name().lower()
        last_name = faker.last_name().lower() + "qacomm"
        email = last_name + "@movilcash.com"
        password = "Compablo12."
        new_name = "comer "+faker.last_name().lower() + " test"
        new_commerce = validate_commerce(new_name,cuit,phone,dni,name,last_name,email,password)
        body_commerce = new_commerce.json()
        print(body_commerce) 
        token_commerce = body_commerce["token"]

        if token_commerce:
            confirm_commer = confirm_commerce(token_commerce,cuit)
            body_confirm = confirm_commer.json()
            print(body_confirm)
            status = body_confirm["status"]["status_code"]
            message = body_confirm["message"]
            self.assertEqual(status,401,f"status: {status}")
            #self.assertEqual(message,"OTP Required")
            code = Redis.validacion_token(token_commerce)
            commerce_otp = confirm_commerce_otp(token_commerce,cuit,code)
            body_comerce_otp = commerce_otp.json()
            print(body_comerce_otp)

            time.sleep(10)
            
            dni_ = faker.random_number(digits=8)
            if dni_ > 8:
                dni_ = faker.random_number(digits=8)
            cuit_ = int("33" + str(dni) + "5")
            device_id = faker.random_number(digits=8)
            name_ = faker.first_name().lower()
            last_name_ = faker.last_name().lower() + "qacomm"
            password_ = "Compablo12."
            new_name_ = "comer "+faker.last_name().lower() + " test"
            new_commerce_ = validate_commerce(new_name_,cuit_,phone,dni,name,last_name_,email,password)
            body_commerce_ = new_commerce_.json()
            print(body_commerce_)          


    def test_create_branch_pj(self):
        
            cuit = 33810754225
            email_ = 'peraltapablito822@gmail.com'
            password_ = "Compablo12."
            device__ = "123"
            
            request_login = login_comercio(cuit,email_, password_,device__)
            response_login = request_login.json()
            print(response_login)
            status = response_login["status"]["status_code"]
            if status == 401:
                user_id_ = Query_db.get_user_id_email(email_)
                print(f"user_id: {user_id_} - device: {device__}")
                 #device_new = faker.random_number(digits=6)
                code_otp = Redis.validacion_otp_login(user_id_,device__)
                #print(code_otp)
                login_new = login_comercio_otp(cuit,email_,password_,device__,code_otp)
                response_login = login_new.json()
            else:
                 pass
            
            token = response_login["data"]["token"]
            name_branch = "branch test" + str(faker.random_number(digits=3))
            create = branch_create(token,name_branch)  
            body_create = create.json()
            print(body_create)
            self.assertEqual(body_create["status"],201,f"Fallo status: {create.status_code}")
            data = body_create["data"]
            assert "branch_id" in data
            assert "commerce_id" in data
            assert "branch_name" in data
            assert "branch_address_id" in data
            commerce_id = data["commerce_id"]
            branch_name = data["branch_name"]
            branch_id = data["branch_id"]


            name_checkout = "test_caja_" + str(faker.random_number(digits=3))
            create_ = checkout_create(token,name_checkout,branch_id)
            body_create_ = create_.json()
            print(body_create_)
            self.assertEqual(body_create_["status"],201)

            # rol = 2
            # repre_type = "attorney"
            # rol = 2

            # phone = int("351" + str(faker.random_number(digits=4)) + "143")
            # dni = faker.random_number(digits=8)
            # name_ = faker.last_name().lower() 
            # #name_ = "Marcos"
            # last_name_ = faker.last_name().lower() + " test"
            # #last_name_ = "Krenz"
            # #email_repre = "marcos.krenz@movilcash.com"
            # email_repre = faker.last_name().lower() + "@movilcash.com"
            # create__ = representative_create(token,rol,repre_type,email_repre,password_,phone,dni,name_,last_name_)
            # body_create__= create__.json()
            # print(body_create__)
            # self.assertEqual(body_create__["status"],201)


    def test_create_representative_rol_2(self):
            # cuit = 33810754225
            # email_ = 'peraltapablito822@gmail.com'
            # password_ = "Compablo12."
            # device__ = "123"

            cuit = 33563426405
            email_ = 'thomasqacomm@movilcash.com'
            password_ = "Compablo12."
            device__ = "1234"
            
            request_login = login_comercio(cuit,email_, password_,device__)
            response_login = request_login.json()
            print(response_login)
            status = response_login["status"]["status_code"]
            if status == 401:
                user_id_ = Query_db.get_user_id_email(email_)
                print(f"user_id: {user_id_} - device: {device__}")
                 #device_new = faker.random_number(digits=6)
                code_otp = Redis.validacion_otp_login(user_id_,device__)
                #print(code_otp)
                login_new = login_comercio_otp(cuit,email_,password_,device__,code_otp)
                response_login = login_new.json()
            else:
                 pass
            
            token = response_login["data"]["token"]
            
            rol = 2
            repre_type = dict_roles[f"{rol}"]

            phone = int("351" + str(faker.random_number(digits=4)) + "143")
            dni = faker.random_number(digits=8)
            name_ = faker.last_name().lower() 
            #name_ = "Marcos"
            last_name_ = faker.last_name().lower() + " test"
            #last_name_ = "Krenz"
            #email_repre = "marcos.krenz@movilcash.com"
            email_repre = faker.last_name().lower() + "@movilcash.com"
            print(f"email_repre: {email_repre}")
            create__ = representative_create(token,rol,repre_type,email_repre,password_,phone,dni,name_,last_name_)
            body_create__= create__.json()
            print(body_create__)
            self.assertEqual(body_create__["status"],201)

    def test_rol_2_can_create_branch(self):
            cuit = 33810754225
            email_ = 'alexander@movilcash.com'
            password_ = "Compablo12."
            device__ = ""
            
            request_login = login_comercio(cuit,email_, password_,device__)
            response_login = request_login.json()
            print(response_login)
            status = response_login["status"]["status_code"]
            self.assertEqual(status,200)
            role = response_login["data"]["client"]["role"]
            self.assertEqual(role,"supervisor")

            token = response_login["data"]["token"]

            name_branch = "branch test" + str(faker.random_number(digits=3))
            create = branch_create(token,name_branch)  
            body_create = create.json()
            print(body_create)
            self.assertEqual(body_create["status"],201,f"Fallo status: {create.status_code}")
            data = body_create["data"]
            assert "branch_id" in data
            assert "commerce_id" in data
            assert "branch_name" in data
            assert "branch_address_id" in data


    def test_rol_2_can_create_checkout(self):
            cuit = 33810754225
            email_ = 'alexander@movilcash.com'
            password_ = "Compablo12."
            device__ = ""
            
            request_login = login_comercio(cuit,email_, password_,device__)
            response_login = request_login.json()
            #print(response_login)
            status = response_login["status"]["status_code"]
            self.assertEqual(status,200)
            role = response_login["data"]["client"]["role"]
            self.assertEqual(role,"supervisor")

            token = response_login["data"]["token"]
            name_branch = "branch test" + str(faker.random_number(digits=3))
            create = branch_create(token,name_branch)  
            body_create = create.json()
            #print(body_create)
            self.assertEqual(body_create["status"],201,f"Fallo status: {create.status_code}")
            data = body_create["data"]
            assert "branch_id" in data
            assert "commerce_id" in data
            assert "branch_name" in data
            assert "branch_address_id" in data
            commerce_id = data["commerce_id"]
            branch_name = data["branch_name"]
            branch_id = data["branch_id"]


            name_checkout = "test_caja_" + str(faker.random_number(digits=3))
            create_ = checkout_create(token,name_checkout,branch_id)
            body_create_ = create_.json()
            print(body_create_)
            self.assertEqual(body_create_["status"],201)

    
    def test_create_representative_rol_3(self):
            cuit = 33810754225
            email_ = 'peraltapablito822@gmail.com'
            password_ = "Compablo12."
            device__ = "123"
            
            request_login = login_comercio(cuit,email_, password_,device__)
            response_login = request_login.json()
            print(response_login)
            status = response_login["status"]["status_code"]
            if status == 401:
                user_id_ = Query_db.get_user_id_email(email_)
                print(f"user_id: {user_id_} - device: {device__}")
                 #device_new = faker.random_number(digits=6)
                code_otp = Redis.validacion_otp_login(user_id_,device__)
                #print(code_otp)
                login_new = login_comercio_otp(cuit,email_,password_,device__,code_otp)
                response_login = login_new.json()
            else:
                 pass
            
            token = response_login["data"]["token"]
            repre_type = "attorney"
            rol = 3

            phone = int("351" + str(faker.random_number(digits=4)) + "143")
            dni = faker.random_number(digits=8)
            name_ = faker.last_name().lower() 
            #name_ = "Marcos"
            last_name_ = faker.last_name().lower() + " test"
            #last_name_ = "Krenz"
            email_repre = faker.last_name().lower() + "@movilcash.com"
            print(f"email_repre: {email_repre}")
            create__ = representative_create(token,rol,repre_type,email_repre,password_,phone,dni,name_,last_name_)
            body_create__= create__.json()
            print(body_create__)
            self.assertEqual(body_create__["status"],201)

    def test_rol_3_can_create_branch(self):
            cuit = 33810754225
            email_ = 'robinson@movilcash.com'
            password_ = "Compablo12."
            device__ = ""
            
            request_login = login_comercio(cuit,email_, password_,device__)
            response_login = request_login.json()
            print(response_login)
            status = response_login["status"]["status_code"]
            self.assertEqual(status,200)
            role = response_login["data"]["client"]["role"]
            self.assertEqual(role,"cashier")

            token = response_login["data"]["token"]
            name_branch = "branch test" + str(faker.random_number(digits=3))
            create = branch_create(token,name_branch)  
            body_create = create.json()
            #print(body_create)
            self.assertEqual(body_create["status"],201,f"Fallo status: {create.status_code}")
            data = body_create["data"]
            assert "branch_id" in data
            assert "commerce_id" in data
            assert "branch_name" in data
            assert "branch_address_id" in data
            

    def test_rol_3_can_create_checkout(self):
            cuit = 33810754225
            email_ = 'robinson@movilcash.com'
            password_ = "Compablo12."
            device__ = ""
            
            request_login = login_comercio(cuit,email_, password_,device__)
            response_login = request_login.json()
            print(response_login)
            status = response_login["status"]["status_code"]
            self.assertEqual(status,200)
            role = response_login["data"]["client"]["role"]
            self.assertEqual(role,"cashier")

            token = response_login["data"]["token"]
            name_branch = "branch test" + str(faker.random_number(digits=3))
            create = branch_create(token,name_branch)  
            body_create = create.json()
            #print(body_create)
            self.assertEqual(body_create["status"],201,f"Fallo status: {create.status_code}")
            data = body_create["data"]
            assert "branch_id" in data
            assert "commerce_id" in data
            assert "branch_name" in data
            assert "branch_address_id" in data
            commerce_id = data["commerce_id"]
            branch_name = data["branch_name"]
            branch_id = data["branch_id"]


            name_checkout = "test_caja_" + str(faker.random_number(digits=3))
            create_ = checkout_create(token,name_checkout,branch_id)
            body_create_ = create_.json()
            print(body_create_)
            self.assertEqual(body_create_["status"],201)

    def test_rol_3_can_create_representative_1(self):
            cuit = 33810754225
            email_ = 'robinson@movilcash.com'
            password_ = "Compablo12."
            device__ = ""
            
            request_login = login_comercio(cuit,email_, password_,device__)
            response_login = request_login.json()
            print(response_login)
            status = response_login["status"]["status_code"]
            self.assertEqual(status,200)
            role = response_login["data"]["client"]["role"]
            self.assertEqual(role,"cashier")

            token = response_login["data"]["token"]
            rol = 1
            repre_type = dict_roles[f"{rol}"]
            phone = int("351" + str(faker.random_number(digits=4)) + "143")
            dni = faker.random_number(digits=8)
            name_ = faker.last_name().lower() 
            #name_ = "Marcos"
            last_name_ = faker.last_name().lower() + " test"
            #last_name_ = "Krenz"
            email_repre = faker.last_name().lower() + "@movilcash.com"
            print(f"email_repre: {email_repre}")
            create__ = representative_create(token,rol,repre_type,email_repre,password_,phone,dni,name_,last_name_)
            body_create__= create__.json()
            print(body_create__)
            self.assertEqual(body_create__["status"],201)

    def test_rol_3_can_create_representative_2(self):
            cuit = 33810754225
            email_ = 'robinson@movilcash.com'
            password_ = "Compablo12."
            device__ = ""
            
            request_login = login_comercio(cuit,email_, password_,device__)
            response_login = request_login.json()
            print(response_login)
            status = response_login["status"]["status_code"]
            self.assertEqual(status,200)
            role = response_login["data"]["client"]["role"]
            self.assertEqual(role,"cashier")

            token = response_login["data"]["token"]
            rol = 2
            repre_type = dict_roles[f"{rol}"]
            phone = int("351" + str(faker.random_number(digits=4)) + "143")
            dni = faker.random_number(digits=8)
            name_ = faker.last_name().lower() 
            #name_ = "Marcos"
            last_name_ = faker.last_name().lower() + " test"
            #last_name_ = "Krenz"
            email_repre = faker.last_name().lower() + "@movilcash.com"
            print(f"email_repre: {email_repre}")
            create__ = representative_create(token,rol,repre_type,email_repre,password_,phone,dni,name_,last_name_)
            body_create__= create__.json()
            print(body_create__)
            self.assertEqual(body_create__["status"],201)

    def test_rol_3_can_create_representative_3(self):
            cuit = 33810754225
            email_ = 'robinson@movilcash.com'
            password_ = "Compablo12."
            device__ = ""
            
            request_login = login_comercio(cuit,email_, password_,device__)
            response_login = request_login.json()
            print(response_login)
            status = response_login["status"]["status_code"]
            self.assertEqual(status,200)
            role = response_login["data"]["client"]["role"]
            self.assertEqual(role,"cashier")

            token = response_login["data"]["token"]
            rol = 3
            repre_type = dict_roles[f"{rol}"]
            phone = int("351" + str(faker.random_number(digits=4)) + "143")
            dni = faker.random_number(digits=8)
            name_ = faker.last_name().lower() 
            #name_ = "Marcos"
            last_name_ = faker.last_name().lower() + " test"
            #last_name_ = "Krenz"
            email_repre = faker.last_name().lower() + "@movilcash.com"
            print(f"email_repre: {email_repre}")
            create__ = representative_create(token,rol,repre_type,email_repre,password_,phone,dni,name_,last_name_)
            body_create__= create__.json()
            print(body_create__)
            self.assertEqual(body_create__["status"],201)

    def test_rol_2_can_delete_branch(self):
            cuit = 33810754225
            email_ = 'alexander@movilcash.com'
            password_ = "Compablo12."
            device__ = ""
            
            request_login = login_comercio(cuit,email_, password_,device__)
            response_login = request_login.json()
            #print(response_login)
            status = response_login["status"]["status_code"]
            self.assertEqual(status,200)
            role = response_login["data"]["client"]["role"]
            self.assertEqual(role,"supervisor")

            token = response_login["data"]["token"]
            # name_branch = "branch test" + str(faker.random_number(digits=3))
            # create = branch_create(token,name_branch)  
            # body_create = create.json()
            # print(body_create)
            # self.assertEqual(body_create["status"],201,f"Fallo status: {create.status_code}")
            # data = body_create["data"]
            # assert "branch_id" in data
            # assert "commerce_id" in data
            # assert "branch_name" in data
            # assert "branch_address_id" in data
            # commerce_id = data["commerce_id"]
            # branch_name = data["branch_name"]
            # branch_id = data["branch_id"]
            branch_id = 442
            delete = branch_delete(token,branch_id)
            body_delete = delete.json()
            print(body_delete)
            
            status = body_delete["status"]["status_code"]
            if status == 400:
                self.fail(f"{body_delete}")
            else:
                self.assertEqual(status,204)
                print(f"response success: {body_delete}")


    def test_rol_2_can_delete_checkout(self):
            cuit = 33810754225
            email_ = 'alexander@movilcash.com'
            password_ = "Compablo12."
            device__ = ""
            
            request_login = login_comercio(cuit,email_, password_,device__)
            response_login = request_login.json()
            #print(response_login)
            status = response_login["status"]["status_code"]
            self.assertEqual(status,200)
            role = response_login["data"]["client"]["role"]
            self.assertEqual(role,"supervisor")

            token = response_login["data"]["token"]
            # name_branch = "branch test" + str(faker.random_number(digits=3))
            # create = branch_create(token,name_branch)  
            # body_create = create.json()
            # #print(body_create)
            # self.assertEqual(body_create["status"],201,f"Fallo status: {create.status_code}")
            # data = body_create["data"]
            # assert "branch_id" in data
            # assert "commerce_id" in data
            # assert "branch_name" in data
            # assert "branch_address_id" in data
            # commerce_id = data["commerce_id"]
            # branch_name = data["branch_name"]
            # branch_id = data["branch_id"]


            # name_checkout = "test_caja_" + str(faker.random_number(digits=3))
            # create_ = checkout_create(token,name_checkout,branch_id)
            # body_create_ = create_.json()
            # print(body_create_)
            # self.assertEqual(body_create_["status"],201)
            # checkout_id = body_create_["data"]["checkout_id"]
            # print(checkout_id)

            checkout_id = 420
            branch_id = 445

            details = checkout_detail(token,checkout_id)
            body_detail = details.json()
            print(body_detail)

            delete = checkout_delete(token,checkout_id,branch_id)
            body_delete = delete.json()
            print(body_delete)
            status = body_delete["status"]["status_code"]
            if status == 400:
                self.fail(f"{body_delete}")
            else:
                self.assertEqual(body_delete["status"],200)
            print(f"response success: {body_delete}") 


    def test_rol_2_can_delete_representative(self):
            cuit = 33810754225
            email_ = 'alexander@movilcash.com'
            password_ = "Compablo12."
            device__ = ""
            
            request_login = login_comercio(cuit,email_, password_,device__)
            response_login = request_login.json()
            #print(response_login)
            status = response_login["status"]["status_code"]
            self.assertEqual(status,200)
            role = response_login["data"]["client"]["role"]
            self.assertEqual(role,"supervisor")

            token = response_login["data"]["token"]

            
            rol = 2
            repre_type = dict_roles[f"{rol}"]
            phone = int("351" + str(faker.random_number(digits=4)) + "143")
            dni = faker.random_number(digits=8)
            name_ = faker.last_name().lower() 
            #name_ = "Marcos"
            last_name_ = faker.last_name().lower() + " test"
            #last_name_ = "Krenz"
            #email_repre = "marcos.krenz@movilcash.com"
            email_repre = faker.last_name().lower() + "@movilcash.com"
            create__ = representative_create(token,rol,repre_type,email_repre,password_,phone,dni,name_,last_name_)
            body_create__= create__.json()
            print(body_create__)
            self.assertEqual(body_create__["status"],201)

            repre_id = body_create__["data"]["representative_id"]

            delete = representative_delete(token,repre_id)
            body_delete = delete.json()
            print(body_delete)

            status = body_delete["status"]
            self.assertEqual(status,204)

            