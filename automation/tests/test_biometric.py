from automation.decode.code_base64 import code_base64_front_dni,code_base64_back_dni,code_base64_face_img
from views import biometric_validate_frist_step,biometric_validate_second_step,biometric_validate_third_step
import time

device_id = "123456"
cuil = "20418099691"

def test_first_step_biometric():
    
    front_dni = biometric_validate_frist_step(device_id,cuil,code_base64_front_dni())
    print(front_dni)



def test_second_step_biometric():
    back_dni = biometric_validate_second_step(device_id,code_base64_back_dni())
    print(back_dni)

def test_third_step_biometric():
    face_img = biometric_validate_third_step(device_id,code_base64_face_img())
    print(face_img)