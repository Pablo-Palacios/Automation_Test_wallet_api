import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import base64
from PIL import Image
from io import BytesIO
import base64
import requests
from img_thales.back_img import get_back_img,get_back_leo,get_back_menor,get_back_dni_vencido
from img_thales.face_img import get_face_leo,get_face_img,get_face_2_img
from img_thales.front_img import get_front_img,get_leo_front,get_front_menor,get_front_dni_vencido
from img_thales.licencia_img import get_front_licencia,get_back_licencia
from img_thales.dni_fail import get_back_fail_id,get_face_fail,get_front_fail_id
from img_thales.img_hadis import front_white_image,back_white_image




#     #Ejemplo de cadena base64 de una imagen
base64_string = back_white_image
    # Decodificar la cadena base64
image_data = base64.b64decode(base64_string)

    # Convertir los bytes a una imagen
image = Image.open(BytesIO(image_data))

    # Mostrar la imagen
image.show()



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

