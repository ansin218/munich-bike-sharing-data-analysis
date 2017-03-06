#uploading MVG bike data
bike_data = read.csv("E:\\MVG_autumn.csv")
bike_data_autumn = bike_data[(bike_data$month == 'October' | bike_data$month == "November"),]

#plotting a bar plot
barplot(table(bike_data_autumn$isdaytime)*100/40373,legend=rownames(table(bike_data$isdaytime)),ylim = c(0, 100),main="Bike Usage in Autumn",ylab = "Percentage of User",xlab = 'Is day time',col = c("blue","green"))
value_mat = data.matrix(table(bike_data_autumn$isdaytime)*100/40373, rownames.force = NA)
text(0.7, 50, paste(format(round(value_mat[1], 2), nsmall = 2),'%'))
text(1.8, 70, paste(format(round(value_mat[2], 2), nsmall = 2),'%'))
