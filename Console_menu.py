import os
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None

from Work_with_dataframes import get_path, get_name, get_dataframe
from Plotting import avg_sunny_hours, avg_temps, avg_rainy_days, avg_windy_days, compare_precipitation, compare_sunny_hours

def console_main_menu():
    list_of_cities = {
        '1': 'Budapest', '2': 'Debrecen', '3': 'Győr', 
        '4': 'Kecskemét', '5': 'Kékestető', '6': 'Miskolc', 
        '7': 'Pogány', '8': 'Siófok', '9': 'Szeged', '10': 'Szombathely'
    }
    options = {
        '1': console_single_menu,
        '2': console_compare_menu
    }
    while True:
        print("Choose an option, and press Enter.\n")
        print("1: Work with a city")
        print("2: Compare two cities")
        print("0: Quit\n")
        
        choice = input("Enter your choice: ")
        if choice == '0':
            break
        elif choice in options:
            options[choice](list_of_cities)
        else:
            print("\nPlease choose a valid option.")

def console_compare_menu(list_of_cities):
    dict_of_aviable_cities = list_of_cities.copy()
    plot_types= {'1': 'Avg. sunny hours', '2': 'Avg. Temperatures', '3': 'Avg. rainy days', '4': 'Compare precipitations (Pie)', 
    '5': 'Compare sunny hours (Bar)', '6': 'Avg. windy days'}
    city1 = ""
    city2 = "invalid"
    invalid = False
    while city2 =="invalid":
        clr_scr()
        if invalid:
            print("  Please choose a valid option !")
        print("Available cities: \n")
        print_table(dict_of_aviable_cities)
        print("Choose the first city, and push Enter. \n")
        n = input()
        city1 = list_of_cities.get(n, "invalid")
        if city1 == "invalid":
            invalid = True
            continue
        invalid = False
        del dict_of_aviable_cities[n]
        while city2 =="invalid":
            clr_scr()
            if invalid:
                print("  Please choose a valid option !")
            print(city1 + " already set. \n")
            print("Available cities: \n")
            print_table(dict_of_aviable_cities)
            print("Choose the second city, and push Enter. \n")
            city2 = list_of_cities.get(input(), "invalid")
            if city2 == "invalid":
                invalid = True
                continue
            
    invalid = False
    plot = ""
    while True:
        clr_scr()
        if invalid:
            print("  Please choose a valid option !")
        print_table(plot_types)
        print("Choose a plot type and push enter: ")
        plot = plot_types.get(input(), "invalid")
        if plot != "invalid":
            break
        else:
            invalid = True
    print("You want to save the ", plot, "(", city1, city2, ") ?")
    print("'1': Yes, I want. '2': No, thx. Just show it. (Push Enter after choose!)")
    save = True if input() == '1' else False
    path1 = get_path(city1)
    path2 = get_path(city2)
    dataframe1 = get_dataframe(path1)
    city_name1 = get_name(path1)
    dataframe2 = get_dataframe(path2)
    city_name2 = get_name(path2)
    match plot:
        case 'Avg. sunny hours':
            avg_sunny_hours((city_name1, city_name2),  save, dataframe1, dataframe2)
        case 'Avg. Temperatures':
            avg_temps((city_name1, city_name2),  save, dataframe1, dataframe2)
        case 'Avg. rainy days':
            avg_rainy_days((city_name1, city_name2),  save, dataframe1, dataframe2)
        case 'Compare precipitations (Pie)':
            compare_precipitation(city_name1, city_name2, save, dataframe1, dataframe2)
        case 'Compare sunny hours (Bar)':
            compare_sunny_hours(city_name1, city_name2, save, dataframe1, dataframe2)
        case 'Avg. windy days':
            avg_windy_days((city_name1, city_name2),  save, dataframe1, dataframe2)

def console_single_menu(list_of_cities):
    plot_types= {'1': 'Avg. sunny hours', '2': 'Avg. Temperatures', '3': 'Avg. rainy days', '4': 'Avg. windy days'}
    city = ""
    invalid = False
    while True:
        clr_scr()
        if invalid:
            print("  Please choose a valid option !")
        print("Available cities: \n")
        print_table(list_of_cities)
        print("Choose an option, and push Enter. \n")
        city = list_of_cities.get(input(), "invalid")
        if city != "invalid":
            break
        else:
            invalid = True
    invalid = False
    plot = ""
    while True:
        clr_scr()
        if invalid:
            print("  Please choose a valid option !")
        print_table(plot_types)
        print("Actual city: " + city)
        print("Choose a plot type and push enter: ")
        plot = plot_types.get(input(), "invalid")
        if plot != "invalid":
            break
        else:
            invalid = True
    print("You want to save the ", plot, "(", city, ") ?")
    print("'1': Yes, I want. '2': No, thx. Just show it. (Push Enter after choose!)")
    save = True if input() == '1' else False
    path = get_path(city)
    dataframe = get_dataframe(path)
    city_name = get_name(path)
    match plot:
        case 'Avg. sunny hours':
            avg_sunny_hours((city_name,),  save, dataframe)
        case 'Avg. Temperatures':
            avg_temps((city_name,),  save, dataframe)
        case 'Avg. rainy days':
            avg_rainy_days((city_name,),  save, dataframe)
        case 'Avg. rainy days':
            avg_windy_days((city_name,),  save, dataframe)

def get_path(city):
    list_of_cities= {'Budapest': 'kor0070', 'Debrecen': 'kor0071', 'Győr': 'kor0072', 
    'Kecskemét': 'kor0073', 'Kékestető': 'kor0074', 'Miskolc': 'kor0075', 'Pogány (Pécs)': 'kor0077',
    'Siófok (Balaton)': 'kor0078', 'Szeged': 'kor0079', 'Szombathely': 'kor0080'}
    return "https://www.ksh.hu/stadat_files/kor/hu/" + list_of_cities[city] + ".csv"

def clr_scr():
        os.system('cls') if os.name == "nt" else os.system('clear')

def print_table(inventory, order = None):
    list1 = []
    if order == "count,asc":
        sorted_items = sorted(inventory.items(), key=lambda x: x[1])
    elif order == "count,desc":
        sorted_items = sorted(inventory.items(), key=lambda x: x[1], reverse=True)
    else:
        sorted_items = list(inventory.items())
    list1.append("-----------------------------------\n          City name:   |   Option:\n-----------------------------------\n")
    for c in range(0, len(sorted_items)):
        list1.append("{0:>22} |{1:>6}\n".format(sorted_items[c][1], sorted_items[c][0]))
    list1.append("-----------------------------------")
    print(''.join(list1))
