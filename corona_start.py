#- importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



#- function index dates
def convert_dates_to_python(df):
    new_index = []
    new_index[0:4] = df.index[0:4]
    new_index[4:] = pd.to_datetime(df.index[4:])
    new_index[4:] = [x.date() for x in new_index[4:]]
    #print(temp_index)
    df.index = new_index
    return df

#-

#-
def return_country(df, country, region=False):
    if country not in df.loc["Country/Region"].values:
        print("No such country value in Country/Region: ", country)
        return None

    if not region:
        print("region false")
        mask = (df.loc["Country/Region"] == country) & (df.loc["Province/State"].isna())
        column_number = mask[mask == True].index[0]
        country_series = df[column_number]
        country_series.name = country_series.iloc[1]

    else:
        mask = (df.loc["Country/Region"] == country) & (df.loc["Province/State"] == region)
        column_number = mask[mask == True].index[0]
        country_series = df[column_number]
        country_series.name = country_series.iloc[1], "/", country_series.iloc[0]
        # print(country_series.iloc[0])

    country_series.drop(country_series.iloc[0:5].index, inplace=True)
    return country_series

#-

#- importing data

url_humdata = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv"

#-

#-
df = pd.read_csv(url_humdata)
df = df.T
#-
df = convert_dates_to_python(df)

print(df.iloc[1])
#-
df.iloc[0:5]


quebec = return_country(df, "Canada", "Quebec")
print(quebec)

#-

#-

poland = return_country(df, "Poland")
print(poland)

#-
plt.figure()

plt.plot(poland)
plt.plot(quebec)
#-
print(df)
#-

pol = return_country(df, "Poland")

#-

def plot_days_from(df, list_countries, amount_days):
    list_series = []
    for c in list_countries:
        print(c)
        country = return_country(df, c)
        print(country.name)
        country = country[-amount_days:]
        list_series.append(country)

    plt.figure()
    for co in list_series:
        plt.plot(co)

#-
plot_days_from(df, ["Poland"], 30)


#-

mask_ab_zero = poland > 0
poland_ab_zero = poland[mask_ab_zero]
poland_ab_zero
#-
poland_ab_zero.plot()
#-
#-
days_poland = len(poland_ab_zero)

#-
poland_ab_zero.plot(logy=True, legend=False)

#-

poland_ab_zero.plot(loglog=True, legend=False)


#- 
def preprocess_country(country_name, df):

    mask = df.loc["Country/Region"] == country_name
    column_number = mask[mask == True].index[0]
    country = df[column_number]

    new_index = []
    new_index[0:4] = country.index[0:4]
    new_index[4:] = pd.to_datetime(country.index[4:])
    country.index = new_index
    country.drop(country.iloc[[0,2,3]].index, inplace=True)
    country.name = country.iloc[0]
    country = country[1:]

    return country


#-

italy = preprocess_country("Italy", df)
print(italy.name)
#-
def ret_starting_from(series, starting_number):
    mask = series >= starting_number
    series_mask = series[mask]
    series_mask = series_mask[:days_poland]
    series_mask.reset_index(drop=True, inplace=True)
    return series_mask

#-

poland_toplot = preprocess_country("Poland", df)
poland_ab_zero_plot = ret_starting_from(poland_toplot, 1)
#-
italy_ab_zero = ret_starting_from(italy, 1)
# italy_ab_zero.plot(logy=True)

print(italy_ab_zero[22])

italy_ab_zero[:days_poland].plot(logy=True)

#-
print(italy_ab_zero[:days_poland])
italy_shorter = italy_ab_zero[:days_poland]
italy_shorter.plot()
#-
df_final = pd.DataFrame([poland_ab_zero, italy_shorter])

df_final
#-

# plt.figure(figsize=(12,5))

ax1 = poland_ab_zero_plot.plot(color='red', grid=True)
ax2 = italy_shorter.plot(color='blue', grid=True)

# h1, l1 = ax1.get_legend_handles_labels()
# h2, l2 = ax2.get_legend_handles_labels()


# plt.legend(h1+h2, l1+l2, loc=2)
plt.show()


#-
print(italy_shorter.index)
print(poland_ab_zero_plot.index)
#-
