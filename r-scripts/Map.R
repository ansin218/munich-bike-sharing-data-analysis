#installing packages
install.packages("leaflet")
install.packages("magrittr")

#loading the library
library(leaflet)
library(magrittr)

#uploading the files
bike_data = read.csv("E:\\MVG.csv")
bike_data_nm = bike_data[!(bike_data$local_name == ''),]
bike_data_nm_tmp = bike_data_nm
bike_data_nm = bike_data_nm_tmp

lon <- c(bike_data_nm$longitude)
lat <- c(bike_data_nm$latitude)
loc <- C(bike_data_nm$local_name)
#creating the popup message
popup_map <- paste(bike_data_nm$bike_id , bike_data_nm$std_timestamp, bike_data_nm$local_name, bike_data_nm$zone_id )

#using leaflet to generate the map
leaflet(bike_data_nm) %>% addTiles() %>% setView(mean(lon), mean(lat), zoom = 13) %>% 
  addCircleMarkers(lng = ~ lon, lat = ~ lat, radius = 5,popup = popup_map,clusterOptions = markerClusterOptions())
