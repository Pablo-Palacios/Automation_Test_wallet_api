import requests
from faker import Faker
import os
from configuracion.views_persona import login


faker = Faker()
first = faker.first_name()

https = ('HTTPS_DEV')


class Endpoints:

        # Commerce Branches CRUD
    COMMERCE_BRANCH_CREATE = "**********"
    COMMERCE_BRANCH_DETAIL ="**********"
    COMMERCE_BRANCH_LIST = "**********"
    COMMERCE_BRANCH_UPDATE ="**********"
    COMMERCE_BRANCH_DELETE = "**********"

    # Commerce checkout CRUD
    COMMERCE_CHECKOUT_CREATE = "**********"
    COMMERCE_CHECKOUT_DETAIL = "**********"
    COMMERCE_CHECKOUT_LIST ="**********"
    COMMERCE_CHECKOUT_UPDATE = "**********"
    COMMERCE_CHECKOUT_DELETE = "**********"

    # Commerce representative CRUD
    COMMERCE_representative_CREATE = "**********"
    COMMERCE_representative_DETAIL = "**********"
    COMMERCE_representative_LIST ="**********"
    COMMERCE_representative_UPDATE ="**********"
    COMMERCE_representative_DELETE = "**********"

    
    pin_get = "**********"
    login_post = "**********"
    login_v1_post = "**********"
    onboarding_validate_post = "**********"
    create_user_post = "**********"
    biometrics_post = "**********"
    search_user_onda_post = "**********"
    balance_post = "**********"
    update_balance_post = "**********"
    validate_cuit_post = "**********"
    search_coelsa_post = "**********"
    get_profile_post = "**********"
    p2p_send_post = "**********"
    get_transactions_post= "**********"
    get_all_transactions_post = "**********"
    change_alias_post = "**********"
    transfer_external_send_post = "**********"
    password_restore_post = "**********"
    password_change_post = "**********"
    otp_password_restore = "**********"
    paid_balance_status_get = "**********"
    paid_balance_activate_post ="**********"
    paid_balance_deactivate_post = "**********"
    get_balance_banking_post = "**********"
    product_offers_post = "**********"
    get_capital_post = "**********"
    simulate_offers_post = "**********"
    installment_plan_post ="**********"
    contract_loans_channels_post ="**********"
    transaction_status_post = "**********"
    cash_out_business_post = "**********"
    get_cbu_banking ="**********"
    post_cbu_banking ="**********"
    delete_cbu_banking ="**********"
    desactivate_cbu_banking = "**********"
    activate_cbu_banking = "**********"
    suspend_patch = "**********"
    delete_patch = "**********"



### BODYS REQUEST ###


#                       ------------------------ PIN ---------------------------------

def pin(token):
    headers = {"x-authorization":token}
    request_pin = requests.post(https + Endpoints.pin_get, headers=headers)
    return request_pin


#                                 --------------------------- AUTH ----------------------------------


def login_comercio(cuit,email,password,device_id):
    body_login = {
        "account": {
            "type": "person"
        },
        "element": {
            "cuit": f"{cuit}",
            "email": f"{email}",
            "password":f"{password}",
            "deviceTag": f"{device_id}",
            "deviceModel": "MARIODEVICE",
            "coordinates": "-31.392779639214137,-64.18016506749302"
            }
        }
    
    request_login = requests.post(https + Endpoints.login_post, json=body_login)

    return request_login


def login_comercio_otp(cuit,email,password,device_id,code):
    param = {"code":code,"channel":"email"}
    body_login = {
        "account": {
            "type": "person"
        },
        "element": {
            "cuit": f"{cuit}",
            "email": f"{email}",
            "password":f"{password}",
            "deviceTag": f"{device_id}",
            "deviceModel": "MARIODEVICE",
            "coordinates": "-31.392779639214137,-64.18016506749302"
            }
        }
    
    request_login = requests.post(https + Endpoints.login_post, params=param,json=body_login)

    return request_login

