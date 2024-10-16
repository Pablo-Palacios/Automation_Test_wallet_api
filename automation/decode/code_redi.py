import pickle
import redis
import os




class Redis:
    def validacion(device_id):

        def get_otp_code(device_id):
            connection_string = ('REDIS_')
            key = f"user_validation:{device_id}"

            redi = redis.Redis.from_url(connection_string)
            raw_data = redi.get(key)

            # if raw_data is None:
            #     return None
            
            
            try:
                return pickle.loads(raw_data)
            except ModuleNotFoundError as e:
                #print(f"Error deserializing data: {e}")
                return raw_data
            except pickle.UnpicklingError:
                print("Data is not pickled, attempting to decode as utf-8 string...")
            except Exception as e:
                print(f"Unexpected error during deserialization: {e}")
                return raw_data

            try:
                return raw_data.decode("utf-8")
            except UnicodeDecodeError:
                print("Failed to decode data as utf-8 string.")
                return raw_data

        #device_id = "1234568"
        result =get_otp_code(device_id)



        import io  # Este módulo se usa para manejar la entrada/salida de bytes

        class SafeUnpickler(pickle.Unpickler):
            def find_class(self, module, name):
                # Si encuentra una clase que no puede cargar, devuelve un marcador de posición (puede ser str)
                if module.startswith("src.") or name in ["ValidationChannels", "ValidationStatus"]:
                    return str
                return super().find_class(module, name)

        def safe_loads(data):
            try:
                return SafeUnpickler(io.BytesIO(data)).load()  # Utiliza io.BytesIO aquí
            except Exception as e:
                print(f"Error deserializing data: {e}")
                return None

        # El dato binario que proporcionaste
        #raw_data = b'\x80\x04\x95%\x01\x00\x00\x00\x00\x00\x00}\x94(\x8c\tdevice_id\x94\x8c\x071234567\x94\x8c\x0ccurrent_step\x94}\x94(\x8c\x07channel\x94\x8c\x17src.core.entities.enums\x94\x8c\x12ValidationChannels\x94\x93\x94\x8c\x05email\x94\x85\x94R\x94\x8c\x06status\x94h\x06\x8c\x10ValidationStatus\x94\x93\x94\x8c\x07pending\x94\x85\x94R\x94\x8c\x04code\x94\x8c\x06975611\x94uh\tN\x8c\x0cphone_number\x94N\x8c\rsms_validated\x94\x89\x8c\x0femail_validated\x94\x89\x8c\x0ecuil_validated\x94\x89\x8c\x13biometric_validated\x94\x89\x8c\x0euser_validated\x94\x89u.'
        raw_data = result
        # Deserializar usando el SafeUnpickler
        data = safe_loads(raw_data)
        if data:
            for key, value in data.items():
                #print(f"{key}: {value}")
                if key == "current_step":
                    code = value["code"]
                    return code
                    

#print(Redis.validacion("1234569"))