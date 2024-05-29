from faker import Factory
import os
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from functions.dataframe import create_dataframe_affiliations
from functions.fake import *
import pandas as pd

#############################################
# CONFIGURATION

nombre_affiliation = 50 # Indiquer le nombre d'affiliation santé et prévoyance à générer, ce nombre est à appliquer pour chacun des prefix
prefix_list = ["APE", "CBO", "JMO", "AGA", "RSA", "AFO", "PAC", "EFL"] # Indiquer une liste de prefix à appliquer aux noms des adhérents et entreprises générés ([""] pour aucun prefix)
# ["APE", "CBO", "JMO", "AGA", "RSA", "AFO", "PAC", "EFL"]
# ["AUTO"]
contrat_sante_code = ["SCSPS-ARCHI", "SCSPS-IMMO"] # Indiquer un code contrat santé
contrat_sante_date = ""            # Indiquer une date de début d'effet pour le contrat santé ("" par défaut pour une date réglementaire à - 2 ans)
contrat_prev_code = ["PCSPS-ARCHI", "PCSPS-IMMO"]  # Indiquer un code contrat prev
contrat_prev_date = ""             # Indiquer une date de début d'effet pour le contrat prev ("" par défaut pour une date réglementaire à - 3 ans)
nom_fichier = "jdd_affiliations"

#############################################

# Total number of row
row_number = nombre_affiliation

# Type attribut for api workflow
type ='affiliation'

# Set date
current_date = date.today()

if contrat_sante_date == "" :
    contrat_sante_date = current_date - relativedelta(years=2) # Set creation date for contrat sante at 2 years in past
    date_sante_year = contrat_sante_date.year
    date_sante_month = contrat_sante_date.month
    date_sante_day = contrat_sante_date.day
    contrat_sante_date = datetime(date_sante_year, date_sante_month, date_sante_day)
    contrat_sante_date = contrat_sante_date.strftime('%Y-%m-%d')
    contrat_sante_date = contrat_sante_date[:-2] + '01'

if contrat_prev_date == "" :
    contrat_prev_date = current_date - relativedelta(years=3) # Set creation date for contrat prev at 2 years in past
    date_prev_year = contrat_prev_date.year
    date_prev_month = contrat_prev_date.month
    date_prev_day = contrat_prev_date.day
    contrat_prev_date = datetime(date_prev_year, date_prev_month, date_prev_day)
    contrat_prev_date = contrat_prev_date.strftime('%Y-%m-%d')
    contrat_prev_date = contrat_prev_date[:-2] + '01'

date_list = [contrat_sante_date, contrat_prev_date]
date_creation = min(date_list)  # Set creation date to the oldest contrat date

# Set contrats sante list
len_sante_code = len(contrat_sante_code)
quotient_sante, remainder_sante = divmod(nombre_affiliation, len_sante_code)
list_contrat_sante = [e for x in zip(*[contrat_sante_code]*quotient_sante) for e in x]
list_sante_remainder = [contrat_sante_code[(len_sante_code - 1)] * remainder_sante]
list_contrat_sante.extend(list_sante_remainder)

# Set contrats prevoyance list
len_prev_code = len(contrat_prev_code)
quotient_prev, remainder_prev = divmod(nombre_affiliation, len_prev_code)
list_contrat_prevoyance = [e for x in zip(*[contrat_prev_code]*quotient_prev) for e in x]
list_prev_remainder = [contrat_prev_code[(len_prev_code - 1)] * remainder_prev]
list_contrat_prevoyance.extend(list_prev_remainder)

# Set path file
dirname = os.path.dirname(__file__)
pathfile = os.path.join(dirname, 'data/')

# Initialize faker factory
fakerFR = Factory.create('fr_FR')

# Set columns spreadsheet name
columns_name = [
                "type", "date_creation",
                "adh_last_name", "adh_first_name", "adh_birth_date", "adh_gender",             # adherent general info
                "adh_mail", "adh_street_address", "adh_postcode", "adh_city", "adh_telephone", # adherent communication info
                "adh_iban", "adh_bic_code", "adh_bank_name", "adh_bank_adress", "adh_bank_postcode", "adh_bank_city", "adh_bank_country_code", # adherent bank info
                "ent_company_name", "ent_siret", "ent_statut", "ent_naf",                      # entreprise general info
                "ent_telephone", "ent_city", "ent_postcode", "ent_street_address", "ent_mail", # entreprise communication info
                "ent_iban", "ent_bic_code", "ent_bank_name", "ent_bank_adress", "ent_bank_postcode", "ent_bank_city", "ent_bank_country_code", # entreprise bank info
                "contrat_sante_code", "contrat_sante_date",                                    # contrat sante info
                "contrat_prev_code", "contrat_prev_date"                                       # contrat prevoyance info
                ]

# Initialize data lists

# Type
list_type = []
list_date_creation = []

# General adherent info
list_adh_last_name = []
list_adh_first_name = []
list_adh_birth_date = []
list_adh_gender = []
# Communication adherent info
list_adh_mail = []
list_adh_street_address = []
list_adh_postcode = []
list_adh_city = []
list_adh_telephone = []
# Bank adherent info
list_adh_iban = []
list_adh_bic_code = []
list_adh_bank_name = []
list_adh_bank_adress = []
list_adh_bank_postcode = []
list_adh_bank_city = []
list_adh_bank_country_code = []

