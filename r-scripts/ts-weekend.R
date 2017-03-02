library(MASS)
file <- "mvg-dataset.csv"
data <- read.csv(file, header=TRUE, sep=",")
data <- data[(data$workingday == "No"),]
png(filename = "ts-weekend.png", width=960, height=560, units="px")
plot(table(data$hour), xlab="Hours", ylab="Frequency", ylim=c(0,2000), xlim=c(0,23))
dev.off()