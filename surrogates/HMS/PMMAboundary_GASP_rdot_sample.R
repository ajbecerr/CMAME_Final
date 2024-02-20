
library(ggplot2)
library(RobustGaSP)
library(repmis)
library(readr)

## Train/test based on sample
#Load data
data <- read_csv("PMMAboundary_GASP_sample_train.csv") 

#Scale define
min_max_norm <- function(x) {
  (x - min(x)) / (max(x) - min(x))
}

#Scale train data
data_scaled <- as.data.frame(lapply(data, min_max_norm))

input=data_scaled[-c(1,2,3,12)]
print(colnames(input))
output=data_scaled[2] 
print(colnames(output))

#Train GaSP
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

finaloutput <- cbind(pred_rgasp_mean,pred_rgasp_sd, output, data$rdot)

write.csv(finaloutput,file="PMMA_rdot_sample_trainaccuracy.csv",row.names=T)

#Validation/testing set
validation_data <- read_csv("PMMAboundary_GASP_sample_test.csv")
#Scale
validation_data_scaled <- as.data.frame(lapply(validation_data, min_max_norm))
validation_input <- validation_data_scaled[-c(1,2,3,12)]
print(colnames(validation_input))
validation_output=validation_data_scaled[2] 
print(colnames(validation_output))

pred_rgasp_mean <- rep(0, nrow(validation_input))
pred_rgasp_sd <- rep(0, nrow(validation_input))

for (i in 1:nrow(validation_input)) {
  temp <- predict.rgasp(m.rgasp, validation_input[i,])
  pred_rgasp_mean[i] <- temp$mean
  pred_rgasp_sd[i] <- temp$sd
}

finalvaloutput <- cbind(pred_rgasp_mean,pred_rgasp_sd,validation_output,validation_data$rdot)
write.csv(finalvaloutput,file="PMMA_rdot_sample_testaccuracy.csv",row.names=T)

save(m.rgasp, file = "PMMA_rdot_sample_model.rda")


