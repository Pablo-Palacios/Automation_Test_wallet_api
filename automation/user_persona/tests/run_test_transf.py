import subprocess
from api_back.mc_automation_qa.pruebas_v2.configuracion.views_persona import login
from api_back.mc_automation_qa.pruebas_v2.configuracion.lib import cbu_random
password = "Pablo123"

def login_in():
        email_ = '**********'
        password_ = "******"
        device = ""
        login_user = login(email_, password_,device)
        response_login = login_user.json()
        #print(response_login)
        
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

def run_transf(token, cvu,amount):
    return subprocess.Popen(
        ['python3', 'transf.py', token, cvu, str(amount)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
def main():
    user = login_in()
    token = user["token"]

    cvu_1 = "0070138530004027543365"
    cvu_2 = "0070138530004027543365"

    amount = 200

    # Lanzar ambas transferencias simultáneamente
    transfer1 = run_transf(token, cvu_1, amount)
    transfer2 = run_transf(token, cvu_2, amount)

    # Capturar los resultados
    stdout1, stderr1 = transfer1.communicate()
    stdout2, stderr2 = transfer2.communicate()

    # Mostrar resultados
    if transfer1.returncode == 0:
        print("Transfer 1 result:", stdout1.decode())
    else:
        print("Error in Transfer 1:", stderr1.decode())

    if transfer2.returncode == 0:
        print("Transfer 2 result:", stdout2.decode())
    else:
        print("Error in Transfer 2:", stderr2.decode())

if __name__ == "__main__":
    main()


