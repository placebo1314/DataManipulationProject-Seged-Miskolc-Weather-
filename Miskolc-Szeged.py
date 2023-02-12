import calendar
import os
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

def analize_data(miskolc, szeged):
    

    # set the figure size
    plt.figure(figsize=(10,5))

    # plot the Sunny_hours of Miskolc
    plt.plot(miskolc['Date'], miskolc['Sunny_hours'], label='Miskolc')

    # plot the Sunny_hours of Szeged
    plt.plot(szeged['Date'], szeged['Sunny_hours'], label='Szeged')

    # set the x-axis label
    plt.xlabel('Date')

    # set the y-axis label
    plt.ylabel('Sunny hours')

    # set the title
    plt.title('Comparison of Sunny Hours in Miskolc and Szeged')

    # add the legend
    plt.legend()

    #plt.show()
    clearPlts()

    # Adding a column for the difference in sunny hours
    fig = plt.figure(figsize=(10,8))
    table_grid = plt.subplot2grid((4,4), (0,3), rowspan=1, colspan=1)
    plot_grid = plt.subplot2grid((4,4), (0,0), rowspan=3, colspan=3)
    fig.set_facecolor('black')
    szeged['Sunny_hours_diff'] = szeged['Sunny_hours'] - miskolc['Sunny_hours']
    szeged['Sunny_hours_diff_pct'] = szeged['Sunny_hours_diff'] / miskolc['Sunny_hours'] * 100

    # Plotting the difference in sunny hours as a bar plot
    bar_colors = []
    for diff in szeged['Sunny_hours_diff']:
        if diff > 0:
            bar_colors.append('yellow')
        else:
            bar_colors.append('black')

    # Plotting the difference in sunny hours as a bar plot
    
    plot_grid.bar(szeged['Date'], szeged['Sunny_hours_diff'], label = 'Szeged', color = bar_colors, edgecolor = bar_colors, width = 5.8)
    plot_grid.set_xlabel('Date')
    plot_grid.set_ylabel('How much sunnier is Szeged than Miskolc?')
    plot_grid.grid(color='lightgray')
    plot_grid.set_facecolor('darkgray')
    plot_grid.spines['bottom'].set_color('white')
    plot_grid.spines['left'].set_color('white')
    plot_grid.spines['top'].set_color('white')
    plot_grid.spines['right'].set_color('white')
    plot_grid.yaxis.label.set_color('white')
    plot_grid.xaxis.label.set_color('white')
    plot_grid.tick_params(axis='both', colors='white')

    formatter = ticker.FuncFormatter(format_yaxis)
    plot_grid.yaxis.set_major_formatter(formatter)
# Calculate the mean difference in sunny hours for each month
    monthly_mean = szeged.groupby(szeged.Date.dt.month)['Sunny_hours_diff_pct'].mean()

    table_data = []
    for month, pct in zip(monthly_mean.index, monthly_mean.values):
        row = [calendar.month_abbr[month], f"+{pct:.1f} %"]
        table_data.append(row)

    table_data_rows = len(table_data)
    cell_colors = [['lightgray', 'lightgray'] for i in range(table_data_rows)]

    table = table_grid.table(cellText=table_data, colLabels=["Month", "Avg. Difference"], cellLoc='center', colLoc='center', cellColours=cell_colors)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    text = table[0, 1].get_text()
    text.set_fontweight('bold')
    for i in range(table_data_rows+1):
        text = table[i, 0].get_text()
        text.set_fontweight('bold')
    table.scale(1, 1.5)
    table.auto_set_column_width(col=0)
    table.auto_set_column_width(col=1)
    table_grid.axis('tight')
    table_grid.axis('off')

    text = 'Placeholder _____ _____\nPlaceholder _____ _____\nPlaceholder _____ _____'
    plot_grid.annotate(text, xy=(-0.12, 1.12), xycoords='axes fraction', fontsize=14,
             bbox=dict(boxstyle="round", fc=(1, 1, 0.902), alpha=0.5),
             horizontalalignment='left', verticalalignment='top')
    plot_grid.yaxis.set_major_locator(ticker.MultipleLocator(10))
    plt.savefig('Newplot.png', dpi=150, bbox_inches='tight')
    plt.show()

    
def format_yaxis(x, pos):
    sign = ""
    if x > 0:
        sign = "+"
    return f"{sign}{x:.0f} hours"

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
             'Szeles napok száma, szélsebesség>=10 m/s ': 'Windy_days_windspeed>=10m/s'}
    data.rename(columns= column_labels, inplace=True)

    #optimize dtype:
    data['Average_temperature_C'] = data['Average_temperature_C'].apply(lambda x: float(x.replace(',', '.')))
    data['Max_temperature_C'] = data['Max_temperature_C'].apply(lambda x: float(x.replace(',', '.')))
    data['Min_temperature_C'] = data['Min_temperature_C'].apply(lambda x: float(x.replace(',', '.')))
    data['Sunny_hours'] = data['Sunny_hours'].apply(lambda x: float(x.split()[0].replace(',', '.')) if x!= ".." else 0)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Precipitation_mm'] = data['Precipitation_mm'].apply(lambda x: int(x))

    #reorder & delete unnecessary columns:
    data = data[['Date', 'Average_temperature_C', 'Max_temperature_C', 'Min_temperature_C', 'Sunny_hours', 'Rainy_days', 
    'Precipitation_mm', 'Windy_days_windspeed>=10m/s']]

    return data


