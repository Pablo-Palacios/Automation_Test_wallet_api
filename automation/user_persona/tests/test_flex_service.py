from decimal import Decimal
import time
from faker import Faker
import uuid
from dotenv import load_dotenv
import os
import requests
from api_back.mc_automation_qa.pruebas_v2.configuracion.views_persona import get_balance, get_transactions, mock_arg_cuentas, onboarding_validate_send_email, onboarding_validate_cuil,onboarding_validate_code_otp_email, onboarding_validate_send_sms, onboarding_validate_code_otp_sms, create_user, login, pin, change_alias, search_user_coelsa_with_alias, search_user_coelsa_with_cvu, transfer_external_send_cvu
from api_back.mc_automation_qa.pruebas_v2.configuracion.lib import cbu_random, device_models, provincias_arg
from unittest import TestCase
from api_back.mc_automation_qa.pruebas_v2.configuracion.config import Query_db
from api_back.mc_automation_qa.pruebas_v2.configuracion.main import email, password, phone, cuit, device_id
from api_back.mc_automation_qa.pruebas_v2.configuracion.code_redi import Redis



load_dotenv()


def login_in():
        email_last = Query_db.get_last_email_client()
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

def login_in_transf():
        email= 'tracypeters@movilcash.com'
        #print(f"ultimo email: {email}")
        request_login = login(email, password)

           #print(request_login.json())
        dic = {}

        response_login = request_login.json()
        #print(response_login)
        if "data" in response_login:
                data = response_login["data"]
                client = response_login["data"]["client"]
                assert "document_number" in client
                assert "commerce_id" in client
                assert "cvu" in client
                cvu = client["cvu"]
                assert "birth_date" in client
                assert "name" in client
                name = client["name"]
                assert "last_name" in client
                assert "alias" in client
                alias = client["alias"]
                assert "cuil" in client
                cuil = client["cuil"]
                token = data["token"]
                dic = {"token":token, "alias":alias, "cvu": cvu,"email":email,"cuil":cuil,"name":name}

        return dic

faker = Faker()
    
