# clean up workspace ------------------------------------------------------
rm(list=ls())

# close all figure --------------------------------------------------------
graphics.off()

# load packages -----------------------------------------------------------
library(Rsolnp)
library(tidyverse)
library(future.apply)
library(glue)

# Ative o plano futuro para paralelismo com 6 workers ---------------------
plan(multisession, workers = 6)

# Carregar os dados de remunerações ---------------------------------------
tabelas <- list.files("data/Pareto_R", full.names = TRUE)

# Lista de funções de utilidade para iterar --------------------------------------
utility_function <- c("cobb_douglas")

for (obs in utility_function) {
  
  # Carregar as funções lazer, consumo e utilidade indireta -----------------
source(glue("R/function/function_{obs}.R"))

# Processamento dos dados e otimização para cada tabela e alpha --------
source(glue("R/results/results_{obs}.R"))
  
# Combinando todos os resultados em um único data frame
final_df <- bind_rows(results, .id = "Tabela")

# Salvando os resultados --------------------------------------------------
write_csv(final_df, glue("data/results/{obs}_df.csv"))
}