def validate_commerce(name_commerce,cuit,phone,document,name,last_name,email,password):
    body = {
    "commerce": {
        "commercial_name": f"{name_commerce}",
        "society_type_id": 5,
        "category_id": 1,
        "commercial_profile": "professional",
        "gross_income_id": 9,
        "tax_status_id": 1,
        "cuit": cuit,
        "commercial_activity_afip": "9700",
        "owner_phone_number": phone,
        "owner_document_number": f"{document}",
        "owner_name": f"{name}",
        "owner_last_name": f"{last_name}"
    },
    "user": {
        "migrated_user": "v2",
        "email" : f"{email}",
        "password" : f"{password}",
        "user_type_id" : 1,
        "user_condition_id" : 1
    }
    }

    request = requests.post(https + Endpoints.commercial_validate_post,json=body)
    return request

def confirm_commerce(token,cuit):
    headers = {"x-authorization":token}
    body = {
        "cuit":f"{cuit}"
    }
    request = requests.post(https + Endpoints.commerce_confirm, headers=headers,json=body)
    return request

def confirm_commerce_otp(token,cuit,code):
    headers = {"x-authorization":token}
    param = {"code":code, "channel":"email"}
    body = {
        "cuit":f"{cuit}"
    }
    request = requests.post(https + Endpoints.commerce_confirm, params=param,headers=headers,json=body)
    return request

def create_commerce_pf(token,name_commerce):
    headers = {"x-authorization":token}
    body = {
        "commercial_name": f"{name_commerce}",
        "society_type_id": 5,
        "category_id": 1,
        "commercial_profile": "professional",
        "gross_income_id": 9,
        "tax_status_id": 1,
        "commercial_activity_afip": "9700"
    }
    
    request = requests.post(https + Endpoints.create_commerce,headers=headers,json=body)
    return request
        


def onboarding_validate_send_email(device_id,email):
    body = {
        "device_id": f"{device_id}",
        "device_name": "model test",
        "coordinates": "-31.392779639214137,-64.18016506749302",
        "validator": "email",
        "address": f"{email}",
        "code": None
    }

    request = requests.post(https + Endpoints.onboarding_validate_post, json=body)
    return request

def onboarding_validate_code_otp_email(device_id,email,code):
    body = {
        "device_id": f"{device_id}",
        "device_name": "model test",
        "coordinates": "-31.392779639214137,-64.18016506749302",
        "validator": "email",
        "address": f"{email}",
        "code": f"{code}"
    }

    request = requests.post(https + Endpoints.onboarding_validate_post, json=body)
    return request

def onboarding_validate_send_sms(device_id,phone_number):
    body = {
        "device_id": f"{device_id}",
        "device_name": "model test",
        "coordinates": "-31.392779639214137,-64.18016506749302",
        "validator": "sms",
        "address": f"{phone_number}",
        "code": None
    }

    request = requests.post(https + Endpoints.onboarding_validate_post, json=body)
    return request

def onboarding_validate_code_otp_sms(device_id,phone_number,code):
    body = {
        "device_id": f"{device_id}",
        "device_name": "model test",
        "coordinates": "-31.392779639214137,-64.18016506749302",
        "validator": "sms",
        "address": f"{phone_number}",
        "code": f"{code}"
    }

    request = requests.post(https + Endpoints.onboarding_validate_post, json=body)
    return request

def onboarding_validate_cuil(device_id,cuil):
    body = {
        "device_id": f"{device_id}",
        "device_name": "model test",
        "coordinates": "-31.392779639214137,-64.18016506749302",
        "validator": "cuil",
        "address": f"{cuil}",
        "code": None
    }

    request = requests.post(https + Endpoints.onboarding_validate_post, json=body)
    return request

def biometric_validate_frist_step(device_id,cuil,base64):
    body = {
        
        "validator":"biometric",
        "step": 1,
        "device_id": f"{device_id}",
        "cuil": f"{cuil}",
        "name": "Connect_Verify_Document_Face_Passive_Liveness",
        "version": 2,
        "input": {
            "captureMethod": "Mobile",
            "croppingMode": "None",
            "countryCode": "ARG",
            "frontWhiteImage": f"{base64}"
            }
    }

    request = requests.post(https + Endpoints.onboarding_validate_post, json=body)
    return request

