from views import login, get_profile, change_alias, search_user_coelsa_with_alias,transfer_external_send_alias
from unittest import TestCase
from automation.database.config import Query_db
from faker import Faker
import time

password ='Pablo123'


faker = Faker()

# LOGIN 
def login_in():
        #email_last = Query_db.get_last_email_client()
        email_last = 'carolfinley@gmail.com'
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
    
    def test_change_alias(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        alias = login_data["alias"]
        name = faker.first_name() 
        num = str(faker.random_number(digits = 2))

        new_alias = f"NEw.{name}.{num}"

        #new_alias = "NEw.Joseph.0"
        print(f"Alias viejo: {alias}")
        print(email)
        print(new_alias)
        
        #email = "elizabethdavis@gmail.com"
        reque_change_alias = change_alias(token, email, new_alias)
        response_change_alias = reque_change_alias.json()
        print(response_change_alias)

        # for item in response_change_alias:
        #     if isinstance(item, dict) and 'response' in item:
        #         response = item["response"]
        #         assert 'message' in response
        #         assert 'status' in response
        #     elif item:
        #         self.assertEqual(item, 202, "No se cambio correctamente el alias")

    # def test_change_alias_two_timens(self):
    #     login_data = login_in()
    #     token = login_data["token"]
    #     email= login_data["email"]
    #     name = faker.first_name() 
    #     num = str(faker.random_number(digits = 2))

    #     new_alias = f"NEw.{name}.{num}"
    #     #print(new_alias)
        
    #     email = "christinehubbard@gmail.com"
    #     reque_change_alias = change_alias(token, email, new_alias)

    #     response_change_alias = reque_change_alias.json()
    #     #print(response_change_alias)

    #     for item in response_change_alias:
    #         if isinstance(item, dict) and 'response' in item:
    #             response = item["response"]
    #             assert 'message' in response
    #             assert 'status' in response
    #         elif item:
    #             self.assertEqual(item, 202, "No se cambio correctamente el alias")

    #     name2 = faker.first_name() 
    #     num2 = str(faker.random_number(digits = 2))
    #     new_alias_2 = f"NEw.{name2}.{num2}"
    #     reque_change_alias_2 = change_alias(UserOnda.token, email, new_alias_2)
    #     for item in reque_change_alias_2.json():
    #         if isinstance(item, dict) and 'response' in item:
    #             response = item["response"]
    #             assert 'message' in response
    #             assert 'status' in response
    #         elif item:
    #             self.assertEqual(item, 202, "No se cambio correctamente el alias")

    # def test_change_alias_and_search(self):
    #     login_data = login_in()
    #     token = login_data["token"]
    #     email= login_data["email"]
    #     name = faker.first_name() 
    #     num = str(faker.random_number(digits = 2))

    #     new_alias = f"NEw.{name}.{num}"
    #     #new_alias = "NEw.Joseph.0"
    #     print(new_alias)
        
    #     #email = "jasminenelson@gmail.com"
    #     reque_change_alias = change_alias(token, email, new_alias)
    #     response_change_alias = reque_change_alias.json()
    #     print(response_change_alias)
    #     message = response_change_alias["message"]
    #     self.assertEqual(message, "alias updated")
    #     code = response_change_alias["code"]
    #     self.assertEqual(code, 202)

    #     alias_search = search_user_coelsa_with_alias(token,new_alias)
    #     print(alias_search.json())

    #     time.sleep(10)
    #     search_coelsa_alias = search_user_coelsa_with_alias(token, new_alias)
    #     response_search_coelsa_alias = search_coelsa_alias.json()
    #     print(response_search_coelsa_alias)

      