def clearPlts():
    plt.clf()
    plt.close("all")

def avg_temps(city_names, is_save, *cities):
    sns.set_style("darkgrid")
    for c in range(len(cities)):
        city_dates = cities[c].Date[cities[c].Date.dt.month % 2 == 0]
        city_temps = cities[c].Average_temperature_C[cities[c].Date.dt.month % 2 == 0]
        plt.plot(city_dates, city_temps, label = city_name[c], linewidth = 2, marker = 'o', markersize = 6, markeredgecolor = 'black')
# plt.plot(city2_dates, city2_temps, label = 'Szeged', color = 'blue', linewidth = 2, marker = 's', markersize = 6, markeredgecolor = 'black')
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1.05), framealpha=0.5, fontsize=12)
    plt.ylabel('Avg. Temperature')
    plt.suptitle('Avg. Temperature (2017-2021)')
    if is_save:
        name = ""
        for i in city_names:
            name += i + "_"
        plt.savefig("Results/" + name + "Avg_temp_(2017-2021)plot.png")
        print("Saved file: \nResults/" + name + "Avg_temp_(2017-2021)plot.png")
    plt.show()
    clearPlts()
    # # Resample the data to calculate average temperature per quarter year
    # miskolc_quarterly = miskolc.resample('Q', on='Date').mean()
    # szeged_quarterly = szeged.resample('Q', on='Date').mean()
    #mpl.style.use('dark_background')
    #sns.set_style("darkgrid")
    # plt.plot(miskolc_quarterly.index, miskolc_quarterly.Average_temperature_C, label = 'Miskolc', color = 'red', 
    # linewidth = 2, marker = 'o', markersize = 6, markeredgecolor = 'black')
    # plt.plot(szeged_quarterly.index, szeged_quarterly.Average_temperature_C, label = 'Szeged', 
    # color = 'blue', linewidth = 2, marker = 's', markersize = 6, markeredgecolor = 'black')

def avg_sunny_hours(city_names, is_save, *cities):
    for c in range(len(cities)):
        plt.plot(cities[c].Date, cities[c].Sunny_hours, label = city_name[c])
    plt.ylabel('Sunny Hours')
    plt.suptitle('Avg. Sunny Hours (2017-2021)')
    plt.show()
    if is_save:
        name = ""
        for i in city_names:
            name += i + "_"
        plt.savefig("Results/" + name + "Avg_temp_(2017-2021)plot.png")
        print("Saved file: \nResults/" + name + "Precipitation_(2017-2021)plot.png")
    clearPlts()

def avg_rainy_days(city_names, is_save, *cities):
    #sns.set_style("ticks")
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for c in range(len(cities)):
        plt.plot(cities[c].groupby(cities[c].Date.dt.strftime('%b'))['Rainy_days'].mean(), label=city_names[c], linewidth=2, marker='o', markersize=8, markeredgecolor='black')
    #plt.plot(szeged.groupby(szeged.Date.dt.strftime('%b'))['Rainy_days'].mean(), label='Szeged', color='blue', linewidth=2, marker='s', markersize=8, markeredgecolor='black')

    plt.ylabel('Rainy days', fontsize=14)
    plt.xlabel('Month', fontsize=13)

    plt.xticks(range(12), month_names, fontsize=12, rotation=45)
    plt.yticks(fontsize=12)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), framealpha=0.5, fontsize=12)
    plt.suptitle('Avg. rainy days (2017-2021)', fontsize=16)
    if is_save:
        name = ""
        for i in city_names:
            name += i + "_"
        plt.savefig("Results/" + name + "Avg_temp_(2017-2021)plot.png")
        print("Saved file: \nResults/" + name + "Avg_rainy_days_(2017-2021)plot.png")
    plt.show()
    clearPlts()

