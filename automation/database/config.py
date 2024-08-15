import psycopg2
from faker import Faker
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

# Confi database 
class Query_db:
        
        host = os.getenv('HOST_DEV')
        database = os.getenv('DATABASE')
        user = os.getenv('USER')
        password = os.getenv('PASSWORD')

        conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password
                )
        
        
        def get_especific_email(email):

                        cursor = Query_db.conn.cursor()
                        # Ejecutar la consulta para obtener los valores del campo 'email' en la tabla 'users'
                        cursor.execute(f"""SELECT email 
                                FROM "walletClients".users
                                WHERE email = '{email}';""")

                        # Obtener todos los resultados
                        result = cursor.fetchone()
                        cursor.close()


                        # Imprimir los valores del campo 'email'
                        return result[0]

        def get_last_email_logeado():

                        cursor = Query_db.conn.cursor()
                        # Ejecutar la consulta para obtener los valores del campo 'email' en la tabla 'users'
                        cursor.execute(f"""SELECT email 
                                FROM "walletClients".users;""")

                        # Obtener todos los resultados
                        result = cursor.fetchall()
                        if result:
                                last_email = result[-1][0]
                        cursor.close()


                        # Imprimir los valores del campo 'email'
                        return last_email if result else None

        def get_last_email_client():

                        cursor = Query_db.conn.cursor()
                        # Ejecutar la consulta para obtener los valores del campo 'email' en la tabla 'users'
                        cursor.execute(f"""SELECT u.email
                                        FROM "walletClients".users u
                                        INNER JOIN "walletClients".clients c ON u.user_id = c.user_id
                                        WHERE c.client_id = (SELECT MAX(client_id) FROM "walletClients".clients);""")

                        # Obtener todos los resultados
                        result = cursor.fetchone()
                        
                        cursor.close()


                        # Imprimir los valores del campo 'email'
                        return result[0] 
        
        def get_last_otp_code():
                        cursor = Query_db.conn.cursor()

                        cursor.execute(f"""SELECT code FROM "walletClients".validate_users;""")

                        resul = cursor.fetchall()
                        if resul:
                                last_value = resul[-1][0]

                        cursor.close()
                        return last_value if resul else None
                
        def get_emailCode(email):
                        cursor = Query_db.conn.cursor()

                        cursor.execute(f"""SELECT code FROM "walletClients".email_register
                                       WHERE email = '{email}';""")

                        result = cursor.fetchone()

                        cursor.close()
                        
                        return result[0]
        
        def get_phoneCode(id_number):
                        cursor = Query_db.conn.cursor()

                        cursor.execute(f"""SELECT code FROM "walletClients".sms_register
                                       WHERE sms_register_id = '{id_number}';""")

                        result = cursor.fetchone()

                        cursor.close()
                        
                        return result[0]
        
        def get_alias_and_cvu_user_with_email(email):
                        cursor = Query_db.conn.cursor()
       
                        cursor.execute(f""" SELECT c.cvu, c.alias
                                       FROM "walletClients".users AS u
                                       INNER JOIN "walletClients".clients AS c ON c.user_id = u.user_id
                                       WHERE u.email = '{email}';""")
                        result = cursor.fetchone()
                        
                        cursor.close()
                        return result if result else None
                
        def get_last_alias():
                        cursor = Query_db.conn.cursor()
                        cursor.execute(f""" SELECT alias
                                       FROM "walletClients".clients
                                       WHERE client_id = (SELECT MAX(client_id) FROM "walletClients".clients);""")
                        result = cursor.fetchone()
                        
                        cursor.close()
                        return result[0]

        def get_last_cvu():
                        cursor = Query_db.conn.cursor()
                        cursor.execute(f""" SELECT cvu
                                       FROM "walletClients".clients
                                       WHERE client_id = (SELECT MAX(client_id) FROM "walletClients".clients);""")
                        result = cursor.fetchone()
                        
                        cursor.close()
                        return result[0]
                
        def get_cvu_user_with_email(email):
                        cursor = Query_db.conn.cursor()
       
                        cursor.execute(f""" SELECT c.cvu
                                       FROM "walletClients".users AS u
                                       INNER JOIN "walletClients".clients AS c ON c.user_id = u.user_id
                                       WHERE u.email = '{email}';""")
                        result = cursor.fetchone()
                        cursor.close()
                        return result[0] if result else None
        
        def get_alias_user_with_email(email):
                        cursor = Query_db.conn.cursor()
       
                        cursor.execute(f""" SELECT c.alias
                                       FROM "walletClients".users AS u
                                       INNER JOIN "walletClients".clients AS c ON c.user_id = u.user_id
                                       WHERE u.email = '{email}';""")
                        result = cursor.fetchone()
                        cursor.close()
                        return result[0] if result else None

        def get_cvu_with_alias(alias):
                cursor = Query_db.conn.cursor()
                cursor.execute(f""" SELECT cvu
                               FROM "walletClients".clients
                               WHERE alias = '{alias}';""")
                result = cursor.fetchone()
                cursor.close()
                return result[0]
        

        def get_deviceId_to_email(email):
                cursor = Query_db.conn.cursor()
                cursor.execute(f""" 
                               SELECT d.device_tag
                               FROM "walletClients".devices AS d
                               INNER JOIN "walletClients".sessions AS s ON s.device_id = d.device_id 
                               WHERE s.email = '{email}';""")
                

                result = cursor.fetchone()
                cursor.close()
                return result[0] if result else None
        
        def get_balance_to_email(email):
                cursor = Query_db.conn.cursor()
                cursor.execute(f""" SELECT c.cvu
                                       FROM "walletClients".users AS u
                                       INNER JOIN "walletClients".clients AS c ON c.user_id = u.user_id
                                       WHERE u.email = '{email}';""")
                cvu = cursor.fetchone()

                
                cursor.execute(f"""
                                SELECT b.available_balance
                                FROM "walletTransactions".balance_onda AS b
                                INNER JOIN "walletClients".clients AS c ON c.balance_id = b.balance_id 
                                WHERE c.cvu = '{cvu[0]}'
                                """)
                
                result = cursor.fetchone()
                return result[0] if result else None
        
        def get_balance_to_cvu(cvu):
                cursor = Query_db.conn.cursor()
                cursor.execute(f"""
                                SELECT b.available_balance
                                FROM "walletTransactions".balance_onda AS b
                                INNER JOIN "walletClients".clients AS c ON c.balance_id = b.balance_id 
                                WHERE c.cvu = '{cvu}'
                                """)
                
                result = cursor.fetchone()
                return result[0] if result else None
        
        def get_transaction_status(trx):
                cursor = Query_db.conn.cursor()
                cursor.execute(f"""SELECT transaction_status 
                                FROM "walletTransactions".transactions 
                               WHERE transaction_request_id = '{trx}'
                                """)
                result = cursor.fetchone()
                return result[0]
        
        

        def get_last_transaction_trx():
                cursor = Query_db.conn.cursor()
                cursor.execute(f"""SELECT transaction_request_id 
                                FROM "walletTransactions".transactions
                               WHERE transaction_id = (SELECT MAX(transaction_id) FROM "walletTransactions".transactions)
                                """)
                id = cursor.fetchone()
                return id[0] 
        
        def transaction_trx(cvu):
                cursor = Query_db.conn.cursor()
                cursor.execute(f"""SELECT t.transaction_request_id
                               FROM "walletTransactions".transactions AS t
                               INNER JOIN (
                                        SELECT MAX(transaction_id) AS max_transaction_id
                                        FROM "walletTransactions".outbounds
                                        WHERE to_cbu = '{cvu}'
                               ) AS o ON max_transaction_id = t.transaction_id
                                """)
                resul = cursor.fetchone()
                return resul[0]
        
        def p2p_trx():
                cursor = Query_db.conn.cursor()
                cursor.execute(f"""SELECT t.transaction_request_id
                               FROM "walletTransactions".transactions AS t
                               INNER JOIN (
                                        SELECT MAX(transaction_id) AS max_transaction_id
                                        FROM "walletTransactions".p2p_transactions 
                               ) AS o ON max_transaction_id = t.transaction_id
                                """)
                resul = cursor.fetchone()
                return resul[0]
        
        def get_code_email_register(email):
                cursor = Query_db.conn.cursor()
                cursor.execute(f"""SELECT code FROM "walletClients".email_register WHERE email = '{email}'""")
                resul = cursor.fetchone()
                return resul[0]
        
        def data_inbounds(txr):
                cursor = Query_db.conn.cursor()
                cursor.execute(f"""SELECT * FROM FROM "walletTransactions".transactions AS t 
                               INNER JOIN "walletTransactions".inbounds as i ON i.transaction_id = t.transaction_id
                               WHERE i.coelsa_id = '{txr}'
                                """)
        




