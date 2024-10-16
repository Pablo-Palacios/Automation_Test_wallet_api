import json
from api_back.mc_automation_qa.pruebas_v2.configuracion.views_persona import login, Endpoints
from api_back.mc_automation_qa.pruebas_v2.configuracion.main import password
import os
import requests


https =('HTTPS_DEV')

def login_in():
        email_ = "*******"
        password_ = "*******"
        #print(f"ultimo email: {email}")
        request_login = login(email_, password_)

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
                dic = {"token":token, "alias":alias, "cvu": cvu,"email":email_,"cuil":cuil,"name":name}

        return dic

def transfer_external_send_cvu(token,cvu, ammount):
    headers = {"x-authorization":token}
    body_transfer = {
        
        "to_type": "number",
        "to_account": f"{cvu}", 
        "amount":f"{ammount}", 
        "concept": "test",
        "description":"qa"
    }

    request_transfer = requests.post(https + Endpoints.transfer_external_send_post, headers=headers, json=body_transfer)
    return request_transfer

if __name__ == "__main__":
    import sys
    token = sys.argv[1]
    cvu = sys.argv[2]
    amount = sys.argv[3]
    response = transfer_external_send_cvu(token, cvu, amount)
    
    result = response.json()
    print(json.dumps(result, indent=4))

    