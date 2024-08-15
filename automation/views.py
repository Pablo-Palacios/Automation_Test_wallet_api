import requests
from faker import Faker
from dotenv import load_dotenv
import os

load_dotenv()

faker = Faker()
first = faker.first_name()

https = os.getenv('HTTPS_DEV')


class Endpoints:
    pin_get = "/pin/get"
    login_post = "/auth/login"
    onboarding_validate_post = "/onboarding/validate"
    create_user_post = "/auth/create-user"
    biometrics_post = "/auth/biometrics"
    search_user_onda_post = "/account/search-user-onda"
    balance_post = "/account/get-balance"
    update_balance_post = "/account/update-balance"
    validate_cuit_post = "/auth/validate-cuil"
    search_coelsa_post = "/account/search-user-coelsa"
    get_profile_post = "/profile/get-profile"
    p2p_send_post = "/p2p/p2p-send"
    get_transactions_post= "/transactions/get-transaction"
    get_all_transactions_post = "/transactions/get-all-transactions"
    change_alias_post = "/profile/change-alias"
    transfer_external_send_post = "/transfer/send"
    password_restore_post = "/password/restore"





### BODYS REQUEST ###


#                                  ------------------------ PIN ---------------------------------

def pin(token):
    headers = {"x-authorization":token}
    request_pin = requests.post(https + Endpoints.pin_get, headers=headers)
    return request_pin


#                                 --------------------------- AUTH ----------------------------------


def login(email,password):
    body_login = {
                    "account": {
                        "type": "person"
                    },
                    "element": {
                        "email": f"{email}",
                        "password": f"{password}",
                        "deviceTag": "",
                        "deviceModel": "mobile",
                        "coordinates": "-31.392779639214137,-64.18016506749302",
                        #"device_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxL3PF598EoLebXsJcanoo4f6iaRAWujtZ2qU5z5kHZ5hMY4oOi9xoO5Uwja/QOrzOhoMVgcFVzGOgxL2skauenGBuity8TT8N10wVHX/0DRKHy6e/p3VMPFgSFPKtwqZNRjF8i9s0WT+7zw5/25VaBi3orhK0IPW+HnIyk4ghLAYPSEGkixkxzSQ3jyzCTOObPoU5AwCdvbui8VVLuUwCjsDo4UG2ZCiuGhLDh1iL2Jpae5kGiaXqbaUsQr2QmVNSc5k32eWKJhrFuRpS36aKglE2hkARtYojQHH60/UZrACs5tSSEMHjLPutYzhXj6S2REya691TcpeVZzlLixxywIDAQAB"
                    }
                }
    
    request_login = requests.post(https + Endpoints.login_post, json=body_login)

    return request_login


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
        "code": False
    }

    request = requests.post(https + Endpoints.onboarding_validate_post, json=body)
    return request

def biometric_validate_frist_step(device_id,cuil,base_64):
    body = {
        
        "validator": "biometric",
        "step": 1,
        "device_id": f"{device_id}",
        "cuil": f"{cuil}",
        "name": "Connect_Verify_Document_Face_Passive_Liveness",
        "version": 2,
        "input": {
            "captureMethod": "Mobile",
            "croppingMode": "None",
            "countryCode": "ARG",
            "frontWhiteImage": f"{base_64}"
            }
    }

    request = requests.post(https + Endpoints.onboarding_validate_post, json=body)
    return request.json()

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



def create_user(email,password,cuit,phone_number, device_models,hashs): 
    body_create_user = {
                            "account": {
                                "type": "person"
                            },
                            "element": {
                                "hash":f"{hashs}",
                                "users": {
                                    "email": f"{email}",
                                    "password": f"{password}",
                                    "userType": "persona",
                                    "documentNumber": 41809969,
                                    "cuil": f"{cuit}",
                                    "gender": "M",
                                    "firstName": f"{first}",
                                    "lastName": "test dev",
                                    "birthDate": "1984-11-04",
                                    "phoneNumber": f"{phone_number}",
                                    "occupation": "developer",
                                    "marital": "",
                                    "condition": "approved"
                                },
                                # "terms": {
                                #     "type": "current",
                                #     "entry": "Cualquier persona que no acepte estos Términos y Condiciones, los cuales tienen carácter obligatorio y vinculante, no podrá acceder a la Plataforma y utilizar los Servicios",
                                #     "userType": 0,
                                #     "updatedBy": 0
                                # },
                                "devices": {
                                    # "device_tag": "D9D2678A-E372-42F0-AE1D-835F5DD3A444",
                                    "deviceTag": "",
                                    "deviceModel": f"{device_models}",
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
    return request_balance



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





def p2p_send(token,to_email):
    headers = {"x-authorization":token}
    send_p2p = {
            "account": {
                "type": "person"
            },
            "element": {
                "to_email": f"{to_email}",
                "amount": 10.55,
                "reference": "test p2p",
                "concept": 1
            }
        }

    resp_send = requests.post("https://endpoint.dev.siempreondav2.com/v2/p2p/p2p-send", headers=headers,json=send_p2p)
    return resp_send.json()


    
def get_transactions(token,trx):
    headers = {"x-authorization":token}
    body_p2p_send = {
    "account": {
        "type": "person"
    },
    "element": {
        "trx_reference": f"{trx}"
    }
    }
    
    request_p2p_send = requests.post(https + Endpoints.get_transactions_post, headers=headers,json=body_p2p_send)
    return request_p2p_send


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
        "concept": "test",
        "description":"dev"
    }

    request_transfer = requests.post(https + Endpoints.transfer_external_send_post, headers=headers, json=body_transfer)
    return request_transfer

def transfer_external_send_alias(token,alias,ammount):
    headers = {"x-authorization":token}
    body_transfer = {
        
        "to_type": "alias",
        "to_account": f"{alias}", 
        "amount":f"{ammount}", 
        "concept": "test",
        "description":"dev"
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



def mock_arg_cuentas(id,cbu,amount):
    body =  {
    "operacionCVU":{
        "tipo":"TRANSFERENCIA",
        "id":f"{id}",
        "cbu": f"{cbu}",
        "importe":f"{amount}",
        "cvu":"0000001700000002002714",
        "cuit_cvu":"20760345351",
        "fecha_negocio":"2024-08-05",
        "titular_cvu":"Daniel test dev",
        "moneda":"032"
        }
    }
    
    request = requests.post("https://plug.dev.siempreondav2.com/coelsa-endpoint/server/debin/AvisoCVU", json=body)
    return request