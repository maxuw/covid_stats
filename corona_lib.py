#- importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#-

#-

def incremental_change(previous_day, today_newcases, double=False):
    # if previous_day == 0 or today_newcases == 0:
        # return(0)
    # else:
    if double==False:
        if previous_day == 0:
            number = np.NaN
        else:
            number = today_newcases/previous_day
    else:
        if today_newcases == 0:
            number = np.NaN
        else:
            number = previous_day/today_newcases

    return number

#-

def increase_series(series_absolute, double=False):
    diff = series_absolute.diff()
    series_new = [0]


    for n in range(len(series_absolute)-1):
        i = incremental_change(series_absolute[n], diff[n+1], double)
        series_new.append(i)

    series_new = pd.Series(series_new)
    series_new.index = series_absolute.index
    return series_new

#-
def increase_df(df, double=False):
    df_ = pd.DataFrame()
    for (columnName, columnData) in df.iteritems():

        inc_series = increase_series(columnData, double)
        df_[columnName] = inc_series
    return df_



#-
def return_from_infections(df, start_number):

    df_ = pd.DataFrame()

    # for (columnName, columnData) in df.iteritems():

    #     country_ = ret_starting_from(columnData, start_number)

    #     df_ = pd.merge(df_, country_, how="outer")
        # if (len(df_) >= len(contry)):
        # df_[columnName] = country_

        # print(country_)
        # print(columnData)
    dfs = [ret_starting_from(columnData, start_number) for columnName, columnData in df.iteritems()]
    df_ = pd.concat(dfs, axis=1)
    # return(dfs)
        # pd.concat(objs, axis=0, join='outer', ignore_index=False, keys=None,
          # levels=None, names=None, verify_integrity=False, copy=True)


    return df_
#-



#-
def ret_starting_from(series, starting_number):
    mask = series >= starting_number
    series_mask = series[mask]
    # series_mask = series_mask[:starting_number]
    series_mask.reset_index(drop=True, inplace=True)
    return series_mask


#-
def return_country(df, country, region=False):
    if country not in df.loc["Country/Region"].values:
        print("No such country value in Country/Region: ", country)
        return None

    if not region:
        # print("region false")
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

    country_series_ = country_series.drop(country_series.iloc[0:5].index, inplace=False)
    return country_series_


#-
def initial_preprocess(df):
    df_ = pd.DataFrame()
    for column_name, column_content in df.iteritems():

    # series_temp = pd.Series(dtype = np.float64)

        if type(column_content[0]) == str:
            name = column_content[1] + "/" + column_content[0]
            # print(series_temp.name)

        else:
            name = column_content[1]

        series_temp = pd.Series(data=column_content[4:], name=name)
        df_[name] = series_temp
    return df_

#-
def df_initial_clean_up(df, list_countries):

    df_ = pd.DataFrame()

    list_series = []
    for c in list_countries:

        if type(c) == tuple:
            country = return_country(df, c[0], c[1])
            country_name = c[0] + "/" + c[1]
            df_[country_name] = country
        
        elif type(c)  == str:
            country = return_country(df, c)
            df_[c] = country

            # print(country.name)
        
    return df_

#-
def df_initial_clean_up_whole(df):

    df_ = pd.DataFrame()

    # dfs = [ret_starting_from(columnData, start_number) for columnName, columnData in df.iteritems()]

    for column_name, content in df.iteritems():
        country = return_country(df, column_name)
        df_[column_name] = country

    return df_

    # list_series = []
    # for c in list_countries:

    #     if type(c) == tuple:
    #         country = return_country(df, c[0], c[1])
    #         country_name = c[0] + "/" + c[1]
    #         df_[country_name] = country
        
    #     elif type(c)  == str:
    #         country = return_country(df, c)
    #         df_[c] = country

    #         # print(country.name)
        
    # return df_

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

# #- importing data

# url_humdata = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv"

# #-

# #-
# df = pd.read_csv(url_humdata)
# df = df.T
# #-
# df = convert_dates_to_python(df)

# print(df.iloc[1])
# #-
# df.iloc[0:5]


# quebec = return_country(df, "Canada", "Quebec")
# print(quebec)

# #-

# #-

# poland = return_country(df, "Poland")
# print(poland)

# #-

# #-
# print(poland)
# #-
# plt.figure()

# plt.plot(poland)
# plt.plot(quebec)
# #-
# print(df)

# #-
# empty_df2 = pd.DataFrame()
# empty_df2["Poland"] = poland
# empty_df2["Quebec"] = quebec

# print(empty_df2)
# empty_df2["Poland"].plot()
# #-
# empty_df = pd.DataFrame()
# empty_df =  empty_df.append(poland)
# empty_df = empty_df.append(quebec)
# print(empty_df)

# #-
# list1 = ()
# print(type(list1))
# if type(list1) == tuple:
#     print("list")

# #-
# list_countries = ["Poland", "Germany", ("Canada", "Quebec")]

# new_df = df_initial_clean_up(df, list_countries)
# print(new_df)
# #-




# #-

# dd = return_from_infections(new_df, 1)
# print(dd)
# #-
def plot_days_from(df, list_countries, amount_days):

    list_series = []
    for c in list_countries:
        print(c)
        country = return_country(df, c)
        print(country.name)
        country = country[-amount_days:]
        list_series.append(country)

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

# #-
# plot_days_from(df, ["Poland", "Lithuania"], 20)

# #-
# def get_fist_day(country_series):

    

# #-

# mask_ab_zero = poland > 0
# poland_ab_zero = poland[mask_ab_zero]
# poland_ab_zero
# #-
# poland_ab_zero.plot()
# #-
# #-
# days_poland = len(poland_ab_zero)

# #-
# poland_ab_zero.plot(logy=True, legend=False)

# #-

# poland_ab_zero.plot(loglog=True, legend=False)


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


# #-

# italy = preprocess_country("Italy", df)
# print(italy.name)

# #-
# pol_ = ret_starting_from(poland, 1)
# print(pol_)
# #-

# poland_toplot = preprocess_country("Poland", df)
# poland_ab_zero_plot = ret_starting_from(poland_toplot, 1)
# #-
# italy_ab_zero = ret_starting_from(italy, 1)
# # italy_ab_zero.plot(logy=True)

# print(italy_ab_zero[22])

# italy_ab_zero[:days_poland].plot(logy=True)

# #-
# print(italy_ab_zero[:days_poland])
# italy_shorter = italy_ab_zero[:days_poland]
# italy_shorter.plot()
# #-
# df_final = pd.DataFrame([poland_ab_zero, italy_shorter])

# df_final
# #-

# # plt.figure(figsize=(12,5))

# ax1 = poland_ab_zero_plot.plot(color='red', grid=True)
# ax2 = italy_shorter.plot(color='blue', grid=True)

# # h1, l1 = ax1.get_legend_handles_labels()
# # h2, l2 = ax2.get_legend_handles_labels()


# # plt.legend(h1+h2, l1+l2, loc=2)
# plt.show()


# (fset 'my_initialize_windws
#    (kmacro-lambda-form [?\C-x ?3 ?\C-x ?2 ?\C-x ?o ?\C-x ?o ?\C-x ?2 ?\C-x ?o ?\C-x ?o] 0 "%d"))


# #-
# print(italy_shorter.index)
# print(poland_ab_zero_plot.index)
# #-
