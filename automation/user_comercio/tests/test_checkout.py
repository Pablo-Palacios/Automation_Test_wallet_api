import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from configuracion.conf_logs import setup_logger_commers
from faker import Faker
from unittest import TestCase
from configuracion.views_comercio import checkout_create,checkout_delete,checkout_detail,checkout_list,checkout_update,login,login_comercio,login_in_whit_email_comercio,login_in_whit_email,branch_create,login_comercio_otp
from configuracion.config import Query_db
from configuracion.code_redi import Redis
faker = Faker()



def login_user():

            cuit = 33810754225
            email_ = 'peraltapablito822@gmail.com'
            password_ = "Compablo12."
            device_ = "1234"

            dic = {}
            
            request_login = login_comercio(cuit,email_, password_,device_)
            response_login = request_login.json()
            #print(response_login)
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
            
            
            if "data" in response_login:
                # data = response_login["data"]
                # client = response_login["data"]["client"]
                token = response_login["data"]["token"]

            dic = {"token":f"{token}"}

            return dic



class Checkout(TestCase):
    def setUp(self):
         #config el logger
         self.logger = setup_logger_commers()
    
    def test_create_checkout(self):
        log = login_user()
        token = log["token"]

        self.logger.info("Running test: test_create_checkout")

        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create_ = branch_create(token,name_branch)
        body_create_ = create_.json()
        branch_id = body_create_["data"]["branch_id"]

        name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        create = checkout_create(token,name_checkout,branch_id)
        body_create = create.json()
        print(body_create)
        self.logger.info(f"response: {body_create}")
        status = body_create["status"]
        if status != 201:
            self.fail(f"{body_create}")
        else:
            self.assertEqual(body_create["status"],201)
            print(f"response success: {body_create}")
            data = body_create["data"]
            assert "checkout_id" in data
            assert "checkout_name" in data
            assert "checkout_qr" in data
            assert "branch_id" in data
            checkout_id = data["checkout_id"]
            checkout_name = data["checkout_name"]
            checkout_qr = data["checkout_qr"]

            data_db = Query_db.get_checkout_info_with_name(checkout_id)
            self.assertEqual(data_db, checkout_name,"No coinciden checkout_name en db")
            if checkout_qr is None:
                print(f"Campo checkout QR vacio: {checkout_qr}")
            else:
                pass



    def test_get_list_checkout(self):
        cuit = 30112223335
        email = "pers_jur_pablo1@gmail.com"
        password = "124578"
        log_1 = login_in_whit_email_comercio(cuit,email,password)
        token = log_1["token"]

        self.logger.info("Runing test: test_get_list_checkout")
        list_ = checkout_list(token)
        body_list = list_.json()

        print(body_list)
        self.logger.info(f"response: {body_list}")

        status = body_list["status"]
        data = body_list["data"]
        if status != 200:
            self.fail(f"Fallo el endpoint: {body_list}")
        else:
            mjs = body_list["message"]
            self.assertEqual(status,200,f"status diferente: {status}")
            self.assertEqual(mjs,'Checkouts listed successfully.')
            assert isinstance(data, list)
            print(f"response success: {body_list}")
        



    def test_get_details_checkout(self):
        log = login_user()
        token = log["token"]

        self.logger.info("Runing test: test_get_details_checkout")
        
        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create_ = branch_create(token,name_branch)
        body_create_ = create_.json()
        branch_id = body_create_["data"]["branch_id"]

        name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        create = checkout_create(token,name_checkout,branch_id)
        body_create = create.json()
        print(body_create)
        checkout_id = body_create["data"]["checkout_id"]
        checkout_name = body_create["data"]["checkout_name"]
        checkout_qr = body_create["data"]["checkout_qr"]

        details = checkout_detail(token,checkout_id)
        body_detail = details.json()
        self.logger.info(f"response: {body_detail}")
        print(body_detail)
        code = body_detail["status"]
        data= body_detail["data"]
        if code != 200:
            self.fail(f"Fallo el endpoits: {body_detail}")
        else:
            self.assertEqual(code,200)
            self.assertEqual(data["checkout_id"],checkout_id)
            self.assertEqual(data["checkout_name"],checkout_name)
            self.assertEqual(data["checkout_qr"],checkout_qr)
            self.assertEqual(data["branch_id"],branch_id)

    
    def test_update_name_checkout(self):
        log = login_user()
        token = log["token"]

        self.logger.info(f"Running test: test_update_name_checkout")

        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create_ = branch_create(token,name_branch)
        body_create_ = create_.json()
        branch_id = body_create_["data"]["branch_id"]

        name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        create = checkout_create(token,name_checkout,branch_id)
        body_create = create.json()
        print(body_create)
        
        checkout_id = body_create["data"]["checkout_id"]
        name_old = Query_db.get_name_checkout_id(body_create["data"]["checkout_id"])
        #print(f"name old checkout: {name_old}")
        new_name_branch = "caja test" + str(faker.random_number(digits=3))
        update = checkout_update(token,new_name_branch,checkout_id,branch_id)
        body_update = update.json()
        
        print(body_update)
        name_update_db = Query_db.get_name_checkout_id(32)
        print(f"name new checkout: {name_update_db}")
        
        status = body_update["status"]
        self.logger.info(f"respose: {body_update}")
        if status == 400:
            self.fail(f"{body_update}")
        else:
            self.assertEqual(status,200)
            print(f"response success: {body_update}")
            if name_update_db == name_old:
                self.fail(f"No se cambio el nombre: name old:{name_old} - name new:{name_update_db}")
            else:
                print("Se cambio correctamente el nombre")



    def test_delete_checkout(self):
        log = login_user()
        token = log["token"]

        # self.logger.info(f"Running test: test_delete_branch")

        # name_branch = "test_branch_" + str(faker.random_number(digits=3))
        # create_ = branch_create(token,name_branch)
        # body_create_ = create_.json()
        # branch_id = body_create_["data"]["branch_id"]

        # name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        # create = checkout_create(token,name_checkout,branch_id)
        # body_create = create.json()
        # print(body_create)
        
        checkout_id = 421
        branch_id = 446

        delete = checkout_delete(token,checkout_id,branch_id)
        body_delete = delete.json()
        print(body_delete)
        status = body_delete["status"]
        if status == 400:
            self.fail(f"{body_delete}")
        else:
            self.assertEqual(body_delete["status"],200)
            print(f"response success: {body_delete}")


    

    def test_create_checkout_len_max_name(self):
        log = login_user()
        token = log["token"]
        
        
        
        self.logger.info("Runing test: test_create_checkout_len_max_name")
        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create_ = branch_create(token,name_branch)
        body_create = create_.json()
        branch_id = body_create["data"]["branch_id"]

        name_checkout = "test_checkout_test_len_max" + str(faker.random_number(digits=3))
        create = checkout_create(token,name_checkout,branch_id)
        body_create = create.json()
        print(body_create)
        self.logger.info(f"response: {body_create}")
        code = body_create["code"]
        self.assertEqual(code,400)

    def test_create_checkout_len_min_name(self):
        log = login_user()
        token = log["token"]

        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create_ = branch_create(token,name_branch)
        body_create = create_.json()
        branch_id = body_create["data"]["branch_id"]

        name_branch = ""
        
        self.logger.info("Runing test: test_create_branch_len_min_name")
        
        create = checkout_create(token,name_branch,branch_id)
        body_create = create.json()
        print(body_create)
        self.logger.info(f"response: {body_create}")
        code = body_create["status"]
        self.assertEqual(code,400,"Se crea branch con name vacio")


    def test_create_branch_with_name_exist(self):
        log = login_user()
        token = log["token"]

        self.logger.info("Runing test: test_create_branch_with_name_exist")

        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create__ = branch_create(token,name_branch)
        body_create__ = create__.json()
        branch_id = body_create__["data"]["branch_id"]

        name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        create = checkout_create(token,name_checkout,branch_id)
        body_create = create.json()
        

        
        create_ = checkout_create(token,name_checkout,branch_id)
        body_create_ = create_.json()
        print(body_create_)
        self.logger.info(f"response: {body_create}")
        if body_create_["data"]["checkout_name"] == name_checkout:
            self.fail("Se genero el user con un nombre de checkout existe")
        else:
            print("No se creo el user")


    
    def test_update_user_delete(self):
        log = login_user()
        token = log["token"]

        name_branch = "test_branch_test" + str(faker.random_number(digits=3))
        
        self.logger.info("Runing test: test_update_user_delete")
        
        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create_ = branch_create(token,name_branch)
        body_create_ = create_.json()
        branch_id = body_create_["data"]["branch_id"]

        name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        create = checkout_create(token,name_checkout,branch_id)
        body_create = create.json()
        print(body_create)
        checkout_id = body_create["data"]["checkout_id"]

        delete = checkout_delete(token,checkout_id,branch_id)
        body_delete = delete.json()
        print(body_delete)

        new_name_branch = "test_branch_test" + str(faker.random_number(digits=3))

        update = checkout_update(token,branch_id,new_name_branch,checkout_id)
        body_update = update.json()
        #print(body_update)
        code = body_update["code"]
        self.assertEqual(code,400,"Se update branch delete")

    def test_get_list_user_delete(self):
        log = login_user()
        token = log["token"]

        self.logger.info(f"Running test: test_update_name_branch")

        
        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create_ = branch_create(token,name_branch)
        body_create_ = create_.json()
        branch_id = body_create_["data"]["branch_id"]

        name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        create = checkout_create(token,name_checkout,branch_id)
        body_create = create.json()
        print(body_create)
        checkout_id = body_create["data"]["checkout_id"]

        delete = checkout_delete(token,checkout_id,branch_id)
        body_delete = delete.json()
        #print(body_delete)

        details = checkout_detail(token,checkout_id)
        body_detail = details.json()
        #print(body_detail)
        self.assertEqual(body_detail["status"],404)

    
    def test_monotribu_create_checkout(self):
        email = "pers_fis_pablo1@gmail.com"
        password = "124578"
        log = login_in_whit_email(email,password)
        token = log["token"]

        self.logger.info("Runing test: test_monotribu_create_checkout")
        name_branch = "test_branch_mono" + str(faker.random_number(digits=3))
        create = branch_create(token,name_branch)
        body_create = create.json()
        self.assertEqual(body_create["status"],201,f"Fallo status: {create.status_code}")
        data = body_create["data"]
        
        branch_id=data["branch_id"]

        name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        create = checkout_create(token,name_checkout,branch_id)
        body_create = create.json()
        print(body_create)
        self.logger.info(f"response: {body_create}")
        status = body_create["status"]
        if status != 201:
            self.fail(f"{body_create}")
        else:
            self.assertEqual(body_create["status"],201)
            print(f"response success: {body_create}")
            data = body_create["data"]
            assert "checkout_id" in data
            assert "checkout_name" in data
            assert "checkout_qr" in data
            assert "branch_id" in data
            checkout_id = data["checkout_id"]
            checkout_name = data["checkout_name"]
            checkout_qr = data["checkout_qr"]

            data_db = Query_db.get_checkout_info_with_name(checkout_id)
            self.assertEqual(data_db, checkout_name,"No coinciden checkout_name en db")
            if checkout_qr is None:
                print(f"Campo checkout QR vacio: {checkout_qr}")
            else:
                pass

        



    def test_monotribu_update_branch(self):
        email = "pers_fis_pablo1@gmail.com"
        password = "124578"
        log = login_in_whit_email(email,password)
        token = log["token"]

        self.logger.info(f"Running test: test_monotribu_update_branch")

        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create_ = branch_create(token,name_branch)
        body_create_ = create_.json()
        branch_id = body_create_["data"]["branch_id"]

        name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        create = checkout_create(token,name_checkout,branch_id)
        body_create = create.json()
        print(body_create)
        
        checkout_id = body_create["data"]["checkout_id"]
        name_old = Query_db.get_name_checkout_id(body_create["data"]["checkout_id"])
        #print(f"name old checkout: {name_old}")
        new_name_branch = "caja test" + str(faker.random_number(digits=3))
        update = checkout_update(token,new_name_branch,checkout_id,branch_id)
        body_update = update.json()
        
        print(body_update)
        name_update_db = Query_db.get_name_checkout_id(body_update["data"]["checkout_id"])
        print(f"name new checkout: {name_update_db}")
        
        status = body_update["status"]
        self.logger.info(f"respose: {body_update}")
        if status == 400:
            self.fail(f"{body_update}")
        else:
            self.assertEqual(status,200)
            print(f"response success: {body_update}")
            if name_update_db == name_old:
                self.fail(f"No se cambio el nombre: name old:{name_old} - name new:{name_update_db}")
            else:
                print("Se cambio correctamente el nombre")


    def test_get_monotribu_details(self):
        
        email = "pers_fis_pablo1@gmail.com"
        password = "124578"
        log = login_in_whit_email(email,password)
        token = log["token"]
        
        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create_ = branch_create(token,name_branch)
        body_create_ = create_.json()
        branch_id = body_create_["data"]["branch_id"]

        name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        create = checkout_create(token,name_checkout,branch_id)
        body_create = create.json()
        print(body_create)

        checkout_id = body_create["data"]["checkout_id"]
        checkout_name = body_create["data"]["checkout_name"]
        checkout_qr = body_create["data"]["checkout_qr"]

        details = checkout_detail(token,checkout_id)
        body_detail = details.json()
        self.logger.info(f"response: {body_detail}")
        print(body_detail)
        code = body_detail["status"]
        data= body_detail["data"]
        if code != 200:
            self.fail(f"Fallo el endpoits: {body_detail}")
        else:
            self.assertEqual(code,200)
            self.assertEqual(data["checkout_id"],checkout_id)
            self.assertEqual(data["checkout_name"],checkout_name)
            self.assertEqual(data["checkout_qr"],checkout_qr)
            self.assertEqual(data["branch_id"],branch_id)


    def test_can_get_details_to_other_user_monotribu(self):
        email = "pers_fis_pablo2@gmail.com"
        password = "124578"
        log_1 = login_in_whit_email(email,password)
        token = log_1["token"]

        self.logger.info("Runing test: test_can_get_details_to_other_user_monotribu")
        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create_ = branch_create(token,name_branch)
        body_create_ = create_.json()
        branch_id = body_create_["data"]["branch_id"]

        name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        create = checkout_create(token,name_checkout,branch_id)
        body_create = create.json()
        print(body_create)
        checkout_id = body_create["data"]["checkout_id"]



        email_ = "pers_fis_pablo1@gmail.com"
        password_ = "124578"
        log_2= login_in_whit_email(email_,password_)
        token_ = log_2["token"]

        
        details = checkout_detail(token_,checkout_id)
        body_detail = details.json()
        print(body_detail)
        status = body_detail["status"]
        if status == 200:
            self.fail("Fallo el test, deja ver los details de otro usuarios monotributistas")
        else:
            print("No fallo el test")
        
        
    def test_can_get_details_to_other_user_comercio(self):
        cuit = 30112223335
        email = "pers_jur_pablo1@gmail.com"
        password = "124578"
        log_1 = login_in_whit_email_comercio(cuit,email,password)
        token = log_1["token"]



        self.logger.info("Runing test: test_can_get_details_to_other_user_comercio")
        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create_ = branch_create(token,name_branch)
        body_create_ = create_.json()
        branch_id = body_create_["data"]["branch_id"]

        name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        create = checkout_create(token,name_checkout,branch_id)
        body_create = create.json()
        print(body_create)
        checkout_id = body_create["data"]["checkout_id"]
        

        cuit_ = 30222333115
        email_ = "pers_jur_pablo2@gmail.com"
        password_ = "124578"
        log_2= login_in_whit_email_comercio(cuit_,email_,password_)
        token_ = log_2["token"]

        
        details = checkout_detail(token_,checkout_id)
        body_detail = details.json()
        print(body_detail)
        status = body_detail["status"]
        if status == 200:
            self.fail("Fallo el test, deja ver los details de otro usuarios")
        else:
            print("No fallo el test")
            status_ = body_detail["status"]["status_code"]
            self.assertEqual(status_, 400)
            mjs = 'Branch does not belong to the commerce'
            self.assertEqual(body_detail["message"],mjs,"No corresponde el mensaje")


    def test_can_update_to_other_user_monotribu(self):
        email = "pers_fis_pablo2@gmail.com"
        password = "124578"
        log_1 = login_in_whit_email(email,password)
        token = log_1["token"]

        self.logger.info("Runing test: test_can_update_to_other_user_monotribu")
        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create_ = branch_create(token,name_branch)
        body_create_ = create_.json()
        branch_id = body_create_["data"]["branch_id"]

        name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        create = checkout_create(token,name_checkout,branch_id)
        body_create = create.json()
        print(body_create)
        checkout_id = body_create["data"]["checkout_id"]
        name_db = Query_db.get_name_checkout_id(checkout_id)

        email_ = "pers_fis_pablo1@gmail.com"
        password_ = "124578"
        log_2= login_in_whit_email(email_,password_)
        token_ = log_2["token"]

        new_name_branch = "caja update mono" 
        update = checkout_update(token_,new_name_branch,checkout_id,branch_id)
        
        name_update_db = Query_db.get_name_checkout_id(checkout_id)
        body_update = update.json()
        print(body_update)
        self.logger.info(f"respose: {body_update}")
        status = body_update["status"]
        if status == 200:
            self.assertIsNot(name_db,name_update_db)
            self.fail("Fallo el test, deja ver los details de otro usuarios monotributistas")
            
        else:
            print("No fallo el test")


    def test_can_update_to_other_user_comercio(self):
        cuit = 30112223335
        email = "pers_jur_pablo1@gmail.com"
        password = "124578"
        log_1 = login_in_whit_email_comercio(cuit,email,password)
        token = log_1["token"]

        self.logger.info("Runing test: test_can_update_to_other_user_comercio")
        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create_ = branch_create(token,name_branch)
        body_create_ = create_.json()
        branch_id = body_create_["data"]["branch_id"]

        name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        create = checkout_create(token,name_checkout,branch_id)
        body_create = create.json()
        print(body_create)
        checkout_id = body_create["data"]["checkout_id"]
        name_db = Query_db.get_name_checkout_id(checkout_id)

        cuit_ = 30222333115
        email_ = "pers_jur_pablo2@gmail.com"
        password_ = "124578"
        log_2= login_in_whit_email_comercio(cuit_,email_,password_)
        token_ = log_2["token"]

        
        new_name_branch = "test_branch_upmono"
        name_db = Query_db.get_checkout_info_with_name(checkout_id)
        new_name_branch = "caja update mono" 
        update = checkout_update(token_,new_name_branch,checkout_id,branch_id)
        body_update = update.json()
        print(body_update)
        name_update_db = Query_db.get_checkout_info_with_name(checkout_id)
        self.logger.info(f"respose: {body_update}")
        status = body_update["status"]
        if status == 200:
            self.assertIsNot(name_db,name_update_db)
            self.fail("Fallo el test, deja ver los details de otro usuarios monotributistas")
            
        else:
            status_ = body_update["status"]["status_code"]
            self.assertEqual(status_,404)
            mjs = 'Branch does not belong to the commerce'
            self.assertEqual(body_update["message"],mjs)



    def test_can_delete_checout_to_other_monotribu(self):
        email = "pers_fis_pablo2@gmail.com"
        password = "124578"
        log_1 = login_in_whit_email(email,password)
        token = log_1["token"]

        self.logger.info("Runing test: test_can_update_to_other_user_monotribu")
        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create_ = branch_create(token,name_branch)
        body_create_ = create_.json()
        branch_id = body_create_["data"]["branch_id"]

        name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        create = checkout_create(token,name_checkout,branch_id)
        body_create = create.json()
        print(body_create)
        checkout_id = body_create["data"]["checkout_id"]

        email_ = "pers_fis_pablo1@gmail.com"
        password_ = "124578"
        log_2= login_in_whit_email(email_,password_)
        token_ = log_2["token"]

        delete = checkout_delete(token_,checkout_id,branch_id)
        body_delete = delete.json()
        self.logger.info(f"response: {body_delete}")
        print(body_delete)
        status = body_delete["status"]
        if status == 200:
            self.fail(f"{body_delete}")
        else:
            self.assertEqual(body_delete["code"],400)
            print(f"response success: {body_delete}")
            

    def test_can_delete_checkout_to_other_comercio(self):
        cuit = 30112223335
        email = "pers_jur_pablo1@gmail.com"
        password = "124578"
        log_1 = login_in_whit_email_comercio(cuit,email,password)
        token = log_1["token"]

        self.logger.info("Runing test: test_can_delete_checout_to_other_comercio")
        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create_ = branch_create(token,name_branch)
        body_create_ = create_.json()
        branch_id = body_create_["data"]["branch_id"]

        name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        create = checkout_create(token,name_checkout,branch_id)
        body_create = create.json()
        print(body_create)
        checkout_id = body_create["data"]["checkout_id"]

        cuit_ = 30222333115
        email_ = "pers_jur_pablo2@gmail.com"
        password_ = "124578"
        log_2= login_in_whit_email_comercio(cuit_,email_,password_)
        token_ = log_2["token"]

        delete = checkout_delete(token_,checkout_id,branch_id)
        body_delete = delete.json()
        self.logger.info(f"response: {body_delete}")
        print(body_delete)
        status = body_delete["status"]["status_code"]
        if status == 200:
            self.fail(f"{body_delete}")
        else:
            self.assertEqual(body_delete["code"],400)
            print(f"response success: {body_delete}")