class Flex(TestCase):
    def test_a_onboarding_success(self):
            
            # REGISTER EMAIL 
            print(email)
            #print(device_id)
            register_email = onboarding_validate_send_email(device_id,email)
            response_email = register_email.json()
            print(response_email)

            if "data" in response_email:
                message = response_email["message"]
                self.assertEqual(message, "email_sent")
                status = response_email["status"]
                self.assertEqual(status, 200)


            # VALIDATE EMAIL
            code = Redis.validacion(device_id)
            email_code = onboarding_validate_code_otp_email(device_id,email,code)
            response_code_email = email_code.json()
            print(response_code_email)
            if "data" in response_code_email:
                message = response_code_email["message"]
                self.assertEqual(message, "email_validated")
                status = response_code_email["status"]
                self.assertEqual(status, 200)

            

            # REGISTER SMS
            register_sms = onboarding_validate_send_sms(device_id,phone)
            response_sms = register_sms.json()
            print(response_sms)

            if "data" in response_sms:
                message = response_sms["message"]
                self.assertEqual(message, "sms_sent")
                status = response_sms["status"]
                self.assertEqual(status, 200)


            # VALIDATE SMS
            code = Redis.validacion(device_id)
            sms_code = onboarding_validate_code_otp_sms(device_id,phone,code)
            response_code_sms = sms_code.json()
            print(response_code_sms)
            if "data" in response_code_sms:
                 message = response_code_sms["message"]
                 self.assertEqual(message, "user_validated")
                 status = response_code_sms["status"]
                 self.assertEqual(status, 200)
   

            # VALIDATE CUIT 
            validate_cuit = onboarding_validate_cuil(device_id,cuit)
            body_cuit = validate_cuit.json()
            if "data" in body_cuit:
                 message = response_code_sms["message"]
                 self.assertEqual(message, "user_validated")
                 status = response_code_sms["status"]
                 self.assertEqual(status, 200)

            # CREATE USER
        
            request_create_user = create_user(email,password, cuit, phone, device_models())
            print(request_create_user)
            body_create_user = request_create_user.json()
            print(body_create_user)
            if "status" in body_create_user:
                code = body_create_user["status"]["status_code"] 
                self.assertEqual(code, 201)


            
           

           

    def test_b_login_success(self):
            request_login = login(email, password)

           #print(request_login.json())

            response_login = request_login.json()
            print(response_login)
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
                #assert token in data
                #token = data["token"]
                #assert "message" in client
                #assert "status" in client
                cont_cuil = str(cuil)
                        
                if len(cont_cuil) > 11 or len(cont_cuil) == 12:
                            print("fail cuil, mal formulado")
                else:
                            print(f"se genero bien el cuil: {len(cont_cuil)}")
                alias_db = Query_db.get_alias_user_with_email(email)
                cvu_db = Query_db.get_cvu_user_with_email(email)

                print(f"alias db: {alias_db}")
                print(f"alias: {alias}")
                print(f"cvu db: {cvu_db}")
                print(f"cvu: {cvu}")

                self.assertEqual(alias_db, alias, "No coincide alias en db")
                self.assertEqual(cvu_db, cvu, "No coincide cvu en db")

                


    def test_change_alias(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        name = faker.first_name() 
        num = str(faker.random_number(digits = 2))

        new_alias = f"NEw.{name}.{num}"
        #new_alias = "NEw.Joseph.0"
        print(new_alias)
        
        #email = "jasminenelson@gmail.com"
        reque_change_alias = change_alias(token, email, new_alias)
        response_change_alias = reque_change_alias.json()
        print(response_change_alias)
        message = response_change_alias["message"]
        self.assertEqual(message, "alias updated")
        code = response_change_alias["code"]
        self.assertEqual(code, 202)

        alias_search = search_user_coelsa_with_alias(token,new_alias)
        print(alias_search.json())
        


    def test_change_alias_two_timens(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        name = faker.first_name() 
        num = str(faker.random_number(digits = 2))

        new_alias = f"NEw.{name}.{num}"
        #print(new_alias)
        
        #email = "stephaniemoore@gmail.com"
        reque_change_alias = change_alias(token, email, new_alias)

        response_change_alias = reque_change_alias.json()
        print(response_change_alias)

        

        name2 = faker.first_name() 
        num2 = str(faker.random_number(digits = 2))
        new_alias_2 = f"NEw.{name2}.{num2}"
        reque_change_alias_2 = change_alias(token, email, new_alias_2)
        print(reque_change_alias_2.json())

    def test_change_alias_and_search(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        name = faker.first_name() 
        num = str(faker.random_number(digits = 2))

        new_alias = f"NEw.{name}.{num}"
        #new_alias = "NEw.Joseph.0"
        print(new_alias)
        
        #email = "jasminenelson@gmail.com"
        reque_change_alias = change_alias(token, email, new_alias)
        response_change_alias = reque_change_alias.json()
        print(response_change_alias)
        message = response_change_alias["message"]
        self.assertEqual(message, "alias updated")
        code = response_change_alias["code"]
        self.assertEqual(code, 202)

        alias_search = search_user_coelsa_with_alias(token,new_alias)
        print(alias_search.json())

        time.sleep(10)
        search_coelsa_alias = search_user_coelsa_with_alias(token, new_alias)
        response_search_coelsa_alias = search_coelsa_alias.json()
        print(response_search_coelsa_alias)


    def test_search_alias_coelsa(self):
            login_data = login_in()
            token = login_data["token"]
            #alias = "DTEST.52.ONDA"
            email = login_data["email"]
            alias = login_data["alias"]
            # cbu_data = cbu_random()
            # alias = cbu_data["alias"]
            # print(alias)
        

            #alias_db = Query_db.get_alias_user_with_email(email)
            #if alias == alias_db:

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
                        
    
    def test_search_cvu_coelsa(self):
        login_data = login_in()
        token = login_data["token"]
        #cbu = "3840200500000005030701"
        email = login_data["email"]
        cbu = login_data["cvu"]
        # cbu_data = cbu_random()
        # cbu = cbu_data["cbu"]

        #cvu_db = Query_db.get_cvu_user_with_email(email)
        #if cvu == cvu_db:
        #print(cvu)
        search_coelsa_cvu = search_user_coelsa_with_cvu(token, cbu)
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
                    #print(cvu_db)
                    #print(found_alias)

    def test_send_trasnfer_external_to_cbu(self):
        login_data = login_in_transf()
        token = login_data["token"]
        email= login_data["email"]
        #email = "jillreed@gmail.com"
        cbu_data = cbu_random()
        cbu = cbu_data["cbu"]
        ammount = 0.01

        balance_send = Query_db.get_balance_to_email(email)
        print(balance_send)
        #balance_in = Query_db.get_balance_to_cvu(cvu)
        #print(f"balance inicial user credit {balance_in}")
        send_transfer = transfer_external_send_cvu(token,cbu,ammount)
        response_transfer_send = send_transfer.json()
        print(response_transfer_send)

        

        balance_send_new = Query_db.get_balance_to_email(email)
                        #print(balance_send_new)
        print("Send transfers")
        print(f"to_cbu: {cbu}")
        print(balance_send_new)
        if balance_send != balance_send_new:
                            #resta= balance_send - balance_send_new
                            #print(f" se resto {resta} de la cuenta {email}")
                            time.sleep(30)
                            trx = Query_db.transaction_trx(cbu)
                            estado = get_transactions(token,trx)
                            body_estado = estado.json()
                            print(body_estado)
                            response =body_estado["trx_status"]
                            self.assertEqual(response, "done", "No se acepto la transferencia automatica")
                                    
                            #balance_in_new = Query_db.get_balance_to_cvu(cbu)
                            #print(f"Saldo final user credit: {balance_in_new}")
                            resta_debit = Decimal(balance_send) - Decimal(ammount)
                            #suma_credit = Decimal(balance_in) + Decimal(ammount)
                            #print(float(suma_credit))
                            self.assertEqual(float(resta_debit), float(balance_send_new), "No se desconto la plata de la cuenta debit")
                            #self.assertEqual(float(suma_credit), float(balance_in_new), "No impacto el dinero en la cuenta credit")
                            # if balance_in != balance_in_new:
                            #     print(f"""
                            #             - inicio balance de cuenta credit: {balance_in} \n
                            #             - impacto de balance actualizado cuenta credit: {balance_in_new} \n
                            #             - status transfer: {response}""")
                    
        else:
            print("NO se resto el monto enviado de la cuenta origen")




    def test_trasfer_in_cbu_to_onda(self):
        login_data = login_in_transf()
        token = login_data["token"]
        email= login_data["email"]
        datos_cbu =cbu_random()

        cvu = login_data["cvu"]
        cuil_ = login_data["cuil"]
        name = login_data["name"]


        cbu = datos_cbu["cbu"]
        alias = datos_cbu["alias"]
        titular = datos_cbu["titular"]
        cuil = datos_cbu["cuil"]
        body = {
                "content": {
                    "operacion": {
                        "comprador": {
                            "cuentaVirtual": {
                                "titular": f"{name}",
                                "cuit": f"{cuil_}",
                                "cvu": f"{cvu}",
                                "psp": "OndaSiempre"
                            },
                            "titular": f"{name}",
                            "cuit": f"{cuil_}",
                            "cuenta": {
                                "banco": "",
                                "sucursal": "",
                                "terminal": "",
                                "alias": "",
                                "cbu": "",
                                "esTitular": 0,
                                "titulares": [],
                                "moneda": ""
                            }
                        },
                        "detalle": {
                            "concepto": "VARS",
                            "idUsuario": 0,
                            "idComprobante": 0,
                            "moneda": "032",
                            "importe": 100,
                            "devolucion": False,
                            "importeComision": 0,
                            "comision": 0,
                            "descripcion": "detalle descripcion"
                        },
                        "vendedor": {
                            "cuentaVirtual": {
                            "titular": "",
                            "cuit": "",
                            "cvu": "",
                            "psp": ""
                        },
                        "titular": f"{titular}",
                        "cuit": f"{cuil}",
                        "cuenta": {
                            "banco": "322",
                            "sucursal": "6027",
                            "terminal": "terminal",
                            "alias": f"{alias}",
                            "cbu": f"{cbu}",
                            "esTitular": 1,
                            "titulares": [
                                f"{titular}"
                            ],
                            "moneda": "032"
                            }
                        },
                        "estado": {
                            "codigo": "PENDIENTE"
                        },
                        "garantiaOk": True,
                        "tipo": "TRANSFERENCIA"
                    },
                    "preautorizado": True
                }
        }
        http_mocks = os.getenv('MOCKS_URL_QA')
        request = requests.post(http_mocks,json=body)
        body_request = request.json()
        coelsa_id = body_request["coelsa_id"]
        print(body_request)
        balance_old = Query_db.get_balance_to_email(email)
        amount = 30
        request_mock = mock_arg_cuentas(coelsa_id,cbu,amount,cvu,cuil_,name)
        self.assertEqual(request_mock.status_code, 200)
        print(request_mock)
        balance_credit = get_balance(token)
        body_balance = balance_credit.json()
        print(body_balance)
        total_balance = body_balance["balance"]["total_balance"]
        print(total_balance)
        suma = Decimal(balance_old) + Decimal(amount)
        self.assertEqual(float(suma),total_balance, "No se impacto la plata en la cuenta credit")



