import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from configuracion.conf_logs import setup_logger_commers
from faker import Faker
from unittest import TestCase
from configuracion.views_comercio import representative_create,representative_delete,representative_detail,representative_list,representative_update,login,login_in_whit_email_comercio,login_in_whit_email
from configuracion.config import Query_db
faker = Faker()



def login_user():

    cuit = '************'
    email_ = '************'
    password_ ='************'

    dic = {}

    request_login = login_in_whit_email_comercio(cuit,email_, password_)
    
    #data = request_login["data"]
    token =request_login["token"]
    #commerce = response["commerce"]

    dic = {"token":f"{token}"}

    return dic




class Repre(TestCase):
    def setUp(self):
         #config el logger
         self.logger = setup_logger_commers()

    # def test_create_representative_comercio(self):
    #     cuit = 30222333885
    #     email = "pers_jur_pablo3@gmail.com"
    #     password = "124578"
    #     log_1 = login_in_whit_email_comercio(cuit,email,password)
    #     token = log_1["token"]

    #     self.logger.info("Runing test: test_create_representative_comercio")
    #     rol = 2
    #     repre_type = "attorney"
    #     create = representative_create(token,rol,repre_type)
    #     body_create = create.json()
    #     self.logger.info(f"response: {body_create}")
    #     print(body_create)
        
        # data = body_create["data"]
        # assert "representative_id" in data
        # assert "commerce_id" in data
        # assert "representative_name" in data
        # assert "representative_address_id" in data
        # commerce_id = data["commerce_id"]
        # representative_name = data["representative_name"]

        # data_db = Query_db.get_representative_info_with_name(representative_name)
        # for i in data_db:
        #     commerce_id_db = data_db[0]
        #     representative_name_db = data_db[1]
        #     self.assertEqual(commerce_id_db,commerce_id,"No coinciden commerce_id en db")
        #     self.assertEqual(representative_name_db, representative_name,"No coinciden representative_name en db")

    # def test_create_representative_monotributista(self):
    #     email = "pers_fis_pablo3@gmail.com"
    #     password = "124578"
    #     log = login_in_whit_email(email,password)
    #     token = log["token"]

    #     self.logger.info("Runing test: test_create_representative_monotributista")
    #     rol = 2
    #     repre_type = "attorney"
    #     create = representative_create(token,rol,repre_type)
    #     body_create = create.json()
    #     self.logger.info(f"response: {body_create}")
    #     status = body_create["status"]
    #     self.assertEqual(status,201)
    #     data = body_create["data"]
        


    def test_get_list_representative(self):
        # cuit = 30222333115
        # email = "pers_jur_pablo2@gmail.com"
        # password = "124578"
        # log_1 = login_in_whit_email_comercio(cuit,email,password)
        # token = log_1["token"]
        email = "pers_fis_pablo1@gmail.com"
        password = "124578"
        log_1 = login_in_whit_email(email,password)
        token = log_1["token"]

        
        self.logger.info(f"Running test: test_get_list_representative")
        list_ = representative_list(token)
        body_list = list_.json()
        self.logger.info(f"response: {body_list}")
        print(body_list)
        status = body_list["status"]
        # data = body_list["data"]
        message = 'Representatives list.'
        mjs = body_list["message"]
        self.assertEqual(mjs,message,f"Fallo en lista: {mjs}")
        self.assertEqual(status,200,f"status diferente: {status}")
        



    def test_get_details_representative(self):
        cuit = 30222333115
        email = "pers_jur_pablo2@gmail.com"
        password = "124578"
        log_1 = login_in_whit_email_comercio(cuit,email,password)
        token = log_1["token"]
        #email = "pers_fis_pablo1@gmail.com"
        # password = "124578"
        # log_1 = login_in_whit_email(email,password)
        # token = log_1["token"]

        self.logger.info(f"Running test: test_get_details_representative")
       

        details = representative_detail(token,10)
        body_detail = details.json()
        print(body_detail)
        self.logger.info(f"response: {body_detail}")
        status = body_detail["status"]
        # data = body_detail["data"]
        self.assertEqual(status,200,f"status diferente: {status}")
        # self.assertEqual(data["commerce_id"],commerce_id)
        # self.assertEqual(data["representative_name"],representative_name)

       
    def test_update_name_representative(self):
        email = "pers_fis_pablo1@gmail.com"
        password = "124578"
        log_1 = login_in_whit_email(email,password)
        token = log_1["token"]

        self.logger.info(f"Running test: test_update_name_representative")

        #repre_id = Query_db.get_last_repre_id()
        # name_representative = "test_representative_" + str(faker.random_number(digits=2))
        # create = representative_create(token,name_representative)
        # body_create = create.json()
        # representative_id = body_create["data"]["representative_id"]


        # new_name_representative = "test_representative_update_" + str(faker.random_number(digits=2))
        new_role = 4
        repre_type = "legal_representative"
        update = representative_update(token,15,new_role,repre_type)
        
        body_update = update.json()
        print(body_update)
        # status = body_update["code"]
        self.logger.info(f"respose: {body_update}")
        # if status == 400:
        #     self.fail(f"{body_update}")
        # else:
        #     self.assertEqual(body_update["code"],200)
        #     print(f"response success: {body_update}")
        


    def test_delete_representative(self):
        email = "pers_fis_pablo1@gmail.com"
        password = "124578"
        log_1 = login_in_whit_email(email,password)
        token = log_1["token"]

        self.logger.info(f"Running test: test_delete_representative")

        # name_representative = "test_representative_" + str(faker.random_number(digits=2))
        # create = representative_create(token,name_representative)
        # body_create = create.json()
        # representative_id = body_create["data"]["representative_id"]

        delete = representative_delete(token,15)
        body_delete = delete.json()
        print(body_delete)
        self.logger.info(f"response: {body_delete}")

        status = body_delete["status"]["status_code"]
        #self.assertEqual(status,204)
        if status == 404:
            self.fail(f"No se genero el borrado{body_delete}")
        else:
            self.assertEqual(body_delete["code"],200)
            print(f"response success: {body_delete}")
    

    def test_create_representative_monotribu_acount_exist(self):
        email = "pers_fis_pablo1@gmail.com"
        password = "124578"
        log = login_in_whit_email(email,password)
        token = log["token"]

        self.logger.info("Runing test: test_create_representative_monotribu_acount_exist")
        rol = 2
        repre_type = "attorney"
        create = representative_create(token,rol,repre_type)
        body_create = create.json()
        self.logger.info(f"response: {body_create}")
        print(body_create)
        status = body_create["code"]
        self.assertEqual(status,400)
        # data = body_create["data"]



    def test_delete_representative_to_other_acount(self):
        cuit = 30222333115
        email = "pers_jur_pablo2@gmail.com"
        password = "124578"
        log_1 = login_in_whit_email_comercio(cuit,email,password)
        token = log_1["token"]

        self.logger.info(f"Running test: test_delete_representative")

        details = representative_detail(token,10)
        body_detail = details.json()
        representative_id = body_detail["data"]["representative_id"]


        email_ = "pers_fis_pablo1@gmail.com"
        password_ = "124578"
        log = login_in_whit_email(email_,password_)
        token_ = log["token"]
        
        delete = representative_delete(token_,10)
        body_delete = delete.json()
        print(body_delete)
        self.logger.info(f"response: {body_delete}")

        status = body_delete["status"]
        self.assertEqual(status,204)


    def test_update_representative_to_other_acount(self):
        cuit = 30222333115
        email = "pers_jur_pablo2@gmail.com"
        password = "124578"
        log_1 = login_in_whit_email_comercio(cuit,email,password)
        token = log_1["token"]

        self.logger.info(f"Running test: test_delete_representative")

        details = representative_detail(token,10)
        body_detail = details.json()
        representative_id = body_detail["data"]["representative_id"]


        email_ = "pers_fis_pablo1@gmail.com"
        password_ = "124578"
        log = login_in_whit_email(email_,password_)
        token_ = log["token"]
        
        new_role = 4
        repre_type = "legal_representative"
        update = representative_update(token_,10,new_role,repre_type)
        
        body_update = update.json()
        print(body_update)
        status = body_update["code"]
        self.logger.info(f"respose: {body_update}")
        mjs = "You don't have permissions to edit this representative, doesn't belong to your commerce"
        self.assertEqual(status,400)
        self.assertEqual(body_update["message"],mjs)