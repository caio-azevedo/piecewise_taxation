# Limpar
rm(list=ls())

# Pacotes
library(Pareto)
library(tidyverse)
library(extrafont)


# Dados

dados <- read.csv("data/dadosPNADc.csv")

#Estimando índice de pareto por MMV

x<- dados |> 
  filter(VD4020>1200) |> 
  pull(VD4020)

neg_log_lik <- function(x, alpha){
  A <- min(x)
  n <- length(x)
  ll <- n*log(alpha)+n*alpha*log(A)-(alpha+1)*sum(log(x))
  return(-ll)
}

fit <- stats::optim(par = 1, fn = neg_log_lik, x = x, 
                    method = "BFGS", hessian = TRUE)

MV<-fit$par

fisher.information.fit <- solve(fit$hessian)
standard.deviance.fit <- sqrt(diag(fisher.information.fit))


t.fit <- fit$par/standard.deviance.fit
pvalue.fit <- 2*(1-pt(abs(t.fit), length(x)-length(fit$par)))
results.fit <- cbind(fit$par, standard.deviance.fit, t.fit, pvalue.fit)
colnames(results.fit) <- c("parâmetros", "desvio-padrão", 
                           "estatística t", "p-valor")
rownames(results.fit) <- c("alpha")
print(results.fit, digits = 3)


# Número de arquivos que você deseja criar
pop<-seq(100000,1000000,50000)
arquivo<-vector('list', length(pop))

# Use um loop "for" para criar os arquivos
for (i in 1:length(pop)) {
  # Crie o nome do arquivo
  arquivo[[i]] <- paste0("data/pareto_", i, ".csv")
  i<-i+1
}

# Criando as distribuições de Rendas teóricas
for (i in c(1:length(pop))) {
  
  set.seed(1)
  pareto<-data.frame(renda=rPareto(0.80*pop[i],1200,MV,120000))
  set.seed(1)
  uniforme<-data.frame(renda=runif(0.20*pop[i],0,1200))
  pareto<-rbind(uniforme,pareto)
  
  write.csv(pareto, file=arquivo[[i]], row.names = FALSE)
}


# Tabela Descritiva -------------------------------------------------------

tab_descr <- pareto |>
  rename("VD4020"=renda) |> 
  summarise("Média" = mean(VD4020),
            "Mediana" = median(VD4020),
            "1º Quartil" = quantile(VD4020, probs=c(0.25)),
            "3º Quartil" = quantile(VD4020, probs=c(0.75)),
            "Mínimo" = min(VD4020),
            "Máximo" = max(VD4020)) |> 
  pivot_longer(cols=everything(),
               names_to = "Medidas-resumo",
               values_to = "Valor")


# Gráficos ----------------------------------------------------------------

source("R/Auxiliares/theme.R")

pareto |> 
  ggplot() +
  aes(x=renda) + 
  geom_histogram(aes(y = after_stat(density)),bins=400, color="black") + 
  tema+
  labs(x = "Rendimento mensal efetivo (em R$)",
       y = "Densidade") +
  coord_cartesian(xlim=c(0,30000))+
  scale_x_continuous(breaks = seq(0,30000,5000))+
  scale_y_continuous(breaks = seq(0,6e-4,1e-4))

pareto |> 
  ggplot() +
  aes(x=renda) + 
  geom_histogram(aes(y = after_stat(density)),bins=400, color = "black") + 
  tema+
  labs(x = "Rendimento mensal efetivo (em R$)",
       y = "Densidade") +
  coord_cartesian(xlim=c(0,10000)) +
  scale_x_continuous(breaks = seq(0,10000,2000))+
  scale_y_continuous(breaks = seq(0,6e-4,1e-4))