def biometric_validate_second_step(device_id,base_64):
    body = {
        
        "validator": "biometric",
        "step": 2,
        "device_id": f"{device_id}",          
        "name": "Connect_Verify_Document_Face_Passive_Liveness",
        "input": {
            "backWhiteImage":f"{base_64}"
            
        }
    }

    request = requests.post(https + Endpoints.onboarding_validate_post, json=body)
    return request.json()

def biometric_validate_third_step(device_id,base_64):
    body = { 
        
        "validator": "biometric",
        "step": 3,
        "device_id": f"{device_id}",
        "name": "Connect_Verify_Document_Face_Passive_Liveness",
        "input": {
            "face":f"{base_64}"
        }
    }

    request = requests.post(https + Endpoints.onboarding_validate_post, json=body)
    return request.json()



def create_user(email,name, last_name, password,cuil,dni,device_id,phone_number,hashs): 
    body_create_user = {
        "account": {
            "type": "person"
        },
        "element": {
            "users": {
                "hash":f"{hashs}",
                "email": f"{email}",
                "password": f"{password}",
                "userType": "persona",
                "documentNumber": f"{dni}",
                "cuil": f"{cuil}",
                "gender": "M",
                "firstName": f"{name}",
                "lastName": f"{last_name}",
                "birthDate": "1984-11-04",
                "phoneNumber": f"{phone_number}",
                "occupation": "developer",
                "marital": "",
                "condition": "approved"
            },
            "devices": {
                "deviceTag": f"{device_id}",
                "deviceModel": "IPhone 15 Pro",
                "deviceLocation": "-37.785834:-122.406417"
            },
            "addresses": {
                "type": "physical",
                "address": "av.siempre viva",
                "addressNumber": 742,
                "apartment": "9B",
                "city": "CORDOBA CAPITAL",
                "province": "CORDOBA",
                "country": "ARG"
            }
        }
    }
    request_create_user = requests.post(https + Endpoints.create_user_post, json=body_create_user)
    return request_create_user


def biometrics(email, deviceTag):
    body_biometrics = {
        "account": {
            "type": "person"
        },
        "element": {
            "email": f"{email}",
            "deviceTag": f"{deviceTag}",
            "device_verified": {
                "user": "AAABBBCCC"
                }
        }
    }

    request_biometric = requests.post(https + Endpoints.biometrics_post, json=body_biometrics)
    return request_biometric

def validate_cuit(cuit):

    body_validate_cuit = {
                
            "account": {
                "type": "person"
            },
            "element":{
                "cuil": f"{cuit}"
            }
    }

    request_validate_cuit = requests.post(https + Endpoints.validate_cuit_post, json=body_validate_cuit)
    return request_validate_cuit



#                                 --------------------------- ACCOUNT ----------------------------------


def search_user_onda_email(token,email):
    headers = {"x-authorization":token}
    body_search_user = {
        "account": {
            "type": "person"
        },
        "element": {
            "email": f"{email}",
            "phoneNumber": ""
        }
    }

    request_search = requests.post(https + Endpoints.search_user_onda_post, headers=headers,json=body_search_user)
    return request_search

def search_user_onda_phone(token,phone):
    headers = {"x-authorization":token}
    body_search_user = {
        "account": {
            "type": "person"
        },
        "element": {
            "phoneNumber": f"{phone}"
        }
    }

    request_search = requests.post(https + Endpoints.search_user_onda_post, headers=headers,json=body_search_user)
    return request_search

def get_balance(token):
    headers = {"x-authorization":token}
    
    request_balance = requests.get(https + Endpoints.balance_post, headers=headers)
    return request_balance.json()



def search_user_coelsa_with_cvu(token,cvu):
        headers = {"x-authorization":token}
        body_search_coelsa_cvu = {
        "account": {
            "type": "person"
        },
        "element": {
            "cvu": f"{cvu}"
        }
        }

        request_search_cvu = requests.post(https + Endpoints.search_coelsa_post, headers=headers,json=body_search_coelsa_cvu)
        return request_search_cvu

