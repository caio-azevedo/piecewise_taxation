from concurrent.futures import ThreadPoolExecutor  # Usando ThreadPoolExecutor
import numpy as np
import pandas as pd
import glob
from scipy.optimize import minimize
import os


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

def U(B, t1, t2, w, L, a, w_lim):
    c_value = C(B, t1, t2, w, L, a, w_lim)
    lz_value = Lz(B, t1, t2, w, L, a, w_lim)
    return np.where(w >= 2.525, c_value**a * lz_value**(1 - a), c_value**a)


# Carregar os nomes dos arquivos de dados
tabelas = glob.glob("data/Pareto/*.csv")  # Certifique-se de que o caminho esteja correto

# Sequência de alphas para iterar
alpha_seq = np.arange(0.30, 0.61, 0.05)  # Inclui 0.60

# Processamento dos dados e otimização
def processar_tabela(tabela):
    pareto = pd.read_csv(tabela)
    w = pareto['renda'] / 240
    n = len(w)
    L = np.repeat(720, n)
    R = 10 * n
    results = []

 
    for alpha in alpha_seq:
        a = np.repeat(alpha, n)
        init = np.clip([1000, 0.1, 0.05, np.median(w)], a_min=[0, 0, 0, np.min(w)], a_max=[np.inf, 1, 1, np.max(w)])

        def objective(x):
            return -np.sum(U(x[0], x[1], x[2], w, L, a, x[3]))

        def constraint(x):
            B, t1, t2, w_lim = x
            return R - np.sum(np.where(w <= w_lim, 
                                       B - t1 * w * (L - Lz(B, t1, t2, w, L, a, w_lim)),
                                       B - t1 * w * (L - Lz(B, t1, t2, w, L, a, w_lim)) - 
                                       t2 * (w - w_lim) * (L - Lz(B, t1, t2, w, L, a, w_lim))))
        
        cons = [{'type': 'eq', 'fun': constraint}]
        bounds = [(0, 2000), (0, 0.99), (0, 0.99), (2.525, 1000)]
        def my_callback(xk):
            print(xk)
        solution = minimize(objective, init, method='SLSQP', bounds=bounds, constraints=cons, callback=my_callback, options={'maxiter': 200, 'disp': True})

        results.append({
            'Alpha': alpha,
            'B': solution.x[0],
            't1': solution.x[1],
            't2': solution.x[2],
            'w_lim': solution.x[3],
            'Iteracoes': solution.nit,
            'Success': solution.success,
            'Objective': solution.fun
        })
            
    return pd.DataFrame(results)



# Executando em paralelo com ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=6) as executor:
    futures = [executor.submit(processar_tabela, tabela) for tabela in tabelas]
    results = [f.result() for f in futures]

# Combinando todos os resultados em um único DataFrame
final_df = pd.concat(results, keys=range(len(tabelas)), names=['Tabela', 'Row'])

# Exibindo e salvando os resultados
final_df.to_csv("data/df_final_piecewise_df.csv")
