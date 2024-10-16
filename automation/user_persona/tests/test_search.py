import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from configuracion.views_persona import login, search_user_coelsa_with_alias, search_user_onda_email, search_user_coelsa_with_cvu,get_profile,search_user_onda_phone
from unittest import TestCase
from configuracion.config import Query_db
from faker import Faker
from configuracion.main import password
from configuracion.lib import cbu_random


faker = Faker()

device_id = ""

# LOGIN 
def login_in():
        email_last = "*******"
        #email_last = 'brianmedinadev@movilcash.com'
        login_user = login(email_last, password)
        response_login = login_user.json()
        
        dic = {}

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

                dic = {"token":token, "alias":alias, "cvu": cvu,"email":email_last}

        return dic


class UserOnda(TestCase):
    
    def test_search_user_onda_email(self):

        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        #mjs = login_data["mjs"]
        #print(mjs)
        search_onda = search_user_onda_email(token,email)
        response_search_onda = search_onda.json()
        #print(response_search_onda)

        for item in response_search_onda:
            if item and 'response' in item:
                response = item["response"]
                assert 'full_name' in response
                assert 'document_number' in response
                assert 'cuil' in response
                assert 'email' in response
                assert 'status' in response
                status = response["status"]
                code = status["status_code"]
                self.assertEqual(code, 200, "No se encontro al user")

    def test_search_user_onda_phone(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        phone = '543516414249'
        #mjs = login_data["mjs"]
        #print(mjs)
        search_onda = search_user_onda_phone(token,phone)
        response_search_onda = search_onda.json()
        #print(response_search_onda)

        for item in response_search_onda:
            if item and 'response' in item:
                response = item["response"]
                assert 'full_name' in response
                assert 'document_number' in response
                assert 'cuil' in response
                assert 'email' in response
                assert 'status' in response
                status = response["status"]
                code = status["status_code"]
                self.assertEqual(code, 200, "No se encontro al user")

    def test_get_profile(self):
        login_data = login_in()
        token = login_data["token"]
        email = login_data["email"]

        request_get_profile = get_profile(token)
        body_profile = request_get_profile.json()
        print(body_profile)
        for item in body_profile:
            if item and 'response' in item:
                response = item["response"]
                assert 'password' in response
                assert 'full_name' in response
                assert 'birth_date' in response
                assert 'phone_number' in response
                assert 'cuil' in response
                assert 'email' in response

    def test_search_alias_coelsa(self):
        login_data = login_in()
        token = login_data["token"]
        alias = login_data["alias"]
        email = login_data["email"]
        #cb = cbu_random()
        alias = "Javier.Sabag.2024"        

        search_coelsa_alias = search_user_coelsa_with_alias(token, alias)
        response_search_coelsa_alias = search_coelsa_alias.json()
        print(response_search_coelsa_alias)

        for item in response_search_coelsa_alias:
                if item and 'response' in item:
                    response = item["response"]
                    assert 'owner' in response
                    owner = response["owner"]
                    assert 'bank' in response
                    assert 'cvu' in response
                    found_cvu = response["cvu"]
                    assert 'alias' in response
                    found_alias = response["alias"]
                    assert 'active' in response
                    assert 'type' in response
                    assert 'status' in response
                    status = response["status"]
                    code = status["status_code"]
                    self.assertEqual(code, 200, "No se encontro el cvu en coelsa")
                    #print(owner)
                    #print(found_cvu)
                    print(found_alias)
    
    def test_search_cvu_coelsa(self):
        login_data = login_in()
        token = login_data["token"]
        cvu = login_data["cvu"]
        email = login_data["email"]
        #cbu_data = cbu_random()
        #cvu = cbu_data["cbu"]
        #cvu = "0720500288000001534218"

        print(cvu)
        search_coelsa_cvu = search_user_coelsa_with_cvu(token, cvu)
        response_search_coelsa_cvu = search_coelsa_cvu.json()
        print(response_search_coelsa_cvu)

        for item in response_search_coelsa_cvu:
                if item and 'response' in item:
                    response = item["response"]
                    assert 'owner' in response
                    owner = response["owner"]
                    assert 'bank' in response
                    assert 'cvu' in response
                    found_cvu = response["cvu"]
                    assert 'alias' in response
                    found_alias = response["alias"]
                    assert 'active' in response
                    assert 'type' in response
                    assert 'status' in response
                    status = response["status"]
                    code = status["status_code"]
                    self.assertEqual(code, 200, "No se encontro el cvu en coelsa")
                    # print(owner)
                    print(found_cvu)
                    print(found_alias)

    
    def test_search_fail_cvu_coelsa(self):
        login_data = login_in()
        token = login_data["token"]
        #cvu = login_data["cvu"]
        email = login_data["email"]
        #cbu_data = cbu_random()
        #cvu = cbu_data["cbu"]
        cvu = "0720500288000001534222"

        search_coelsa_cvu = search_user_coelsa_with_cvu(token, cvu)
        response_search_coelsa_cvu = search_coelsa_cvu.json()
        print(response_search_coelsa_cvu)
        self.assertEqual(search_coelsa_cvu.status_code, 400,f"Status difirente: {search_coelsa_cvu.status_code}")

    def test_search_fail_cvu_coelsa(self):
        login_data = login_in()
        token = login_data["token"]
        #cvu = login_data["cvu"]
        email = login_data["email"]
        #cbu_data = cbu_random()
        #cvu = cbu_data["cbu"]
        alias = "Sabag.2024"

        search_coelsa_alias = search_user_coelsa_with_alias(token, alias)
        response_search_coelsa_cvu = search_coelsa_alias.json()
        print(response_search_coelsa_cvu)
        self.assertEqual(search_coelsa_alias.status_code, 406,f"Status difirente: {search_coelsa_alias.status_code}")

        


        