def compare_precipitation(city1_name, city2_name, is_save, city1_data, city2_data):
    fig = plt.figure(figsize=(15, 10))
    ax1 = plt.subplot2grid((1, 2), (0, 0))
    ax2 = plt.subplot2grid((1, 2), (0, 1))
    labels = calendar.month_name[1:]
    autopct = '%1.1f%%'
    values1 = city1_data.groupby(city1_data.Date.dt.month)['Precipitation_mm'].mean()
    values2 = city2_data.groupby(city2_data.Date.dt.month)['Precipitation_mm'].mean()
    colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'gray', 'pink', 'silver', 'gold', 'brown', 'purple']

    ax1.pie(values1, labels = labels,
               autopct = autopct, explode = [0.05]*12,
               shadow = True, startangle = 90, counterclock = False, colors = colors, pctdistance = 0.85)
    ax1.set_title('Monthly Average Precipitation in' + city1_name, fontsize = 14, fontweight = 'bold')
    centre_circle = plt.Circle((0,0),0.7,fc = 'white')
    ax1.add_artist(centre_circle)
    rain_sum = city1_data.groupby(city1_data.Date.dt.month)['Precipitation_mm'].mean().sum()
    ax1.text(0, 0, f"Avg. rain per year: {rain_sum:.1f} mm", ha="center", va="center", fontweight = 'bold')

    ax2.pie(values2, labels = labels,
               autopct = autopct, explode=[0.05]*12,
               shadow = True, startangle = 90, counterclock = False, colors = colors, pctdistance = 0.85)
    ax2.set_title('Monthly Average Precipitation in ' + city2_name, fontsize = 14, fontweight = 'bold')
    centre_circle = plt.Circle((0,0),0.7,fc = 'white')
    ax2.add_artist(centre_circle)
    rain_sum = city2_data.groupby(city2_data.Date.dt.month)['Precipitation_mm'].mean().sum()
    ax2.text(0, 0, f"Avg. rain per year: {rain_sum:.1f} mm", ha="center", va="center", fontweight = 'bold')
    ax1.set_aspect(0.85)
    ax2.set_aspect(0.85)
    if is_save:
        name = city1_name + "_" + city2_name
        plt.savefig("Results/" + name + "Avg_temp_(2017-2021)plot.png")
        print("Saved file: \nResults/" + name + "_Precipitation(2017-2021)CirclePlots.png")
    plt.show()
    clearPlts()

def menu():
    # list_of_cities= {'Budapest': 'kor0070', 'Debrecen': 'kor0071', 'Győr': 'kor0072', 
    # 'Kecskemét': 'kor0073', 'Kékestető': 'kor0074', 'Miskolc': 'kor0075', 'Pogány': 'kor0077',
    # 'Siófok': 'kor0078', 'Szeged': 'kor0079', 'Szombathely': 'kor0080'}
    list_of_cities= {'1': 'Budapest', '2': 'Debrecen', '3': 'Győr', 
    '4': 'Kecskemét', '5': 'Kékestető', '6': 'Miskolc', '7': 'Pogány',
    '8': 'Siófok', '9': 'Szeged', '10': 'Szombathely'}
    x = ""
    while x != "0":
        print("Choose an option, and push Enter. \n")
        x = input("'1': Work with a city, '2': Compare two cities ('0': Quit) \n")
        if x == "1":
            single_menu(list_of_cities)
        elif x == "2":
            compare_menu(list_of_cities)
        elif x == "0":
            break
        else:
            clr_scr()
            print("  Please choose a valid option !")

def single_menu(list_of_cities):
    plot_types= {'1': 'Avg. sunny hours', '2': 'Avg. Temperatures', '3': 'Avg. rainy days'}
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
            avg_sunny_hours((city_name),  save, dataframe)
        case 'Avg. Temperatures':
            avg_temps((city_name),  save, dataframe)
        case 'Avg. rainy days':
            avg_rainy_days((city_name),  save, dataframe)

def compare_menu(list_of_cities):
    dict_of_aviable_cities = list_of_cities.copy()
    plot_types= {'1': 'Avg. sunny days', '2': 'Avg. Temperatures', '3': 'Avg. rainy days', '4': 'Compare precipitations'}
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
        case 'Avg. sunny days':
            avg_sunny_hours((city_name1, city_name2),  save, dataframe1, dataframe2)
        case 'Avg. Temperatures':
            avg_temps((city_name1, city_name2),  save, dataframe1, dataframe2)
        case 'Avg. rainy days':
            avg_rainy_days((city_name1, city_name2),  save, dataframe1, dataframe2)
        case 'Compare precipitations':
            compare_precipitation(city_name1, city_name2, save, dataframe1, dataframe2)


def get_path(city):
    list_of_cities= {'Budapest': 'kor0070', 'Debrecen': 'kor0071', 'Győr': 'kor0072', 
    'Kecskemét': 'kor0073', 'Kékestető': 'kor0074', 'Miskolc': 'kor0075', 'Pogány': 'kor0077',
    'Siófok': 'kor0078', 'Szeged': 'kor0079', 'Szombathely': 'kor0080'}
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
    # city1 = optimize_data(pd.read_csv("stadat-kor0075-15.9.2.6-hu.csv", encoding = 'unicode_escape', header = 1 ,sep=";"))
    # city2 = optimize_data(pd.read_csv("stadat-kor0079-15.9.2.10-hu.csv", encoding = 'unicode_escape', header = 1 ,sep=";"))
    # #analize_data(city1, city2)
    # city1_name = pd.read_csv("stadat-kor0075-15.9.2.6-hu.csv", encoding='unicode_escape', header=None, nrows=1).values[0][0].split()[1]
    
    menu()

main()