def search_user_coelsa_with_alias(token,alias):
        headers = {"x-authorization":token}
        body_search_coelsa_alias = {
        "account": {
            "type": "person"
        },
        "element": {
            "alias": f"{alias}"
        }
        }

        request_search_alias = requests.post(https + Endpoints.search_coelsa_post, headers=headers,json=body_search_coelsa_alias)
        return request_search_alias


def get_profile(token):
    headers = {"x-authorization":token}

    request_get_profile = requests.get(https + Endpoints.get_profile_post, headers=headers)
    return request_get_profile





def p2p_send(token,to_email,amount):
    headers = {"x-authorization":token}
    send_p2p = {
            
            
                "email": f"{to_email}",
                "amount": f"{amount}",
                "reference": "test p2p",
                "conceptId": 1
            
        }

    resp_send = requests.post(https + Endpoints.p2p_send_post, headers=headers,json=send_p2p)
    return resp_send.json()

def p2p_send_01(token,to_email):
    headers = {"x-authorization":token}
    send_p2p = {
            "account": {
                "type": "person"
            },
            "element": {
                "to_email": f"{to_email}",
                "amount": 0.01,
                "reference": "test p2p",
                "concept": 1
            }
        }

    resp_send = requests.post(https + Endpoints.p2p_send_post, headers=headers,json=send_p2p)
    return resp_send


    
def get_transactions(token,trx):
    params = {"id":trx}
    headers = {"x-authorization":token}
   
    
    request_ = requests.get(https + Endpoints.get_transactions_post, params=params,headers=headers)
    return request_


def get_all_transactions(token):
    headers = {"x-authorization":token}
    
    request_all_transac = requests.get(https + Endpoints.get_all_transactions_post, headers=headers)
    return request_all_transac


def change_alias(token,email,new_alias):
    headers = {"x-authorization":token}
    body_change = {
    "account": {
        "type": "person"
    },
    "element": {
        "email": f"{email}",
        "new_alias": f"{new_alias}"
    }
    }

    request_change = requests.post(https + Endpoints.change_alias_post, headers=headers, json=body_change)
    return request_change


def transfer_external_send_cvu(token,cvu,ammount):
    headers = {"x-authorization":token}
    body_transfer = {
        
        "to_type": "number", 
        "to_account": f"{cvu}", 
        "amount":f"{ammount}", 
        "reference": "test",
        "conceptId": 1
        #"description":"dev",
        
    }

    request_transfer = requests.post(https + Endpoints.transfer_external_send_post, headers=headers, json=body_transfer)
    return request_transfer

def transfer_external_send_alias(token,alias,ammount):
    headers = {"x-authorization":token}
    body_transfer = {
        
        "to_type": "alias", 
        "to_account": f"{alias}", 
        "amount":f"{ammount}", 
        "reference": "test",
        "conceptId": 1
    }

    request_transfer = requests.post(https + Endpoints.transfer_external_send_post, headers=headers, json=body_transfer)
    return request_transfer

def restore_password_send_code_email(email):
    body_send_password = {
        "deviceId": "835F5DD3A4042F0-AE1D",
        "deviceName": "",
        "coordinates": "coordinates",
        "validator": "email",
        "address": f"{email}"
    }

    request = requests.post(https + Endpoints.password_restore_post, json=body_send_password)
    return request

def restore_password_email(email, code, newpassword, confirmpassword):
    body_send_password = {
        "deviceId": "835F5DD3A4042F0-AE1D",
        "deviceName": "",
        "coordinates": "coordinates",
        "validator": "email",
        "address": f"{email}",
        "code": f"{code}",
        "newPassword": f"{newpassword}",
        "confirmNewPassword": f"{confirmpassword}"
    }

    request = requests.post(https + Endpoints.password_restore_post, json=body_send_password)
    return request



def mock_arg_cuentas(id,cbu,amount,cvu,cuit_cvu,name):
    body =  {
    "operacionCVU":{
        "tipo":"TRANSFERENCIA",
        "id":f"{id}",
        "cbu": f"{cbu}",
        "importe":f"{amount}",
        "cvu":f"{cvu}",
        "cuit_cvu":f"{cuit_cvu}",
        "fecha_negocio":"2024-08-05",
        "titular_cvu":f"{name}",
        "moneda":"032"
        }
    }
    
    request = requests.post("https://plug.dev.siempreondav2.com/coelsa-endpoint/server/debin/AvisoCVU", json=body)
    return request


