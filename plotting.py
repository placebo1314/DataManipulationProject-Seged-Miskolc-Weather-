import calendar
import seaborn as sns
import matplotlib.ticker as ticker
from colorama import Fore
import matplotlib.pyplot as plt
import matplotlib as mpl
import tkinter as tk
from tkinter import messagebox

def set_dark_bg():
    mpl.style.use('dark_background')
    sns.set_palette('bright')

def save_message(city_names, plot_type):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("File saved", f"Saved file: \nResults/{city_names}{plot_type}_(2017-2021)plot.png")

def avg_temps(city_names, selected_option, is_save, *cities):
    set_dark_bg()
    colors = ['red', 'blue', 'purple', 'green']
    for c in range(len(cities)):
        color = colors[c]
        marker = 'o' if (c % 2 == 0) else 's'
        if selected_option == "All years and months":
            # city_dates = cities[c].Date[cities[c].Date.dt.month % 2 == 0]
            # city_temps = cities[c].Average_temperature_C[cities[c].Date.dt.month % 2 == 0]
            city_dates = cities[c].Date
            city_temps = cities[c].Average_temperature_C
        elif selected_option == "All quarter year":
            city_quarterly = cities[c].resample('Q', on='Date').mean()
            city_dates = city_quarterly.index
            city_temps =city_quarterly.Average_temperature_C
        else:
            #city_dates = calendar.month_name[1:]
            city_dates = [calendar.month_name[i][:3] for i in range(1, 13)]
            city_temps = cities[c].groupby(cities[c].Date.dt.month)['Average_temperature_C'].mean()

        plt.plot(city_dates, city_temps, label = city_names[c], linewidth = 2, marker = marker, color = color, markersize = 6, markeredgecolor = 'black')
    
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), framealpha=0.5, fontsize=12)
    plt.legend(loc='upper right', bbox_to_anchor=(1.06, 1.05), framealpha=0.5, fontsize=10)
    plt.ylabel('Avg. Temperature')
    plt.suptitle('Avg. Temperature (2017-2021)')
    if is_save:
        name = '-'.join(city_names)
        save_message(name, "_Avg_temp")
        plt.savefig("Results/" + name + "_Avg_temp_(2017-2021)plot.png")
    plt.show()
    clearPlts()

def avg_sunny_hours(city_names, selected_option, is_save, *cities):
    set_dark_bg()
    lack_of_data = False
    lack_in_city = ""
    colors = ['red', 'blue', 'purple', 'green']
    for c in range(len(cities)):
        if (cities[c].Sunny_hours == -1).any():
            lack_of_data = True
            lack_in_city += city_names[c]
        color = colors[c]
        if selected_option == "All years and months":
            city_dates = cities[c].Date
            city_temps = cities[c].Sunny_hours
        elif selected_option == "All quarter year":
            city_quarterly = cities[c].resample('Q', on='Date').mean()
            city_dates = city_quarterly.index
            city_temps =city_quarterly.Sunny_hours
        else:
            city_dates = [calendar.month_name[i][:3] for i in range(1, 13)]
            city_temps = cities[c].groupby(cities[c].Date.dt.month)['Sunny_hours'].mean()

        plt.plot(city_dates, city_temps, label = city_names[c], color = color)
    plt.ylabel('Sunny Hours')
    plt.suptitle('Avg. Sunny Hours (2017-2021)')
    plt.legend(loc='center left', bbox_to_anchor = (0.93, 0.97), framealpha = 0.5, fontsize = 10)
    
    if lack_of_data:
        #print(f"\n {Fore.RED}Not enough data in", lack_in_city + ". (Where lack of data display -1 on the diagram !)" + "\033[0m")
        messagebox.showwarning("Warning", f"Not enough data in {lack_in_city}. ( Sorry, but on the ksh.hu not enogh 'Sunny_hours' data! :( )")
    plt.show()

    if is_save:
        name = '-'.join(city_names)
        save_message(name, "avg_sunny_hours")
        plt.savefig("Results/" + name + "avg_sunny_hours_(2017-2021)plot.png")
    clearPlts()