faker = Faker()
email = 'aguusstefanini@gmail.com'
cvu2 = '0000001700000002002578'
number = '543516619221'
cvu = '0000001700000002002530'
alias = "PTEST.44.ONDA"

#print(Query_db.get_last_email_client())

#print(Query_db.p2p_trx())

#print(Query_db.get_code_email_register(email))

# trasn = uuid.uuid1()
# print(trasn)
# last_cvu = Query_db.get_last_cvu()
# print(last_cvu)
#print(Query_db.transaction_trx(cvu))
# trx= Query_db.get_last_transaction_trx()
# print(Query_db.get_transaction_status(trx))
#phone = int("54351" + str(faker.random_number(digits=7)))
#print(phone)
# alias = 'GCOOK.21.ONDA'
# # a = Query_db.tb_users.get_one_otp_code()
#print(Query_db.get_balance_to_cvu(cvu2))
#print(Query_db.get_balance_to_cvu(cvu))
#print(Query_db.get_balance_to_email(email))


#print(Query_db.get_last_email_client())
#print(Query_db.get_last_cvu())


#print(Query_db.get_phoneCode(number))
#print(Query_db.get_alias_user_with_email(email))
# dni = 24880627
#print(Query_db.get_alias_and_cvu_user_with_email(email))
#print(Query_db.get_data_with_alias(alias))
#print(Query_db.get_last_alias())
#print(Query_db.get_emailCode(email))

#print(Query_db.get_deviceId_to_email(email))

#print(Query_db.get_alias_with_max())