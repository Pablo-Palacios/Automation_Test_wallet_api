import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from configuracion.conf_logs import setup_logger_commers
from faker import Faker
from unittest import TestCase
from configuracion.views_comercio import branch_create,checkout_create,representative_create,login_comercio,login_in_whit_email,login_in_whit_email_comercio,create_commerce_pf
from configuracion.views_persona import login,login_otp
from configuracion.config import Query_db
from configuracion.code_redi import Redis
faker = Faker()


class User(TestCase):
    def setUp(self):
         #config el logger
         self.logger = setup_logger_commers()

    def test_create_commerce_persona_fisica(self):
        email = "davidwallacedev@movilcash.com"
        password = "Pablo123"
        device = "1234"
        log_1 = login(email,password,device)
        #print(log_1.json())
        status = log_1.status_code
        if status == 401:
            user_id = Query_db.get_user_id_email(email)
            code = Redis.validacion_otp_login(user_id,device)
            log_ = login_otp(email,password,device,code)
            print(log_.json())
        token = log_1["token"]

        new_name_comer = str(faker.last_name().lower()) + " com pf"
        create_commerce = create_commerce_pf(token,new_name_comer)
        body_cre = create_commerce.json() 
        assert 'commerce_id' in body_cre






    def test_create_all_step_monotributista(self):
        self.logger.info("Runing test: test_create_all_step_monotributista")
        email = "morrowqa@movilcash.com"
        password = "Pablo123"
        device = Query_db.get_deviceId_to_email(email)
        log_1 = login_in_whit_email(email,password,device)
        token = log_1["token"]

        
        name_branch = "branch " + str(faker.random_number(digits=3))
        create = branch_create(token,name_branch)
        body_create = create.json()
        
        print(body_create)
        self.logger.info(f"response_create_branch: {body_create}")
        self.assertEqual(body_create["status"],201)
        
        branch_id = body_create["data"]["branch_id"]

        name_checkout = "test_caja_" + str(faker.random_number(digits=3))
        create_ = checkout_create(token,name_checkout,branch_id)
        body_create_ = create_.json()
        print(body_create_)
        self.logger.info(f"response create_checkout: {body_create_}")
        self.assertEqual(body_create_["status"],201)

        rol = 2
        repre_type = "attorney"

        create__ = representative_create(token,rol,repre_type)
        body_create__= create__.json()
        self.logger.info(f"response create representative: {body_create__}")
        self.assertEqual(body_create__["status"],201)
