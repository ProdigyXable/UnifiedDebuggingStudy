
library("ggpubr")
library(ggplot2)
library(reshape2)
library(cowplot)
#library(ggpmisc)


figWidth<-15
figHeight<-5
textFont<-4



#Metrics<-c("Top1","Top3","Top5","MFR","MAR")
Metrics<-c("Top1","MFR")
#Patches<-c("Total","Plausible","CleanFix","NoisyFix","NoneFix","NegFix")
Patches<-c("TotalPatch","MethodByTotal", "PlausiblePatch","MethodsByPlausible")


plot_list = list()
count=1
pdf(paste(c("../../Results/FinalResults/RQ1_2.pdf"),collapse=""), width=figWidth, height=figHeight)

for(Me in Metrics){
	for(pa in Patches){

		file_name = paste(c('./Rdata/', pa,Me,'.txt'),collapse="")

		df <- read.csv(file_name,header=FALSE,sep = " ")
		df<-t(df)
		#df<-na.omit(df)
		df<-as.data.frame(df)
		colnames(df) <- c("Metric","Patch")
		
		
		#pdf(paste(c("C:\\Users\\xia\\Desktop\\r\\",pa,Me,".pdf"),collapse=""), width=figWidth, height=figHeight)
		
		#p <- ggplot(df, aes(x = Plausible, y = Metric)) + geom_point()+ geom_smooth(method='lm',colour="blue",formula = y ~ x) + ggtitle("Correlation") + 
		#theme(plot.title = element_text(size = 6, face = "bold"),text = element_text(size=9),axis.text=element_text(size=6)) +
		#stat_poly_eq(aes(label = paste(..eq.label..)), label.x.npc = "left", label.y.npc = "top" , formula = y ~ x, parse = TRUE, size = 1.5)

		p<-ggscatter(data=df, x = "Patch", y = "Metric", size = 1.5,
		          add = "reg.line", conf.int = TRUE, 
		          cor.coef = TRUE, cor.coeff.args = list(method = "pearson",label.sep = "\n"),add.params = list(color = "black", fill = "lightgray"),
		          xlab = pa, ylab = Me,font.label = c(20, "plain")) + xscale("log10", .format = TRUE)
		plot_list[[count]] = p
		count=count+1
	}
}
# prow<-plot_grid(plot_list[[1]]+theme(legend.position="none"),
# 						plot_list[[2]]+theme(legend.position="none"),
# 						plot_list[[3]]+theme(legend.position="none"),
# 						plot_list[[4]]+theme(legend.position="none"),
# 						plot_list[[5]]+theme(legend.position="none"),
# 						plot_list[[6]]+theme(legend.position="none"),
# 						plot_list[[7]]+theme(legend.position="none"),
# 						plot_list[[8]]+theme(legend.position="none"),
# 						plot_list[[9]]+theme(legend.position="none"),
# 						#ncol = 3)
# 						#nrow = 1, align = 'h')
# 						nrow = 2, align = 'h')
prow<-plot_grid(plotlist=plot_list, nrow = 2, align = 'h')
		#legend_b <- get_legend(plot_list[[1]] + theme(legend.position=c(0.933,4.94)))
		#p <- plot_grid( prow, legend_b, ncol = 1, rel_heights = c(1, .2))
		print(prow)
		dev.off()


