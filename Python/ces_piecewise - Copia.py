import pandas as pd
import numpy as np
from scipy.optimize import minimize
from scipy.integrate import quad
from scipy.stats import pareto, uniform

# 2) TWO-BRACKET PIECEWISE ANALYSIS

# A produtividade crítica na qual um indivíduo que enfrenta a menor taxa marginal de imposto (t1) escolhe ganhar exatamente o limite de ganhos 'ycheck' é
# dado por:

def wtilde(t1,ycheck,a,k):
    return ((a*((ycheck)**k))/(1-t1))**(1/(1+k))

# Da mesma forma, a produtividade crítica na qual um indivíduo que enfrenta a taxa marginal superior de imposto (t2) escolhe ganhar exatamente o limite de ganhos
#'ycheck' é dado por:

def wtilde2(t1,t2,ycheck,a,k):
    return ((a*((ycheck)**k))/(1-t2))**(1/(1+k))

# Juntando tudo isso, a função de ganhos ideal para um indivíduo de produtividade n é dada por:

def C(w,t1,t2,ycheck,a,k):
    if w<wtilde(t1,ycheck,a,k):
        return ((w*(1-t1)/a)**(1/k))*w
    elif (ntilde(t1,ycheck,a,k)<=n<=
    ntilde2(t1,t2,ycheck,a,k)):
        return ycheck
    else:
        return ((w*(1-t2)/a)**(1/k))*w

# Multiplicando a função de ganhos ideal pela distribuição de produtividade que o pdf dá:

def C_pdf(w,t1,t2,ycheck,a,k,MV,minn):
    return C(w,t1,t2,ycheck,a,k)*pareto.pdf(w,MV,loc=0,scale=minn)

# Integrando isso sobre todas as produtividades, obtém-se, assim, os ganhos médios sobre a subpopulação capaz.

def C_bar(t1,t2,ycheck,a,k,MV,minn):
    return quad(C_pdf,minn,100,args=(t1,t2,ycheck,a,k,MV,minn))[0]

# As diferenças entre os ganhos de um indivíduo com n > ntilde2 e o limite de ganhos, multiplicado pela distribuição de produtividade pdf são
# dado por:

def C_diff_pdf(w,t1,t2,ycheck,a,k,MV,minn):
    return ((((w*(1-t2)/a)**(1/k))*w-ycheck)* pareto.pdf(w,MV,loc=0,scale=minn))

# O número de indivíduos capazes que ganham acima do limiar «ycheck» é dado por:

def prop_ycheck(t1,ycheck,a,k,MV,minn):
    return 1-pareto.cdf(wtilde(t1,ycheck,a,k),MV,loc=0,scale=minn)

# A utilidade indireta de um indivíduo de produtividade n é dada por:

def v(w,t1,t2,ycheck,B,a,k):
    if w<wtilde(t1,ycheck,a,k):
        return np.log(((w*(1-t1)/a)**(1/k))*w*(1-t1)+ B - a*(((((w*(1-t1)/a)**(1/k)))**(1+k))/(1+k)))
    elif wtilde(t1,ycheck,a,k)<=w<=wtilde2(t1,t2,ycheck,a,k):
        return np.log(ycheck*(1-t1)+ B -a*(((ycheck/w)**(1+k))/(1+k)))
    else:
        return np.log(ycheck*(t2-t1)+((w*(1-t2)/a)**(1/k))*w*(1-t2)+ B -a*(((((w*(1-t2)/a)**(1/k)))**(1+k))/(1+k)))

# Multiplicando a função utilidade indireta pela produtividade que o pdf dá:

def v_pdf(w,t1,t2,ycheck,B,a,k,MV,minn):
    return (v(w,t1,t2,ycheck,B,a,k)*pareto.pdf(w,MV,loc=0,scale=minn))

# 2.1) PROBLEMA DE OTIMIZAÇÃO POR PARTES

R = 10
minn = 1
MV = 1.2952
k = 4

def objective(x, a):
    B, t1, t2, ycheck = x
    return -quad(v_pdf, minn, 545, args=(t1,t2,ycheck,B,a,k,MV,minn))[0]


def constraint_eq(x,a):
    B, t1, t2, ycheck = x
    integral_result = quad(C_pdf,minn,wtilde(x[1],x[3],a,k) ,args=(x[1],x[2],x[3],a,k,MV,minn))[0]
    integral_result2 = quad(C_diff_pdf,wtilde2(x[1],x[2],x[3],a,k),545,args=(x[1],x[2],x[3],a,k,MV,minn))[0]
    return (x[1]*(integral_result + x[3]*prop_ycheck(x[1],x[3],a,k,MV,minn))+
                      x[2]* integral_result2)- (R + x[0])


results_list = []

for a_value in np.arange(0.30, 0.61, 0.15):
    cons = [{'type': 'eq', 'fun': constraint_eq, 'args': (a_value,)}]
    bounds = [(0, 5000), (0, 0.99), (0, 0.99), (2.525, 1000)]
    init = [100, 0.1, 0.1, 10]

    solution = minimize(objective, init, args=(a_value,), method='SLSQP', constraints=cons, bounds=bounds, options={'maxiter': 200})
    results_list.append({'a': a_value, 'B': solution.x[0], 't1': solution.x[1], 't2': solution.x[2], 'ycheck': solution.x[3], 'fun': solution.fun,
                         'success': solution.success, 'Objective': solution.fun, 'Iteracoes': solution.nit})

results_df = pd.DataFrame(results_list)
results_df.to_csv('data/output_results/resultado_otimizacao_ces.csv', index=False)















