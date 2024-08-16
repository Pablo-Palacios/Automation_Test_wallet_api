from views import login, p2p_send,mock_arg_cuentas,get_all_transactions,get_transactions,get_balance,transfer_external_send_cvu,transfer_external_send_alias
from unittest import TestCase
from automation.database.config import Query_db
from faker import Faker
import time
from automation.lib.main import password
import requests
from decimal import Decimal
from automation.lib.lib import cbu_random, cvu_random
from dotenv import load_dotenv
import os

load_dotenv()

faker = Faker()

device_id = ""

# LOGIN 
def login_in():
        email_last = "carolfinley@gmail.com"
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

class Transf(TestCase):
    def test_p2p(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]

    
        to_email = Query_db.get_last_email_client()
        balance_send = Query_db.get_balance_to_email(email)
        balance_in = Query_db.get_balance_to_email(to_email)
        print(balance_send)
        print(balance_in)

        send_p2p = p2p_send(token,to_email)
        print(send_p2p)
 
        balance_send_new = Query_db.get_balance_to_email(email)
        balance_in_new = Query_db.get_balance_to_email(to_email)
        print(balance_send_new)
        print(balance_in_new)

        debit = float(balance_send) - 10.55
        credit = float(balance_in) + 10.55

        self.assertEqual(float(debit), float(balance_send_new), "No se desconto la plata en la cuenta debit")
        self.assertEqual(float(credit), float(balance_in_new), "No se impacto la plata en la cuenta credit")
        
        trx = Query_db.p2p_trx()
        estado = get_transactions(token,trx)
        print(estado.json())
        for item in estado.json():
                    if isinstance(item, dict) and 'response' in item:
                        response = item["response"]
                        assert 'trx_reference' in response
                        status = response["status"]["status_code"]
                        self.assertEqual(status,200, "No trajo la transactions")
    
    def test_p2p_centavos(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        amount = 0.35
        to_email = Query_db.get_last_email_client()
        balance_send = Query_db.get_balance_to_email(email)
        balance_in = Query_db.get_balance_to_email(to_email)
        #print(balance_send)
        #print(balance_in)
        send_p2p = p2p_send(token,email, to_email, amount)
        response_p2p = send_p2p.json()
        balance_send_new = Query_db.get_balance_to_email(email)
        balance_in_new = Query_db.get_balance_to_email(to_email)
        #print(balance_send_new)
        #print(balance_in_new)
        #print(response_p2p)
        for item in response_p2p:
            if isinstance(item, dict) and 'response' in item:
                mjs = item["response"]["message"]
                self.assertEqual(mjs, 'Transfer successful')
            elif item:
                self.assertEqual(item, 201, "Tranfers dropp")

            trx = Query_db.p2p_trx()
            estado = get_transactions(token,trx)
            json_estado = estado.json()
            for item in json_estado:
                    if isinstance(item, dict) and 'response' in item:
                        response = item["response"]
                        assert 'trx_reference' in response
                        status = response["status"]["status_code"]
                        self.assertEqual(status,200, "No trajo la transactions")

    def test_all_transactions_user(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        all_transactions = get_all_transactions(token)
        response_all_transactions = all_transactions.json()
        
        #print(response_all_transactions)
        for item in response_all_transactions:
            if isinstance(item, dict) and 'response' in item:
                response = item["response"]
                assert 'transactions' in response
                status = response["status"]["status_code"]
                self.assertEqual(status, 200, "No trajo correctamente las transactions")

    def test_get_last_transaction(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        all_transactions = get_all_transactions(token)
        response_all_transactions = all_transactions.json()
        for item in response_all_transactions:
            if isinstance(item, dict) and 'response' in item:
                response = item["response"]
                assert 'transactions' in response
                last_transaction = response['transactions'][0]
                #print(last_transaction)
                trx_reference = last_transaction["trx_reference"]
        
                get_trans = get_transactions(token, email,trx_reference)
                response_get_trans = get_trans.json()
                #print(response_get_trans)
                for item in response_get_trans:
                    if isinstance(item, dict) and 'response' in item:
                        response = item["response"]
                        assert 'trx_reference' in response
                        status = response["status"]["status_code"]
                        self.assertEqual(status,200, "No trajo la transactions")


    def test_send_trasnfer_external_to_cvu(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        #email = "jillreed@gmail.com"
        cvu_data = cvu_random()
        cvu = cvu_data["cvu"]
        ammount = 00.15

        balance_send = Query_db.get_balance_to_email(email)
        print(f"balance inicial: f{balance_send}")
        #balance_in = Query_db.get_balance_to_cvu(cvu)
        #print(f"balance inicial user credit {balance_in}")
        send_transfer = transfer_external_send_cvu(token,cvu,ammount)
        response_transfer_send = send_transfer.json()
        print(response_transfer_send)

        

        balance_send_new = Query_db.get_balance_to_email(email)
                        #print(balance_send_new)
        print("Send transfers")
        print(f"to_cvu: {cvu}")
        print(balance_send_new)
        if balance_send != balance_send_new:
                            #resta= balance_send - balance_send_new
                            #print(f" se resto {resta} de la cuenta {email}")
                            time.sleep(30)
                            trx = Query_db.transaction_trx(cvu)
                            estado = get_all_transactions(token)
                            body_estado = estado.json()
                            print(body_estado)
                            response =body_estado["trx_status"]
                            self.assertEqual(response, "done", "No se acepto la transferencia automatica")
                                    
                            #balance_in_new = Query_db.get_balance_to_cvu(cvu)
                            #print(f"Saldo final user credit: {balance_in_new}")
                            resta_debit = Decimal(balance_send) - Decimal(ammount)
                            #suma_credit = Decimal(balance_in) + Decimal(ammount)
                            #print(float(suma_credit))
                            self.assertEqual(float(resta_debit), float(balance_send_new), "No se desconto la plata de la cuenta debit")
                            #self.assertEqual(float(suma_credit), float(balance_in_new), "No impacto el dinero en la cuenta credit")
                            
                    
        else:
            print("NO se resto el monto enviado de la cuenta origen")

    def test_send_trasnfer_external_to_alias(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        cvu_data = cvu_random()
        alias = cvu_data["alias"]
        

        ammount = 200

        balance_send = Query_db.get_balance_to_email(email)
        cvu = Query_db.get_cvu_with_alias(alias)
        print(f"balance user {balance_send}")
        balance_in = Query_db.get_balance_to_cvu(cvu)
        print(f"balance inicial user {balance_in}")

       
        send_transfer = transfer_external_send_alias(token,alias,ammount)
        response_transfer_send = send_transfer.json()

        
        print(balance_send_new)
        print("Send transfers")
        print(f"to_alias: {alias}")

        time.sleep(30)
        balance_send_new = Query_db.get_balance_to_email(email)
        if balance_send != balance_send_new:
                            resta= balance_send - balance_send_new
                            print(f" se resto {resta} de la cuenta {email}")
                            time.sleep(30)
                            trx = Query_db.transaction_trx(cvu)
                            estado = get_all_transactions(token)
                            body_estado = estado.json()
                            print(body_estado)
                            response =body_estado["trx_status"]
                            self.assertEqual(response, "done", "No se acepto la transferencia automatica")
                                    
                            balance_in_new = Query_db.get_balance_to_cvu(cvu)
                            print(f"Saldo final user credit: {balance_in_new}")
                            resta_debit = Decimal(balance_send) - Decimal(ammount)
                            suma_credit = Decimal(balance_in) + Decimal(ammount)
                            print(float(suma_credit))
                            self.assertEqual(float(resta_debit), float(balance_send_new), "No se desconto la plata de la cuenta debit")
                            self.assertEqual(float(suma_credit), float(balance_in_new), "No impacto el dinero en la cuenta credit")
                            
        else:
            print("NO se resto el monto enviado de la cuenta origen")
                    
                    
    def test_send_trasnfer_external_to_cbu(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        email = "jillreed@gmail.com"
        cbu_data = cbu_random()
        cbu = cbu_data["cbu"]
        ammount = 22.38

        balance_send = Query_db.get_balance_to_email(email)
        print(balance_send)
        balance_in = Query_db.get_balance_to_cvu(cbu)
        print(f"balance inicial user credit {balance_in}")
        send_transfer = transfer_external_send_cvu(token,cbu,ammount)
        response_transfer_send = send_transfer.json()
        print(response_transfer_send)

        

        balance_send_new = Query_db.get_balance_to_email(email)
        print(balance_send_new)
        print("Send transfers")
        print(f"to_cbu: {cbu}")
        print(balance_send_new)
        if balance_send != balance_send_new:
                            resta= balance_send - balance_send_new
                            print(f" se resto {resta} de la cuenta {email}")
                            time.sleep(30)
                            trx = Query_db.transaction_trx(cbu)
                            estado = get_transactions(token,trx)
                            body_estado = estado.json()
                            print(body_estado)
                            response =body_estado["trx_status"]
                            self.assertEqual(response, "done", "No se acepto la transferencia automatica")
                                    
                            balance_in_new = Query_db.get_balance_to_cvu(cbu)
                            print(f"Saldo final user credit: {balance_in_new}")
                            resta_debit = Decimal(balance_send) - Decimal(ammount)
                            suma_credit = Decimal(balance_in) + Decimal(ammount)
                            print(float(suma_credit))
                            self.assertEqual(float(resta_debit), float(balance_send_new), "No se desconto la plata de la cuenta debit")
                            self.assertEqual(float(suma_credit), float(balance_in_new), "No impacto el dinero en la cuenta credit")
                            if balance_in != balance_in_new:
                                print(f"""
                                        - inicio balance de cuenta credit: {balance_in} \n
                                        - impacto de balance actualizado cuenta credit: {balance_in_new} \n
                                        - status transfer: {response}""")
                    
        else:
            print("NO se resto el monto enviado de la cuenta origen")

    def test_send_trasnfer_external_to_cbu(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        #email = "jillreed@gmail.com"
        cvu = cvu_random()
        ammount = 22.38

        balance_send = Query_db.get_balance_to_email(email)
        print(balance_send)
        balance_in = Query_db.get_balance_to_cvu(cvu)
        print(f"balance inicial user credit {balance_in}")
        send_transfer = transfer_external_send_cvu(token,cvu,ammount)
        response_transfer_send = send_transfer.json()
        print(response_transfer_send)

        

        balance_send_new = Query_db.get_balance_to_email(email)
        print(balance_send_new)
        print("Send transfers")
        print(f"to_cvu: {cvu}")
        print(balance_send_new)
        if balance_send != balance_send_new:
                            resta= balance_send - balance_send_new
                            print(f" se resto {resta} de la cuenta {email}")
                            time.sleep(30)
                            trx = Query_db.transaction_trx(cvu)
                            estado = get_transactions(token,trx)
                            body_estado = estado.json()
                            print(body_estado)
                            response =body_estado["trx_status"]
                            self.assertEqual(response, "done", "No se acepto la transferencia automatica")
                                    
                            balance_in_new = Query_db.get_balance_to_cvu(cvu)
                            print(f"Saldo final user credit: {balance_in_new}")
                            resta_debit = Decimal(balance_send) - Decimal(ammount)
                            suma_credit = Decimal(balance_in) + Decimal(ammount)
                            print(float(suma_credit))
                            self.assertEqual(float(resta_debit), float(balance_send_new), "No se desconto la plata de la cuenta debit")
                            self.assertEqual(float(suma_credit), float(balance_in_new), "No impacto el dinero en la cuenta credit")
                            if balance_in != balance_in_new:
                                print(f"""
                                        - inicio balance de cuenta credit: {balance_in} \n
                                        - impacto de balance actualizado cuenta credit: {balance_in_new} \n
                                        - status transfer: {response}""")
                    
        else:
            print("NO se resto el monto enviado de la cuenta origen")



    def test_trasfer_in_cbu_to_onda(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        datos_cbu =cbu_random()

        cbu = datos_cbu["cbu"]
        alias = datos_cbu["alias"]
        titular = datos_cbu["titular"]
        cuil = datos_cbu["cuil"]
        body = {
                "content": {
                    "operacion": {
                            
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
        amount = 30.45
        request_mock = mock_arg_cuentas(coelsa_id,cbu,amount)
        self.assertEqual(request_mock.status_code, 200)
        print(request_mock)
        balance_credit = get_balance(token)
        body_balance = balance_credit.json()
        print(body_balance)
        total_balance = body_balance["balance"]["total_balance"]
        print(total_balance)
        #suma = Decimal(balance_old) + Decimal(amount)
        #self.assertEqual(float(suma),total_balance, "No se impacto la plata en la cuenta credit")


    def test_trasfer_in_cvu_to_onda(self):
        login_data = login_in()
        token = login_data["token"]
        email= login_data["email"]
        cvu_data = cvu_random()

        cvu = cvu_data["cvu"]
        titular = cvu_data["titular"]
        cuil = cvu_data["cuil"]

        body = {
                "content": {
                    "operacion": {
                          
                        "vendedor": {
                            "cuentaVirtual": {
                            "titular": f"{titular}",
                            "cuit": f"{cuil}",
                            "cvu": f"{cvu}",
                            "psp": "1"
                        },
                        "titular": "Mercado libre",
                        "cuit": "20111111112",
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
                        "estado": {
                            "codigo": "PENDIENTE"
                        },
                        "garantiaOk": True,
                        "tipo": "TRANSFERENCIA"
                    },
                    "preautorizado": True
                }
        }
        https_mocks = os.getenv('DEV')
        request = requests.post(https_mocks,json=body)
        body_request = request.json()
        coelsa_id = body_request["coelsa_id"]
        print(coelsa_id)
        balance_old = Query_db.get_balance_to_email(email)
        amount = 110.55
        request_mock = mock_arg_cuentas(coelsa_id,cvu,amount)
        self.assertEqual(request_mock.status_code, 200)
        print(request_mock)
        balance_credit = get_balance(token)
        body_balance = balance_credit.json()
        print(body_balance)
        total_balance = body_balance["balance"]["total_balance"]
        suma = Decimal(balance_old) + Decimal(amount)
        self.assertEqual(float(suma),float(total_balance), "No se impacto la plata en la cuenta credit")

        



                    
                        


                
                
     