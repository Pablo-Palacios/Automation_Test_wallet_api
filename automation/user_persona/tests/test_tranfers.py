import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from configuracion.views_persona import login, p2p_send,mock_arg_cuentas,get_all_transactions,get_transactions,get_balance,transfer_external_send_cvu,transfer_external_send_alias,login_in_whit_email
from unittest import TestCase
from configuracion.config import Query_db
from faker import Faker
import time
from configuracion.main import password
import requests
from decimal import Decimal
from configuracion.lib import cbu_random, cvu_random
import os



faker = Faker()

device_id = ""

# LOGIN 
def login_in():
        email_ = "*******"
        password_ = "*******"
        
        login_user = login(email_, password_)
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
                name = client["name"]
                assert "last_name" in client
                assert "alias" in client
                alias = client["alias"]
                assert "cuil" in client
                cuil = client["cuil"]
                #assert "email" in client
                token = data["token"]

                dic = {"token":token, "alias":alias, "cvu": cvu,"email":email_,"cuil":cuil,"name":name}

        return dic

class Transf(TestCase):
    def test_p2p(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]

    
        to_email = "michaelschmittdev@movilcash.com"
        balance_send = Query_db.get_balance_to_email(email)
        balance_in = Query_db.get_balance_to_email(to_email)
        #print(balance_send)
        #print(balance_in)
        amount = 45.19

        send_p2p = p2p_send(token,to_email,amount)
        print(send_p2p)
 
        balance_send_new = Query_db.get_balance_to_email(email)
        balance_in_new = Query_db.get_balance_to_email(to_email)
        #print(balance_send_new)
        #print(balance_in_new)

        resta_debit = Decimal(balance_send) - Decimal(amount)
        suma_credit = Decimal(balance_in) + Decimal(amount)

        self.assertEqual(float(resta_debit), float(balance_send_new), "No se desconto la plata de la cuenta debit")
        self.assertEqual(float(suma_credit), float(balance_in_new), "No se ingreso la plata de la cuenta credit")

        trx = send_p2p["trx_reference"]
        gets = get_transactions(token,trx)
        gets_body = gets.json()
        status = gets_body["trx_status"]
        self.assertEqual(status,"done","No se acepto la transferencia")
        print(gets_body)
    
    def test_p2p_monto_minimo(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]

    
        to_email = "michaelschmittdev@movilcash.com"
        balance_send = Query_db.get_balance_to_email(email)
        balance_in = Query_db.get_balance_to_email(to_email)
        #print(balance_send)
        #print(balance_in)
        amount = 1

        send_p2p = p2p_send(token,to_email,amount)
        print(send_p2p)
 
        balance_send_new = Query_db.get_balance_to_email(email)
        balance_in_new = Query_db.get_balance_to_email(to_email)
        #print(balance_send_new)
        #print(balance_in_new)

        resta_debit = Decimal(balance_send) - Decimal(amount)
        suma_credit = Decimal(balance_in) + Decimal(amount)

        self.assertEqual(float(resta_debit), float(balance_send_new), "No se desconto la plata de la cuenta debit")
        self.assertEqual(float(suma_credit), float(balance_in_new), "No se ingreso la plata de la cuenta credit")

        trx = send_p2p["trx_reference"]
        gets = get_transactions(token,trx)
        gets_body = gets.json()
        status = gets_body["trx_status"]
        self.assertEqual(status,"done","No se acepto la transferencia")
        print(gets_body)

    def test_p2p_monto_menor_minimo(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]

    
        to_email = "michaelschmittdev@movilcash.com"
        #balance_send = Query_db.get_balance_to_email(email)
        #balance_in = Query_db.get_balance_to_email(to_email)
        #print(balance_send)
        #print(balance_in)
        amount = 0.1

        send_p2p = p2p_send(token,to_email,amount)
        print(send_p2p)
        status = send_p2p["status"]["status_code"]
        self.assertEqual(status, 400, f"status diferente: {status}")

    def test_p2p_monto_cero(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]

    
        to_email = "michaelschmittdev@movilcash.com"
        #balance_send = Query_db.get_balance_to_email(email)
        #balance_in = Query_db.get_balance_to_email(to_email)
        #print(balance_send)
        #print(balance_in)
        amount = 0

        send_p2p = p2p_send(token,to_email,amount)
        print(send_p2p)
        status = send_p2p["status"]["status_code"]
        self.assertEqual(status, 400, f"status diferente: {status}")

    def test_error_p2p_number_negative(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]

    
        to_email = "michaelschmittdev@movilcash.com"
        balance_send = Query_db.get_balance_to_email(email)
        balance_in = Query_db.get_balance_to_email(to_email)
        #print(balance_send)
        #print(balance_in)
        amount = -1

        send_p2p = p2p_send(token,to_email,amount)
        print(send_p2p)
 
        balance_send_new = Query_db.get_balance_to_email(email)
        balance_in_new = Query_db.get_balance_to_email(to_email)

        if balance_send_new != balance_send or balance_in_new != balance_in:
            self.fail("Falla el tests, se cambio el el saldo debit and credit")
        else:
            balance_send_new == balance_send or balance_in_new == balance_in
            print("test success")
        
        


    def test_all_transactions_user(self):
        login_data = login_in()
        token = login_data["token"]
        all_transactions = get_all_transactions(token)
        self.assertEqual(all_transactions.status_code,200,"Fallo status get transaction")
        response_all_transactions = all_transactions.json()
        print(response_all_transactions)
        if response_all_transactions:
            assert "skip" in response_all_transactions
            assert "limit" in response_all_transactions
            assert "pages" in response_all_transactions
            assert "total" in response_all_transactions
            assert "data" in response_all_transactions
            assert isinstance(response_all_transactions["data"], list), "La clave 'data' no es una lista"

        

    def test_get_last_transaction(self):
        login_data = login_in()
        token = login_data["token"]
        all_transactions = get_all_transactions(token)
        response_all_transactions = all_transactions.json()
        data = response_all_transactions["data"]
        last = data[0]
        trx_last = last["trx_reference"]
        gets_trans = get_transactions(token,trx_last)
        self.assertEqual(gets_trans.status_code,200,"Fallo status get transaction")
        body_gets_trans = gets_trans.json()

        if body_gets_trans:
            assert "trx_reference" in body_gets_trans
            assert "trx_status" in body_gets_trans
            assert "direction" in body_gets_trans
            assert "type" in body_gets_trans
            assert "currency" in body_gets_trans
            assert "amount" in body_gets_trans
            assert "related_full_name" in body_gets_trans
            assert "related_cbu" in body_gets_trans
            assert "related_cuit" in body_gets_trans
            assert "concept" in body_gets_trans
            assert "reference" in body_gets_trans
            assert "created_time" in body_gets_trans
            assert "updated_time" in body_gets_trans
            


    def test_send_trasnfer_external_to_cvu_cbu(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        cvu_data = cbu_random()
        cvu = cvu_data["cbu"]
        print(cvu)

        ammount = 123.29

        balance_send = Query_db.get_balance_to_email(email)
        print(f"balance inicial: f{balance_send}")
     
        send_transfer = transfer_external_send_cvu(token,cvu,ammount)
        response_transfer_send = send_transfer.json()
        print(response_transfer_send)
        
             
        time.sleep(10)
            
        balance_send_new = Query_db.get_balance_to_email(email)

        resta_debit = Decimal(balance_send) - Decimal(ammount)
                                
        self.assertEqual(float(resta_debit), float(balance_send_new), "No se desconto la plata de la cuenta debit")

        trx = response_transfer_send["trx_reference"]
        gets = get_transactions(token,trx)

        print(gets.json())

    def test_trasnfer_external_to_cvu_cbu_monto_minimo(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        cvu_data = cbu_random()
        cvu = cvu_data["cbu"]
        print(cvu)

        ammount = 1

        balance_send = Query_db.get_balance_to_email(email)
        print(f"balance inicial: f{balance_send}")
     
        send_transfer = transfer_external_send_cvu(token,cvu,ammount)
        response_transfer_send = send_transfer.json()
        print(response_transfer_send)
        
             
        time.sleep(10)
            
        balance_send_new = Query_db.get_balance_to_email(email)

        resta_debit = Decimal(balance_send) - Decimal(ammount)
                                
        self.assertEqual(float(resta_debit), float(balance_send_new), "No se desconto la plata de la cuenta debit")

        trx = response_transfer_send["trx_reference"]
        gets = get_transactions(token,trx)

        print(gets.json())
    
    def test_trasnfer_external_to_cvu_cbu_monto_cero(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        cvu_data = cbu_random()
        cvu = cvu_data["cbu"]
        print(cvu)

        ammount = 0

        balance_send = Query_db.get_balance_to_email(email)
        print(f"balance inicial: f{balance_send}")
     
        send_transfer = transfer_external_send_cvu(token,cvu,ammount)
        response_transfer_send = send_transfer.json()
        print(response_transfer_send)
        status = response_transfer_send["status"]["status_code"]
        self.assertEqual(status,400,f"status = {status}")
        
             
        # time.sleep(10)
            
        # balance_send_new = Query_db.get_balance_to_email(email)

        # resta_debit = Decimal(balance_send) - Decimal(ammount)
                                
        # self.assertEqual(float(resta_debit), float(balance_send_new), "No se desconto la plata de la cuenta debit")

        # trx = response_transfer_send["trx_reference"]
        # gets = get_transactions(token,trx)

        # print(gets.json())

    def test_trasnfer_external_to_cvu_cbu_monto_menor_minimo(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        cvu_data = cbu_random()
        cvu = cvu_data["cbu"]
        print(cvu)

        ammount = 0.1

        balance_send = Query_db.get_balance_to_email(email)
        print(f"balance inicial: f{balance_send}")
     
        send_transfer = transfer_external_send_cvu(token,cvu,ammount)
        response_transfer_send = send_transfer.json()
        print(response_transfer_send)
        status = response_transfer_send["status"]["status_code"]
        self.assertEqual(status,400,f"status = {status}")
             
        # time.sleep(10)
            
        # balance_send_new = Query_db.get_balance_to_email(email)

        # resta_debit = Decimal(balance_send) - Decimal(ammount)
                                
        # self.assertEqual(float(resta_debit), float(balance_send_new), "No se desconto la plata de la cuenta debit")

        # trx = response_transfer_send["trx_reference"]
        # gets = get_transactions(token,trx)

        # print(gets.json())
        

    def test_send_trasnfer_external_negative_to_cvu_cbu(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        cvu_data = cbu_random()
        cvu = cvu_data["cbu"]
        print(cvu)

        ammount = -1

        balance_send = Query_db.get_balance_to_email(email)
        print(f"balance inicial: f{balance_send}")
     
        send_transfer = transfer_external_send_cvu(token,cvu,ammount)
        response_transfer_send = send_transfer.json()
        print(response_transfer_send)
        self.assertEqual(send_transfer.status_code,400,"Se efecto la transferencia")
        time.sleep(10)
            
        balance_send_new = Query_db.get_balance_to_email(email)
        self.assertEqual(float(balance_send), float(balance_send_new), "Se desconto la plata de la cuenta debit")

        
    def test_send_trasnfer_external_to_alias(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        cvu_data = cbu_random()
        alias = "Javier.Sabag.2024"

        ammount = 1

        balance_send = Query_db.get_balance_to_email(email)
        print(f"balance user {balance_send}")
      
       
        send_transfer = transfer_external_send_alias(token,alias,ammount)
        response_transfer_send = send_transfer.json()
        print(response_transfer_send)
        self.assertEqual(send_transfer.status_code,200,"No Se efecto la transferencia")
 
        time.sleep(10)
            
        balance_send_new = Query_db.get_balance_to_email(email)

        resta_debit = Decimal(balance_send) - Decimal(ammount)
                                
        self.assertEqual(float(resta_debit), float(balance_send_new), "No se desconto la plata de la cuenta debit")
        
        trx = response_transfer_send["trx_reference"]
        gets = get_transactions(token,trx)

        print(gets.json())

    def test_trasnfer_external_to_alias_monto_minimo(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        cvu_data = cbu_random()
        alias = "Javier.Sabag.2024"

        ammount = 1

        balance_send = Query_db.get_balance_to_email(email)
        print(f"balance user {balance_send}")
      
       
        send_transfer = transfer_external_send_alias(token,alias,ammount)
        response_transfer_send = send_transfer.json()
        print(response_transfer_send)
        self.assertEqual(send_transfer.status_code,200,"No Se efecto la transferencia")
 
        time.sleep(10)
            
        balance_send_new = Query_db.get_balance_to_email(email)

        resta_debit = Decimal(balance_send) - Decimal(ammount)
                                
        self.assertEqual(float(resta_debit), float(balance_send_new), "No se desconto la plata de la cuenta debit")
        
        trx = response_transfer_send["trx_reference"]
        gets = get_transactions(token,trx)

        print(gets.json())
    
    def test_trasnfer_external_to_alias_monto_cero(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        cvu_data = cbu_random()
        alias = "Javier.Sabag.2024"

        ammount = 0

        balance_send = Query_db.get_balance_to_email(email)
        print(f"balance user {balance_send}")
      
       
        send_transfer = transfer_external_send_alias(token,alias,ammount)
        response_transfer_send = send_transfer.json()
        print(response_transfer_send)
        status = response_transfer_send["status"]["status_code"]
        self.assertEqual(status,400,f"status: {status}")
        
 
        # time.sleep(10)
            
        # balance_send_new = Query_db.get_balance_to_email(email)

        # resta_debit = Decimal(balance_send) - Decimal(ammount)
                                
        # self.assertEqual(float(resta_debit), float(balance_send_new), "No se desconto la plata de la cuenta debit")
        
        # trx = response_transfer_send["trx_reference"]
        # gets = get_transactions(token,trx)

        # print(gets.json())
        
    def test_trasnfer_external_to_alias_monto_menor_minimo(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        cvu_data = cbu_random()
        alias = "Javier.Sabag.2024"

        ammount = 0.01

        balance_send = Query_db.get_balance_to_email(email)
        print(f"balance user {balance_send}")
      
       
        send_transfer = transfer_external_send_alias(token,alias,ammount)
        response_transfer_send = send_transfer.json()
        print(response_transfer_send)
        status = response_transfer_send["status"]["status_code"]
        self.assertEqual(status,400,f"status: {status}")
 
        # time.sleep(10)
            
        # balance_send_new = Query_db.get_balance_to_email(email)

        # resta_debit = Decimal(balance_send) - Decimal(ammount)
                                
        # self.assertEqual(float(resta_debit), float(balance_send_new), "No se desconto la plata de la cuenta debit")
        
        # trx = response_transfer_send["trx_reference"]
        # gets = get_transactions(token,trx)

        # print(gets.json())

    def test_trasfer_in_cbu_to_onda(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        cvu = login_data["cvu"]
        cuil_ = login_data["cuil"]
        name = login_data["name"]
        datos_cbu =cbu_random()

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
        https_mocks = os.getenv('MOCKS_URL_DEV')
        request = requests.post(https_mocks,json=body)
        body_request = request.json()
        coelsa_id = body_request["coelsa_id"]
        print(body_request)
        balance_old = Query_db.get_balance_to_email(email)
        amount = 30
        request_mock = mock_arg_cuentas(coelsa_id,cbu,amount,cvu,cuil,name)
        self.assertEqual(request_mock.status_code, 200)
        print(request_mock)
        balance_credit = get_balance(token)
        body_balance = balance_credit
        print(body_balance)
        total_balance = body_balance["balance"]["total_balance"]
        print(total_balance)
        suma = Decimal(balance_old) + Decimal(amount)
        self.assertEqual(float(suma),total_balance, "No se impacto la plata en la cuenta credit onda")

    def test_transfer_external_to_fail_acount_alias(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        alias = "Sabag.2024"

        ammount = 43.33

        balance_send = Query_db.get_balance_to_email(email)
        print(f"balance user {balance_send}")
      
       
        send_transfer = transfer_external_send_alias(token,alias,ammount)
        response_transfer_send = send_transfer.json()
        self.assertEqual(send_transfer.status_code,400,"Se efecto la transferencia")
        print(response_transfer_send)
 
        time.sleep(2)
            
        balance_send_new = Query_db.get_balance_to_email(email)
                                
        self.assertEqual(float(balance_send), float(balance_send_new), "Se desconto la plata de la cuenta debit")

    

    def test_transfer_external_to_fail_acount_cvu_cbu(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        cvu = "0070138530004027543312"

        ammount = 43.33

        balance_send = Query_db.get_balance_to_email(email)
        print(f"balance user {balance_send}")
      
       
        send_transfer = transfer_external_send_cvu(token,cvu,ammount)
        response_transfer_send = send_transfer.json()
        self.assertEqual(send_transfer.status_code,400,"Se efecto la transferencia")
        print(response_transfer_send)
 
        time.sleep(2)
            
        balance_send_new = Query_db.get_balance_to_email(email)
                                
        self.assertEqual(float(balance_send), float(balance_send_new), "Se desconto la plata de la cuenta debit")



    # def test_trasfer_in_cvu_to_onda(self):
    #     login_data = login_in()
    #     token = login_data["token"]
    #     email= login_data["email"]
    #     cvu_data = cvu_random()

    #     cvu = cvu_data["cvu"]
    #     titular = cvu_data["titular"]
    #     cuil = cvu_data["cuil"]

    #     body = {
    #             "content": {
    #                 "operacion": {
    #                     "comprador": {
    #                         "cuentaVirtual": {
    #                             "titular": "Daniel",
    #                             "cuit": "20812332731",
    #                             "cvu": "0000001700000002002820",
    #                             "psp": "OndaSiempre"
    #                         },
    #                         "titular": "Daniel",
    #                         "cuit": "20812332731",
    #                         "cuenta": {
    #                             "banco": "",
    #                             "sucursal": "",
    #                             "terminal": "",
    #                             "alias": "",
    #                             "cbu": "",
    #                             "esTitular": 0,
    #                             "titulares": [],
    #                             "moneda": ""
    #                         }
    #                     },
    #                     "detalle": {
    #                         "concepto": "VARS",
    #                         "idUsuario": 0,
    #                         "idComprobante": 0,
    #                         "moneda": "032",
    #                         "importe": 100,
    #                         "devolucion": False,
    #                         "importeComision": 0,
    #                         "comision": 0,
    #                         "descripcion": "detalle descripcion"
    #                     },
    #                     "vendedor": {
    #                         "cuentaVirtual": {
    #                         "titular": f"{titular}",
    #                         "cuit": f"{cuil}",
    #                         "cvu": f"{cvu}",
    #                         "psp": "1"
    #                     },
    #                     "titular": "Mercado libre",
    #                     "cuit": "20111111112",
    #                     "cuenta": {
    #                         "banco": "",
    #                         "sucursal": "",
    #                         "terminal": "",
    #                         "alias": "",
    #                         "cbu": "",
    #                         "esTitular": 0,
    #                         "titulares": [],
    #                         "moneda": ""
    #                         }
    #                     },
    #                     "estado": {
    #                         "codigo": "PENDIENTE"
    #                     },
    #                     "garantiaOk": True,
    #                     "tipo": "TRANSFERENCIA"
    #                 },
    #                 "preautorizado": True
    #             }
    #     }
    #     https_mocks = os.getenv('MOCKS_URL_DEV')
    #     request = requests.post(https_mocks,json=body)
    #     body_request = request.json()
    #     coelsa_id = body_request["coelsa_id"]
    #     print(coelsa_id)
    #     balance_old = Query_db.get_balance_to_email(email)
    #     amount = 110.55
    #     request_mock = mock_arg_cuentas(coelsa_id,cvu,amount)
    #     self.assertEqual(request_mock.status_code, 200)
    #     print(request_mock)
    #     balance_credit = get_balance(token)
    #     body_balance = balance_credit.json()
    #     print(body_balance)
    #     total_balance = body_balance["balance"]["total_balance"]
    #     suma = Decimal(balance_old) + Decimal(amount)
    #     self.assertEqual(float(suma),float(total_balance), "No se impacto la plata en la cuenta credit")





    def test_send_p2p_accound_empty(self):
        email_ = "meredithgregorydev@movilcash.com"
        password_ = "Pablo123"
        login_data = login_in_whit_email(email_,password_)
        token = login_data["token"]

        balance = get_balance(token)
        #print(balance)
        available = balance["balance"]["available_balance"]
        if available == 0.0:
            
            to_email = "michaeldavisdev@movilcash.com"
            amount = 120

            send_p2p = p2p_send(token,to_email,amount)
            print(send_p2p)
            status = send_p2p["status"]["status_code"]
            message = send_p2p["message"]

            self.assertEqual(status, 400, "Se genero la transf p2p con cuenta vacia")
            self.assertEqual(message,"InsufficientBalanceException: Insufficient balance")
        else:
            self.fail("La cuenta tiene plata, no esta vacia")
            




    def test_send_trasnfer_external_accound_empty(self):
        email_ = "meredithgregorydev@movilcash.com"
        password_ = "Pablo123"
        login_data = login_in_whit_email(email_,password_)
        token = login_data["token"]
        

        balance = get_balance(token)
        #print(balance)
        available = balance["balance"]["available_balance"]
        if available == 0.0:
            cbu_data = cbu_random()
            cbu = "0070076430004058345624"
            ammount = 100

            send_transfer = transfer_external_send_cvu(token,cbu,ammount)
            response_transfer_send = send_transfer.json()
            print(response_transfer_send)

            status = response_transfer_send["status"]["status_code"]
            message = response_transfer_send["message"]

            self.assertEqual(status, 400, "Se genero la transf ext saliente con cuenta vacia")
            self.assertEqual(message,"InsufficientBalanceException: Insufficient balance")
        else:
            self.fail("La cuenta tiene plata, no esta vacia")


        











            

        
            





                

                

        



