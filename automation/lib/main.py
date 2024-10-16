from faker import Faker


faker = Faker()

email = faker.first_name().lower() + faker.last_name().lower() + "@gmail.com"
#email = "pablo.palacios@ssysctech.com"
#device_id = 
device_id = faker.random_number(digits=8)
# device_id = uuid.uuid4().hex.upper()
cuit = int("20" + str(faker.random_number(digits=8)) + "1")
#cuit = faker.random_number(digits=9)
#cuit = "2002432739"
#password = faker.password(length=10, special_chars=True, digits=True, upper_case=True)
#phone = int("54351" + str(faker.random_number(digits=7)))
phone = int("351" + str(faker.random_number(digits=6)) + "1")
#phone = "543516619221"
password = "*******"