def avg_rainy_days(city_names, selected_option, is_save, *cities):
    #sns.set_style("ticks")
    set_dark_bg()
    colors = ['red', 'blue', 'purple', 'green']
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for c in range(len(cities)):
        color = colors[c]
        marker = 'o' if (c+1 % 2 == 0) else 's'
        if selected_option == "All years and months":
            city_dates = cities[c].Date
            city_temps = cities[c].Rainy_days
        elif selected_option == "All quarter year":
            city_quarterly = cities[c].resample('Q', on='Date').mean()
            city_dates = city_quarterly.index
            city_temps =city_quarterly.Rainy_days
        else:
            city_dates = [calendar.month_name[i][:3] for i in range(1, 13)]
            city_temps = cities[c].groupby(cities[c].Date.dt.month)['Rainy_days'].mean()
        #plt.plot(cities[c].groupby(cities[c].Date.dt.strftime('%b'))['Rainy_days'].mean(), label=city_names[c], linewidth=2, marker=marker, markersize=8, markeredgecolor='black', color = color)
        plt.plot(city_dates, city_temps, label=city_names[c], linewidth=2, marker=marker, markersize=8, markeredgecolor='black', color = color)

    plt.ylabel('Rainy days', fontsize=14)
    plt.xlabel('Month', fontsize=13)

    plt.xticks(range(12), month_names, fontsize=12, rotation=45)
    plt.yticks(fontsize=12)

    plt.legend(loc = 'center left', bbox_to_anchor = (0.93, 0.97), framealpha = 0.5, fontsize = 10)
    plt.suptitle('Avg. rainy days (2017-2021)', fontsize=16)
    if is_save:
        name = '-'.join(city_names)
        save_message(name, "_Avg_rainy_days")
        plt.savefig("Results/" + name + "_Avg_rainy_days_(2017-2021)plot.png")
    plt.show()
    clearPlts()

def compare_precipitation(city_names, is_save, *dataframes):
    set_dark_bg()
    num_cities = len(city_names)
    num_rows = (num_cities - 1) // 2 + 1
    fig, axs = plt.subplots(num_rows, 2, figsize=(15, 10*num_rows))
    axs = axs.flatten()

    colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'darkgray', 'gray', 'orange', 'silver', '#2BC20E', 'brown', 'purple']
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    labels = month_names
    autopct = '%1.1f%%'

    for i, (city_name, city_data) in enumerate(zip(city_names, dataframes)):
        ax = axs[i]
        values = city_data.groupby(city_data.Date.dt.month)['Precipitation_mm'].mean()
        ax.pie(values, labels=labels, autopct=autopct, explode=[0.05]*12,
               shadow=True, startangle=90, counterclock=False, colors=colors, pctdistance=0.85)
        ax.set_title('Monthly Average Precipitation in ' + city_name, fontsize=14, fontweight='bold')
        centre_circle = plt.Circle((0, 0), 0.7, fc='black')
        ax.add_artist(centre_circle)
        rain_sum = city_data.groupby(city_data.Date.dt.month)['Precipitation_mm'].mean().sum()
        ax.text(0, -1.25, f"Avg. rain per year: {rain_sum:.1f} mm", ha="center", va="center", fontweight='bold')
        ax.set_aspect(0.85)

    for i in range(num_cities, num_rows * 2):
        fig.delaxes(axs[i])

    if is_save:
        name = '-'.join(city_names)
        save_message(name, "Precipitation")
        plt.savefig("Results/" + name + "_Precipitation(2017-2021)CirclePlots.png")
    plt.show()
    clearPlts()

def compare_sunny_hours(city_names, is_save, *dataframes):
        set_dark_bg()
        # Adding a column for the difference in sunny hours
        lack_of_data = False
        lack_in_city = ""
        city1_data = dataframes[0]
        city2_data = dataframes[1]
        city1_name = city_names[0]
        city2_name = city_names[1]
        for c in range(2):
            if (dataframes[c].Sunny_hours == -1).any():
                lack_of_data = True
                lack_in_city += city_names[c]
        fig = plt.figure(figsize=(10,8))
        table_grid = plt.subplot2grid((4,4), (0,3), rowspan=1, colspan=1)
        plot_grid = plt.subplot2grid((4,4), (0,0), rowspan=3, colspan=3)
        fig.set_facecolor('black')
        city1_data['Sunny_hours_diff'] = city1_data['Sunny_hours'] - city2_data['Sunny_hours']
        city1_data['Sunny_hours_diff_pct'] = city1_data['Sunny_hours_diff'] / city2_data['Sunny_hours'] * 100

        # Plotting the difference in sunny hours as a bar plot
        bar_colors = []
        for diff in city1_data['Sunny_hours_diff']:
            if diff > 0:
                bar_colors.append('yellow')
            else:
                bar_colors.append('black')

        # Plotting the difference in sunny hours as a bar plot
        plot_grid.bar(city1_data['Date'], city1_data['Sunny_hours_diff'], label = city1_name, color = bar_colors, edgecolor = bar_colors, width = 5.8)
        plot_grid.set_xlabel('Date')
        plot_grid.set_ylabel(city1_name)
        plot_grid.grid(color='lightgray')
        plot_grid.set_facecolor('darkgray')
        smokewhite = (245/255, 245/255, 245/255)
        plot_grid.spines['bottom'].set_color(smokewhite)
        plot_grid.spines['left'].set_color(smokewhite)
        plot_grid.spines['top'].set_color(smokewhite)
        plot_grid.spines['right'].set_color(smokewhite)
        plot_grid.yaxis.label.set_color(smokewhite)
        plot_grid.xaxis.label.set_color(smokewhite)
        plot_grid.tick_params(axis='both', colors=smokewhite)
        plt.suptitle(f"How much sunnier is {city1_name} than {city2_name} ?", fontsize = 16, color = smokewhite)

        formatter = ticker.FuncFormatter(format_yaxis)
        plot_grid.yaxis.set_major_formatter(formatter)
        # Calculate the mean difference in sunny hours for each month
        monthly_mean = city1_data.groupby(city1_data.Date.dt.month)['Sunny_hours_diff_pct'].mean()

        table_data = []
        for month, pct in zip(monthly_mean.index, monthly_mean.values):
            row = [calendar.month_abbr[month], f"+{pct:.1f} %"]
            table_data.append(row)

        table_data_rows = len(table_data)
        cell_colors = [['darkgray', 'darkgray'] for i in range(table_data_rows)]

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
    
        if lack_of_data:
            #print(f"\n {Fore.RED}Not enough data in", lack_in_city + ". (Where lack of data display -1 on the diagram !)" + "\033[0m")
            messagebox.showwarning("Warning", f"Not enough data in {lack_in_city}. ( Sorry, but on the ksh.hu not enogh 'Sunny_hours' data! :( )")
    
        if is_save:
            name = '-'.join(city_names)
            save_message(name, "_compare_sunny_hours")
            plt.savefig("Results/" + name + "_compare_sunny_hours_(2017-2021)plot.png")
        plt.show()

