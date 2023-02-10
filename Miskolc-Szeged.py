import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def analize_data(miskolc, szeged):
    #print(miskolc.head(15))
    #print(miskolc.tail(15))

    
    

def optimize_data(data):
    year = 2017
    month = 1
    data["Date"] = ""
    #clean 'nan'-s and unnecessary rows:
    for i in range(len(data['Date'])):
        if ((str(data['Hónap'][i]) == "nan") | ((str(data['Hónap'][i]).find("jan") != -1) & (str(data['Hónap'][i]).find("dec") != -1))):
            data.drop(i, axis=0, inplace=True)
            month -= 1
            continue
        elif str(data['Év'][i]) != "nan":
            year = data['Év'][i]
        else:
            data['Év'][i] = year
        if i != 0:
            if month <= 11:
                month += 1
            else:
                month = 1
            data['Date'][i] = str(data['Év'][i]).replace('.', '') + '-' + str(month)

    # change column labels:
    column_labels = {
             'Közép- hõmérséklet, °C': 'Average_temperature_C',
             'Maximális hõmérséklet, °C': 'Max_temperature_C',
             'Minimális hõmérséklet, °C': 'Min_temperature_C',
             'Csapadékos nap ': 'Rainy_days',
             'Csapadékos nap': 'Rainy_days',
             'Lehullott csapadék, mm ': 'Precipitation_mm',
             'Lehullott csapadék, mm': 'Precipitation_mm',
             'A napsütéses órák száma ': 'Sunny_hours',
             'Szeles napok száma, szélsebesség>=10 m/s ': 'Windy_days_windspeed>=10m/s'}
    data.rename(columns= column_labels, inplace=True)

    #optimize dtype:
    data['Average_temperature_C'] = data['Average_temperature_C'].apply(lambda x: float(x.replace(',', '.')))
    data['Max_temperature_C'] = data['Max_temperature_C'].apply(lambda x: float(x.replace(',', '.')))
    data['Min_temperature_C'] = data['Min_temperature_C'].apply(lambda x: float(x.replace(',', '.')))
    data['Sunny_hours'] = data['Sunny_hours'].apply(lambda x: float(x.split()[0].replace(',', '.')))
    data['Date'] = pd.to_datetime(data['Date'])

    #reorder & delete unnecessary columns:
    data = data[['Date', 'Average_temperature_C', 'Max_temperature_C', 'Min_temperature_C', 'Sunny_hours', 'Rainy_days', 
    'Precipitation_mm', 'Windy_days_windspeed>=10m/s']]
    #data.drop('Év', axis = 1, inplace = True)
    #data.drop('Hónap', axis = 1, inplace = True)

    return data


def main():
    miskolc = optimize_data(pd.read_csv("stadat-kor0075-15.9.2.6-hu.csv", encoding = 'unicode_escape', header = 1 ,sep=";"))
    szeged = optimize_data(pd.read_csv("stadat-kor0079-15.9.2.10-hu.csv", encoding = 'unicode_escape', header = 1 ,sep=";"))
    analize_data(miskolc, szeged)

main()