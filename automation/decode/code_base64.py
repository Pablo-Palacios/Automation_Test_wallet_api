
import base64
from PIL import Image
from io import BytesIO
import base64
import requests

def code_base64_front_dni():
# Ruta de la imagen
    image_path = '/home/pablopalacios/code/movilcash_backend/automation/tests/dev_v2/fotos_thales/dni_frente_2_correctp.png'


    # #Leer la imagen en modo binario
    with open(image_path, 'rb') as image_file:
        # Codificar la imagen a Base64
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Mostrar el código Base64 resultante
    
    base_64 = str(base64_image)
    return base_64


def code_base64_back_dni():
# Ruta de la imagen
    image_path = '/home/pablopalacios/code/movilcash_backend/automation/tests/dev_v2/fotos_thales/dorso_3.jpeg'

    # Leer la imagen en modo binario
    with open(image_path, 'rb') as image_file:
        # Codificar la imagen a Base64
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    #Mostrar el código Base64 resultante
    
    base_64 = str(base64_image)
    return base_64





def code_base64_face_img():
# Ruta de la imagen
    image_path = '/home/pablopalacios/code/movilcash_backend/automation/tests/dev_v2/fotos_thales/foto_4.png'

    # # Leer la imagen en modo binario
    with open(image_path, 'rb') as image_file:
        # Codificar la imagen a Base64
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    #Mostrar el código Base64 resultante
    base_64 = str(base64_image)
    return base_64


#     #Ejemplo de cadena base64 de una imagen
# base64_string = code_base64_face_img()
#     # Decodificar la cadena base64
# image_data = base64.b64decode(base64_string)

#     # Convertir los bytes a una imagen
# image = Image.open(BytesIO(image_data))

#     # Mostrar la imagen
# image.show()



# url = "https://api.base64-image.de/convert"

#     with open(image_path, 'rb') as image_file:
#         files = {'file':image_file}
#         response = requests.post(url, files=files)
    
#     if response.status_code == 200:
#         base_64 = response.text
#         return base_64
#     else:
#         print(f"Error: {response.status_code}")


#print(code_base64_front_dni())
#print(code_base64_back_dni())
#print(code_base64_face_img())

