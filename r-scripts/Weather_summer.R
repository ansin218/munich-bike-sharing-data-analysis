#uploading MVG bike data
bike_data = read.csv("E:\\MVG.csv")
bike_data_nm = bike_data[!(bike_data$local_name == ''),]

# Pie chart for weather Modified
bike_data_nm$weather[bike_data_nm$weather == "Clear" |
                     bike_data_nm$weather == "Mostly clear" |
                     bike_data_nm$weather == "Mostly sunny" |
                     bike_data_nm$weather == "Partly sunny" ] = "Sunny"

bike_data_nm$weather[bike_data_nm$weather == "Clouds and sun" |
                       bike_data_nm$weather == "Mostly cloudy" |
                       bike_data_nm$weather == "Partly cloudy" |
                       bike_data_nm$weather == "Some clouds" ] = "Cloudy"

bike_data_nm$weather[bike_data_nm$weather == "Drizzle" |
                       bike_data_nm$weather == "Light rain" |
                       bike_data_nm$weather == "Light rain shower" |
                       bike_data_nm$weather == "Rain shower"|
                       bike_data_nm$weather == "Rain/drizzle" ] = "Rain"

bike_data_nm$weather[bike_data_nm$weather == "Thundershower" ] = "Thunderstorm"

bike_data_nm$weather[bike_data_nm$weather == "Ground fog" |
                       bike_data_nm$weather == "Light fog" |
                       bike_data_nm$weather == "Dense fog" |
                       bike_data_nm$weather == "Mist" ] = "Foggy"

lbls <- c("Cloudy","Foggy","Rain","Sunny","Thunderstorm")
pct <- round(table(bike_data_nm$weather)/sum(table(bike_data_nm$weather))*100)
lbls <- paste(lbls, c(17,2,7,71,2)) # add percents to labels
lbls <- paste(lbls,"%",sep="") # ad % to labels

#plotting the pie chart
pie(c("Cloudy" = 17,"Foggy" = 2 ,"Rain" = 7,"Sunny" = 71 ,"Thunderstorm" = 2),labels = lbls, col=rainbow(length(lbls)),
    main="Weather")
