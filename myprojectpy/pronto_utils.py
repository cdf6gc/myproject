import wget
import os
import zipfile
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn; seaborn.set()
import urllib3
import urllib2
import pdb
def download_if_needed(URL, filename):
    """
    downloads files if not in local environment
    """
    filepresent=False
    downloadsuccess=True
    if os.path.exists(filename):
        print('It Already Exists ' + filename)
        filepresent=True
    else:
        try: urllib2.urlopen(URL)
        except urllib2.URLError as e:
              downloadsuccess=False
        if downloadsuccess==True:
            http = urllib3.PoolManager()
            url='https://s3.amazonaws.com/pronto-data/open_data_year_one.zip'
            response = http.request('GET', url)
            with open('open_data_year_one.zip', 'wb') as f:
                f.write(response.data)
        else:
            print 'Broken Link, Check URL or try again later'
    return (filepresent, downloadsuccess)
def get_pronto_data():
    """
    downloads pronto data
    """
    download_if_needed('https://s3.amazonaws.com/pronto-data/open_data_year_one.zip', 'open_data_year_one.zip')

def get_trip_data():
    """
    exports trip data as dataframe
    """
    get_pronto_data();
    zf=zipfile.ZipFile('open_data_year_one.zip')
    filehandle=zf.open('2015_trip_data.csv')
    return pd.read_csv(filehandle)

def get_weather_data():
    """
    exports weather data as dataframe
    """
    get_pronto_data();
    zf=zipfile.ZipFile('open_data_year_one.zip')
    filehandle=zf.open('2015_weather_data.csv')
    return pd.read_csv(filehandle)

def get_trips_and_weather():
    """
    Combines weather and trip data into one dataframe
    """
    trips=get_trip_data()
    weather=get_weather_data()

    date=pd.DatetimeIndex(trips['starttime'])

    tripsbydate=trips.pivot_table('trip_id', aggfunc='count', index=date.date, columns='usertype')

    weather=weather.set_index('Date')

    weather.index=pd.DatetimeIndex(weather.index)

    combineddate=weather.join(tripsbydate)
    combineddate=combineddate.iloc[:-1]
    return combineddate
def plot_daily_total(plotname):

    data=get_trips_and_weather()
    fig, ax = plt.subplots(2, figsize=(14,6), sharex=True)
    data['Annual Member'].plot(ax=ax[0], title='Annual Member')
    data['Short-Term Pass Holder'].plot(ax=ax[1], title='Short Term Pass Holder')
    fig.savefig('Daily_Totals.png')
    pdb.set_trace()
    plotcreated=False
    if os.path.exists(plotname):
        plotcreated=True
        return (plotcreated)
    else:
        return (plotcreated)

def remove_data(filename):
    success=False;
    if os.path.exists(filename):
        success=True;
        os.remove(filename)
    else:
        success=False;
        print "File Not Present"
    return success
def plot_x_vs_y(dataset, x, y, output):
    xdata = dataset[x]
    ydata = dataset[y]
    plt.scatter(xdata, ydata)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(x+' vs '+y)
    plt.savefig(output+'.pdf', bbox_inches='tight')
