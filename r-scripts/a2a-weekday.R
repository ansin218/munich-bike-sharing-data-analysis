library(MASS)
file <- "mvg-dataset.csv"
data <- read.csv(file, header=TRUE, sep=",")
data <- data[(data$workingday == "Yes"),]
data <- data[(data$AAA == "Yes"),]
sourceCount =  data$destination
sourceCount.freq = table(sourceCount)
png(filename = "a2a-weekday.png", width=960, height=560, units="px")
op0 = par()    
op1 = op0$mar
op1[2] = 25
par(mar = op1)
yy = barplot(sort(sourceCount.freq, decreasing=TRUE)[1:20], horiz=TRUE, xlab="Number Of Observations", main="Most Popular Routes Within Same Area on Weekdays", xlim=c(0,2500), width=10, las=2, col="orange")
text(y = yy, x = sort(sourceCount.freq, decreasing=TRUE)[1:20] + 150, label = sort(sourceCount.freq, decreasing=TRUE)[1:20], pos = 2, cex = 0.7, col = "red")
dev.off()