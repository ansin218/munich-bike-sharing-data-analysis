#uploading MVG bike data from excel file
bike_data_nm = read.csv("E:\\MVG.csv")

#creating file with row number!!!
for(i in 1:nrow(bike_data_nm)){
  bike_data_nm$row_number[i] =  i
}


#creating file with source and destination!!!
for(i in 1:nrow(bike_data_nm)){
  bike_data_nm_delete = bike_data_nm[bike_data_nm$bike_id == bike_data_nm$bike_id[i], ]
  bike_data_nm_delete = bike_data_nm_delete[bike_data_nm_delete$row_number > i, ]
  if (nrow(bike_data_nm_delete) != 0) {
    bike_data_nm$destination[i] =  toString(bike_data_nm_delete$local_name[1])
  }
}

#In case of last location there will be no destination
bike_data_nm$destination[bike_data_nm$destination == 1] = ""
bike_data_nm$destination[bike_data_nm$destination == 3] = ""
bike_data_nm$destination[bike_data_nm$destination == 5] = ""
bike_data_nm$destination[bike_data_nm$destination == 21] = ""
bike_data_nm$destination[bike_data_nm$destination == 26] = ""
bike_data_nm$destination[bike_data_nm$destination == 1214] = ""
bike_data_nm$destination[bike_data_nm$destination == ""] = "Last Location"

#write the file
write.csv(bike_data_nm, file = "E:\\MVG_destination.csv",row.names=FALSE)
