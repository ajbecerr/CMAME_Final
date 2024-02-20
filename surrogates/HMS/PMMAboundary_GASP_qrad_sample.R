
library(ggplot2)
library(RobustGaSP)
library(repmis)
library(readr)

## Train/test based on sample
#Load data

data <- read_csv("PMMAboundary_GASP_sample_train.csv") 

#Scale train data
data_scaled<- scale(data)
data_scaled <- as.data.frame(data_scaled)


input=data_scaled[-c(1,2,3,12)]
print(colnames(input))
output=data_scaled[3] 
print(colnames(output))

m.rgasp=rgasp(design = input, response = output, trend=matrix(1,length(output),1), zero.mean = "Yes", nugget.est=T)

#Check training is good
testing_input <- input
print(colnames(testing_input))


pred_rgasp_mean <- rep(0, nrow(testing_input))
pred_rgasp_sd <- rep(0, nrow(testing_input))

for (i in 1:nrow(testing_input)) {
  temp <- predict.rgasp(m.rgasp, testing_input[i,])
  pred_rgasp_mean[i] <- temp$mean
  pred_rgasp_sd[i] <- temp$sd
}

finaloutput <- cbind(pred_rgasp_mean,pred_rgasp_sd, output, data$qrad)

write.csv(finaloutput,file="PMMA_qrad_sample_trainaccuracy.csv",row.names=T)

#Validation/testing set
validation_data <- read_csv("PMMAboundary_GASP_sample_test.csv")
#Scale
validation_data_scaled <- as.data.frame(scale(validation_data))

validation_input <- validation_data_scaled[-c(1,2,3,12)]
print(colnames(validation_input))

validation_output <- validation_data_scaled[3]
print(colnames(validation_output))

pred_rgasp_mean <- rep(0, nrow(validation_input))
pred_rgasp_sd <- rep(0, nrow(validation_input))

for (i in 1:nrow(validation_input)) {
  temp <- predict.rgasp(m.rgasp, validation_input[i,])
  pred_rgasp_mean[i] <- temp$mean
  pred_rgasp_sd[i] <- temp$sd
}

finalvaloutput <- cbind(pred_rgasp_mean,pred_rgasp_sd,validation_output,validation_data$qrad)
write.csv(finalvaloutput, "PMMA_qrad_sample_testaccuracy.csv", row.names = T)



save(m.rgasp, file = "PMMA_qrad_sample_model.rda")