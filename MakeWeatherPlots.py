import os
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from ttkthemes import ThemedStyle

from plotting import avg_sunny_hours, avg_temps, avg_rainy_days, avg_windy_days, compare_precipitation, compare_sunny_hours

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

list_of_cities= {'1': 'Budapest', '2': 'Debrecen', '3': 'Győr', 
    '4': 'Kecskemét', '5': 'Kékestető', '6': 'Miskolc', '7': 'Pogány (Pécs)',
    '8': 'Siófok (Balaton)', '9': 'Szeged', '10': 'Szombathely'}

def visual_main_menu():
    def single_menu_action():
        root.destroy()
        visual_single_menu()

    def compare_menu_action():
        root.destroy()
        visual_compare_menu()

    def quit_action():
        root.destroy()

    root = tk.Tk()
    root.title("City Menu")
    root.geometry("300x400")
    root.configure(background='darkgray')

    style = ThemedStyle(root)
    style.set_theme("plastik")
    style.configure('TButton', font = ('Arial', 14), foreground = '#6B6B6B', background = '#6B6B6B', padding = 10, borderwidth = 0)
    
    single_menu_button = ttk.Button(root, text="Work with a city", command=single_menu_action)
    compare_menu_button = ttk.Button(root, text="Compare cities", command=compare_menu_action)
    quit_button = ttk.Button(root, text="Quit", command=quit_action)
    
    single_menu_button.pack(pady=5)
    compare_menu_button.pack(pady=5)
    quit_button.pack(pady=10)
    
    root.mainloop()

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

city_listbox = {}
selected_cities_indexes = []

def visual_compare_menu():
    # Create new Toplevel window for compare menu
    root = tk.Tk()
    root.title("City Menu")
    root.geometry("300x500")

    # Create city selection listbox
    global city_listbox
    city_listbox = Listbox(root, selectmode=MULTIPLE)
    for city in list_of_cities.values():
        city_listbox.insert(END, city)
    city_listbox.pack(padx=10, pady=10)

    # Create a function to update the selected_cities list
    def update_selected_cities(event):
        global selected_cities_index
        for i in city_listbox.curselection():
            if i not in selected_cities_indexes:
                selected_cities_indexes.append(i)
        for j in selected_cities_indexes:
            if j not in city_listbox.curselection():
                selected_cities_indexes.remove(j)

    # Bind the update_selected_cities function to the ListboxSelect event
    city_listbox.bind("<<ListboxSelect>>", update_selected_cities)

    # Create button to generate visualizations
    def generate_visualizations():
        # Call visual_plot_menu with selected cities and plot types
        plot_types= {'1': 'Avg. sunny hours', '2': 'Avg. Temperatures', '3': 'Avg. rainy days', '4': 'Compare precipitations (Pie)', 
        '5': "Compare two city's sunny hours (Bar)", '6': 'Avg. windy days'}
        root.destroy()
        selected_cities = []
        for index in selected_cities_indexes:
            city = list_of_cities.get(str(index+1))
            selected_cities.append(city)
        visual_plot_menu(plot_types, selected_cities)


    def back_action():
        root.destroy()
        visual_main_menu()

    style = ThemedStyle(root)
    style.set_theme("plastik")
    style.configure('TButton', font = ('Arial', 14), foreground = '#6B6B6B', background = '#6B6B6B', padding = 5, borderwidth = 0)

    generate_button = ttk.Button(root, text='Generate Visualizations', command=generate_visualizations)
    generate_button.pack(padx=10, pady=10)

    back_button = ttk.Button(root, text="Back", command = back_action)
    back_button.pack(side=tk.BOTTOM, pady=10)

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

