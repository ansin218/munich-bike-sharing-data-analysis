#uploading file
bike_data = read.csv("E:\\MVG.csv")
for(i in 1:nrow(bike_data)){
  v  = sapply(strsplit( toString(bike_data$std_timestamp[i]) , " " ), `[` , 2 )
  bike_data$hour[i] = sapply(strsplit( v , ":" ), `[` , 1 )
}

write.csv(bike_data, file = "E:\\MVG_Hour.csv",row.names=FALSE)
