'''
Considerações importantes:

Cáculo de rendimento mensal feito com (rendimento anual / 12) é conta de padeiro.
A fórmula correta dos juros compostos é: M = P * (1 + r/n)^(n*t)

O código considera o reinvestimento de proventos, o que é essencial para dar inicio ao "efeito bola de neve".
A inflação não está sendo considerada.

Essa simulação deixa claro que consistência, especialmente no inicio onde os aportes são uma parcela significativa do total, é a chave para geração de renda passiva.
Ao investir com disciplina, flutuações de curto prazo são mitigadas e se percebe os benefícios do crescimento composto.
'''
import matplotlib.pyplot as plt
import numpy as np

def atualizacao_valor(saldo, aporte_mensal, renda_passiva_mensal, rendimento_mensal, soma_valor_bolso, dividend_yield_anual):
    
    saldo += aporte_mensal + renda_passiva_mensal
    saldo *= rendimento_mensal
    
    soma_valor_bolso += aporte_mensal

    renda_passiva_anual = saldo * dividend_yield_anual
    renda_passiva_mensal = renda_passiva_anual / 12

    return saldo, soma_valor_bolso, renda_passiva_mensal

def construcao_grafico(lista_aportado, lista_redimento, lista_renda_passiva):

    plt.bar(np.arange(len(lista_aportado)), lista_aportado, label='Bolso')
    plt.bar(np.arange(len(lista_redimento)), lista_redimento, bottom=lista_aportado, label='Rendimento')
    plt.ylabel('Saldo')
    plt.xlabel('Períodos')
    plt.title('Total investido ao Longo do tempo')
    plt.grid(True)
    plt.legend()
    # Adiciona os valores do saldo dentro das barras
    for i, valor in enumerate(lista_aportado):
        plt.text(i, valor/2, f"{round(valor, 2)}", ha='center', va='center')

    # Adiciona os valores do rendimento dentro das barras
    for i, valor in enumerate(lista_redimento):
        plt.text(i, lista_aportado[i] + valor/2, f"{round(valor, 2)}", ha='center', va='center')

    # Adiciona os valores da renda passiva no topo das barras
    #Ideia de melhoria, para as primeiras colunas, usar um valor de Y maior para não ficar sobreposto
    for i, valor in enumerate(lista_redimento):
        plt.text(i, lista_aportado[i]*1.2 + valor, f"{round(lista_renda_passiva[i], 2)}", ha='center', va='top')

    plt.show() 

def comparar_ao_cdi(valor_inicial, aporte_mensal, anos, meses):

    cdi_mensal = pow((1+TAXA_CDI), (1/12))
    saldo_cdi =  valor_inicial*cdi_mensal

    tempo = anos*12 + meses
    while tempo > 1:

        saldo_cdi = (saldo_cdi + aporte_mensal)*cdi_mensal
        tempo -= 1

    return saldo_cdi

def tempo_para_renda_desejada(valor_inicial, aporte_mensal, rendimento_anual, dividend_yield_anual, renda_passiva_desejada):
    
    saldo = valor_inicial
    meses = 0
    renda_passiva_mensal = 0
    rendimento_mensal = pow((1+rendimento_anual), (1/12))
    lista_aportado, lista_redimento, lista_renda_passiva = [], [], []
    soma_valor_bolso = valor_inicial

    while renda_passiva_mensal < renda_passiva_desejada:
        
        saldo, soma_valor_bolso, renda_passiva_mensal = atualizacao_valor(saldo, aporte_mensal, renda_passiva_mensal, rendimento_mensal, soma_valor_bolso, dividend_yield_anual)

        if meses % INTERVALO_COLUNAS == 0:
            lista_aportado.append(soma_valor_bolso)
            lista_redimento.append(saldo - soma_valor_bolso)
            lista_renda_passiva.append(renda_passiva_mensal)

        meses += 1
    
    if soma_valor_bolso != lista_aportado[-1]:
        lista_aportado.append(soma_valor_bolso)
        lista_redimento.append(saldo - soma_valor_bolso)
        lista_renda_passiva.append(renda_passiva_mensal)

    anos = meses // 12
    meses_restantes = meses % 12
    
    print('Saldo: {:,.2f}'.format(saldo))
    print('Investindo em 100% do CDI seria: {:,.2f}'.format(comparar_ao_cdi(valor_inicial, aporte_mensal, anos, meses_restantes)))
    print('Uma diferença de: {:,.2f}'.format(saldo - comparar_ao_cdi(valor_inicial, aporte_mensal, anos, meses_restantes)))
    print(f"Levará aproximadamente {anos} anos e {meses_restantes} meses para atingir a renda passiva desejada de R${renda_passiva_desejada:,.2f} mensais.")
    construcao_grafico(lista_aportado, lista_redimento, lista_renda_passiva)

