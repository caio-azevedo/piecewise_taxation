# clean up workspace ------------------------------------------------------
rm(list=ls())

# close all figure --------------------------------------------------------
graphics.off()

# load packages -----------------------------------------------------------
library(Pareto)
library(PNADcIBGE)
library(tidyverse)
library(survey)
library(xtable)
library(glue)


options(scipen = 999)


# Import data script ------------------------------------------------------
dadosPNADc <- get_pnadc(year=2023, quarter=4, vars=c("VD4020", "VD4035"),
                        reload = FALSE, deflator = FALSE)

df <- get_pnadc(year=2023, quarter=4, vars=c("VD4020", "VD4035"),
                design=FALSE, reload = FALSE, deflator=FALSE)

df <- df |> 
  mutate("ID" = row_number(), .before = everything()) |> 
  select(ID, VD4020, VD4035) |> 
  drop_na()

write_csv(df, "data/dadosPNADc.csv")


# Calculando algumas medidas descritivas ----------------------------------

# Média -------------------------------------------------------------------
mediarenda <- svymean(x=~VD4020, design=dadosPNADc, na.rm=TRUE)
conf_medida <- confint(mediarenda, level = 0.95)
mediarenda <- as.data.frame(mediarenda)

mediarenda <- mediarenda |> 
  rename("Estimativa"=1, "Erro Padrão"=2) |> 
  mutate("Medidas-resumo"= c("Média"), .before = Estimativa) |> 
  bind_cols(conf_medida) |> 
  as_tibble()

# Quantis -----------------------------------------------------------------
quantisrenda <- svyquantile(~VD4020, dadosPNADc, quantiles = c(.25,.5,.75), 
                            na.rm = TRUE)
quantisrenda <- as.data.frame(quantisrenda$VD4020)

quantisrenda <- quantisrenda |> 
  select("Estimativa"=1,"Erro Padrão"=4, "2.5 %"= 2, "97.5 %" = 3) |> 
  mutate("Medidas-resumo"= c("1º Quartil", "2º Quartil", "3º Quartil"),
         .before = Estimativa) |> 
  as_tibble()


# Máximo e mínimo ---------------------------------------------------------
max <- max(df$VD4020, na.rm=T)
min <- min(df$VD4020, na.rm=T)

# Decis -------------------------------------------------------------------
decisrenda <- svyquantile(~VD4020, dadosPNADc, interval.type=c("mean"),
                          quantiles = seq(0.1,1,0.1), na.rm = T)
decisrenda<-as.data.frame(decisrenda$VD4020)

# Gerando a tabela para LaTex ---------------------------------------------
est_descr <- rbind(mediarenda, quantisrenda)

tab<-xtable(est_descr, caption = "Densidade do Rendimento Mensal Efetivo -
            4º Tri/2023", label = "sum")
print(tab,file="Tabelas/tab1.tex",compress=F, include.rownames = F)

tab2<-xtable(decisrenda, caption = "Decis da distribuição de rendimentos efetivos -
            4º Tri/2023", label = "sum")
print(tab2,file="Tabelas/tab2.tex",compress=F, include.rownames = F)


# Figuras -----------------------------------------------------------------

# Histograma --------------------------------------------------------------

svyhist(~ as.numeric(VD4020), main="",dadosPNADc, xlab = "Rendimento Mensal Efetivo (em R$)", 
        ylab="Densidade", xlim=c(0,30000),freq = FALSE,breaks = 500) 
dev.copy(pdf,"graf1.pdf")
dev.off()

svyhist(~ as.numeric(VD4020), main="",dadosPNADc, xlab = "Rendimento Mensal Efetivo (em R$)", 
        ylab="Densidade", freq = FALSE, xlim=c(0,10000),breaks = 500)
dev.copy(pdf,"graf2.pdf")
dev.off()

svyhist(~ as.numeric(VD4035), dadosPNADc, main = "Histograma", 
        xlab = "Número de Horas Trabalhadas")
dev.copy(pdf,"graf3.pdf")
dev.off()


# Boxplot -----------------------------------------------------------------

#graf4 <- svyboxplot(VD4020 ~ 1, dadosPNADc, main = "", ylim=c(0,5000))

# Dispersão ---------------------------------------------------------------

#graf5 <- svyplot(VD4035~VD4020, dadosPNADc, pch=19)

