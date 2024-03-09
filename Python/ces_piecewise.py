# 2) TWO-BRACKET PIECEWISE ANALYSIS

# A produtividade crítica na qual um indivíduo que enfrenta a menor taxa marginal de imposto (t1) escolhe ganhar exatamente o limite de ganhos 'ycheck' é
# dado por:

def ntilde(t1,ycheck,a,k):
    return ((a*((ycheck)**k))/(1-t1))**(1/(1+k))

# Da mesma forma, a produtividade crítica na qual um indivíduo que enfrenta a taxa marginal superior de imposto (t2) escolhe ganhar exatamente o limite de ganhos
#'ycheck' é dado por:

def ntilde2(t1,t2,ycheck,a,k):
    return ((a*((ycheck)**k))/(1-t2))**(1/(1+k))

# Juntando tudo isso, a função de ganhos ideal para um indivíduo de produtividade n é dada por:

def y(n,t1,t2,ycheck,a,k):
    if n<ntilde(t1,ycheck,a,k):
        return ((n*(1-t1)/a)**(1/k))*n
    elif (ntilde(t1,ycheck,a,k)<=n<=
    ntilde2(t1,t2,ycheck,a,k)):
        return ycheck
    else:
        return ((n*(1-t2)/a)**(1/k))*n

# Multiplicando a função de ganhos ideal pela distribuição de produtividade que o pdf dá:

def ypdf(n,t1,t2,ycheck,a,k,mu,minn):
    return y(n,t1,t2,ycheck,a,k)*pareto.pdf(n,mu,loc=0,scale=minn)

# Integrando isso sobre todas as produtividades, obtém-se, assim, os ganhos médios sobre a subpopulação capaz.

def ybar(t1,t2,ycheck,a,k,mu,minn):
    return quad(ypdf,minn,100,args=(t1,t2,ycheck,a,k,mu,minn))[0]

# As diferenças entre os ganhos de um indivíduo com n > ntilde2 e o limite de ganhos, multiplicado pela distribuição de produtividade pdf são
# dado por:

def ydiffpdf(n,t1,t2,ycheck,a,k,mu,minn):
    return ((((n*(1-t2)/a)**(1/k))*n-ycheck)* pareto.pdf(n,mu,loc=0,scale=minn))

# O número de indivíduos capazes que ganham acima do limiar «ycheck» é dado por:

def propoycheck(t1,ycheck,a,k,mu,minn):
    return 1-pareto.cdf(ntilde(t1,ycheck,a,k),mu,loc=0,scale=minn)

# A utilidade indireta de um indivíduo de produtividade n é dada por:

def v(n,t1,t2,ycheck,m,a,k):
    if n<ntilde(t1,ycheck,a,k):
        return np.log(((n*(1-t1)/a)**(1/k))*n*(1-t1)+m- a*(((((n*(1-t1)/a)**(1/k)))**(1+k))/(1+k)))
    elif ntilde(t1,ycheck,a,k)<=n<=ntilde2(t1,t2,ycheck,a,k):
        return np.log(ycheck*(1-t1)+m-a*(((ycheck/n)**(1+k))/(1+k)))
    else:
        return np.log(ycheck*(t2-t1)+((n*(1-t2)/a)**(1/k))*n*(1-t2)+m-a*(((((n*(1-t2)/a)**(1/k)))**(1+k))/(1+k)))

# Multiplicando a função utilidade indireta pela produtividade que o pdf dá:

def vpdf(n,t1,t2,ycheck,m,a,k,mu,minn):
    return (v(n,t1,t2,ycheck,m,a,k)*pareto.pdf(n,mu,loc=0,scale=minn))

# A utilidade indireta média sobre a subpopulação capaz é:

def wa(t1,t2,ycheck,m,a,k,mu,minn):
    return quad(vpdf,minn,100,args=(t1,t2,ycheck,m,a,k,mu,minn))[0]

# A utilidade indireta marginal de um indivíduo capaz é:

def vmpw(n,t1,t2,ycheck,m,a,k):
    if n < ntilde(t1, ycheck, a, k):
        return 1/(((n*(1 - t1)/a)**(1/k))*n*(1 - t1) + m - a*(((((n*(1 - t1)/a)**(1/k)))**(1 + k))/(1 + k)))
    elif (ntilde(t1, ycheck, a, k)<= n <= ntilde2(t1, t2, ycheck, a, k)):
        return 1/(ycheck*(1 - t1)+ m - a*(((ycheck/n)**(1 + k))/(1 + k)))
    else:
        return 1/(ycheck*(t2 - t1) + ((n*(1 - t2)/a)**(1/k))*n*(1 - t2)+ m - a*(((((n*(1 - t2)/a)**(1/k)))**(1 + k))/(1 + k)))

# Multiplicando isso pela distribuição de produtividade pdf então dá:

def vmpwpdf(n,t1,t2,ycheck,m,a,k,mu,minn):
    return (vmpw(n,t1,t2,ycheck,m,a,k)*pareto.pdf(n,mu,loc=0,scale=minn))

# A média smvi sobre a subpopulação capaz é assim:

def sbarpw(t1,t2,ycheck,m,a,k,mu,minn):
    return quad(vmpwpdf,minn,100,args=(t1,t2,ycheck,m,a,k,mu,minn))[0]

# A desigualdade entre grupos no avergae smvi é definida por:

def betapw(t1,t2,ycheck,ma,mun,a,k,mu,minn):
    return ux(mun)-sbarpw(t1,t2,ycheck,ma,a,k,mu,minn)

# 2.1) PROBLEMA DE OTIMIZAÇÃO POR PARTES


# Vamos x=(x[0],x[1],x[2],x[3],x[4])=(t1,t2,ycheck,b,c) denotam as variáveis que estamos otimizando.
# Escrito em termos do vetor de escolha, a receita tributária líquida na economia é dada por:

def budget(x,a,k,theta,mu,minn,r):
    return (1-theta)*(x[0]*(quad(ypdf,minn,ntilde(x[0],x[2],a,k) ,args=(x[0],x[1],x[2],a,k,mu,minn))[0]+ x[2]*propoycheck(x[0],x[2],a,k,mu,minn))+
                      x[1]*quad(ydiffpdf,ntilde2(x[0],x[1],x[2],a,k),100,args=(x[0],x[1],x[2],a,k,mu,minn))[0])-r
















