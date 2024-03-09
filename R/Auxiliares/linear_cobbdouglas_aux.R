
# Limpando ----------------------------------------------------------------


rm(list=ls())


# Pacotes -----------------------------------------------------------------


library(Rsolnp)
library(tidyverse)



# Dados -------------------------------------------------------------------


tabelas<-list.files("data/Pareto") # ler todas os arquivos da pasta


# Objetos de apoio (loop) -------------------------------------------------


arquivo<-vector('list', length(tabelas))
df<-list()



# Criando arquivos --------------------------------------------------------


for (j in 1:length(tabelas)) {
  # Crie o nome do arquivo
  arquivo[[j]] <- paste0("Dados/Pareto/pareto_", j, ".RData")

# Abrir um rData
load(arquivo[[j]])
w<-pareto$renda/240


# Número de indivíduos ----------------------------------------------------


n <- length(w)


# Parâmetros da função de utilidade ---------------------------------------


alpha<-seq(0.30,0.60,0.01)

b<-vector('list',length(alpha))

for (i in c(1:length(alpha))) {

a<-rep(alpha[i],n)
v<-1


# Trabalho ----------------------------------------------------------------


L<-rep(720,n)


# Receita do governo ------------------------------------------------------


R<-10*n


# Valores iniciais para o algoritmo ---------------------------------------


init <- c(100,0.1)


# Lazer -------------------------------------------------------------------


Lz<-function(B,t,w,L,a){
  ifelse(w>=2.525,((1-a)*(B+(1-t)*w*L)/((1-t)*w)),720)
}


# Consumo -----------------------------------------------------------------


C<-function(B,t,w,L,a){
  ifelse(w>=2.525,a*(B + (1-t)*w*L),B)
}

# Utilidade

U<-function(B,t,w,L,a){
  ifelse(w>=2.525,C(B,t,w,L,a)^a*Lz(B,t,w,L,a)^(1-a),
         C(B,t,w,L,a)^a)
}


# Função Objetivo - Função Bem-estar Atkinson e Feldstein, com Utilidade Cobb Douglas
# Sinal negativo por ser uma maximização

objetivo <- function(x) {
  B <- x[1]; t <- x[2]; w<-w[seq(1,n,1)];L<-L[seq(1,n,1)];a<-a[seq(1,n,1)]
  -(sum(U(B,t,w,L,a)))
}


# Restrição de igualdade:  ------------------------------------------------

eq<-function(x){
  B <- x[1]; t <- x[2]; w<-w[seq(1,n,1)]; L<-L[seq(1,n,1)] ;a<-a[seq(1,n,1)]
  R + sum(B - t*w*(L-Lz(B,t,w,L,a)))
}



# Limite da restrição de desigualdade -------------------------------------


restricao <- c(R)

# Limite inferior (lower) e superior (upper) da restrição de desigualdade
lx <- c(0,0)
ux <- c(0.2*R,1)



# SOLUÇÃO  Restrição de igualdade -----------------------------------------

  solucao<- Rsolnp::solnp(pars = init, fun = objetivo,
                          eqfun = eq, eqB = 0, LB=lx,
                          UB=ux, control=list(outer.iter=200))

  b[[i]]<-c(solucao$pars,solucao$outer.iter, solucao$lagrange)
  i<-i+1
} # fim do primeiro loop

df[[j]]<-rbind(data.frame(),do.call(rbind,b))
rownames(df[[j]])<-c(alpha)
colnames(df[[j]])<-c("B","t","Interações","Lagrange")
j<-j+1
} # fim do segundo loop

basev<-do.call(rbind,df)
baseh<-do.call(cbind,df)

save(basev,file="data/resultados1.RData")
save(baseh,file="data/resultados2.RData")
save(df,file="data/df.RData")
