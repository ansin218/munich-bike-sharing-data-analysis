#uploading MVG bike data
bike_data = read.csv("E:\\MVG_isdaytime_summer.csv")

#plotting a bar plot
barplot(table(bike_data$isdaytime)*100/72130,legend=rownames(table(bike_data$isdaytime)),ylim = c(0, 100),main="Bike Usage in Summer",ylab = "Percentage of User",xlab = 'Is day time',col = c("blue","green"))
value_mat = data.matrix(table(bike_data$isdaytime)*100/72130, rownames.force = NA)
text(0.7, 30, paste(format(round(value_mat[1], 2), nsmall = 2),'%'))
text(1.9, 90, paste(format(round(value_mat[2], 2), nsmall = 2),'%'))
