library(ggplot2)
library(reshape2)
library(cowplot)

figWidth<-10
figHeight<-5
textFont<-10



file_name = paste(c('./RData.csv'),collapse="")
pdf(paste(c('../../Results/FinalResults/RQ4_2.pdf'),collapse=""), width=figWidth, height=figHeight)
df <- read.csv(file_name,header=TRUE,sep=",")
df<-as.data.frame(df)
colnames(df) <- c("Tech","Top1","Comb")
p<-ggplot(data=df, aes(x=Comb, y=Top1, group=Tech,colour=Tech,shape=Tech)) +geom_line(aes(linetype=Tech),size=1.7)+
geom_point(size=2)+theme(text=element_text(size=20),legend.position="top",legend.title = element_blank())+
scale_x_continuous(name="Comb", breaks=seq(1,13,by=1), limits=c(1,13))
print(p)
dev.off()