def visual_single_menu():
    def city_action(city):
        plot_types= {'1': 'Avg. sunny hours', '2': 'Avg. Temperatures', '3': 'Avg. rainy days', '4': 'Avg. windy days'}
        global selected_city
        selected_city = city
        root.destroy()
        visual_plot_menu(plot_types, selected_city)

    root = tk.Tk()
    root.title("City Menu")
    root.geometry("300x500")

    def back_action():
        root.destroy()
        visual_main_menu()

    style = ThemedStyle(root)
    style.set_theme("plastik")
    style.configure('TButton', font = ('Arial', 14), foreground = '#6B6B6B', background = '#6B6B6B', padding = 5, borderwidth = 0)

    for city in list_of_cities.values():
        button = ttk.Button(root, text=city, command=lambda c=city: city_action(c))
        button.pack()

    back_button = ttk.Button(root, text="Back", command = back_action)
    back_button.pack(side=tk.BOTTOM, pady=10)

    root.mainloop()

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

def visual_plot_menu(plot_types, city_name):
    root = tk.Tk()
    root.title("Plot Menu")
    root.geometry("300x400")

    def back_action():
        root.destroy()
        visual_single_menu()

    style = ThemedStyle(root)
    style.set_theme("plastik")
    style.configure('TButton', font = ('Arial', 14), foreground = '#6B6B6B', background = '#6B6B6B', padding = 5, borderwidth = 0)

    for key, value in plot_types.items():
        button = ttk.Button(root, text = value, command = lambda city_name=city_name, plot_type = value: show_plot_action(city_name, plot_type, False, root))
        button.pack()

    back_button = ttk.Button(root, text="Back", command = back_action)
    back_button.pack(side = tk.BOTTOM, pady=10)

    root.mainloop()

selected_city = ""

def show_plot_action(city_names, plot_type, save, root):
    # if type(city_names) == str:
    #     city_names = [city_names]
    question = "You want to save the " + plot_type + " of " + ", ".join(city_names) + "?"
    paths = [get_path(city_name) for city_name in city_names]
    dataframes = [get_dataframe(path) for path in paths]
    city_names = [get_name(path) for path in paths]

    if plot_type == "Compare two city's sunny hours (Bar)":
        if len(city_names) != 2:
            root.destroy()
            messagebox.showwarning("Warning", f"Please coose strictly 2 cities if you want this plot type !)")
        else:
            root.destroy()
            save = messagebox.askyesno("Save Plot", question)
            compare_sunny_hours(city_names, save, *dataframes)
    else:
        root.destroy()
        save = messagebox.askyesno("Save Plot", question)
        
    if plot_type == 'Avg. sunny hours':
        avg_sunny_hours(city_names, save, *dataframes)
    elif plot_type == 'Avg. Temperatures':
        #group_by_month = True
        avg_temps(city_names, save, *dataframes)
    elif plot_type == 'Avg. rainy days':
        avg_rainy_days(city_names, save, *dataframes)
    elif plot_type == 'Avg. windy days':
        avg_windy_days(city_names, save, *dataframes)
    elif plot_type == 'Compare precipitations (Pie)':
        compare_precipitation(city_names, save, *dataframes) 
    visual_main_menu()

# def show_plot_action(city_name, plot_type, save, root):
#     question = "You want to save the " + plot_type + " of " + city_name + "?"
#     save = messagebox.askyesno("Save Plot", question)
#     path = get_path(city_name)
#     dataframe = get_dataframe(path)
#     city_name = get_name(path)

#     root.destroy()
#     if plot_type == 'Avg. sunny hours':
#             avg_sunny_hours((city_name,), save, dataframe)
#     elif plot_type == 'Avg. Temperatures':
#             avg_temps((city_name,), save, dataframe)
#     elif plot_type == 'Avg. rainy days':
#             avg_rainy_days((city_name,), save, dataframe)
#     elif plot_type == 'Avg. windy days':
#             avg_windy_days((city_name,), save, dataframe)
#     visual_main_menu()

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

def get_name(path):
    return pd.read_csv(path, encoding='unicode_escape', header=None, nrows=1).values[0][0].split()[1]

def get_dataframe(path):
    return optimize_data(pd.read_csv(path, encoding = 'unicode_escape', header = 1 ,sep=";"))

def main():
    #console_main_menu()
    visual_main_menu()
    #data = optimize_data(pd.read_csv("stadat-kor0072-15.9.2.3-hu.csv", encoding = 'unicode_escape', header = 1 ,sep=";"))
    #avg_sunny_hours(("proba",), False, data)

main()