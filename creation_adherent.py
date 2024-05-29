from faker import Factory
import os
from functions.dataframe import create_dataframe_adherent
from functions.fake import *
import pandas as pd

#############################################
# CONFIGURATION

nombre_adherent = 50 # Indiquer le nombre d'adhérent à générer
prefix_list = ["APE", "CBO", "JMO", "AGA", "RSA", "AFO", "PAC", "EFL"]  # Indiquer une liste de prefix à appliquer aux noms des adhérents et entreprises générés ([''] pour aucun prefix)
# ["APE", "CBO", "JMO", "AGA", "RSA", "AFO", "PAC", "EFL"]
# ["AUTO"]
nom_fichier = "jdd_adherents"

#############################################

# Set number of sheet row
row_number = nombre_adherent

# Type attribut for api workflow
type='adherent'

# Set path output file
dirname = os.path.dirname(__file__)
pathfile = os.path.join(dirname, 'data/')

# Initialize faker factory
fakerFR = Factory.create('fr_FR')

# Set columns spreadsheet name
columns_name = [
                "type", "adh_last_name", "adh_first_name", "adh_birth_date", "adh_gender",                                        # adherent general info
                "adh_mail", "adh_street_address", "adh_postcode", "adh_city", "adh_telephone",                                        # adherent communication info
                "adh_iban", "adh_bic_code", "adh_bank_name", "adh_bank_adress", "adh_bank_postcode", "adh_bank_city", "adh_bank_country_code" # adherent bank info
                ]

# Initialize data lists

# General info
list_type= []
list_adh_last_name = []
list_adh_first_name = []
list_adh_birth_date = []
list_adh_gender = []
# Communication info variables set
list_adh_mail = []
list_adh_street_address = []
list_adh_postcode = []
list_adh_city = []
list_adh_telephone = []
# Bank info
list_adh_iban = []
list_adh_bic_code = []
list_adh_bank_name = []
list_adh_bank_adress = []
list_adh_bank_postcode = []
list_adh_bank_city = []
list_adh_bank_country_code = []

# Generate fake data for each row
for prefix in prefix_list :
    for i in range (0, row_number):
        # Variables initialization
        first_name_gender = fake_first_name_gender(fakerFR)
        bank_info = fake_bank_info()

        # General info variables set
        adh_last_name = fake_last_name(prefix, fakerFR)
        adh_first_name = first_name_gender[0]
        adh_birth_date = fake_birth_date_adult(fakerFR)
        adh_gender = first_name_gender[1]
        # Communication info variables set
        adh_mail = fake_mail_two_name(adh_first_name, adh_last_name)
        adh_street_address = fake_street_adress(fakerFR)
        adh_postcode = fake_postalcode(fakerFR)
        adh_city = fake_city(fakerFR)
        adh_telephone = fake_phone_number(fakerFR)
        # Bank info variables set
        adh_iban = bank_info['iban']
        adh_bic_code = bank_info['bic_code']
        adh_bank_name = bank_info['bank_name']
        adh_bank_adress = fake_street_adress(fakerFR)
        adh_bank_postcode =  fake_postalcode(fakerFR)
        adh_bank_city = fake_city(fakerFR)
        adh_bank_country_code = bank_info['country_code']

        # Append variables to lists

        # General info list append
        list_type.append(type)
        list_adh_last_name.append(adh_last_name)
        list_adh_first_name.append(adh_first_name)
        list_adh_birth_date.append(adh_birth_date)
        list_adh_gender.append(adh_gender)
        # Communication info list append
        list_adh_mail.append(adh_mail)
        list_adh_street_address.append(adh_street_address)
        list_adh_postcode.append(adh_postcode)
        list_adh_city.append(adh_city)
        list_adh_telephone.append(adh_telephone)
        # Bank info list append
        list_adh_iban.append(adh_iban)
        list_adh_bic_code.append(adh_bic_code)
        list_adh_bank_name.append(adh_bank_name)
        list_adh_bank_adress.append(adh_bank_adress)
        list_adh_bank_postcode.append(adh_bank_postcode)
        list_adh_bank_city.append(adh_bank_city)
        list_adh_bank_country_code.append(adh_bank_country_code)

# Create dataframe 
df = create_dataframe_adherent(list_type, list_adh_last_name, list_adh_first_name, list_adh_birth_date, list_adh_gender, 
                      list_adh_mail, list_adh_street_address, list_adh_postcode, list_adh_city, list_adh_telephone, 
                      list_adh_iban, list_adh_bic_code, list_adh_bank_name, list_adh_bank_adress, list_adh_bank_postcode, list_adh_bank_city, list_adh_bank_country_code,
                      columns_name)

# Set dataframe type to string to prevent format error
df = df.astype('str')

# Translate dataframe to spreadsheet
df.to_csv(f'{pathfile}{nom_fichier}_newman.csv', encoding='utf-8', index=False, sep=',')
#df.to_excel(f'{pathfile}jdd_personnes_physiques.xlsx', sheet_name=type, index=False)

# Translate dataframe to excel sheet and hide some columns
with pd.ExcelWriter(f'{pathfile}{nom_fichier}.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='JDD', index=False)   
    worksheet = writer.sheets['JDD']
    worksheet.set_column('A:A', None, None, {'hidden': 1})
    worksheet.set_column('E:G', None, None, {'hidden': 1})
    worksheet.set_column('I:J', None, None, {'hidden': 1})
    worksheet.set_column('L:Q', None, None, {'hidden': 1})