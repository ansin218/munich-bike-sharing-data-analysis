#uploading MVG bike data
bike_datan = read.csv("E:\\MVG_autumn.csv")
bike_datan = bike_datan[(bike_datan$month == 'October' | bike_datan$month == "November"),]

# Pie chart for weather
bike_datan$weather[bike_datan$weather == "Clear" |
                       bike_datan$weather == "Mostly clear" |
                       bike_datan$weather == "Mostly sunny" |
                       bike_datan$weather == "Partly sunny" ] = "Sunny"

bike_datan$weather[bike_datan$weather == "Clouds and sun" |
                       bike_datan$weather == "Mostly cloudy" |
                       bike_datan$weather == "Partly cloudy" |
                       bike_datan$weather == "Some clouds" ] = "Cloudy"


bike_datan$weather[bike_datan$weather == "Drizzle" |
                       bike_datan$weather == "Light rain" |
                     bike_datan$weather == "Light rain shower" |
                     bike_datan$weather == "Drizzle and rain" |
                     bike_datan$weather == "Rain and drizzle" |
                     bike_datan$weather == "Rain and snow" |
                     bike_datan$weather == "Rain shower"|
                       bike_datan$weather == "Rain/drizzle" ] = "Rain"


bike_datan$weather[bike_datan$weather == "Thundershower" ] = "Thunderstorm"

bike_datan$weather[bike_datan$weather == "Ground fog" |
                     bike_datan$weather == "Light fog" |
                     bike_datan$weather == "Dense fog" |
                     bike_datan$weather == "Mist" ] = "Foggy"
bike_datan$weather[bike_datan$weather == "Light snow shower" |
                     bike_datan$weather == "Light snow" |
                     bike_datan$weather == "Snow and rain" |
                     bike_datan$weather == "Snow" ] = "Snow"

table(bike_datan$weather)


lbls <- c("Cloudy","Foggy","Rain","Sunny","Snow")
table(bike_datan$weather)

pct <- round(table(bike_datan$weather)/sum(table(bike_datan$weather))*100)
pct
lbls <- paste(lbls, c(39,17,10,33,1)) # add percents to labels
lbls <- paste(lbls,"%",sep="") # ad % to labels

#plotting the pie chart
pie(c("Cloudy" = 39,"Foggy" = 17 ,"Rain" = 10,"Sunny" = 33,"Snow" = 1 ),labels = lbls, col=rainbow(length(lbls)),
    main="Weather")
