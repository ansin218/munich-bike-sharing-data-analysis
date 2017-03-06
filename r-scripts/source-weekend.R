library(MASS)
file <- "mvg-dataset.csv"
data <- read.csv(file, header=TRUE, sep=",")
data <- data[(data$workingday == "No"),]
sourceCount =  data$local_name
sourceCount.freq = table(sourceCount)
png(filename = "source-weekend.png", width=960, height=560, units="px")
op0 = par()    
op1 = op0$mar
op1[2] = 25
par(mar = op1)
yy = barplot(sort(sourceCount.freq, increasing=TRUE), horiz=TRUE, xlab="Number Of Bikes", main="Outgoing Bikes On Weekends", xlim=c(0,4000), width=10, las=2, col="blue")
text(y = yy, x = sort(sourceCount.freq, increasing=TRUE) + 250, label = sort(sourceCount.freq, increasing=TRUE), pos = 2, cex = 0.7, col = "red")
dev.off()