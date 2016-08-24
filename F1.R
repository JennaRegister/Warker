library(ggplot2)
data1= read.table("segment.csv")
data1$Model= "Experiment Phonemes Only"
data2 = read.table("englishuniform.csv")
data2$Model = "English Uniform"
data3 = read.table("englishweighted.csv")
data3$Model = "English Weighted"
data4 = read.table("classes.csv")
data4$Model = "Classes"
data= rbind(data1,data2)
data = rbind (data,data3)
data = rbind(data,data4)
colnames(data) = c("TargetF1", "TargetRecall", "TargetPrecision", "TrainingF1","TrainingRecall","TrainingPrecision","Data","Model")
data$Model = as.factor(data$Model)



colors = c("Target"="red","Training"="slateblue")


ggsave("Acquisition.pdf",plt,width=8,height=5)

targetcolors = c("Target Recall"="red","Target Precision"="slateblue")
plt = ggplot(data[data$Model!="Classes",], aes(Data,TrainingRecall,colour="Target Recall"))+
  stat_summary(fun.y=mean,geom="line")+
  stat_summary(aes(Data,TrainingPrecision, colour="Target Precision"),fun.y=mean,geom="line")+
  facet_wrap(~Model)+
  xlim(0,100)+
  ggtitle("Fit to the Target Rule Across Data Amount")+
  ylab("F1 Score")+
  scale_colour_manual(name="Accuracy",values=targetcolors)+
  theme_bw()
plt
