library(MASS)
file <- "mvg-dataset.csv"
data <- read.csv(file, header=TRUE, sep=",")
data <- data[(data$workingday == "Yes"),]
png(filename = "ts-weekday.png", width=960, height=560, units="px")
plot(table(data$hour), xlab="Hours", ylab="Frequency", ylim=c(0,5000), xlim=c(0,23))
dev.off()