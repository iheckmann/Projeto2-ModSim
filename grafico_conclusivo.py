#IMPLEMENTAÇÃO
dt = 1
tf = 3*3600
t_lista = np.arange(0, tf+dt, dt)

#temperaturas iniciais de garrafa e bebida (K)
T_G0 = 273.15 + 20.1
T_B0 = 273.15 + 19.6

alvo = 5 #temperatura desejada da bebida (°C)
lista_TA0 = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5] #temperaturas iniciais da água (°C)

tempos = []
for TA0 in lista_TA0:
    x_lista = odeint(modelo, [273.15+TA0, T_G0, T_B0], t_lista)
    Tb = x_lista[:,2] - 273.15
    i = np.where(Tb <= alvo)[0]
    if len(i) > 0:
        tempos.append(t_lista[i[0]]/60)
    else:
        tempos.append(np.nan) #nunca chega no alvo

plt.plot(lista_TA0, tempos, 'o-')
for T, t in zip(lista_TA0, tempos):
    if not np.isnan(t):
        plt.text(T, t+1.5, '%.0f' % t, ha='center') #escreve tempo em cima de cada ponto

plt.title('Tempo para a bebida chegar a %d °C em função da temperatura inicial da água' % alvo)
plt.xlabel('Temperatura inicial da água ($°C$)')
plt.ylabel('Tempo ($min$)')
plt.grid()
plt.show()