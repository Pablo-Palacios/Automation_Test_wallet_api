import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from configuracion.views_persona import get_cbu_banking,create_cbu_banking,login_in_whit_email,desactivate_cbu_banking,activate_cbu_banking
from unittest import TestCase
from configuracion.main import password
from configuracion.config import Query_db


class UserOndaCbu(TestCase):
    def test_create_cbu(self):
   

        cbu_2 ="*******"
        email_2 = "*******"
        user_2 = login_in_whit_email(email_2,password)
        token_2 = user_2["token"]

        
        create = create_cbu_banking(token_2,cbu_2)
        body_create = create.json()
        print(body_create)
        status = body_create["status"]
        self.assertEqual(status,201,"No se creo el cbu del user")
        cbu_db = Query_db.get_cbu_bfsa_with_email(email_2)
        self.assertEqual(cbu_db,cbu_2,"No coinciden cbu en basedatos")            



    def test_get_cbu_user(self):
        email = "*******"
        user = login_in_whit_email(email,password)
        token = user["token"]

        get_cbu = get_cbu_banking(token)
        body = get_cbu.json()
        print(body)
        status = body["status"]
        self.assertEqual(status,200,"No trajo los datos del usuario")
        data = body["data"]
        for i in data:
            assert "cbuId" in i
            assert "userId" in i
            assert "cbu" in i
            assert "isActive" in i



    def test_desactivate(self):
        email = "*******"
        user = login_in_whit_email(email,password)
        token = user["token"]

        get_cbu = get_cbu_banking(token)
        body = get_cbu.json()
        
        data = body["data"]
        for i in data:
            cbuId = i["cbuId"]

        delete_ = desactivate_cbu_banking(token,cbuId)
        body_desactivate = delete_.json()
        print(body_desactivate)
        status = body_desactivate["status"]
        self.assertEqual(status,204,"No se elimino el cbu")
        is_active = Query_db.get_cbu_bfsa_is_active_with_email(email)
        self.assertEqual(is_active,False,"No se desactivo el cbu del user")

    def test_activate(self):
        email = "*******"
        user = login_in_whit_email(email,password)
        token = user["token"]

        get_cbu = get_cbu_banking(token)
        body = get_cbu.json()
        
        data = body["data"]
        for i in data:
            cbuId = i["cbuId"]

        delete_ = activate_cbu_banking(token,cbuId)
        body_desactivate = delete_.json()
        print(body_desactivate)
        status = body_desactivate["status"]
        self.assertEqual(status,204,"No se elimino el cbu")
        is_active = Query_db.get_cbu_bfsa_is_active_with_email(email)
        self.assertEqual(is_active,True,"No se activo el cbu del user")
        

    def test_create_cbu_with_user_dont_have(self):
        pass

    def test_create_cbu_already_exist(self):
        pass

    
    def test_delete_cbu_already_delete(self):
        pass

    def test_get_user_without_cbu(self):
        pass





    