def avg_precipitation(city_names, selected_option, is_save, *cities):
    #sns.set_style("ticks")
    set_dark_bg()
    colors = ['red', 'blue', 'purple', 'green']
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for c in range(len(cities)):
        color = colors[c]
        marker = 'o' if (c+1 % 2 == 0) else 's'
        if selected_option == "All years and months":
            city_dates = cities[c].Date
            city_temps = cities[c].Precipitation_mm
        elif selected_option == "All quarter year":
            city_quarterly = cities[c].resample('Q', on='Date').mean()
            city_dates = city_quarterly.index
            city_temps =city_quarterly.Precipitation_mm
        else:
            city_dates = [calendar.month_name[i][:3] for i in range(1, 13)]
            city_temps = cities[c].groupby(cities[c].Date.dt.month)['Precipitation_mm'].mean()
        plt.plot(city_dates, city_temps, label=city_names[c], linewidth=2, marker=marker, markersize=8, markeredgecolor='black', color = color)

    plt.ylabel('Precipitation (mm)', fontsize=14)
    #plt.xlabel('Month', fontsize=13)

    plt.xticks(range(12), month_names, fontsize=12, rotation=45)
    plt.yticks(fontsize=12)

    plt.legend(loc = 'center left', bbox_to_anchor = (0.93, 0.97), framealpha = 0.5, fontsize = 10)
    plt.suptitle('Avg. Precipitation (mm) (2017-2021)', fontsize=16)
    if is_save:
        name = '-'.join(city_names)
        save_message(name, "_Avg_Precipitation_mm")
        plt.savefig("Results/" + name + "_Avg_Precipitation_mm_(2017-2021)plot.png")
    plt.show()
    clearPlts()

def avg_windy_days(city_names, selected_option, is_save, *cities):
    set_dark_bg()
    colors = ['red', 'blue', 'purple', 'green']
    for c in range(len(cities)):
        color = colors[c]
        marker = 'o' if (c+1 % 2 == 0) else 's'
        if selected_option == "All years and months":
            city_dates = cities[c].Date
            city_temps = cities[c]['Windy_days_windspeed>=10m/s']
        elif selected_option == "All quarter year":
            city_quarterly = cities[c].resample('Q', on='Date').mean()
            city_dates = city_quarterly.index
            city_temps =city_quarterly['Windy_days_windspeed>=10m/s']
        else:
            city_dates = [calendar.month_name[i][:3] for i in range(1, 13)]
            city_temps = cities[c].groupby(cities[c].Date.dt.month)['Windy_days_windspeed>=10m/s'].mean()
        plt.plot(city_dates, city_temps, label = city_names[c], linewidth = 2, marker = marker, markersize = 6, markeredgecolor = 'black', color = color)
    plt.legend(loc = 'upper right', bbox_to_anchor = (0.93, 0.97), framealpha = 0.5, fontsize = 10)
    plt.ylabel('Avg. Windy days')
    plt.suptitle('Avg. Windy days (2017-2021)')
    if is_save:
        name = '-'.join(city_names)
        save_message(name, "_Avg_Windy_days")
        plt.savefig("Results/" + name + "_Avg_Windy_days_(2017-2021)plot.png")
    plt.show()
    clearPlts()

def clearPlts():
    plt.clf()
    plt.close("all")

def format_yaxis(x, pos):
    sign = ""
    if x > 0:
        sign = "+"
    return f"{sign}{x:.0f} hours"