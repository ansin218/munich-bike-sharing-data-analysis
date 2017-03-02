#*******************************************************************************
#Program  : scrapping MVG Rad data to postgres database                        *
#Database : POSTGRES                                                           *
#Language : Python                                                             *
#Date     : 01.05.2016                                                         *
#*******************************************************************************

#*******************************************************************************
#******************************importing packages*******************************
#*******************************************************************************
import time #time
import psycopg2 #psycopg2 to connect to POSTGRES database
import json #json to load json
import urllib2 #urlib2 to open url
from   datetime import datetime #datetime
import calendar #date

#*******************************************************************************
#*********************connecting to the postgres database***********************
#*******************************************************************************
try:
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost'\
    password='smohanta'")
    cur = conn.cursor()
except:
    print "Unable to connect to the database"

#*******************************************************************************
#***************************reading weather table*******************************
#*******************************************************************************
#selecting records from table weather
cur.execute("SELECT * from weather")
rows_weather = cur.fetchall()

#*******************************************************************************
#********************calcualtion for holiday using holidayapi*******************
#*******************************************************************************
year      = time.strftime("%Y")
day       = time.strftime("%d")
month_num = time.strftime("%m")

#wd_url = "http://holidayapi.com/v1/holidays?country=DE&year=" + str(year) +    \
#"&month=" + str(month_num) + "&day=" + str(day)
#dataHoliday = json.load(urllib2.urlopen(wd_url))

if time.strftime("%A") == "Saturday" or time.strftime("%A") == "Sunday" :
    workingday = "No"
#elif len(dataHoliday["holidays"]) == 0:
#    workingday = "Yes"
#else:
#    workingday = "No"
else:
    workingday = "Yes"


#*******************************************************************************
#scrapping data from MVG https://carsharing.mvg-mobil.de/json/stations.php (json)
#*******************************************************************************
data = json.load(urllib2.urlopen("https://carsharing.mvg-mobil.de/json/stations.php"))

#initializing variables
#*******************
i = 0 #counter for total iteration
j = 0 #counts total bike in a station
k = 0 #counter to get bike id
exists = 0
new_bike = 0
new = 0
zone_id   = ""
date      = ""
provider  = "MVG Rad"
date_var  = time.strftime("%d%m%Y")
month     = time.strftime("%B")

#Main logic starts
counter = data["cnt"]#counter holds the total number of records scrapped

