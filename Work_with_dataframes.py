import pandas as pd

def optimize_data(data):
    # Initialize year and month
    year = 2017
    month = 1
    data["Date"] = ""

    #clean 'nan'-s and unnecessary rows:
    for i in range(len(data)):
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
             'A napsütéses órák száma': 'Sunny_hours',
             'Szeles napok száma, szélsebesség>=10 m/s ': 'Windy_days_windspeed>=10m/s',
             'Szeles napok száma, szélsebesség>=10 m/s': 'Windy_days_windspeed>=10m/s'}
    data.rename(columns= column_labels, inplace=True)

    #optimize dtype:
    data['Average_temperature_C'] = data['Average_temperature_C'].apply(lambda x: float(x.replace(',', '.')))
    data['Max_temperature_C'] = data['Max_temperature_C'].apply(lambda x: float(x.replace(',', '.')))
    data['Min_temperature_C'] = data['Min_temperature_C'].apply(lambda x: float(x.replace(',', '.')))
    data['Sunny_hours'] = data['Sunny_hours'].apply(lambda x: float(x.split()[0].replace(',', '.')) if x!= ".." else -1)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Precipitation_mm'] = data['Precipitation_mm'].apply(lambda x: int(x))

    #reorder & delete unnecessary columns:
    data = data[['Date', 'Average_temperature_C', 'Max_temperature_C', 'Min_temperature_C', 'Sunny_hours', 'Rainy_days', 
    'Precipitation_mm', 'Windy_days_windspeed>=10m/s']]

    return data

def get_path(city):
    list_of_cities= {'Budapest': 'kor0070', 'Debrecen': 'kor0071', 'Győr': 'kor0072', 
    'Kecskemét': 'kor0073', 'Kékestető': 'kor0074', 'Miskolc': 'kor0075', 'Pogány (Pécs)': 'kor0077',
    'Siófok (Balaton)': 'kor0078', 'Szeged': 'kor0079', 'Szombathely': 'kor0080'}
    return "https://www.ksh.hu/stadat_files/kor/hu/" + list_of_cities[city] + ".csv"

def get_name(path):
    return pd.read_csv(path, encoding='unicode_escape', header=None, nrows=1).values[0][0].split()[1]

def get_dataframe(path):
    return optimize_data(pd.read_csv(path, encoding = 'unicode_escape', header = 1 ,sep=";"))