def paid_balance_status(token):
    headers = {"x-authorization":token}
    request = requests.get(https + Endpoints.paid_balance_status_get, headers=headers)
    return request


def paid_balance_activate(token):
    headers = {"x-authorization":token}
    request = requests.post(https + Endpoints.paid_balance_activate_post, headers=headers)
    return request


def paid_balance_deativate(token):
    headers = {"x-authorization":token}
    request = requests.post(https + Endpoints.paid_balance_deactivate_post, headers=headers)
    return request


    
def get_balance_banking(token):
    headers = {"x-authorization":token}
    body_balance = {
        "cbu":"3150100602001528630014"
    }
    request = requests.post(https + Endpoints.get_balance_banking_post, headers=headers, json=body_balance)
    return request

def product_offers_banking(token,productId):
    headers = {"x-authorization":token}
    body= {
        "productId":f"{productId}"
    }
    request = requests.post(https + Endpoints.product_offers_post, headers=headers, json=body)
    return request
    
def get_capital_banking(token,productUid):
    headers = {"x-authorization":token}
    body = {
        "productUid": f"{productUid}"
    }
    request = requests.post(https + Endpoints.get_capital_post, headers=headers, json=body)
    return request

def simulate_offers_banking(token,accountUid,productUid,amount):
    headers = {"x-authorization":token}
    body = {
        "accountUid": f"{accountUid}",
        "productUid": f"{productUid}",
        "amount": f"{amount}",
        "installmentPeriod": "30"
    }
    request = requests.post(https + Endpoints.simulate_offers_post, headers=headers, json=body)
    return request

def installment_plan_banking(token,accountUid,simulateUid,creditDestination,installmentQuantity):
    headers = {"x-authorization":token}
    body={
        "accountUid": f"{accountUid}",
        "simulateUid": f"{simulateUid}",
        "creditDestination": f"{creditDestination}",
        "installmentQuantity": f"{installmentQuantity}"
    }
    request = requests.post(https + Endpoints.installment_plan_post, headers=headers, json=body)
    return request

def contract_loands_channels_banking(token,accountUid,simulateUid,amount,installmentQuantity):
    headers = {"x-authorization":token}
    body={
        "accountUid": f"{accountUid}",
        "simulateUid": f"{simulateUid}",
        "amount": f"{amount}",
        "installmentQuantity": f"{installmentQuantity}",
        "insurance": "S"
    }
    request = requests.post(https + Endpoints.contract_loans_channels_post, headers=headers, json=body)
    return request

def transaction_status_banking(token, idTransaction):
    headers = {"x-authorization":token}
    body={
        "idTransaction": f"{idTransaction}"
    }
    request = requests.post(https + Endpoints.transaction_status_post, headers=headers, json=body)
    return request

def cash_out_business_banking(token,amount):
    headers = {"x-authorization":token}
    body={
        "amount": f"{amount}",
        "code": "1"
    }
    request = requests.post(https + Endpoints.cash_out_business_post, headers=headers, json=body)
    return request



def login_in_whit_email(email,password,device):
        
        login_user = login(email, password,device)
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

                dic = {"token":token, "alias":alias, "cvu": cvu,"email":email,"cuil":cuil,"name":name}

        return dic


def login_in_whit_email_comercio(cuit,email,password,device):
        
        login_user = login_comercio(cuit,email, password,device)
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

                dic = {"token":token, "alias":alias, "cvu": cvu,"email":email,"cuil":cuil,"name":name}

        return dic




def representative_create(token,rol,representative_type,email,password,phone,dni,name,last_name):
    headers = {"x-authorization":f"{token}"}
    body = {
        
        "role":rol, 
        "representative_type": f"{representative_type}",
        "user_email": f"{email}",
        "user_password": f"{password}",
        "phone_number": phone,
        "document_number": dni,
        "name":f"{name}",
        "last_name":f"{last_name}"
    }
        
   
    request_ = requests.post(https + Endpoints.COMMERCE_representative_CREATE, headers=headers,json=body)
    return request_


