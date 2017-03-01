#*******************************************************************************
#Program  : updating weather to postgres database                              *
#Database : POSTGRES                                                           *
#Language : Python                                                             *
#Date     : 01.05.2016                                                         *
#*******************************************************************************

#*******************************************************************************
#******************************importing packages*******************************
#*******************************************************************************
import calendar #date
from   datetime import datetime #datetime
import psycopg2 #psycopg2 to connect to POSTGRES database
import json #json to load json
import urllib2 #urlib2 to open url

#*******************************************************************************
#*********************connecting to the postgres database***********************
#*******************************************************************************

try:
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost'\
    password='smohanta'")
    cur = conn.cursor()
except:
    print "I am unable to connect to the database"

#*******************************************************************************
#***************************updating weather table******************************
#*******************************************************************************

#initializing variables
weatherLine  = []
keys = ['2601656', '2601654', '2601652','2601655','2601657','2601650','2601648'\
       ,'2601649','2601647','167509','2601651','2601658','167470','167468',    \
       '2601660','2601659','2601661','2601653','2601645', '2601644','2601643', \
       '0','2601642','2601646','167496','0','0','167597','177684']
#keys = ['2601656', '2601654']
zone = 0

#deleting data from table weather
cur.execute("DELETE from weather;")
conn.commit

#selecting records from table zone
cur.execute("SELECT zone_id, location from zone")
rows = cur.fetchall()

#update weather table using accuweather api
for number in keys:
    zone =  zone + 1
    if number != '0':
        weatherLine = "http://dataservice.accuweather.com/currentconditions/v1/"\
        +number+"?apikey=fcfrsLdCBFgSBgbq5jLqEl4HHNeAERcv&language=en&details=true"
                         
        dataWeather     = json.load(urllib2.urlopen(weatherLine))
        epochtime       = dataWeather[0]["EpochTime"]
        weather         = dataWeather[0]["WeatherText"]
        isday           = dataWeather[0]["IsDayTime"]
        temp            = dataWeather[0]["Temperature"]["Metric"]["Value"]
        temp_unit       = dataWeather[0]["Temperature"]["Metric"]["Unit"]
        feels_like      = dataWeather[0]["RealFeelTemperature"]["Metric"]["Value"]
        feels_like_unit = dataWeather[0]["RealFeelTemperature"]["Metric"]["Unit"]
        wind_speed      = dataWeather[0]["Wind"]["Speed"]["Metric"]["Value"]
        wind_speed_unit = dataWeather[0]["Wind"]["Speed"]["Metric"]["Unit"]
        dew             = dataWeather[0]["DewPoint"]["Imperial"]["Value"]
        dew_unit        = dataWeather[0]["DewPoint"]["Imperial"]["Unit"]

        d = datetime.now()
        std_timestamp = d #standard timestamp

        s = str(d)
        timestamp_easy = int(s[0:4] + s[5:7] + s[8:10] + s[11:13] + s[14:16] + \
        s[17:19]+ s[21:26]) #easy timestamp to work with

        for row in rows:
           if row[0] == zone:
               location = row[1]

        entry = ({"key":number, "zone": zone ,"location":location,             \
        "std_timestamp":std_timestamp,                   					   \
        "timestamp_easy":timestamp_easy, "weather": weather ,                  \
        "isdaytime": isday , "temp_value": temp,     						   \
        "temp_unit":temp_unit,"feels_like":feels_like,                         \
        "feels_like_unit":feels_like_unit,"wind_speed":wind_speed,             \
        "wind_unit":wind_speed_unit, "dew_point":dew,"dew_point_unit":dew_unit})

        #inserting data into database
        cur.execute("""INSERT INTO weather VALUES (%(key)s, %(zone)s,          \
        %(location)s,%(std_timestamp)s ,%(timestamp_easy)s,      			   \
        %(weather)s,%(isdaytime)s,%(temp_value)s,%(temp_unit)s,                \
        %(feels_like)s,%(feels_like_unit)s,%(wind_speed)s ,%(wind_unit)s,      \
        %(dew_point)s,%(dew_point_unit)s)""", entry)
        conn.commit()
