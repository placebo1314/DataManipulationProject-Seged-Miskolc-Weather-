import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from ttkthemes import ThemedStyle

from Work_with_dataframes import get_path, get_name, get_dataframe
from Plotting import avg_sunny_hours, avg_temps, avg_rainy_days, avg_windy_days, compare_precipitation, compare_sunny_hours, avg_precipitation

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

def visual_single_menu():
    list_of_cities= {'1': 'Budapest', '2': 'Debrecen', '3': 'Győr', 
    '4': 'Kecskemét', '5': 'Kékestető', '6': 'Miskolc', '7': 'Pogány (Pécs)',
    '8': 'Siófok (Balaton)', '9': 'Szeged', '10': 'Szombathely'}

    def city_action(city):
        plot_types= {'1': 'Avg. sunny hours', '2': 'Avg. Temperatures', '3': 'Avg. rainy days', '4': 'Avg. windy days', '5': 'Avg. precipitations'}
        selected_city = [city]
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

def visual_compare_menu():
    list_of_cities= {'1': 'Budapest', '2': 'Debrecen', '3': 'Győr', 
    '4': 'Kecskemét', '5': 'Kékestető', '6': 'Miskolc', '7': 'Pogány (Pécs)',
    '8': 'Siófok (Balaton)', '9': 'Szeged', '10': 'Szombathely'}
    
    selected_cities_indexes = []
    
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
        plot_types= {'1': 'Avg. sunny hours', '2': 'Avg. Temperatures', '3': 'Avg. rainy days', '4': 'Avg. precipitations', '5': 'Compare precipitations (Pie)', 
        '6': "Compare two city's sunny hours (Bar)", '7': 'Avg. windy days'}
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

    selected_option = tk.StringVar(value="All years and months")
    option_list = ["All years and months", "All quarter year", "Group by months"]

    # Add the combobox widget to the window
    option_label = ttk.Label(root, text="Select an option:")
    option_label.pack(pady=10)
    option_combobox = ttk.Combobox(root, textvariable=selected_option, values=option_list, state="readonly")
    option_combobox.pack()

    for key, value in plot_types.items():
        button = ttk.Button(root, text = value, command = lambda city_name=city_name, plot_type = value: show_plot_action(city_name, plot_type, selected_option.get(), False, root))
        button.pack()

    back_button = ttk.Button(root, text="Back", command = back_action)
    back_button.pack(side = tk.BOTTOM, pady=10)

    root.mainloop()

def show_plot_action(city_names, plot_type, selected_option, save, root):
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
        avg_sunny_hours(city_names, selected_option, save, *dataframes)
    elif plot_type == 'Avg. Temperatures':
        avg_temps(city_names, selected_option, save, *dataframes)
    elif plot_type == 'Avg. rainy days':
        avg_rainy_days(city_names, selected_option, save, *dataframes)
    elif plot_type == 'Avg. windy days':
        avg_windy_days(city_names, selected_option, save, *dataframes)
    elif plot_type == 'Compare precipitations (Pie)':
        compare_precipitation(city_names, save, *dataframes)
    elif plot_type == 'Compare precipitations (Pie)':
        compare_precipitation(city_names, save, *dataframes)
    elif plot_type == 'Avg. precipitations':
        avg_precipitation(city_names, save, *dataframes)
    visual_main_menu()