def branch_create(token,branch_name):
    body = {
        
        "branch_name": f"{branch_name}",
        
        
    }

    headers = {"x-authorization":f"{token}"}
   
    request_ = requests.post(https + Endpoints.COMMERCE_BRANCH_CREATE, headers=headers,json=body)
    return request_
    

def checkout_create(token,checkout_name,branch_id):
    
    body = {
        "checkout_name": f"{checkout_name}",
        "branch_id": f"{branch_id}"
       
    }

    headers = {"x-authorization":f"{token}"}
   
    request_ = requests.post(https + Endpoints.COMMERCE_CHECKOUT_CREATE, headers=headers,json=body)
    return request_
    







def representative_detail(token,id):
    params = {"id":f"{id}"}
    headers = {"x-authorization":f"{token}"}
    
    request_ = requests.get(https + Endpoints.COMMERCE_representative_DETAIL, params=params,headers=headers)
    return request_


def branch_detail(token,id):
    params = {"id":f"{id}"}
    headers = {"x-authorization":f"{token}"}
   
    
    request_ = requests.get(https + Endpoints.COMMERCE_BRANCH_DETAIL, params=params,headers=headers)
    return request_
    

def checkout_detail(token,id):
    params = {"id":f"{id}"}
    headers = {"x-authorization":f"{token}"}
   
    
    request_ = requests.get(https + Endpoints.COMMERCE_CHECKOUT_DETAIL, params=params,headers=headers)
    return request_








def representative_list(token):
    headers = {"x-authorization":f"{token}"}
   
    
    request_ = requests.get(https + Endpoints.COMMERCE_representative_LIST,headers=headers)
    return request_


def branch_list(token):
    headers = {"x-authorization":f"{token}"}
   
    request_ = requests.get(https + Endpoints.COMMERCE_BRANCH_LIST,headers=headers)
    return request_
    

def checkout_list(token):
    headers = {"x-authorization":f"{token}"}
    
    request_ = requests.get(https + Endpoints.COMMERCE_CHECKOUT_LIST,headers=headers)
    return request_






def representative_update(token,repre_id,new_rol,new_representative_type):
    headers = {"x-authorization":f"{token}"}
    body={
        "representative_id": f"{repre_id}",
        "representative_type": f"{new_representative_type}",
        "role": f"{new_rol}"
    }
    
    request_ = requests.put(https + Endpoints.COMMERCE_representative_UPDATE,headers=headers,json=body)
    return request_


def branch_update(token,id,branch_name_new):
    headers = {"x-authorization":f"{token}"}
    body={
        "branch_id":f"{id}",
        "branch_name": f"{branch_name_new}"
        
    }
    
    request_ = requests.put(https + Endpoints.COMMERCE_BRANCH_UPDATE,headers=headers,json=body)
    return request_
    

def checkout_update(token,checkout_name_new,checkout_id,branch_id):
    
    headers = {"x-authorization":f"{token}"}
    body={
        "checkout_name": f"{checkout_name_new}",
        "checkout_id":f"{checkout_id}",
        "branch_id":f"{branch_id}"
    }
    
    
    request_ = requests.put(https + Endpoints.COMMERCE_CHECKOUT_UPDATE,headers=headers,json=body)
    return request_
    





def representative_delete(token,repre_id):
    headers = {"x-authorization":f"{token}"}
    body={
        "representative_id": f"{repre_id}",
    }
   
    
    request_ = requests.delete(https + Endpoints.COMMERCE_representative_DELETE,headers=headers,json=body)
    return request_



def branch_delete(token,id):
    headers = {"x-authorization":f"{token}"} 
    body={
        "branch_id":f"{id}"
        }
    
    request_ = requests.delete(https + Endpoints.COMMERCE_BRANCH_DELETE,headers=headers,json=body)
    return request_
    

def checkout_delete(token,che_id,branch_id):
    headers = {"x-authorization":f"{token}"}
    body={
        "branch_id":f"{branch_id}",
        "checkout_id":f"{che_id}"
        }
   
    
    request_ = requests.delete(https + Endpoints.COMMERCE_CHECKOUT_DELETE,headers=headers,json=body)
    return request_



    