# General entreprise info
list_ent_company_name = []
list_ent_siret = []
list_ent_statut = []
list_ent_naf = []
# Communiation entreprise info
list_ent_telephone = []
list_ent_city = []
list_ent_postcode = []
list_ent_street_address = []
list_ent_mail = []
# Bank entreprise info
list_ent_iban = []
list_ent_bic_code = []
list_ent_bank_name = []
list_ent_bank_adress = []
list_ent_bank_postcode = []
list_ent_bank_city = []
list_ent_bank_country_code = []

# Contrat info
list_contrat_sante_code = []
list_contrat_sante_date = []
list_contrat_prevoyance_code = []
list_contrat_prevoyance_date = []

# Generate fake data for each row
for prefix in prefix_list :
    for i in range (0, row_number) :
        # Adherent variables initialization 
        first_name_gender = fake_first_name_gender(fakerFR)
        adh_bank_info = fake_bank_info()

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
        adh_iban = adh_bank_info['iban']
        adh_bic_code = adh_bank_info['bic_code']
        adh_bank_name = adh_bank_info['bank_name']
        adh_bank_adress = fake_street_adress(fakerFR)
        adh_bank_postcode =  fake_postalcode(fakerFR)
        adh_bank_city = fake_city(fakerFR)
        adh_bank_country_code = adh_bank_info['country_code']

        # Entreprise variables initialization
        ent_bank_info = fake_bank_info()

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
        ent_iban = ent_bank_info['iban']
        ent_bic_code = ent_bank_info['bic_code']
        ent_bank_name = ent_bank_info['bank_name']
        ent_bank_adress = fake_street_adress(fakerFR)
        ent_bank_postcode =  fake_postalcode(fakerFR)
        ent_bank_city = fake_city(fakerFR)
        ent_bank_country_code = ent_bank_info['country_code']

        # Append variables to lists
        list_type.append(type)
        list_date_creation.append(date_creation)
        # Append adherent lists
        list_adh_last_name.append(adh_last_name)
        list_adh_first_name.append(adh_first_name)
        list_adh_birth_date.append(adh_birth_date)
        list_adh_gender.append(adh_gender)
        list_adh_mail.append(adh_mail)
        list_adh_street_address.append(adh_street_address)
        list_adh_postcode.append(adh_postcode)
        list_adh_city.append(adh_city)
        list_adh_telephone.append(adh_telephone)
        list_adh_iban.append(adh_iban)
        list_adh_bic_code.append(adh_bic_code)
        list_adh_bank_name.append(adh_bank_name)
        list_adh_bank_adress.append(adh_bank_adress)
        list_adh_bank_postcode.append(adh_bank_postcode)
        list_adh_bank_city.append(adh_bank_city)
        list_adh_bank_country_code.append(adh_bank_country_code)
        # Append entreprises lists
        list_ent_company_name.append(ent_company_name)
        list_ent_siret.append(ent_siret)
        list_ent_statut.append(ent_statut)
        list_ent_naf.append(ent_naf)
        list_ent_telephone.append(ent_telephone)
        list_ent_city.append(ent_city)
        list_ent_postcode.append(ent_postcode)
        list_ent_street_address.append(ent_street_address)
        list_ent_mail.append(ent_mail)
        list_ent_iban.append(ent_iban)
        list_ent_bic_code.append(ent_bic_code)
        list_ent_bank_name.append(ent_bank_name)
        list_ent_bank_adress.append(ent_bank_adress)
        list_ent_bank_postcode.append(ent_bank_postcode)
        list_ent_bank_city.append(ent_bank_city)
        list_ent_bank_country_code.append(ent_bank_country_code)
        # Append contrats lists
        list_contrat_sante_date.append(contrat_sante_date)         
        list_contrat_prevoyance_date.append(contrat_prev_date)
    # Extend contrats lists
    list_contrat_sante_code.extend(list_contrat_sante)
    list_contrat_prevoyance_code.extend(list_contrat_prevoyance)

# Create dataframe 
df = create_dataframe_affiliations(list_type, list_date_creation, list_adh_last_name, list_adh_first_name, list_adh_birth_date, list_adh_gender, 
                                   list_adh_mail, list_adh_street_address, list_adh_postcode, list_adh_city, list_adh_telephone, 
                                   list_adh_iban, list_adh_bic_code, list_adh_bank_name, list_adh_bank_adress, list_adh_bank_postcode, list_adh_bank_city, list_adh_bank_country_code, 
                                   list_ent_company_name, list_ent_siret, list_ent_statut, list_ent_naf, 
                                   list_ent_telephone, list_ent_city, list_ent_postcode, list_ent_street_address, list_ent_mail, 
                                   list_ent_iban, list_ent_bic_code, list_ent_bank_name, list_ent_bank_adress, list_ent_bank_postcode, list_ent_bank_city, list_ent_bank_country_code, 
                                   list_contrat_sante_code, list_contrat_sante_date, list_contrat_prevoyance_code, list_contrat_prevoyance_date,
                                   columns_name)

# Set dataframe type to string to prevent format error
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
    worksheet.set_column('U:X', None, None, {'hidden': 1})
    worksheet.set_column('Z:AA', None, None, {'hidden': 1})
    worksheet.set_column('AC:AH', None, None, {'hidden': 1})