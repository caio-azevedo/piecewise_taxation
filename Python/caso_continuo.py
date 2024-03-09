import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import pareto


np.random.seed(1)

# Definindo a população total e os parâmetros
n = 100000
MV = 1.25198493709081  # Parâmetro de forma da distribuição de Pareto
scale_pareto = 50000  # Parâmetro de escala da distribuição de Pareto

# Gerando a distribuição de salários de Pareto para 80% da população
pareto_salaries = pareto.rvs(MV, scale=scale_pareto, size=int(0.8 * n))

# Gerando a distribuição de salários uniforme para 20% da população
uniform_salaries = np.random.uniform(0, 900, size=int(0.2 * n))

# Combinando as duas distribuições
combined_salaries = np.concatenate((uniform_salaries, pareto_salaries))

# Criando um DataFrame
salaries_df = pd.DataFrame({'renda': combined_salaries})

salarios = salaries_df / 240

# Funções C e Lz
def C(B, t, w, L, alpha):
    return np.where(w >= 2.525, alpha * (B + (1 - t) * w * L), B)

def Lz(B, t, w, L, alpha):
    return np.where(w >= 2.525, ((1 - alpha) * (B + (1 - t) * w * L) / ((1 - t) * w)), 720)

# Utilidade do agente
def utilidade_agente(t, B, w, alpha, L):
    c = C(B, t, w, L, alpha)  # Consumo
    lz = Lz(B, t, w, L, alpha)  # Lazer
    return np.where(w >= 2.525, c**alpha * lz**(1 - alpha), c**a)

# Função objetivo para maximização (bem-estar social negativo)
def objetivo(x, salarios, alpha, L):
    t, B = x
    utilidades = np.array([utilidade_agente(t, B, w, alpha, L) for w in salarios])
    return -np.sum(utilidades)

# Restrição orçamentária do governo
def restrição_orçamentária(x, R, salarios):
    t, B = x
    receita = np.sum(t * salarios)
    return receita - (R + n * B)

# Otimização
def otimizar_bem_estar(alpha, R, L, salarios):
    cons = {'type': 'eq', 'fun': restrição_orçamentária, 'args': (R, salarios)}
    bounds = [(0, 1), (None, None)]  # t entre 0 e 1, B não negativo
    init_guess = [0.1, 1000]  # Chute inicial para taxa de imposto e transferência

    resultado = minimize(lambda x: objetivo(x, salarios, alpha, L), init_guess, method='SLSQP', bounds=bounds, constraints=cons)
    return resultado.x

# Executar a otimização
alpha = 0.3  # Exemplo de valor para alpha
R = 10 * n  # Receita necessária (despesas governamentais mais transferências)
L = 720  # Horas de lazer (fixas para simplificação)
resultado_otimização = otimizar_bem_estar(alpha, R, L, salarios)

print(resultado_otimização)
