from faker import Faker
from schwifty import IBAN
from unidecode import unidecode
import random

iban_fr_list = [{'bank_name': 'Banque de France', 'bank_code': '30001', 'bic_code': 'AGRIFRPP'},
               {'bank_name': 'BNP Paribas', 'bank_code': '30004', 'bic_code': 'BNPAFRPP'},
               {'bank_name': 'Crédit Agricole', 'bank_code': '30006', 'bic_code': 'AGRIFRPP'},
               {'bank_name': 'Banque Populaire', 'bank_code': '10107', 'bic_code': 'CCBPFRPP'},
               {'bank_name': "Caisse d'Epargne", 'bank_code': '11315', 'bic_code': 'CEPAFRPP'},
               {'bank_name': 'Crédit Lyonnais (LCL)', 'bank_code': '30002', 'bic_code': 'CRLYFRPP'},
               {'bank_name': 'HSBC', 'bank_code': '30056', 'bic_code': 'CCFRFRCR'},
               {'bank_name': 'Crédit Mutuel', 'bank_code': '11808', 'bic_code': 'CMBRFR2B'},
               {'bank_name': 'La Banque Postale', 'bank_code': '10011', 'bic_code': 'PSSTFRPP'},
               {'bank_name': 'AXA Banque', 'bank_code': '12548', 'bic_code': 'AXABFRPP'}]

naf_codes = ['4399C', '4399D', '4120A', '4120B', '4211Z', '4212Z', '4213A', '4213B', '4221Z', '4222Z', '4291Z', '4299Z']

statuts = ["SAS", "SARL", "SA"] 

def fake_phone_number(fake: Faker) -> str:
    """Generate a fake phone number"""
    p = f'06{fake.msisdn()[5:]}'
    phone_number = p[:2] + '.' + p[2:4] + '.' + p[4:6] + '.' + p[6:8] + '.' + p[8:]
    return phone_number

def fake_street_adress(fake: Faker) -> str:
    """Generate a fake street adress"""
    street_address =  " ".join((unidecode(fake.street_address().replace (',', ' '))).split())
    if street_address[0].isdigit() == False:
        street_number = random.randint(1, 50)
        street_address = str(street_number) + ' ' + street_address
    return street_address

def fake_birth_date_adult(fake: Faker) -> str:
    """Generate a fake birth date for adult person"""
    birth_date = str(fake.date_between(start_date='-65y', end_date='-19y'))
    return birth_date

def fake_birth_date_enfant(fake: Faker) -> str:
    """Generate a fake birth date for child person"""
    birth_date = str(fake.date_between(start_date='-17y', end_date='-1y'))
    return birth_date

def fake_first_name_gender(fake: Faker) -> str:
    """Generate a fake first name for a random gender"""
    first_name = ''
    gender = ''
    if random.choice([True, False]):
        first_name = unidecode(fake.first_name_female())
        gender = "FEMALE"
    else:
        first_name = unidecode(fake.first_name_male())
        gender = "MALE"
    return first_name, gender

def fake_last_name(prefix, fake: Faker) -> str:
    """Generate a fake last name"""
    if prefix != "" : prefix = prefix + " "
    return unidecode(prefix + fake.last_name())

def fake_city(fake: Faker) -> str:
    """Generate a fake city"""
    return unidecode(fake.city())

def fake_postalcode(fake: Faker) -> str:
    """Generate a fake postal code"""
    return (fake.postcode()).zfill(5)

def fake_mail_one_name(name) -> str:
    """Generate a fake mail with the name of a person in it"""
    return (name.lower().replace(',', '').replace('.', '').replace(' ', '') + "@" + "fakemail.com")

def fake_mail_two_name(name1, name2):
    """Generate a fake mail with two name in it"""
    return (name1.lower() + "." + name2.lower() + "@" + "fakemail.com").replace(' ', '')

def fake_siret(fake: Faker) -> str:
    """Generate a fake siret"""
    return fake.siret().replace (' ', '')

def fake_company_name(prefix, statut, fake: Faker) -> str:
    """Generate a fake company name"""
    if prefix != "" : prefix = prefix + " "
    name = (unidecode(fake.company())).replace('.', '')
    name = name.replace(' SAS', '').replace(' SARL', '').replace(' SA', '')
    company_name = prefix + name + ' ' + statut
    return company_name

def fake_bank_info(country_code='FR'):
    """Generate fake bank informations with fake iban"""
    bank_info_dict = random.choice(iban_fr_list)
    account_code = random.randint(10000000000, 99999999999)
    iban = IBAN.generate('FR', bank_code=bank_info_dict['bank_code'], account_code=str(account_code))
    iban = iban.replace('<IBAN', '').replace('>', '')
    bank_info_dict['iban'] = iban
    bank_info_dict['country_code'] = country_code
    return bank_info_dict

def fake_naf_code():
    """Generate fake naf code"""
    naf_code = random.choice(naf_codes)
    return naf_code

def fake_entreprise_statut():
    """Generate fake entreprise statut"""
    entreprise_statut = random.choice(statuts)
    return entreprise_statut