def renda_mensal_estimada_apos_anos(valor_inicial, aporte_mensal, rendimento_anual, dividend_yield_anual, anos, meses):
    
    saldo = valor_inicial
    tempo = anos * 12 + meses
    renda_passiva_mensal = 0
    rendimento_mensal = pow((1 + rendimento_anual), (1 / 12))
    lista_aportado, lista_redimento, lista_renda_passiva = [], [], []
    soma_valor_bolso = valor_inicial

    for _ in range(tempo):
        
        saldo, soma_valor_bolso, renda_passiva_mensal = atualizacao_valor(saldo, aporte_mensal, renda_passiva_mensal, rendimento_mensal, soma_valor_bolso, dividend_yield_anual)

        if _ % INTERVALO_COLUNAS == 0:
            lista_aportado.append(soma_valor_bolso)
            lista_redimento.append(saldo - soma_valor_bolso)
            lista_renda_passiva.append(renda_passiva_mensal)

    if soma_valor_bolso != lista_aportado[-1]:
        lista_aportado.append(soma_valor_bolso)
        lista_redimento.append(saldo - soma_valor_bolso)
        lista_renda_passiva.append(renda_passiva_mensal)

    print('Saldo: {:,.2f}'.format(saldo))
    print('Investindo em 100% do CDI seria: {:,.2f}'.format(comparar_ao_cdi(valor_inicial, aporte_mensal, anos, meses)))
    print('Uma diferença de: {:,.2f}'.format(saldo - comparar_ao_cdi(valor_inicial, aporte_mensal, anos, meses)))
    print(f"A renda mensal estimada após {anos} anos e {meses} meses é de aproximadamente R${renda_passiva_mensal:,.2f}")
    construcao_grafico(lista_aportado, lista_redimento, lista_renda_passiva)

#Exemplo de uso:
#valor_inicial = float(input("Informe o valor inicial: "))
#aporte_mensal = float(input("Informe o valor do aporte mensal: "))
#rendimento_anual = float(input("Informe o rendimento anual esperado (em decimal): "))
#dividend_yield_anual = float(input("Informe o dividend yield anual (em decimal): "))
#renda_passiva_desejada = float(input("Informe a renda passiva desejada: "))

valor_inicial = float(15000)
aporte_mensal = float(1000)
rendimento_anual = float(0.10)
dividend_yield_anual = float(0.069)
renda_passiva_desejada = float(0)
anos_informados, meses_informados = int(10), int(0)
#100% do CDI está em 0.1365
TAXA_CDI = float(0.1365)
INTERVALO_COLUNAS = int(12)

if anos_informados == 0 and meses_informados == 0:
    tempo_para_renda_desejada(valor_inicial, aporte_mensal, rendimento_anual, dividend_yield_anual, renda_passiva_desejada)
else:
    renda_mensal_estimada_apos_anos(valor_inicial, aporte_mensal, rendimento_anual, dividend_yield_anual, anos_informados, meses_informados)
