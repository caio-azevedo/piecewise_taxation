# clean up workspace ------------------------------------------------------
rm(list=ls())

# close all figure --------------------------------------------------------
graphics.off()

# load packages -----------------------------------------------------------
library(Rsolnp)
library(tidyverse)
library(future.apply)

# Ative o plano futuro para paralelismo com 6 workers ---------------------
plan(multisession, workers = 6)

# Carregar os nomes dos arquivos de dados .csv
tabelas <- list.files("data/Pareto_R", full.names = TRUE, pattern = "\\.csv$")

# Funções definidas -------------------------------------------------------

# Função lazer
Lz <- function(B, t, w, L, a) {
  ifelse(w >= 2.525, ((1 - a) * (B + (1 - t) * w * L) / ((1 - t) * w)), 720)
}

# Função consumo
C <- function(B, t, w, L, a) {
  ifelse(w >= 2.525, a * (B + (1 - t) * w * L), B)
}

# Função utilidade indireta
U <- function(B, t, w, L, a) {
  c_value <- C(B, t, w, L, a)
  lz_value <- Lz(B, t, w, L, a)
  ifelse(w >= 2.525, c_value^a * lz_value^(1 - a), c_value^a)
}

# Sequência de alphas para iterar
alpha_seq <- seq(0.30, 0.60, 0.01)

# Processamento dos dados e otimização ------------------------------------
results <- future_lapply(tabelas, function(tabela) {
  pareto <- read_csv(tabela)
  w <- pareto$renda / 240
  n <- length(w)
  L <- rep(720, n)
  R <- 10 * n
  
  map_dfr(alpha_seq, function(alpha) {
    a <- rep(alpha, n)
    init <- c(100, 0.1)
    
    eq <- function(x) {
      B <- x[1]
      t <- x[2]
      R + sum(B - t * w * (L - Lz(B, t, w, L, a)))
    }
    
    solucao <- solnp(pars = init, 
                     fun = function(x) -sum(U(x[1], x[2], w, L, a)),
                     eqfun = eq, eqB = 0, 
                     LB = c(0, 0), UB = c(Inf, 1), 
                     control = list(outer.iter = 200))
    
    tibble(Alpha = alpha, B = solucao$pars[1], t = solucao$pars[2], Iteracoes = solucao$outer.iter, Lagrange = list(solucao$lagrange))
  }, .id = "ID")
}, future.seed = TRUE)

# Combinando todos os resultados em um único data frame
final_df <- bind_rows(results, .id = "Tabela")

# Exibindo os resultados
write_csv(final_df, "data/cobb_douglas_df.csv")
