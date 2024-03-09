

# Cobb Douglas ------------------------------------------------------------


# Lazer -------------------------------------------------------------------
Lz <- function(B, t, w, L, a) {
  ifelse(w >= 2.525, ((1 - a) * (B + (1 - t) * w * L) / ((1 - t) * w)), 720)
}


# Consumo -----------------------------------------------------------------
C <- function(B, t, w, L, a) {
  ifelse(w >= 2.525, a * (B + (1 - t) * w * L), B)
}


# Utilidade indireta ------------------------------------------------------
U <- function(B, t, w, L, a) {
  c_value <- C(B, t, w, L, a)
  lz_value <- Lz(B, t, w, L, a)
  ifelse(w >= 2.525, c_value^a * lz_value^(1 - a), c_value^a)
}


# Sequência de alphas para iterar -----------------------------------------
alpha_seq <- seq(0.30, 0.60, 0.01)
