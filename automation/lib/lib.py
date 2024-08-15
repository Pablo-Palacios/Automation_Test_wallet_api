from faker import Faker

faker = Faker()


# formato fake de device id
# >>> ids = uuid.uuid4().hex.upper()
# >>> print(ids[:8], ids[8:12], ids[12:16], ids[16:20], ids[20:], sep="-")
# 56452922-BE43-46B5-B494-D8961BB95C71



# Lista de modelos de celulares

modelos_de_celulares = [
    "Samsung Galaxy S21",
    "iPhone 13",
    "Xiaomi Mi 11",
    "OnePlus 9",
    "Nokia G50",
    "Huawei P50",
    "Oppo Find X3"
]

# Lista de provincias argentinas
provincias_argentinas = [
    "Buenos Aires",
    "Catamarca",
    "Chaco",
    "Chubut",
    "Córdoba",
    "Corrientes",
    "Entre Ríos",
    "Formosa",
    "Jujuy",
    "La Pampa",
    "La Rioja",
    "Mendoza",
    "Misiones",
    "Neuquén",
    "Río Negro",
    "Salta",
    "San Juan",
    "San Luis",
    "Santa Cruz",
    "Santa Fe",
    "Santiago del Estero",
    "Tierra del Fuego",
    "Tucumán"
]

celco = [
    "ar.personal",
    "ar.movistar",
    "ar.claro"
]

cbu = [
    {"cbu":"0070138530004027543365", "alias":"Fernando.DORAO.2024","cuil":"20284257902", "titular":"Fernando DORAO"},
    {"cbu":"0070076430004058345624", "alias":"Susana.Garcia.2024","cuil":"27220623748", "titular":"Susana Garcia"},
    {"cbu":"1500005300005568466996", "alias":"Susana.Garcia.2023","cuil":"27220623748", "titular":"Susana Garcia"},
    {"cbu":"3840200500000005030701", "alias":"Guillermo.Cook.2024","cuil":"20394483266", "titular":"Guillermo Cook"},
    {"cbu":"0720500288000001534218", "alias":"Javier.Sabag.2024","cuil":"20329919634", "titular":"Javier Sabag"},
    {"cbu":"0070355830004016466688", "alias":"Camila.Careggio.2024","cuil":"27433696854", "titular":"Camila Careggio"},
    {"cbu":"0200918011000013729044", "alias":"Christian.Kreitzer.2024","cuil":"20248806274", "titular":"Christian Kreitzer"},
    {"cbu":"2850320030094201261561", "alias":"Silvia.Rafia.Cauca.2024","cuil":"27222245112", "titular":"Silvia Rafia Cauca"}
]

cvu = [
    {"cvu":"0000007900202488062743", "alias":"C0RD0BA.UALA","cuil":"20248806274", "titular":"Christian Kreitzer"},
    {"cvu":"0000003100043274816742", "alias":"C0RD0BA.MP","cuil":"20248806274", "titular":"Christian"},
    {"cvu":"0000003100045597925983", "alias":"gbsrz.mp","cuil":"27957538652", "titular":"Gabriela Suarez"},
    {"cvu":"0000177500000005499252", "alias":"20451280792.RPY1","cuil":"20451280792", "titular":"Facundo Rombola"},
    {"cvu":"1430001713008081890011", "alias":"gustavoduran187","cuil":"20956935556", "titular":"Gustavo Duran"},
    {"cvu":"0000076500000027169603", "alias":"aanrique8.ppay","cuil":"27445013337", "titular":"Aracelli Anrique"}
]
def cvu_random():
    selected_cvu = faker.random.choice(cvu)
    return selected_cvu

def cbu_random():
    selected_cbu = faker.random.choice(cbu)
    return selected_cbu

def ar_celco():
    return str(faker.random_element(celco))

def device_models():
    return str(faker.random_element(modelos_de_celulares))

def provincias_arg():
    return str(faker.random_element(provincias_argentinas))