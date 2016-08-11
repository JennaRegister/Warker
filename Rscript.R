library(ggplot2)
library(gdata)
data1= read.csv("firstsegmentAllData.csv")
data1$Model = "Segment"
data1=data1[order(data1$Data),]
data2=read.csv("firstclassesAllData.csv")
data2$Model= "Classes"
data2=data2[order(data2$Data),]
data3=read.csv("firstenglishAllData.csv")
data3$Model= "English"
data3=data3[order(data3$Data),]
data4=read.csv("FirstEnglishUniformAllData.csv")
data4$Model="EnglishUniform"
data4=data4[order(data4$Data),]


data=rbind(data1,data2)
data=rbind(data,data3)
data=rbind(data,data4)
data$Data=as.numeric(as.character(data$Data))
data$Type = "NotInTraining"
training = c('h e s', 'm e s', 'm e g', 'h e g', 'm e n', 'h e m', 'm e k', 'k e s', 'h e k', 'k e N', 'k e g', 'h e n', 'm e N', 'k e n', 'h e N', 'f e N', 'g e N', 'n e N', 'n e s', 'f e n', 'g e n', 'g e m', 'f e m', 'g e k', 'f e k', 'f e g', 'f e s', 'n e g', 'k e m', 'n e m', 'g e s', 'n e k')
target = c('f e s', 'f e n', 'f e m', 'f e g', 'f e s', 'f e k', 'f e N', 'n e s', 'n e n', 'n e m', 'n e g', 'n e s', 'n e k', 'n e N', 'm e s', 'm e n', 'm e m', 'm e g', 'm e s', 'm e k', 'm e N', 'g e s', 'g e n', 'g e m', 'g e g', 'g e s', 'g e k', 'g e N', 'h e s', 'h e n', 'h e m', 'h e g', 'h e s', 'h e k', 'h e N', 'k e s', 'k e n', 'k e m', 'k e g', 'k e s', 'k e k', 'k e N')
dataamount=c(1,11,21,31,41,51,61,71,81,91)



data$Type[data$Word %in% training]="InTraining"
data$Target = "NotTarget"
data$Target[data$Word %in% target]="Target"

data$Accuracy = 0
data$Accuracy[data$Type=="InTraining"] = 1

data$TargetAcc = 0
data$TargetAcc[data$Target=="Target"] = 1


data$Passed = FALSE
data$Passed[data$Model == "English" & data$Probability>0.000000002]=TRUE






colors = c("Precision"="red","Recall"="slateblue")
plt = ggplot(data[data$Probability>1.953126e-09,], aes(Data,TargetAcc,colour="Precision"))+
  facet_wrap(~Model)+
  stat_summary(aes(Data,Accuracy,colour="Recall"),fun.y=mean,geom="line",alpha=0.5,size=1)+
  stat_summary(fun.y=mean, geom="line",alpha=0.5,size=1)+
  ylab("Proportion Correct (Precision vs. Recall)")+
  xlab("Amount of Data")+
  ylim(0,1)+
  scale_colour_manual(name="Accuracy",values=colors)+
  theme_bw()
  
plt

plt = ggplot(data[data$Probability>1.99e-09,], aes(Data,TargetAcc,colour="Precision"))+
  facet_wrap(~Model)+
  stat_smooth(aes(Data,Accuracy,colour="Recall"),fun.y=mean,geom="line",alpha=0.5,size=1)+
  stat_smooth(fun.y=mean, geom="line",alpha=0.5,size=1)+
  ylab("Proportion Correct (Precision vs. Recall)")+
  xlab("Amount of Data")+
  scale_colour_manual(name="Accuracy",values=colors)+
  theme_bw()

plt




plt
plt = ggplot(data[data$Probability>1.99e-09 & data$Data==91&data$Model=="English",], aes(Type,Probability))+
  facet_wrap(~Model)+
  geom_boxplot(stat="boxplot")+
  ylab("Probability of Producing Word")+
  xlab("Words")+
  theme_bw()
plt

plt = ggplot(data[data$Probability>1.99e-09&data$Data %in% dataamount &data$Model=="English",], aes(Word,Probability))+
  facet_grid(~Data)+
  geom_text(aes(label=Word, colour=Type),size=3)+
  ggtitle("Probabilities of Learning Over Time for Segment Model")+
  ylab("Probability of Producing Word")+
  xlab("Words")+
  theme_bw()+
  scale_colour_manual(name="Type",values=c("limegreen","red"))+
  
  theme(
    axis.text.x=element_blank(),
    axis.ticks.x=element_blank())
plt
plt = ggplot(data[data$Probability>1.99e-09&data$Data %in% dataamount &data$Model=="Segment",], aes(Word,Probability))+
  facet_grid(~Data)+
  geom_text(aes(label=Word, colour=Target),size=3)+
  ggtitle("Probabilities of Learning Over Time for Segment Model")+
  ylab("Probability of Producing Word")+
  xlab("Words")+
  theme_bw()+
  scale_colour_manual(name="Type",values=c("red","limegreen"))+
  
  theme(
    axis.text.x=element_blank(),
    axis.ticks.x=element_blank())
plt

plt = ggplot(data[data$Probability>1.953126e-09&data$Data %in% dataamount &data$Model=="Segment",],aes(Data,Probability))+
  facet_wrap(~Word)+
  geom_line()
plt

plt = ggplot(data[data$Probability>1.953126e-09&data$Data %in% dataamount &data$Model=="EnglishUniform",],aes(Data,Probability))+
  facet_wrap(~Word)+
  geom_line()
plt


plt = ggplot(data[data$Probability>1.953126e-09&data$Data %in% dataamount &data$Model=="English",],aes(Data,Probability))+
  facet_wrap(~Word)+
  geom_line()
plt
