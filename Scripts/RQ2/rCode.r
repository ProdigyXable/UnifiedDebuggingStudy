library(ggplot2)
library(reshape2)
library(cowplot)

figWidth<-20
figHeight<-10
textFont<-10

#epoch === repair tool
#losses  === tech(sbfl and profl)
#Subs == patches (correct, plausible noncorrect)
#model == result.txt

Basedir="./"


Subs<-c("FL")


losses<-c("NegFix","NoneFix","NoisyFix","CleanFix")

model<-"result"

epochs<-c("jGenProg","GenProg-A","jMutRepair","kPar","RSRepair-A","jKali","Kali-A","Dynamoth","ACS","Cardumen","Arja","Simfix","FixMiner","AVATAR","TBar","PraPR")

#Metrics<-c("Top1","Top3","Top5","MFR","MAR")
Metrics<-c("Top1","MFR")

for(sub in Subs){
	plot_list = list()
	count=1
	pdf(paste(c("../../Results/FinalResults/","RQ2.pdf"),collapse=""), width=figWidth, height=figHeight)

		for(me in Metrics){
				
			combinemet=cbind(epochs)
			for(loss in losses){
				datafile=paste(Basedir,loss,"/",sub,"/",model,".txt",sep="")
				datamodel<-read.table(datafile,sep = " ")
				colnames(datamodel) <- c("Tool","Top1","Top3","Top5","MFR","MAR")
				combinemet=cbind(combinemet,datamodel[,me])
			}
			combinemet=data.frame(combinemet)
			#colnames(combinemet) <- c("epochs","within-project","cross-project","cross-validation")
			colnames(combinemet) <- c("Tool","NegFix","NoneFix","NoisyFix","CleanFix")
			combinemet <- melt(combinemet, id.vars='Tool')
			colnames(combinemet) <- c("Tool","model","value")
			combinemet$value <- as.numeric(as.character(combinemet$value))
			p<-ggplot(combinemet, aes(x=Tool, y=value, group=model, colour=model,shape=model)) +
				geom_line(aes(linetype=model),size=1.7)+geom_point(size=2)+ ylab(me)+theme(text=element_text(size=20),legend.position="top")
			plot_list[[count]] = p
			count=count+1
				
		}
			
		prow<-plot_grid(plot_list[[1]]+theme(legend.position="none"),
						plot_list[[2]]+theme(legend.position="none"),
						#plot_list[[3]]+theme(legend.position="none"),
						#plot_list[[4]]+theme(legend.position="none"),
						#plot_list[[5]]+theme(legend.position="none"),
						#nrow = 1, align = 'h',labels = sub)
						nrow = 2, align = 'h')
		legend_b <- get_legend(plot_list[[1]] + theme(legend.position=c(0.967,45), legend.title = element_blank(),
														legend.text = element_text( size = 11)))
		p <- plot_grid( prow, legend_b, ncol = 1, rel_heights = c(1.1, .01))
		print(p)
		dev.off()
	
}
