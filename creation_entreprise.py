from faker import Factory
import os
from datetime import date
from dateutil.relativedelta import relativedelta
from functions.dataframe import create_dataframe_entreprise
from functions.fake import *
import pandas as pd

#############################################
# CONFIGURATION

nombre_entreprise = 50 # Indiquer le nombre d'entreprise à générer
prefix_list = ["APE", "CBO", "JMO", "AGA", "RSA", "AFO", "PAC", "EFL"]  # Indiquer une liste de prefix à appliquer aux noms des adhérents et entreprises générés ([''] pour aucun prefix)
# ["APE", "CBO", "JMO", "AGA", "RSA", "AFO", "PAC", "EFL"]
# ["AUTO"]
nom_fichier = "jdd_entreprises"

date_creation = ""  # Indiquer une date de début d'activité ("" par défaut pour une date à - 1 an)

#############################################

# Set number of sheet row
row_number = nombre_entreprise

# Type attribut for api workflow
type='entreprise'

# Set creation date
current_date = date.today()

if date_creation == "" :
    date_creation = current_date - relativedelta(years=1) # Set begin date for contrat sante at 2 years in past
    date_creation_year = date_creation.year
    date_creation_month = date_creation.month
    contrat_sante_date = f'{date_creation_year}-{date_creation_month}-01'

# Set path output file
dirname = os.path.dirname(__file__)
pathfile = os.path.join(dirname, 'data/')

# Initialize faker factory
fakerFR = Factory.create('fr_FR')

# Set columns spreadsheet name
columns_name = ["type", "date_creation", "ent_company_name", "ent_siret", "ent_statut", "ent_naf", # entreprise general info
                "ent_telephone", "ent_city", "ent_postcode", "ent_street_address", "ent_mail",     # entreprise communication info
                "ent_iban", "ent_bic_code", "ent_bank_name", "ent_bank_adress", "ent_bank_postcode", "ent_bank_city", "ent_bank_country_code" # entreprise bank info
                ]

# Initialize data lists
list_type = []
list_date_creation = []
list_ent_company_name = []
list_ent_siret = []
list_ent_statut = []
list_ent_naf = []
list_ent_telephone = []
list_ent_city = []
list_ent_postcode = []
list_ent_street_address = []
list_ent_mail = []
list_ent_iban = []
list_ent_bic_code = []
list_ent_bank_name = []
list_ent_bank_adress = []
list_ent_bank_postcode = []
list_ent_bank_city = []
list_ent_bank_country_code = []
list_date_creation = []

# Generate fake data for each row
for prefix in prefix_list :
    for i in range (0, row_number):
        # Variables initialization
        bank_info = fake_bank_info()

        # General info variables set
        ent_statut = fake_entreprise_statut()
        ent_company_name = fake_company_name(prefix, ent_statut, fakerFR)
        ent_siret = fake_siret(fakerFR)
        ent_naf = fake_naf_code()
        # Communication info variables set
        ent_telephone = fake_phone_number(fakerFR)
        ent_city = fake_city(fakerFR)
        ent_postcode = fake_postalcode(fakerFR)
        ent_street_address = fake_street_adress(fakerFR)
        ent_mail = fake_mail_one_name(ent_company_name)
        # Bank info variables set
        ent_iban = bank_info['iban']
        ent_bic_code = bank_info['bic_code']
        ent_bank_name = bank_info['bank_name']
        ent_bank_adress = fake_street_adress(fakerFR)
        ent_bank_postcode =  fake_postalcode(fakerFR)
        ent_bank_city = fake_city(fakerFR)
        bank_country_code = bank_info['country_code']

        # Append variables to lists

        # General info list append
        list_type.append(type)
        list_date_creation.append(date_creation)
        list_ent_company_name.append(ent_company_name)
        list_ent_siret.append(ent_siret)
        list_ent_statut.append(ent_statut)
        list_ent_naf.append(ent_naf)
        # Communication info list append
        list_ent_telephone.append(ent_telephone)
        list_ent_city.append(ent_city)
        list_ent_postcode.append(ent_postcode)
        list_ent_street_address.append(ent_street_address)
        list_ent_mail.append(ent_mail)
        # Bank info list append
        list_ent_iban.append(ent_iban)
        list_ent_bic_code.append(ent_bic_code)
        list_ent_bank_name.append(ent_bank_name)
        list_ent_bank_adress.append(ent_bank_adress)
        list_ent_bank_postcode.append(ent_bank_postcode)
        list_ent_bank_city.append(ent_bank_city)
        list_ent_bank_country_code.append(bank_country_code)

# Create dataframe 
df = create_dataframe_entreprise(list_type, list_date_creation, list_ent_company_name, list_ent_siret, list_ent_statut, list_ent_naf, 
                               list_ent_telephone, list_ent_city, list_ent_postcode, list_ent_street_address, list_ent_mail, 
                               list_ent_iban, list_ent_bic_code, list_ent_bank_name, list_ent_bank_adress, list_ent_bank_postcode, list_ent_bank_city, list_ent_bank_country_code,
                               columns_name)

df = df.astype('str')

# Translate dataframe to spreadsheet
df.to_csv(f'{pathfile}{nom_fichier}_newman.csv', encoding='utf-8', index=False, sep=',')

# Translate dataframe to excel sheet and hide some columns
with pd.ExcelWriter(f'{pathfile}{nom_fichier}.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='JDD', index=False)   
    worksheet = writer.sheets['JDD']
    worksheet.set_column('A:B', None, None, {'hidden': 1})
    worksheet.set_column('G:H', None, None, {'hidden': 1})
    worksheet.set_column('J:K', None, None, {'hidden': 1})
    worksheet.set_column('M:R', None, None, {'hidden': 1})
