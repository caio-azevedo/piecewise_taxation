import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy.integrate import quad
from scipy.stats import pareto, uniform

# Definindo as funções conforme o ajuste anterior
def Lz(B, t, w, L, a):
    return np.where(w >= 2.525, ((1 - a) * (B + (1 - t) * w * L) / ((1 - t) * w)), 720)

def C(B, t, w, L, a):
    return np.where(w >= 2.525, a * (B + (1 - t) * w * L), B)

def v(B, t, w, L, a):
    c_value = C(B, t, w, L, a)
    lz_value = Lz(B, t, w, L, a)
    return np.where(w >= 2.525, c_value**a * lz_value**(1 - a), c_value**a)

def v_pdf(w, B, t, L, a, minn):
    return np.where(w >= minn, v(B, t, w, L, a) * pareto.pdf(w, MV, loc=0, scale=minn), v(B, t, w, L, a) * uniform.pdf(w, loc=0, scale= minn))

def Lt_pdf(w, B, t, L, a, minn):
    return np.where(w >= minn, w * (L - Lz(B, t, w, L, a)) * pareto.pdf(w, MV, loc=0, scale=minn), w * (L - Lz(B, t, w, L, a)) * uniform.pdf(w, loc=0, scale= minn))




# Parâmetros iniciais
L = 720
R = 10
minn = 5
MV = 1.2952

def objective(x, a):
    B, t = x
    return -quad(v_pdf, minn, 545, args=(B, t, L, a, minn))[0]

def constraint_eq(x, a):
    B, t = x
    return R + B - t * quad(Lt_pdf, minn, 545, args=(B, t, L, a, minn))[0]


# Inicialize uma lista para armazenar os resultados temporariamente
results_list = []

for a_value in np.arange(0.30, 0.61, 0.05):
    cons = [{'type': 'eq', 'fun': constraint_eq, 'args': (a_value,)}]
    bounds = [(0, None), (0, 1)]
    init = [100, 0.1]

    solution = minimize(objective, init, args=(a_value,), method='SLSQP', constraints=cons, bounds=bounds, options={'maxiter': 200})

    # Adicionando o resultado como um dicionário à lista
    results_list.append({'a': a_value, 'B': solution.x[0], 't': solution.x[1], 'fun': solution.fun, 'success': solution.success,
                         'Objective': solution.fun, 'Iteracoes': solution.nit})

# Convertendo a lista de resultados em um DataFrame
results_df = pd.DataFrame(results_list)

print(results_df)














   
