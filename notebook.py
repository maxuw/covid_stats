#-
import corona_lib
import pandas as pd
import numpy as np
#-
url_humdata = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv"

#-
df = pd.read_csv(url_humdata)
df = df.T

#-
df = corona_lib.convert_dates_to_python(df)

#-
df_cleanup = corona_lib.df_initial_clean_up(df, ["Poland", "Italy", "Germany", "Spain", "Sweden"])

#-
print(df_cleanup)

#-
poland_100 = len(corona_lib.ret_starting_from(df_cleanup["Poland"], 100))
poland_1000 = len(corona_lib.ret_starting_from(df_cleanup["Poland"], 1000))

#-
diff = df_cleanup.diff()

#-
pol_inc = [incremental_change(df_cleanup.loc[df_cleanup.index[i-1], "Poland"], diff.loc[df_cleanup.index[i], "Poland"]) for i in range(len(df_cleanup)) if i > 0]

#-
print(len(df_cleanup))
print(len(pol_inc))

print(pol_inc)
#-
pol_inc = pol_inc[-poland_1000:]
#-
print(poland_1000)
print(pol_inc)

#-

def incremental_change(previous_day, today_newcases):
    if previous_day == 0:
        return(0)
    else:
        number = today_newcases/previous_day
    
    return number

def increase_series(series_absolute):
    diff = series_absolute.diff()
    series_new = [0]


    for n in range(len(series_absolute)-1):
        i = incremental_change(series_absolute[n], diff[n+1])
        series_new.append(i)

    series_new = pd.Series(series_new)
    series_new.index = series_absolute.index
    return series_new

#-
#-

def incremental_change(previous_day, today_newcases, double=False):
    if previous_day == 0 or today_newcases == 0:
        return(0)
    else:
        if double==False:
            number = today_newcases/previous_day
        else:
            number = previous_day/today_newcases
    
    return number

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


#-

pol_inc = increase_series(df_cleanup["Poland"])

#-
print(pol_inc[-10:])

print(df_cleanup["Poland"].iloc[-10:])
print(df_cleanup["Poland"].iloc[-10:].diff())

#-

pol_inc[-poland_1000:].plot.bar()
#-
pol_days_double = increase_series(df_cleanup["Poland"], double=True)

#-
print(pol_days_double)

pol_days_double.plot.bar()

#-
