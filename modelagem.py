import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from math import *

#PARÂMETROS:

#massas (kg)
ma = 3.0 # água gelada (medir o volume na caixa)
mg = 0.210 # garrafa de vidro (pesar vazia)
mb = 0.330 # bebida (~330 mL)


# geo. da garrafa (m) - dois cilindros
D1, H1 = 0.060, 0.13 # corpo
D2, H2 = 0.025, 0.10 # gargalo

#áreas (m2)
Ag = np.pi*D1*H1 + np.pi*D2*H2 + np.pi*D1**2/4

#vidro
d = 0.003 # espessura (m)
k = 1.0 # condutividade (W/(m.K))

#Temperaturas iniciais (K)
T_A0 = 273.15 + 2 # água gelada
T_G0 = 273.15 + 25 # garrafa
T_B0 = 273.15 + 25 # bebida  

#Calores específicos (J/(kg.K))
ca = 4186
cg = 840
cb = 4000

#coeficiente de transferência convectiva da água (W/(m2.K))
ha = 35
hb = 50


#MODELO:
R1 = 1/(ha*Ag) 
R2 = (d/2)/(k*Ag)
R3 = 1/(hb*Ag)

def modelo(x, t):
    Ta = x[0]
    Tg = x[1]
    Tb = x[2]
    Q1 = (Ta - Tg)/(R1 + R2)
    Q2 = (Tb - Tg)/(R2 + R3)

    dTadt = 1/(ma*ca) * (-Q1)
    dTgdt = 1/(mg*cg) * (Q1 - Q2)
    dTbdt = 1/(mb*cb) * (Q2)
    return [dTadt, dTgdt, dTbdt]


#IMPLEMENTAÇÃO:
#Condições iniciais
T_0 = [T_A0, T_G0, T_B0]

#Lista de tempo
dt = 1 #(segundos)
tf = 7200 #2 horas
t_lista = np.arange(0,tf+dt,dt)

#Resolução numérica
x_lista = odeint(modelo,T_0,t_lista)
Ta_lista = x_lista[:,0]-273.15
Tg_lista = x_lista[:,1]-273.15
Tb_lista = x_lista[:,2]-273.15

plt.plot(t_lista/60, Ta_lista, label='Água gelada')
plt.plot(t_lista/60, Tg_lista, label='Garrafa')
plt.plot(t_lista/60, Tb_lista, label='Bebida')
plt.title('Temperatura da cerveja na água gelada em função do tempo')
plt.xlabel('Tempo ($min$)')
plt.ylabel('Temperatura ($°C$)')
plt.legend()
plt.grid()
plt.show()