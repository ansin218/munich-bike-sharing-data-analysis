library(MASS)
file <- "mvg-dataset.csv"
data <- read.csv(file, header=TRUE, sep=",")
data <- data[(data$workingday == "No"),]
data <- data[(data$AAA == "Yes"),]
sourceCount =  data$destination
sourceCount.freq = table(sourceCount)
png(filename = "a2a-weekend.png", width=960, height=560, units="px")
op0 = par()    
op1 = op0$mar
op1[2] = 25
par(mar = op1)
yy = barplot(sort(sourceCount.freq, decreasing=TRUE)[1:20], horiz=TRUE, xlab="Number Of Observations", main="Most Popular Routes Within Same Area on Weekends", xlim=c(0,1000), width=10, las=2, col="orange")
text(y = yy, x = sort(sourceCount.freq, decreasing=TRUE)[1:20] + 50, label = sort(sourceCount.freq, decreasing=TRUE)[1:20], pos = 2, cex = 0.7, col = "red")
dev.off()