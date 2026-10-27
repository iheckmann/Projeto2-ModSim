import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#massas (kg)
ma = 13.04
mg = 0.218
mb = 0.335

#geometria da garrafa (m)
D1, H1 = 0.059, 0.140
D2, H2 = 0.034, 0.045
Ag = np.pi*D1*H1 + np.pi*D2*H2 + np.pi*D1**2/4

#vidro
d = 0.003387
k = 1.0

#calores específicos
ca = 4186
cg = 840
cb = 4000

#convecção
ha = 51 #somente ha. hb foi removido pois ele é so relevante para a garrafa, não para a bebida

#temperaturas iniciais (K) = primeiras leituras do experimento
T_A0 = 273.15 + 0.0
T_G0 = 273.15 + 5.0
T_B0 = 273.15 + 9.9

#MODELO
R1 = 1/(ha*Ag)
R2 = (d/2)/(k*Ag)

def modelo(x, t):
    Ta = x[0]
    Tg = x[1]
    Tb = x[2]
    QB = (Tb - Tg)/(R1 + R2)
    QA = (Tg - Ta)/R2
    dTadt = 1/(ma*ca) * QA
    dTgdt = 1/(mg*cg) * (QB - QA)
    dTbdt = 1/(mb*cb) * (-QB)
    return [dTadt, dTgdt, dTbdt]

#IMPLEMENTAÇÃO
dt = 1
tf = 4300 # duração do experimento (s)
t_lista = np.arange(0, tf+dt, dt)
x_lista = odeint(modelo, [T_A0, T_G0, T_B0], t_lista)
Tb_lista = x_lista[:,2] - 273.15

#DADOS DO EXPERIMENTO
dados = np.loadtxt('temperaturas_extraidas.csv', delimiter=',', skiprows=1)
t_exp = dados[:,2]*100 #s (os quadros foram amostrados de 100 em 100)
t_exp[t_exp > 2497] += 3900 - 2497 #soma o intervalo sem gravação (18h07 até 18h30)
Tb_exp = dados[:,3]

#ERRO DO MODELO
Tb_modelo = np.interp(t_exp, t_lista, Tb_lista)
erro_C = np.mean(np.abs(Tb_modelo - Tb_exp))
erro_queda = erro_C/(Tb_exp[0] - Tb_exp[-1])*100
print('Erro médio =', round(erro_C, 2), '°C')
print('Erro em relação à queda total =', round(erro_queda, 1), '%')

#GRÁFICO
plt.plot(t_lista/60, Tb_lista, label='Modelo')
plt.scatter(t_exp[::4]/60, Tb_exp[::4], color='red', label='Experimento')
plt.title('Temperatura da bebida em função do tempo')
plt.xlabel('Tempo ($min$)')
plt.ylabel('Temperatura ($°C$)')
plt.axvspan(2497/60, 3900/60, color='gray', alpha=0.2, label='Sem gravação')
plt.legend()
plt.grid()
plt.show()