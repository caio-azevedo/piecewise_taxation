from sympy import symbols, diff, simplify

# Definindo as variáveis
w, alpha, B, t = symbols('w alpha B t')

# Expressão para l* com base na equação rearranjada
l_star = ((1 - alpha) * (B + (1 - t) * w * 720) / ((1 - t) * w))

# L como função de w
L_w = 720 - l_star

# Derivada de L em relação a w
dL_dw = diff(L_w, w)

# Simplificando a expressão da derivada
dL_dw_simplified = simplify(dL_dw)

print(dL_dw_simplified)



