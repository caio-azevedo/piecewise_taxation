results <- future_lapply(tabelas, function(tabela) {
  load(tabela)
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
