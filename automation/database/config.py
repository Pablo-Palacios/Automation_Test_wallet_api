import psycopg2
from faker import Faker
import uuid
import os



# Confi database 
class Query_db:
        
        host = ('HOST_DEV')
        database = ('DATABASE')
        user = "********"
        password = ('PASSWORD')

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
                                       WHERE client_id = (SELECT MAX(client_id) FROM "walletClients".clients;""")
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
       
                        cursor.execute(f"""SELECT *
                                       FROM "walletClients".users AS u
                                       INNER JOIN "walletClients".clients AS c ON c.user_id = u.user_id
                                       WHERE u.email = '{email}';""")
                        result = cursor.fetchone()
                        #cursor.close()
                        return result

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
                
        def get_cuil_with_email(email):
                cursor = Query_db.conn.cursor()
                cursor.execute(f""" SELECT cuil
                                       FROM "walletClients".users AS u
                                       INNER JOIN "walletClients".clients AS c ON c.user_id = u.user_id
                                       WHERE u.email = '{email}';""")
                cuil = cursor.fetchone()

                return cuil[0]
        
        def get_cbu_bfsa_with_email(email):
                cursor = Query_db.conn.cursor()
                cursor.execute(f""" SELECT cbu
                                    FROM "walletClients".cbus_bfsa AS c 
                                    INNER JOIN "walletClients".users AS u ON u.user_id = c.user_id
                                    WHERE u.email = '{email}';
                                """)
                cbu = cursor.fetchone()
                return cbu[0]
        
        def get_cbu_bfsa_is_active_with_email(email):
                cursor = Query_db.conn.cursor()
                cursor.execute(f""" SELECT is_active
                                    FROM "walletClients".cbus_bfsa AS c 
                                    INNER JOIN "walletClients".users AS u ON u.user_id = c.user_id
                                    WHERE u.email = '{email}';
                                """)
                boolean = cursor.fetchone()

                return boolean[0]
        
        def get_branch_info_with_name(id):
                cursor = Query_db.conn.cursor()
                cursor.execute(f"""SELECT branch_name FROM "walletClients".branches WHERE branch_id = '{id}'""")
                data = cursor.fetchone()
                return data[0]
        
        def get_last_branch_id():
                cursor = Query_db.conn.cursor()
                cursor.execute("""SELECT branch_id, commerce_id, branch_name 
                               FROM "walletClients".branches
                               WHERE branch_id = (SELECT MAX(branch_id)FROM "walletClients".branches)""")
                data = cursor.fetchone()
                return data
        
        def get_last_checkout_id():
                cursor = Query_db.conn.cursor()
                cursor.execute("""SELECT checkout_id, checkout_name,checkout_qr,branch_id 
                               FROM "walletClients".checkouts
                               WHERE checkout_id = (SELECT MAX(checkout_id)FROM "walletClients".checkouts)""")
                data = cursor.fetchone()
                return data
        
        def get_name_checkout_id(id):
                cursor = Query_db.conn.cursor()
                cursor.execute(f"""SELECT checkout_name
                               FROM "walletClients".checkouts
                               WHERE checkout_id = '{id}'""")
                data = cursor.fetchone()
                return data[0]
        
        def get_checkout_info_with_name(id):
                cursor = Query_db.conn.cursor()
                cursor.execute(f"""SELECT checkout_name FROM "walletClients".checkouts WHERE checkout_id = '{id}'""")
                data = cursor.fetchone()
                return data[0]

        def get_last_repre_id():
                cursor = Query_db.conn.cursor()
                cursor.execute("""SELECT representative_id, representative_type, user_id,commerce_id,role
                               FROM "walletClients".representatives 
                               WHERE representative_id = (SELECT MAX(representative_id)FROM "walletClients".representatives)""")
                data = cursor.fetchone()
                return data
        def get_device_with_email(email):
                cursor = Query_db.conn.cursor()
                cursor.execute(f"""SELECT d.device_tag FROM "walletClients".devices d 
                                INNER JOIN "walletClients".devices_user du ON du.device_id = d.device_id 
                                INNER JOIN "walletClients".users u ON u.user_id = du.user_id 
                                WHERE u.email = '{email}'""")
                data = cursor.fetchone()
                return data
        def get_user_id_email(email):
                cursor = Query_db.conn.cursor()
                cursor.execute(f"""SELECT u.user_id FROM "walletClients".users u 
                                WHERE u.email = '{email}'""")
                data = cursor.fetchone()
                return data[0]
        
        def get_phone_with_email(email):
                cursor = Query_db.conn.cursor()
                cursor.execute(f"""SELECT c.phone_number FROM "walletClients".clients c
                               INNER JOIN "walletClients".users u ON u.user_id = c.user_id
                                WHERE u.email = '{email}'""")
                data = cursor.fetchone()
                return data
        

