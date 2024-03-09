
from concurrent.futures import ThreadPoolExecutor  # Usando ThreadPoolExecutor
import numpy as np
import pandas as pd
import glob
from scipy.optimize import minimize

# Funções vetorizadas
def Lz(B, t, w, L, a, w_lim):
    return np.where(w >= w_lim, ((1 - a) * (B + (1 - t) * w * L) / ((1 - t) * w)), 720)

def C(B, t, w, L, a, w_lim):
    return np.where(w >= w_lim, a * (B + (1 - t) * w * L), B)

def U(B, t, w, L, a, w_lim):
    c_value = C(B, t, w, L, a, w_lim)
    lz_value = Lz(B, t, w, L, a, w_lim)
    return np.where(w >= w_lim, c_value**a * lz_value**(1 - a), c_value**a)

# Carregar os nomes dos arquivos de dados
tabelas = glob.glob("data/Pareto/*.csv")  # Certifique-se de que o caminho esteja correto

# Sequência de alphas para iterar
alpha_seq = np.arange(0.30, 0.61, 0.1)  # Inclui 0.60

# Função para processamento dos dados e otimização
def processar_tabela(tabela):
    pareto = pd.read_csv(tabela)
    w = pareto['renda'] / 240
    n = len(w)
    L = np.repeat(720, n)
    R = 10 * n
    results = []

    for alpha in alpha_seq:
        a = np.repeat(alpha, n)
        init = [100, 0.1, 2.525]

        def objective(x):
            return -np.sum(U(x[0], x[1], w, L, a, x[2]))

        def constraint_eq(x):
            return R + np.sum(x[0] - x[1] * w * (L - Lz(x[0], x[1], w, L, a, x[2])))

        cons = ({'type': 'eq', 'fun': constraint_eq})
        bounds = [(0, None), (0, 1), (2.525, None)]
        
        solution = minimize(objective, init, method='SLSQP', constraints=cons, bounds=bounds, options={'maxiter': 200})
        
        # Corrigido: Agora acessando os atributos do objeto de solução diretamente
        results.append({
            'Alpha': alpha,
            'B': solution.x[0],
            't': solution.x[1],
            'w_lim': solution.x[2],
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
final_df.to_csv("data/teste_df.csv")



