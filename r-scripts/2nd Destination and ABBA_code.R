#uploading MVG bike data from excel file
bike_data = read.csv("E:\\MVG.csv")

#creating file with source and 2nd destination!!!
for(i in 1:nrow(bike_data)){
  bike_data_delete = bike_data[bike_data$bike_id == bike_data$bike_id[i], ]
  bike_data_delete = bike_data_delete[bike_data_delete$row_number > i, ]
  if (nrow(bike_data_delete) != 0) {
    bike_data$destination2[i] =  toString(bike_data_delete$destination[1])
  }
}


#Creating column ABBA 
#If the local_name and destination2 is same than yes else no
bike_data = bike_data[bike_data$destination != 'Last Location', ]
for(i in 1:nrow(bike_data)){
  if ( bike_data$local_name[i] == bike_data$destination2[i] ) {
    bike_data$ABBA[i] =  'Y'
  }
  else
  {    
    bike_data$ABBA[i] =  'N'
  }
}

#writing the file
write.csv(bike_data, file = "E:\\MVG_2nd_destination.csv",row.names=FALSE)
