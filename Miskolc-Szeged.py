import calendar
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

def analize_data(miskolc, szeged):
    # # Resample the data to calculate average temperature per quarter year
    # miskolc_quarterly = miskolc.resample('Q', on='Date').mean()
    # szeged_quarterly = szeged.resample('Q', on='Date').mean()
    #mpl.style.use('dark_background')
    sns.set_style("darkgrid")
    # plt.plot(miskolc_quarterly.index, miskolc_quarterly.Average_temperature_C, label = 'Miskolc', color = 'red', 
    # linewidth = 2, marker = 'o', markersize = 6, markeredgecolor = 'black')
    # plt.plot(szeged_quarterly.index, szeged_quarterly.Average_temperature_C, label = 'Szeged', 
    # color = 'blue', linewidth = 2, marker = 's', markersize = 6, markeredgecolor = 'black')

    miskolc_dates = miskolc.Date[miskolc.Date.dt.month % 2 == 0]
    miskolc_temps = miskolc.Average_temperature_C[miskolc.Date.dt.month % 2 == 0]

    szeged_dates = szeged.Date[szeged.Date.dt.month % 2 == 0]
    szeged_temps = szeged.Average_temperature_C[szeged.Date.dt.month % 2 == 0]

    plt.plot(miskolc_dates, miskolc_temps, label = 'Miskolc', color = 'red', linewidth = 2, marker = 'o', markersize = 6, markeredgecolor = 'black')
    plt.plot(szeged_dates, szeged_temps, label = 'Szeged', color = 'blue', linewidth = 2, marker = 's', markersize = 6, markeredgecolor = 'black')

    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1.05), framealpha=0.5, fontsize=12)
    plt.ylabel('Avg. Temperature')
    plt.suptitle('Compare Avg. Temperature (2017-2021)')
    plt.savefig('Results/Miskolc_Szeged_Avg_temp_(2017-2021)plot.png')
    #plt.show()
    clearPlts()


    #sns.set_style("ticks")
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    plt.plot(miskolc.groupby(miskolc.Date.dt.strftime('%b'))['Rainy_days'].mean(), label='Miskolc', color='red', linewidth=2, marker='o', markersize=8, markeredgecolor='black')
    plt.plot(szeged.groupby(szeged.Date.dt.strftime('%b'))['Rainy_days'].mean(), label='Szeged', color='blue', linewidth=2, marker='s', markersize=8, markeredgecolor='black')

    plt.ylabel('Avg. Rainy days', fontsize=14)
    plt.xlabel('Month', fontsize=13)

    plt.xticks(range(12), month_names, fontsize=12, rotation=45)
    plt.yticks(fontsize=12)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), framealpha=0.5, fontsize=12)
    plt.suptitle('Compare Avg. rainy days (2017-2021)', fontsize=16)

    plt.savefig('Results/Miskolc_Szeged_Avg_rainy_days_(2017-2021)plot.png', dpi=150, bbox_inches='tight')
    #plt.show()
    clearPlts()


    fig = plt.figure(figsize=(15, 10))
    ax1 = plt.subplot2grid((1, 2), (0, 0))
    ax2 = plt.subplot2grid((1, 2), (0, 1))
    labels = calendar.month_name[1:]
    autopct = '%1.1f%%'
    values1 = miskolc.groupby(miskolc.Date.dt.month)['Precipitation_mm'].mean()
    values2 = szeged.groupby(szeged.Date.dt.month)['Precipitation_mm'].mean()
    colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'gray', 'pink', 'silver', 'gold', 'brown', 'purple']

    ax1.pie(values1, labels = labels,
               autopct = autopct, explode = [0.05]*12,
               shadow = True, startangle = 90, counterclock = False, colors = colors, pctdistance = 0.85)
    ax1.set_title('Monthly Average Precipitation in Miskolc', fontsize = 14, fontweight = 'bold')
    centre_circle = plt.Circle((0,0),0.7,fc = 'white')
    ax1.add_artist(centre_circle)
    rain_sum = miskolc.groupby(miskolc.Date.dt.month)['Precipitation_mm'].mean().sum()
    ax1.text(0, 0, f"Avg. rain per year: {rain_sum:.1f} mm", ha="center", va="center", fontweight = 'bold')

    ax2.pie(values2, labels = labels,
               autopct = autopct, explode=[0.05]*12,
               shadow = True, startangle = 90, counterclock = False, colors = colors, pctdistance = 0.85)
    ax2.set_title('Monthly Average Precipitation in Szeged', fontsize = 14, fontweight = 'bold')
    centre_circle = plt.Circle((0,0),0.7,fc = 'white')
    ax2.add_artist(centre_circle)
    rain_sum = szeged.groupby(szeged.Date.dt.month)['Precipitation_mm'].mean().sum()
    ax2.text(0, 0, f"Avg. rain per year: {rain_sum:.1f} mm", ha="center", va="center", fontweight = 'bold')
    ax1.set_aspect(0.85)
    ax2.set_aspect(0.85)
    plt.savefig('Results/Miskolc_Szeged_Precipitation(2017-2021)plot.png')
    #plt.show()
    clearPlts()

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

    table = table_grid.table(cellText=table_data, colLabels=["Month", "Avg. Difference"], cellLoc='center', colLoc='center')#loc
    table.auto_set_font_size(False)
    table.set_fontsize(10)
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

    # plt.plot(miskolc.Date, miskolc.Sunny_hours, label = 'Miskolc', color = 'red')
    # plt.plot(szeged.Date, szeged.Sunny_hours, label = 'Szeged', color = 'blue')
    # plt.ylabel('Avg. Temperature')
    # plt.suptitle('Compare Avg. Temperature (2017-2021)')
    # plt.show()
    # clearPlts()

    
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
             'Szeles napok száma, szélsebesség>=10 m/s ': 'Windy_days_windspeed>=10m/s'}
    data.rename(columns= column_labels, inplace=True)

    #optimize dtype:
    data['Average_temperature_C'] = data['Average_temperature_C'].apply(lambda x: float(x.replace(',', '.')))
    data['Max_temperature_C'] = data['Max_temperature_C'].apply(lambda x: float(x.replace(',', '.')))
    data['Min_temperature_C'] = data['Min_temperature_C'].apply(lambda x: float(x.replace(',', '.')))
    data['Sunny_hours'] = data['Sunny_hours'].apply(lambda x: float(x.split()[0].replace(',', '.')))
    data['Date'] = pd.to_datetime(data['Date'])
    data['Precipitation_mm'] = data['Precipitation_mm'].apply(lambda x: int(x))

    #reorder & delete unnecessary columns:
    data = data[['Date', 'Average_temperature_C', 'Max_temperature_C', 'Min_temperature_C', 'Sunny_hours', 'Rainy_days', 
    'Precipitation_mm', 'Windy_days_windspeed>=10m/s']]

    return data


def clearPlts():
    plt.clf()
    plt.close("all")

def main():
    miskolc = optimize_data(pd.read_csv("stadat-kor0075-15.9.2.6-hu.csv", encoding = 'unicode_escape', header = 1 ,sep=";"))
    szeged = optimize_data(pd.read_csv("stadat-kor0079-15.9.2.10-hu.csv", encoding = 'unicode_escape', header = 1 ,sep=";"))
    analize_data(miskolc, szeged)

main()