import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from configuracion.conf_logs import setup_logger_commers
from faker import Faker
from unittest import TestCase
from configuracion.views_comercio import branch_create,branch_delete,branch_detail,branch_list,branch_update,login_comercio,login_in_whit_email,login_in_whit_email_comercio
from configuracion.config import Query_db
from configuracion.main import password
faker = Faker()



# def login_user():

#     cuit = 30715699415
#     email_ = 'comercio_pj@gmail.com'
#     password_ = "326598"

#     dic = {}

#     request_login = login_comercio(cuit,email_, password_)
#     response = request_login.json()
#     data = response["data"]
#     token = data["token"]
#     #commerce = response["commerce"]

#     dic = {"token":f"{token}"}

#     return dic




class Branch(TestCase):
    def setUp(self):
         #config el logger
         self.logger = setup_logger_commers()

    def test_create_branch_pf(self):
        email = 'wellsqa@movilcash.com'
        device = Query_db.get_deviceId_to_email(email)
        log = login_in_whit_email(email,password,device)
        token = log["token"]

        self.logger.info("Runing test: test_create_branch")
        name_branch = "branch " + str(faker.random_number(digits=3))
        create = branch_create(token,name_branch)
        body_create = create.json()
        print(body_create)
        self.logger.info(f"response: {body_create}")
        self.assertEqual(body_create["status"],201,f"Fallo status: {create.status_code}")
        data = body_create["data"]
        assert "branch_id" in data
        assert "commerce_id" in data
        assert "branch_name" in data
        assert "branch_address_id" in data
        commerce_id = data["commerce_id"]
        branch_name = data["branch_name"]
        branch_id = data["branch_id"]

        data_db = Query_db.get_branch_info_with_name(branch_id)
        
        self.assertEqual(data_db, branch_name,"No coinciden branch_name en db")


    def test_get_list_branch_pf(self):
        email = '************'
        device = Query_db.get_deviceId_to_email(email)
        log = login_in_whit_email(email,password,device)
        token = log["token"]

        
        self.logger.info(f"Running test: test_get_list_branch")
        list_ = branch_list(token)
        body_list = list_.json()
        print(body_list)
        self.logger.info(f"response: {body_list}")
        status = body_list["status"]
        data = body_list["data"]
        message = 'Branches retrieved successfully.'
        mjs = body_list["message"]
        self.assertEqual(mjs,message,f"Fallo en lista: {mjs}")
        self.assertEqual(status,200,f"status diferente: {status}")
        assert isinstance(data,list),"El objeto 'data' no es una lista"

        
    def test_get_details_branch_pf(self):
        email = '************'
        device = Query_db.get_deviceId_to_email(email)
        log = login_in_whit_email(email,password,device)
        token = log["token"]

        self.logger.info(f"Running test: test_get_details_branch")
        

        name_branch = "branch " + str(faker.random_number(digits=3))
        create = branch_create(token,name_branch)
        body_create = create.json()
        branch_id = body_create["data"]["branch_id"]
        branch_name = body_create["data"]["branch_name"]
        comerce_id = body_create["data"]["commerce_id"]
        details = branch_detail(token,branch_id)
        body_detail = details.json()
        print(body_detail)
        self.logger.info(f"response: {body_detail}")
        status = body_detail["status"]
        data = body_detail["data"]
        self.assertEqual(status,200,f"status diferente: {status}")
        self.assertEqual(data["commerce_id"],comerce_id)
        self.assertEqual(data["branch_name"],branch_name)

       
    def test_update_name_branch_pf(self):
        email = '************'
        device = Query_db.get_deviceId_to_email(email)
        log = login_in_whit_email(email,password,device)
        token = log["token"]

        self.logger.info(f"Running test: test_update_name_branch")

        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create = branch_create(token,name_branch)
        body_create = create.json()
        branch_id = body_create["data"]["branch_id"]


        new_name_branch = "branch_update_" + str(faker.random_number(digits=3))
        update = branch_update(token,branch_id,new_name_branch)
        body_update = update.json()
        print(body_update)
        status = body_update["status"]
        self.logger.info(f"respose: {body_update}")
        if status == 400:
            self.fail(f"{body_update}")
        else:
            self.assertEqual(body_update["status"],200)
            print(f"response success: {body_update}")
            name_db = Query_db.get_branch_info_with_name(branch_id)
            self.assertEqual(name_db,body_update["data"]["branch_name"])

        
    def test_delete_branch_pf(self):
        email = '************'
        device = Query_db.get_deviceId_to_email(email)
        log = login_in_whit_email(email,password,device)
        token = log["token"]

        self.logger.info(f"Running test: test_delete_branch")

        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create = branch_create(token,name_branch)
        body_create = create.json()
        
        branch_id = body_create["data"]["branch_id"]

        delete = branch_delete(token,branch_id)
        body_delete = delete.json()
        self.logger.info(f"response: {body_delete}")
        print(body_delete)
        
        status = body_delete["status"]
        if status == 400:
            self.fail(f"{body_delete}")
        else:
            self.assertEqual(status,204)
            print(f"response success: {body_delete}")
    

    def test_create_branch_len_max_name(self):
        email = '************'
        device = Query_db.get_deviceId_to_email(email)
        log = login_in_whit_email(email,password,device)
        token = log["token"]
        
        name_branch = "test_branch_test_len_max" + str(faker.random_number(digits=3))
        
        self.logger.info("Runing test: test_create_branch_len_max_name")
        
        create = branch_create(token,name_branch)
        body_create = create.json()
        print(body_create)
        self.logger.info(f"response: {body_create}")
        code = body_create["code"]
        self.assertEqual(code,400)
        mjs = "value too long for type character varying(20)\n"
        self.assertEqual(body_create["message"],mjs)

    def test_create_branch_len_min_name(self):
        email = '************'
        device = Query_db.get_deviceId_to_email(email)
        log = login_in_whit_email(email,password,device)
        token = log["token"]
        
        name_branch = ""
        
        self.logger.info("Runing test: test_create_branch_len_min_name")
        
        create = branch_create(token,name_branch)
        body_create = create.json()
        print(body_create)
        self.logger.info(f"response: {body_create}")
        if body_create["status"] == 201:
            self.fail("deja crear branch con name vacio")
        else:    
            code = body_create["status"]["status_code"]
            self.assertEqual(code,400,"Se crea branch con name vacio")


    def test_create_branch_with_name_exist(self):
        email = '************'
        device = Query_db.get_deviceId_to_email(email)
        log = login_in_whit_email(email,password,device)
        token = log["token"]

        last_branch = Query_db.get_last_branch_id()
        #branch_id=last_branch[0]
        #commerce_id = last_branch[1]
        branch_name = last_branch[2]

        self.logger.info("Runing test: test_create_branch_with_name_exist")
        
        create = branch_create(token,branch_name)
        body_create = create.json()
        print(body_create)
        self.logger.info(f"response: {body_create}")
        if body_create["data"]["branch_name"] == branch_name and body_create["status"] == 201:
            self.fail("Se genero el user con un nombre de branch existe")
        else:
            print("No se creo el user")


    def test_update_user_delete(self):
        email = '************'
        device = Query_db.get_deviceId_to_email(email)
        log = login_in_whit_email(email,password,device)
        token = log["token"]

        name_branch = "test_branch_test" + str(faker.random_number(digits=3))
        
        self.logger.info("Runing test: test_update_user_delete")
        
        create = branch_create(token,name_branch)
        body_create = create.json()
        #print(body_create)
        self.logger.info(f"response: {body_create}")
        branch_id = body_create["data"]["branch_id"]

        delete = branch_delete(token,branch_id)
        body_delete = delete.json()
        #print(body_delete)

        new_name_branch = "test_branch_test" + str(faker.random_number(digits=3))

        update = branch_update(token,branch_id,new_name_branch)
        body_update = update.json()
        self.logger.info(f"response: {body_update}")
        #print(body_update)
        code = body_update["code"]
        self.assertEqual(code,400,"Se update branch delete")

    def test_get_list_user_delete(self):
        email = '************'
        device = Query_db.get_deviceId_to_email(email)
        log = login_in_whit_email(email,password,device)
        token = log["token"]

        self.logger.info(f"Running test: test_update_name_branch")

        name_branch = "test_branch_" + str(faker.random_number(digits=3))
        create = branch_create(token,name_branch)
        

        last_branch = Query_db.get_last_branch_id()
        branch_id=last_branch[0]

        delete = branch_delete(token,branch_id)
        body_delete = delete.json()
        #print(body_delete)


        details = branch_detail(token,branch_id)
        body_detail = details.json()
        self.logger.info(f"response: {body_detail}")
        #print(body_detail)
        self.assertEqual(body_detail["status"]["status_code"],404)

    
    def test_monotribu_create_branch(self):
        email = '************'
        password = '************'
        log = login_in_whit_email(email,password)
        token = log["token"]

        self.logger.info("Runing test: test_monotribu_create_branch")
        name_branch = "test_branch_mono" + str(faker.random_number(digits=3))
        create = branch_create(token,name_branch)
        body_create = create.json()
        print(body_create)
        self.logger.info(f"response: {body_create}")
        self.assertEqual(body_create["status"],201,f"Fallo status: {create.status_code}")
        data = body_create["data"]
        assert "branch_id" in data
        assert "commerce_id" in data
        assert "branch_name" in data
        assert "branch_address_id" in data
        branch_name = data["branch_name"]
        branch_id = data["branch_id"]

        data_db = Query_db.get_branch_info_with_name(branch_id)
        
        self.assertEqual(data_db, branch_name,"No coinciden branch_name en db")


    def test_monotribu_update_branch(self):
        email = '************'
        password = '************'
        log = login_in_whit_email(email,password)
        token = log["token"]

        self.logger.info("Runing test: test_monotribu_update_branch")
        name_branch = "test_branch_mono_" + str(faker.random_number(digits=3))
        create = branch_create(token,name_branch)
        body_create = create.json()
        print(body_create)
        branch_id = body_create["data"]["branch_id"]
    

        new_name_branch = "test_branch_upmono"
        name_db_old = Query_db.get_branch_info_with_name(branch_id)
        update = branch_update(token,branch_id,new_name_branch)
        body_update = update.json()
        print(body_update)
        self.logger.info(f"respose: {body_update}")
        self.assertEqual(body_update["status"],200)
        print(f"response: {body_update}")
        name_db = Query_db.get_branch_info_with_name(branch_id)
        self.assertIsNot(name_db,name_db_old, "No se cambio en la base de datos el nombre")


    def test_get_monotribu_details(self):
        self.logger.info("Runing test: test_get_monotribu_details")
        email = '************'
        password = '************'
        log = login_in_whit_email(email,password)
        token = log["token"]

        name_branch = "branch " + str(faker.random_number(digits=3))
        create = branch_create(token,name_branch)
        body_create = create.json()
        branch_id = body_create["data"]["branch_id"]
        branch_name = body_create["data"]["branch_name"]
        comerce_id = body_create["data"]["commerce_id"]

        details = branch_detail(token,branch_id)
        body_detail = details.json()
        print(body_detail)
        self.logger.info(f"response: {body_detail}")
        status = body_detail["status"]
        data = body_detail["data"]
        self.assertEqual(status,200,f"status diferente: {status}")
        self.assertEqual(data["commerce_id"],comerce_id)
        self.assertEqual(data["branch_name"],branch_name)


    def test_can_get_details_to_other_user_monotribu(self):
        email = '************'
        password = '************'
        log_1 = login_in_whit_email(email,password)
        token = log_1["token"]

        self.logger.info("Runing test: test_can_get_details_to_other_user_monotribu")
        name_branch = "test_branch_mono" + str(faker.random_number(digits=3))
        create = branch_create(token,name_branch)
        body_create = create.json()
        #print(body_create)
        branch_id = body_create["data"]["branch_id"]
        self.assertEqual(body_create["status"],201,f"Fallo status: {create.status_code}")

        email_ ='************'
        password_ = '************'
        log_2= login_in_whit_email(email_,password_)
        token_ = log_2["token"]

        
        details = branch_detail(token_,branch_id)
        body_detail = details.json()
        print(body_detail)
        self.logger.info(f"response: {body_detail}")
        status = body_detail["status"]
        if status == 200:
            self.fail("Fallo el test, deja ver los details de otro usuarios monotributistas")
        else:
            print("No fallo el test")
        
        
    def test_can_get_details_to_other_user_comercio(self):
        cuit = '************'
        email = '************'
        password = '************'
        log_1 = login_in_whit_email_comercio(cuit,email,password)
        token = log_1["token"]

        self.logger.info("Runing test: test_can_get_details_to_other_user_monotribu")
        name_branch = "test_branch_mono" + str(faker.random_number(digits=3))
        create = branch_create(token,name_branch)
        body_create = create.json()
        #print(body_create)
        branch_id = body_create["data"]["branch_id"]
        self.assertEqual(body_create["status"],201,f"Fallo status: {create.status_code}")
        

        cuit_ = '************'
        email_ = '************'
        password_ = '************'
        log_2= login_in_whit_email_comercio(cuit_,email_,password_)
        token_ = log_2["token"]

        
        details = branch_detail(token_,branch_id)
        body_detail = details.json()
        print(body_detail)
        self.logger.info(f"response: {body_detail}")
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
        email = '************'
        password = '************'
        log_1 = login_in_whit_email(email,password)
        token = log_1["token"]

        self.logger.info("Runing test: test_can_update_to_other_user_monotribu")
        name_branch = "test_branch_mono" + str(faker.random_number(digits=3))
        create = branch_create(token,name_branch)
        body_create = create.json()
        print(body_create)
        branch_id = body_create["data"]["branch_id"]
        name_db_old = Query_db.get_branch_info_with_name(branch_id)
        self.assertEqual(body_create["status"],201,f"Fallo status: {create.status_code}")

        email_ ='************'
        password_ = '************'
        log_2= login_in_whit_email(email_,password_)
        token_ = log_2["token"]

        
        new_name_branch = "test_branch_upmono"
        name_db = Query_db.get_branch_info_with_name(branch_id)
        update = branch_update(token_,branch_id,new_name_branch)
        body_update = update.json()
        print(body_update)
        self.logger.info(f"respose: {body_update}")
        status = body_update["status"]
        if status == 200:
            self.assertIsNot(name_db,name_db_old)
            self.fail("Fallo el test, deja ver los details de otro usuarios monotributistas")
            
        else:
            print("No fallo el test")


    def test_can_update_to_other_user_comercio(self):
        cuit = '************'
        email = "pers_jur_pablo1@gmail.com"
        password = "124578"
        log_1 = login_in_whit_email_comercio(cuit,email,password)
        token = log_1["token"]

        self.logger.info("Runing test: test_can_update_to_other_user_comercio")
        name_branch = "test_branch_mono" + str(faker.random_number(digits=3))
        create = branch_create(token,name_branch)
        body_create = create.json()
        print(body_create)
        branch_id = body_create["data"]["branch_id"]
        name_db_old = Query_db.get_branch_info_with_name(branch_id)
        self.assertEqual(body_create["status"],201,f"Fallo status: {create.status_code}")

        cuit_ = 30222333115
        email_ = "pers_jur_pablo2@gmail.com"
        password_ = "124578"
        log_2= login_in_whit_email_comercio(cuit_,email_,password_)
        token_ = log_2["token"]

        
        new_name_branch = "test_branch_upmono"
        name_db = Query_db.get_branch_info_with_name(branch_id)
        update = branch_update(token_,branch_id,new_name_branch)
        body_update = update.json()
        print(body_update)
        self.logger.info(f"respose: {body_update}")
        status = body_update["status"]
        if status == 200:
            self.assertIsNot(name_db,name_db_old)
            self.fail("Fallo el test, deja ver los details de otro usuarios monotributistas")
            
        else:
            status_ = body_update["status"]["status_code"]
            self.assertEqual(status_,404)
            mjs = 'Branch does not belong to the commerce'
            self.assertEqual(body_update["message"],mjs)
            

    def test_can_delete_to_other_monotribu(self):
        email = "pers_fis_pablo2@gmail.com"
        password = "124578"
        log_1 = login_in_whit_email(email,password)
        token = log_1["token"]

        self.logger.info("Runing test: test_can_update_to_other_user_monotribu")
        name_branch = "test_branch_mono" + str(faker.random_number(digits=3))
        create = branch_create(token,name_branch)
        body_create = create.json()
        print(f"user: {email}: {body_create}") 
        branch_id = body_create["data"]["branch_id"]
        self.assertEqual(body_create["status"],201,f"Fallo status: {create.status_code}")

        email_ = "pers_fis_pablo1@gmail.com"
        password_ = "124578"
        log_2= login_in_whit_email(email_,password_)
        token_ = log_2["token"]

        delete = branch_delete(token_,branch_id)
        body_delete = delete.json()
        print(body_delete)
        self.logger.info(f"response: {body_delete}")
        status = body_delete["status"]
        if status == 204:
            self.fail(f"Se borro el branch de otro monotributista {body_delete}")
        else:
            self.assertEqual(status,400)
            print(f"response success: {body_delete}")


    def test_can_delete_to_other_comercio(self):
        cuit = 30112223335
        email = "pers_jur_pablo1@gmail.com"
        password = "124578"
        log_1 = login_in_whit_email_comercio(cuit,email,password)
        token = log_1["token"]

        self.logger.info("Runing test: test_can_update_to_other_user_comercio")
        name_branch = "test_branch_mono" + str(faker.random_number(digits=3))
        create = branch_create(token,name_branch)
        body_create = create.json()
        print(body_create)
        branch_id = body_create["data"]["branch_id"]
        self.assertEqual(body_create["status"],201,f"Fallo status: {create.status_code}")

        cuit_ = '************'
        email_ = "pers_jur_pablo2@gmail.com"
        password_ = "124578"
        log_2= login_in_whit_email_comercio(cuit_,email_,password_)
        token_ = log_2["token"]

        delete = branch_delete(token_,branch_id)
        body_delete = delete.json()
        print(body_delete)
        self.logger.info(f"response: {body_delete}")
        status = body_delete["status"]
        if status == 204:
            self.fail(f"Se borro el branch de otro comercio {body_delete}")
        else:
            status = body_delete["status"]["status_code"]
            self.assertEqual(status,400)
            print(f"response success: {body_delete}")




        

        
        



        



       

