while i < counter:#looping through the whole data to process one by one
    #number 11 is the bike section
    if data["sta"][i]["prv"] == 11 :

        latitude  = data["sta"][i]["loc"][0]
        longitude = data["sta"][i]["loc"][1]
        bikeorstations_Id = data["sta"][i]["id"]
        timestamp = time.time()
        current_time = time.strftime("%H%M%S")

        if time.strftime("%B") == "March" or time.strftime("%B") == "April" or \
        time.strftime("%B") == "May":
            season = "Spring"
        elif time.strftime("%B") == "June" or time.strftime("%B") == "July" or \
        time.strftime("%B") == "August":
            season = "Summer"
        elif time.strftime("%B") == "September" or time.strftime("%B") == \
        "October" or time.strftime("%B") == "November":
            season = "Autumn"
        else:
            season = "Winter"

        location        = ""
        weather         = ""
        isdaytime       = ""
        isday           = ""
        temp            = 0
        temp_unit       = ""
        feels_like      = 0
        feels_like_unit = ""
        wind_speed      = 0
        wind_speed_unit = ""
        dew             = 0
        dew_unit        = 0
        location        = ""
        easy_timestamp  = 0

        if "zid" in data["sta"][i]:
            zone_id = data["sta"][i]["zid"]	
            for row in rows_weather:
                if row[1] == str(zone_id) :
                    weather         = row[5]
                    isday           = row[6]
                    temp            = row[7]
                    temp_unit       = row[8]
                    feels_like      = row[9]
                    feels_like_unit = row[10]
                    wind_speed      = row[11]
                    wind_speed_unit = row[12]
                    dew             = row[13]
                    dew_unit        = row[14]
                    location        = row[2]
                    weather_timestamp  = row[4]

            if "vhc" in data["sta"][i]:
                countVch = len(data['sta'][i]['vhc'])
                numberofbike = countVch
                j = j + countVch

                while k < countVch :
                    bike_id = data["sta"][i]["vhc"][k]["id"]
                    k = k+1

                    try:
						cur.execute("SELECT bike_id, latitude, longitude,timestamp_update \
						FROM public.mvgtodb  WHERE BIKE_ID = %(bike_id)s order by timestamp_update desc limit 1;",{'bike_id':bike_id})
						rows_latest_loc = cur.fetchall()
						conn.commit()
                    except Exception, e:
						conn.rollback()
                    if cur.rowcount == 1:
                        for rows in rows_latest_loc:
                            if rows[1] != latitude or rows[2] != longitude :
                                print 'new location'
                                print rows_latest_loc
                                new_bike = new_bike + 1
                                print latitude
                                print longitude
                                print bike_id
                                d = datetime.now()
                                std_timestamp = d #standard timestamp

                                s = str(d)
                                timestamp_update = int(s[0:4] + s[5:7] + s[8:10] + s[11:13] + s[14:16] + \
                                s[17:19]+ s[21:26]) #easy timestamp to work with


                                entry = ({"bike_id":bike_id, "latitude":latitude , "longitude": \
                                longitude,  "timestamp_update":timestamp_update,\
								"std_timestamp":std_timestamp,"weather_timestamp":weather_timestamp,\
								"zone_id": zone_id ,"provider": provider , "year":\
                                year, "date": date_var,"month":month, "season":season,\
                                "bikeorstations_Id":bikeorstations_Id, "numberofbike":numberofbike,\
                                "workingday":workingday,\
                                "current_time":current_time,"local_name":location,\
                                "weather":weather,"isdaytime":isday,\
                                "temp_value":temp,"temp_unit":temp_unit,"feels_like":feels_like,\
                                "feels_like_unit":feels_like_unit,"wind_speed":wind_speed,"wind_unit":wind_speed_unit,\
                                "dew_point":dew,"dew_point_unit":dew_unit})
									
                                #inserting data into database
                                try:
                                    cur.execute("""INSERT INTO mvgtodb VALUES (%(bike_id)s, %(latitude)s,\
                                    %(longitude)s,%(timestamp_update)s,%(std_timestamp)s,%(weather_timestamp)s,\
									%(zone_id)s,%(provider)s,%(year)s,%(date)s,%(month)s,\
                                    %(season)s,%(bikeorstations_Id)s ,%(numberofbike)s,%(workingday)s,\
                                    %(current_time)s,%(local_name)s,%(weather)s,\
                                    %(isdaytime)s,%(temp_value)s,%(temp_unit)s,\
                                    %(feels_like)s,%(feels_like_unit)s,%(wind_speed)s,%(wind_unit)s,\
                                    %(dew_point)s,%(dew_point_unit)s) """, entry)
                                    conn.commit()
                                except Exception, e:
                                    conn.commit()
                                    exists = exists + 1
                            else:
                                exists = exists + 1
                    else:
                        new_bike = new_bike + 1
                        d = datetime.now()
                        std_timestamp = d #standard timestamp

                        s = str(d)
                        timestamp_update = int(s[0:4] + s[5:7] + s[8:10] + s[11:13] + s[14:16] + \
                        s[17:19]+ s[21:26]) #easy timestamp to work with


                        entry = ({"bike_id":bike_id, "latitude":latitude , "longitude": \
                        longitude,  "timestamp_update":timestamp_update,\
						"std_timestamp":std_timestamp,"weather_timestamp":weather_timestamp,\
						"zone_id": zone_id ,"provider": provider , "year":\
                        year, "date": date_var,"month":month, "season":season,\
                        "bikeorstations_Id":bikeorstations_Id, "numberofbike":numberofbike,\
                        "workingday":workingday,\
                        "current_time":current_time,"local_name":location,\
                        "weather":weather,"isdaytime":isday,\
                        "temp_value":temp,"temp_unit":temp_unit,"feels_like":feels_like,\
                        "feels_like_unit":feels_like_unit,"wind_speed":wind_speed,"wind_unit":wind_speed_unit,\
                        "dew_point":dew,"dew_point_unit":dew_unit})

                        #inserting data into database
                        try:
                            cur.execute("""INSERT INTO mvgtodb VALUES (%(bike_id)s, %(latitude)s,\
                            %(longitude)s,%(timestamp_update)s,%(std_timestamp)s,%(weather_timestamp)s,\
							%(zone_id)s,%(provider)s,%(year)s,%(date)s,%(month)s,\
                            %(season)s,%(bikeorstations_Id)s ,%(numberofbike)s,%(workingday)s,\
                            %(current_time)s,%(local_name)s,%(weather)s,\
                            %(isdaytime)s,%(temp_value)s,%(temp_unit)s,\
                            %(feels_like)s,%(feels_like_unit)s,%(wind_speed)s,%(wind_unit)s,\
                            %(dew_point)s,%(dew_point_unit)s)""", entry)
                            conn.commit()
                        except Exception, e:
                            exists = exists + 1

    i = i + 1
    k = 0 #clear


print "Number of Rad = %s" %j
print "Number of Rad already exists in db = %s" %exists
new = new_bike
print "Number of Rad update = %s" %new

d = datetime.now()
std_timestamp = str(d) #standard timestamp
entry = ({"timestamp":std_timestamp, "scanned_bike":j , "updated_bike": new})
cur.execute("""INSERT INTO mvglogdb VALUES (%(timestamp)s, %(scanned_bike)s,\
%(updated_bike)s) """, entry)
conn.commit()

