import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy.integrate import quad
from scipy.stats import pareto, uniform

# Funções vetorizadas ajustadas
def Lz(B, t1, t2, w, L, a, w_lim):
    conditions = [
        (w < 2.525),
        (w >= 2.525) & (w <= w_lim),
        (w > w_lim)
    ]
    choices = [
        720,
        ((1 - a) * (B + (1 - t1) * w * L)) / ((1 - t1) * w),
        ((1 - a) * (B + (1 - t1) * w * L + (1-t2)*(w - w_lim)*L)) / ((1 - t1) * w + (1 - t2)*(w - w_lim))
    ]
    return np.select(conditions, choices)

def C(B, t1, t2, w, L, a, w_lim):
    conditions = [
        (w < 2.525),
        (w >= 2.525) & (w <= w_lim),
        (w > w_lim)
    ]
    choices = [
        B,
        a * (B + (1 - t1) * w * L),
        a * (B + (1 - t1) * w * L + (1-t2)*(w - w_lim)*L)
    ]
    return np.select(conditions, choices)

def v(B, t1, t2, w, L, a, w_lim):
    c_value = C(B, t1, t2, w, L, a, w_lim)
    lz_value = Lz(B, t1, t2, w, L, a, w_lim)
    return c_value ** a * lz_value ** (1 - a)

def v_pdf(w, B, t1, t2, L, a, w_lim, minn):
    return np.where(w >= minn, v(B, t1, t2, w, L, a, w_lim) * pareto.pdf(w, 1.3, loc=0, scale=minn),
                    v(B, t1, t2, w, L, a, w_lim) * uniform.pdf(w, loc=0, scale=minn))

def Lt_pdf(w, B, t1, t2, L, a, w_lim, minn):
    return np.where(w >= minn, w * (L - Lz(B, t1, t2, w, L, a, w_lim)) * pareto.pdf(w, 1.3, loc=0, scale=minn),
                    w * (L - Lz(B, t1, t2, w, L, a, w_lim)) * uniform.pdf(w, loc=0, scale=minn))

L = 720
R = 10
minn = 5
MV = 1.2952

def objective(x, a):
    B, t1, t2, w_lim = x
    return -quad(v_pdf, minn, 545, args=(B, t1, t2, L, a, w_lim, minn))[0]

def constraint_eq(x, a):
    B, t1, t2, w_lim = x
    integral_result = quad(Lt_pdf, minn, 545, args=(B, t1, t2, L, a, w_lim, minn))[0]
    return R + B - t1 * integral_result - t2 * integral_result - t2 * w_lim * integral_result

results_list = []

for a_value in np.arange(0.30, 0.61, 0.15):
    cons = [{'type': 'eq', 'fun': constraint_eq, 'args': (a_value,)}]
    bounds = [(0, 5000), (0, 1), (0, 1), (2.525, 1000)]
    init = [100, 0.1, 0.1, 10]

    solution = minimize(objective, init, args=(a_value,), method='SLSQP', constraints=cons, bounds=bounds, options={'maxiter': 200})
    results_list.append({'a': a_value, 'B': solution.x[0], 't1': solution.x[1], 't2': solution.x[2], 'w_lim': solution.x[3], 'fun': solution.fun, 'success': solution.success, 'Objective': solution.fun, 'Iteracoes': solution.nit})

results_df = pd.DataFrame(results_list)
results_df.to_csv('data/output_results/resultado_otimizacao.csv', index=False)
print(results_df)



        
