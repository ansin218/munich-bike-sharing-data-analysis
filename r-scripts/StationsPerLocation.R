bike_data = read.csv("E:\\Tum\\Semester 3\\1.IDP\\3.Work\\analysis\\busy stations\\bike_usage_analysis.csv")
op0 = par()    
op1 = op0$mar
op1[2] = 21
par(mar = op1)
barplot(table(bike_data$locations),xlim = c(0, 10),main="Stations/location",xlab = "Number of Stations",col = c("blue"),horiz = TRUE, las=2)
