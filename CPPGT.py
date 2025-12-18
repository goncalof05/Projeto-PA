import csv
import os
from datetime import datetime

# CSV file paths
CATALOGO_FILE = "catalogo.csv"
MOVIMENTOS_FILE = "movimentos.csv"
PEDIDOS_FILE = "pedidos.csv"

# Initialize CSV files if they don't exist
def inicializar_ficheiros():
    if not os.path.exists(CATALOGO_FILE):
        with open(CATALOGO_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['idItem', 'tipo', 'nome', 'descricao', 'categoria', 'preco', 'duracaoPadraoMin', 'stock', 'ativo'])
    
    if not os.path.exists(MOVIMENTOS_FILE):
        with open(MOVIMENTOS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['idItem', 'tipo', 'quantidade', 'data', 'descricao'])
    
    if not os.path.exists(PEDIDOS_FILE):
        with open(PEDIDOS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['idPedido', 'nome', 'dataHora', 'estado', 'total'])

# Read catalog from CSV
def ler_catalogo():
    catalogo = []
    if os.path.exists(CATALOGO_FILE):
        with open(CATALOGO_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row:
                    catalogo.append({
                        'idItem': int(row['idItem']),
                        'tipo': row['tipo'],
                        'nome': row['nome'],
                        'descricao': row['descricao'],
                        'categoria': row['categoria'],
                        'preco': float(row['preco']),
                        'duracaoPadraoMin': row['duracaoPadraoMin'] if row['duracaoPadraoMin'] else None,
                        'stock': int(row['stock']),
                        'ativo': row['ativo'].lower() == 'true'
                    })
    return catalogo

# Write catalog to CSV
def guardar_catalogo(catalogo):
    with open(CATALOGO_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['idItem', 'tipo', 'nome', 'descricao', 'categoria', 'preco', 'duracaoPadraoMin', 'stock', 'ativo'])
        writer.writeheader()
        for item in catalogo:
            writer.writerow({
                'idItem': item['idItem'],
                'tipo': item['tipo'],
                'nome': item['nome'],
                'descricao': item['descricao'],
                'categoria': item['categoria'],
                'preco': item['preco'],
                'duracaoPadraoMin': item['duracaoPadraoMin'] if item['duracaoPadraoMin'] else '',
                'stock': item['stock'],
                'ativo': str(item['ativo']).lower()
            })

# Validate item data
def validar_item(item):
    erros = []
    if item['preco'] < 0:
        erros.append("Preço não pode ser negativo")
    if item['stock'] < 0:
        erros.append("Stock não pode ser negativo")
    if item['ativo'] not in [True, False]:
        erros.append("Estado ativo deve ser true ou false")
    return erros

# Register stock movement
def registar_movimento(idItem, tipo, quantidade, descricao=""):
    with open(MOVIMENTOS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([idItem, tipo, quantidade, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), descricao])

# Filter catalog by multiple criteria
def filtrar_catalogo(catalogo, categoria=None, preco_min=None, preco_max=None, ativo=None, stock_minimo=None):
    filtrados = catalogo
    
    if categoria:
        filtrados = [item for item in filtrados if item['categoria'].lower() == categoria.lower()]
    if preco_min is not None:
        filtrados = [item for item in filtrados if item['preco'] >= preco_min]
    if preco_max is not None:
        filtrados = [item for item in filtrados if item['preco'] <= preco_max]
    if ativo is not None:
        filtrados = [item for item in filtrados if item['ativo'] == ativo]
    if stock_minimo is not None:
        filtrados = [item for item in filtrados if item['stock'] >= stock_minimo]
    
    return filtrados

# Get next ID
def proximo_id(catalogo):
    return max([item['idItem'] for item in catalogo], default=0) + 1

# Display catalog in table format
def exibir_catalogo(itens):
    if not itens:
        print("Nenhum item encontrado")
        return
    
    print("\n" + "="*120)
    print(f"{'ID':<5} {'Tipo':<10} {'Nome':<30} {'Categoria':<15} {'Preço':<10} {'Stock':<10} {'Ativo':<8}")
    print("="*120)
    for item in itens:
        ativo_str = "Sim" if item['ativo'] else "Não"
        print(f"{item['idItem']:<5} {item['tipo']:<10} {item['nome']:<30} {item['categoria']:<15} €{item['preco']:<9.2f} {item['stock']:<10} {ativo_str:<8}")
    print("="*120 + "\n")

# Show indicators
def mostrar_indicadores(catalogo):
    ativos = [item for item in catalogo if item['ativo']]
    stock_baixo = [item for item in ativos if item['stock'] < 50]
    
    print("\n" + "="*60)
    print("INDICADORES")
    print("="*60)
    print(f"Itens ativos: {len(ativos)}")
    print(f"Produtos com stock baixo (<50): {len(stock_baixo)}")
    
    if stock_baixo:
        print("\nProdutos com stock baixo:")
        for item in stock_baixo:
            print(f"  - {item['nome']}: {item['stock']} unidades")
    
    # Average price by category
    categorias = set(item['categoria'] for item in ativos)
    print("\nPreço médio por categoria:")
    for cat in sorted(categorias):
        itens_cat = [item for item in ativos if item['categoria'] == cat]
        preco_medio = sum(item['preco'] for item in itens_cat) / len(itens_cat)
        print(f"  - {cat}: €{preco_medio:.2f}")
    
    print("="*60 + "\n")

# Create order
def criar_encomenda(catalogo):
    exibir_catalogo([item for item in catalogo if item['ativo']])
    
    pedido = {}
    quant = {}
    total = {}
    totalF = 0
    
    for item in catalogo:
        if not item['ativo']:
            continue
        
        print(f"Quantas unidades de '{item['nome']}' pretende? (0 para pular)")
        try:
            q = float(input())
            if q < 0:
                print("Quantidade não pode ser negativa")
                q = 0
            elif q > item['stock']:
                print(f"Stock insuficiente. Máximo disponível: {item['stock']}")
                q = 0
            
            if q > 0:
                quant[item['idItem']] = q
                total[item['idItem']] = item['preco'] * q
                totalF += total[item['idItem']]
                # Register movement
                registar_movimento(item['idItem'], 'saida', q, 'Encomenda')
                # Update stock
                item['stock'] -= q
        except ValueError:
            print("Entrada inválida")
    
    if totalF == 0:
        print("Nenhum item adicionado à encomenda")
        return
    
    print("\n" + "="*60)
    print("RESUMO DA ENCOMENDA")
    print("="*60)
    for item in catalogo:
        if item['idItem'] in quant:
            print(f"{item['nome']}: {quant[item['idItem']]} x €{item['preco']:.2f} = €{total[item['idItem']:.2f}")
    
    print(f"{'TOTAL':<40}: €{totalF:.2f}")
    print("="*60)
    
    nome = input("\nNome para a encomenda: ")
    
    # Save order
    with open(PEDIDOS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([proximo_id_pedido(), nome, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'confirmada', totalF])
    
    guardar_catalogo(catalogo)
    print(f"Encomenda no nome de '{nome}' criada com sucesso!")

# Get next order ID
def proximo_id_pedido():
    pedidos = []
    if os.path.exists(PEDIDOS_FILE):
        with open(PEDIDOS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row:
                    pedidos.append(int(row['idPedido']))
    return max(pedidos, default=0) + 1

# Main menu
def main():
    inicializar_ficheiros()
    catalogo = ler_catalogo()
    
    print("="*60)
    print("BEM-VINDO AO SISTEMA DE GESTÃO DE CATÁLOGO")
    print("="*60)
    
    while True:
        print("\n1 - Criar encomenda")
        print("2 - Ver catálogo completo")
        print("3 - Filtrar catálogo")
        print("4 - Ver disponibilidade")
        print("5 - Indicadores")
        print("0 - Sair")
        
        op = input("\nEscolha uma opção: ").strip()
        
        if op == '1':
            criar_encomenda(catalogo)
        elif op == '2':
            catalogo = ler_catalogo()
            exibir_catalogo([item for item in catalogo if item['ativo']])
        elif op == '3':
            print("\nFiltrar por categoria (deixe em branco para ignorar):")
            categoria = input().strip() or None
            print("Preço mínimo (deixe em branco para ignorar):")
            preco_min = float(input()) if input().strip() else None
            print("Preço máximo (deixe em branco para ignorar):")
            preco_max = float(input()) if input().strip() else None
            
            filtrados = filtrar_catalogo(catalogo, categoria=categoria, preco_min=preco_min, preco_max=preco_max, ativo=True)
            exibir_catalogo(filtrados)
        elif op == '4':
            catalogo = ler_catalogo()
            disponiveis = [item for item in catalogo if item['ativo'] and item['stock'] > 0]
            exibir_catalogo(disponiveis)
        elif op == '5':
            catalogo = ler_catalogo()
            mostrar_indicadores(catalogo)
        elif op == '0':
            print("Obrigado, volte sempre!")
            break
        else:
            print("Opção inválida, tente outra vez")

if __name__ == "__main__":
    main()
def calcTotal(orderMaterialQtd, materialPrice):
    total = 0
    for i in range(0, len(orderMaterialQtd) - 1 + 1, 1):
        total = total + orderMaterialQtd[i] * materialPrice[i]
    
    return total

def materialsShow(materialsQualquerCoisa, materialsPrice):
    print("Lista de Materiais")
    for i in range(0, len(materialsQualquerCoisa) - 1 + 1, 1):
        print(str(i + 1) + "- " + materialsQualquerCoisa[i] + "(" + str(materialsPrice[i]) + " €/uni)")

def menu():
    print("Estas são as opções do menu")
    print("1 - Consultar stock")
    print("2 - Criar pedido")
    print("3 - Consultar pedido")
    print("4 - Cancelar/Listar pedidos")
    print("5 - Avaliar serviço")
    print("0 - Sair")
    option = int(input())
    
    return option

def orderConsult(materialsName, orderMaterialQtd, materialsPrice):
    for i in range(0, len(orderMaterialQtd) - 1 + 1, 1):
        print(" - O material selecionado foi " + materialsName[i] + " com a quantidade de " + str(orderMaterialQtd[i]) + " e custo " + str(orderMaterialQtd[i] * materialsPrice[i]))

def orderCreate(materialsName, orderMaterialQtd, materialsPrice):
    z = 0
    again = 0
    while True:    #This simulates a Do Loop
        materialsShow(materialsName, materialsPrice)
        materialSelecionado = int(input())
        if materialSelecionado > len(materialsName) or materialSelecionado == 0:
            print("Opção Inválida")
        else:
            print("Qual a quantidade pretendida?")
            qtd = float(input())
            orderMaterialQtd[materialSelecionado - 1] = orderMaterialQtd[materialSelecionado - 1] + qtd
        print("Deseja escolher mais materiais? " + chr(13) + "Se sim, insira 1. Se não, insira 0")
        again = int(input())
        z = z + 1
        if again != 1: break

def stockConsult(materialsName, materialsQtd, materialsPrice):
    for i in range(0, len(materialsName) - 1 + 1, 1):
        print(materialsName[i] + " - " + str(materialsQtd[i]) + " unidades | " + str(materialsPrice[i]) + "€/u")

def stockValidate(materialsName, materialsQtd, orderMaterialQtd, materialsPrice):
    for i in range(0, len(orderMaterialQtd) - 1 + 1, 1):
        if orderMaterialQtd[i] > 0:
            if orderMaterialQtd[i] > materialsQtd[i]:
                print(" - " + materialsName[i] + "(" + str(orderMaterialQtd[i]) + ") . A quantidade encomendada é superior à quantidade em stock " + str(materialsQtd[i]))
            else:
                materialsQtd[i] = materialsQtd[i] - orderMaterialQtd[i]
                print(" - " + materialsName[i] + " com a quantidade de " + str(orderMaterialQtd[i]) + " e custo " + str(orderMaterialQtd[i] * materialsPrice[i]))

# Main
qtPedidos = 100
pedidosCount = 0
pedidosId = [0] * (qtPedidos)
pedidosEstado = [""] * (qtPedidos)
pedidosOrigem = [""] * (qtPedidos)
pedidosDestino = [""] * (qtPedidos)
pedidosJanelaInicio = [""] * (qtPedidos)
pedidosJanelaFim = [""] * (qtPedidos)
pedidosItens = [""] * (qtPedidos)
items = [""] * (qtPedidos)
orderMaterialQtd = [0] * (7)
materialsPrice = [0] * (7)
materialsQtd = [0] * (7)

materialsPrice[0] = 10
materialsPrice[1] = 20
materialsPrice[2] = 35
materialsPrice[3] = 1
materialsPrice[4] = 2
materialsPrice[5] = 2
materialsPrice[6] = 150
materialsQtd[0] = 20
materialsQtd[1] = 20
materialsQtd[2] = 20
materialsQtd[3] = 20
materialsQtd[4] = 20
materialsQtd[5] = 20
materialsQtd[6] = 20
materialsName = [""] * (7)

materialsName[0] = "cimento(10kg)"
materialsName[1] = "cimento(25kg)"
materialsName[2] = "cimento(50kg)"
materialsName[3] = "tijolo furado(30 x 20 x 11cm)"
materialsName[4] = "tijolo maciço (22 x 11 x 5cm)"
materialsName[5] = "tijolo maciço (40 x 20 x 19cm)"
materialsName[6] = "areia (m3)"
repeat = 0
menuCall = 0
print("Seja bem-vindo ao sistema de encomendas" + chr(13) + "Qual o seu nome?")
for i in range(0, 6 + 1, 1):
    orderMaterialQtd[i] = 0
username = input()
while True:    #This simulates a Do Loop
    option = menu()
    if option == 1:
        stockConsult(materialsName, materialsQtd, materialsPrice)
        menuCall = 1
    else:
        if option == 2:
            while True:    #This simulates a Do Loop
                print("Indique o material que pretende")
                orderCreate(materialsName, orderMaterialQtd, materialsPrice)
                print("A lista de materiais encomendada é a seguinte:")
                stockValidate(materialsName, materialsQtd, orderMaterialQtd, materialsPrice)
                total = calcTotal(orderMaterialQtd, materialsPrice)
                print("Indique a origem do pedido:")
                origem = input()
                print("Indique o destino do pedido:")
                destino = input()
                print("Indique o início da janela de entrega:")
                janelaInicio = input()
                print("Indique o fim da janela de entrega:")
                janelaFim = input()
                itensPedido = ""
                idItem = -1
                while idItem == 0:
                    print("Indique o ID do material (0 para terminar):")
                    idItem = int(input())
                    if idItem == 0:
                        if itensPedido == "":
                            print("Deve inserir pelo menos 1 item")
                    else:
                        print("Indique a quantidade:")
                        qtItem = int(input())
                        if qtItem <= 0:
                            print("Quantidade inválida.")
                        else:
                            if itensPedido == "":
                                itensPedido = str(idItem) + ":" + str(qtItem)
                            else:
                                itensPedido = itensPedido + "|" + str(idItem) + ":" + str(qtItem)
                pedidosCount = pedidosCount + 1
                idx = pedidosCount
                pedidosId[idx] = idx
                pedidosEstado[idx] = "pendente"
                pedidosOrigem[idx] = origem
                pedidosDestino[idx] = destino
                pedidosJanelaInicio[idx] = janelaInicio
                pedidosJanelaFim[idx] = janelaFim
                pedidosItens[idx] = itensPedido
                print("Pedido criado com ID: " + str(pedidosId[idx]))
                idItem = -1
                print("Obrigado " + username + " pela sua encomenda" + chr(13) + " O total de encomenda é " + str(total) + " euros")
                print("Deseja realizar uma nova encomenda? Se sim, insira 1. Se não, insira 0")
                repeat = int(input())
                if repeat != 1: break
            print("Validar stock...")
            stockOk = True
            for i in range(0, 6 + 1, 1):
                if orderMaterialQtd[i] > 0:
                    if materialsQtd[i] >= orderMaterialQtd[i]:
                        materialsQtd[i] = materialsQtd[i] - orderMaterialQtd[i]
                        print(materialsName[i] + " stock atualizado: " + str(materialsQtd[i]))
                    else:
                        print("Stock insuficiente para " + materialsName[i])
                        stockOk = False
            if stockOk == True:
                print("Stock atualizado com sucesso.")
            else:
                print("Alguns itens não têm stock suficiente.")
            menuCall = 1
        else:
            if option == 3:
                orderConsult(materialsName, orderMaterialQtd, materialsPrice)
                menuCall = 1
                print("Digite o ID do pedido que deseja consultar:")
                idPedidoEscolhido = int(input())
                found = 0
                for i in range(1, pedidosCount + 1, 1):
                    if pedidosId[i] == idPedidoEscolhido:
                        found = 1
                        print("Pedido encontrado:")
                        print("Origem: ")
                        print(str(pedidosOrigem[i]))
                        print("Destino: ")
                        print(str(pedidosDestino[i]))
                        print("Janela: ")
                        print(str(pedidosJanelaInicio[i]))
                        print(" até ")
                        print(str(pedidosJanelaFim[i]))
                        print("Estado atual: ")
                        print(str(pedidosEstado[i]))
                    else:
                        if found == 0:
                            print("Pedido não encontrado.")
                        else:
                            print("Tracking conluído com sucesso.")
            elif option == 4:
                    print("Digite o ID do pedido que deseja cancelar:")
                    idPedidoEscolhido = int(input())
                    found = 0
                    for i in range(1, pedidosCount + 1, 1):
                        if pedidosId[i] == idPedidoEscolhido:
                            found = i
                            if pedidosEstado[i] == "cancelada":
                                pedidosEstado[i] = "cancelada"
                                print("Pedido cancelado com sucesso!")
                            else:
                                print("Não é possivel cancelar este pedido")
                                print("Estado atual: ")
                                print(pedidosEstado[i])
                    if found == 0:
                        print("Pedido não encontrado.")
                    else:
                        print("Operação de cancelamento concluida.")
                    print("Digite o estado dos pedidos que deseja listar (pendente / concluida / cancelada):")
                    estadoEscolhido = input()
                    found = 0
                    if pedidosCount == 0:
                        print("Não existem pedidos registados.")
                    for i in range(1, pedidosCount + 1, 1):
                        if pedidosEstado[i] == estadoEscolhido:
                            found = 1
                            print("ID: " + str(pedidosId[i]))
                            print("Origem: " + pedidosOrigem[i])
                            print("Destino: " + pedidosDestino[i])
                            print("Janela: " + pedidosJanelaInicio[i] + " até " + pedidosJanelaFim[i])
                            print("Estado: " + pedidosEstado[i])
                    if found == 0:
                        print("Não existem pedidos com o estado indicado.")
                    else:
                        print("Fim da listagem.")
            elif option == 5:
                        print("Digite o ID do pedido que deseja avaliar:")
                        idPedidoEscolhido = int(input())
                        found = 0
                        for i in range(1, pedidosCount + 1, 1):
                            if pedidosEstado[i] == "":
                                if pedidosId[i] == idPedidoEscolhido:
                                    found = 1
                                    if pedidosEstado[i] == "concluida":
                                        print("Pedido elegivel para avaliação.")
                                        print("Indique rating (1 a 5):")
                                        rating = int(input())
                                        if rating < 1 or rating > 5:
                                            print("Rating inválido.")
                                        print("Escreve um comentário (opcional):")
                                        comentario = input()
                                        print("Obrigado! A sua avaliação foi registada.")
                                    else:
                                        print("Só é possivel avaliar pedidos concluídos.")
                        if found == 0:
                            print("Pedido não encontrado.")
                        else:
                            print("Avaliação terminada.")
                        found = 0
            menuCall = 0
    if menuCall != 1: break
print("Obrigado por confiar na nossa empresa")

eventosId = [-1] * (50)
eventosPedidoId = [0] * (50)
eventosEstafetaId = [0] * (50)
eventosEstado = [""] * (50)
eventosTimestamp = [""] * (50)
eventosLocalizacao = [""] * (50)
eventosDescricao = [""] * (50)
anomaliaPedidoId = [0] * (50)
anomaliaEstafetaId = [0] * (50)
anomaliaMotivo = [""] * (50)
anomaliaData = [""] * (50)

i = 0
option = 0
eventosCount = 0
anomaliasCount = 0
totalEntregues = 0
totalFalhadas = 0
taxaSucesso = 0.0

print("SISTEMA DE TRACKING DO ESTAFETA")
print("Escolha uma das opções abaixo:")
print("1 - Registar novo evento")
print("2 - Consultar eventos")
print("3 - Ver métricas")
print("4 - Consultar anomalias")
print("5 - Editar ou remover evento")
print("6 - Sair")
option = int(input())

if option == 1:
    eventosId[eventosCount] = eventosCount
    print("Digite o ID do pedido")
    eventosPedidoId[eventosCount] = int(input())
    print("Digite o ID do Estafeta")
    eventosEstafetaId[eventosCount] = int(input())
    print("Digite o estado (aceite, em recolha, em distribuição, entregue, falhada)")
    eventosEstado[eventosCount] = input()
    print("Digite o timestamp (ex: 2025-10-28 14:22)")
    eventosTimestamp[eventosCount] = input()
    print("Digite a localização")
    eventosLocalizacao[eventosCount] = input()
    print("Digite a descrição")
    eventosDescricao[eventosCount] = input()

    if eventosEstado[eventosCount] == "entregue":
        totalEntregues += 1
    elif eventosEstado[eventosCount] == "falhada":
        totalFalhadas += 1
        anomaliaPedidoId[anomaliasCount] = eventosPedidoId[eventosCount]
        anomaliaEstafetaId[anomaliasCount] = eventosEstafetaId[eventosCount]
        anomaliaData[anomaliasCount] = eventosTimestamp[eventosCount]
        print("Motivo da falha:")
        anomaliaMotivo[anomaliasCount] = input()
        anomaliasCount += 1

    eventosCount += 1
    print("Evento registado!")

elif option == 2:
    if eventosCount == 0:
        print("Nenhum evento registado")
    else:
        for i in range(0, eventosCount):
            if eventosId[i] != -1:
                print("Evento ID:" + str(eventosId[i]))
                print("Pedido:" + str(eventosPedidoId[i]))
                print("Estafeta:" + str(eventosEstafetaId[i]))
                print("Estado:" + eventosEstado[i])
                print("Timestamp:" + eventosTimestamp[i])
                print("Localização:" + eventosLocalizacao[i])
                print("Descrição:" + eventosDescricao[i])
                print("")

elif option == 3:
    if totalEntregues + totalFalhadas > 0:
        taxaSucesso = (float(totalEntregues) / (totalEntregues + totalFalhadas)) * 100
    else:
        taxaSucesso = 0.0
    print("Métricas do Estafeta")
    print("Total de entregas:" + str(totalEntregues))
    print("Total de falhas:" + str(totalFalhadas))
    print("Taxa de Sucesso:" + str(taxaSucesso) + "%")

elif option == 4:
    if anomaliasCount == 0:
        print("Nenhuma anomalia registada")
    else:
        print("Anomalias registadas")
        for i in range(0, anomaliasCount):
            print("Pedido:" + str(anomaliaPedidoId[i]))
            print("Estafeta:" + str(anomaliaEstafetaId[i]))
            print("Motivo:" + anomaliaMotivo[i])
            print("Data:" + anomaliaData[i])
            print("")

elif option == 5:
    if eventosCount == 0:
        print("Nenhum evento registado")
    else:
        for i in range(0, eventosCount):
            if eventosId[i] != -1:
                print("ID:" + str(eventosId[i]))
                print("Pedido:" + str(eventosPedidoId[i]))
                print("Estafeta:" + str(eventosEstafetaId[i]))
                print("Estado:" + eventosEstado[i])
                print("Localização:" + eventosLocalizacao[i])
                print("")
        print("Digite o ID do evento que deseja editar ou remover")
        idEditar = int(input())
        eventoEncontrado = False
        for i in range(0, eventosCount):
            if eventosId[i] == idEditar:
                eventoEncontrado = True
                print("Evento encontrado")
                print("Escolha: 1- Editar | 2- Remover")
                escolha = int(input())
                if escolha == 1:
                    estado_antigo = eventosEstado[i]
                    print("Digite novo estado")
                    novo_estado = input()
                    print("Digite nova localização")
                    eventosLocalizacao[i] = input()
                    print("Digite nova descrição")
                    eventosDescricao[i] = input()

                    if estado_antigo == "entregue":
                        totalEntregues -= 1
                    elif estado_antigo == "falhada":
                        totalFalhadas -= 1
                        # remover anomalia associada
                        found_j = -1
                        for j in range(0, anomaliasCount):
                            if (anomaliaPedidoId[j] == eventosPedidoId[i] and
                                anomaliaEstafetaId[j] == eventosEstafetaId[i] and
                                anomaliaData[j] == eventosTimestamp[i]):
                                found_j = j
                                break
                        if found_j != -1:
                            for k in range(found_j, anomaliasCount - 1):
                                anomaliaPedidoId[k] = anomaliaPedidoId[k + 1]
                                anomaliaEstafetaId[k] = anomaliaEstafetaId[k + 1]
                                anomaliaMotivo[k] = anomaliaMotivo[k + 1]
                                anomaliaData[k] = anomaliaData[k + 1]
                            anomaliaPedidoId[anomaliasCount - 1] = 0
                            anomaliaEstafetaId[anomaliasCount - 1] = 0
                            anomaliaMotivo[anomaliasCount - 1] = ""
                            anomaliaData[anomaliasCount - 1] = ""
                            anomaliasCount -= 1

                    eventosEstado[i] = novo_estado
                    if novo_estado == "entregue":
                        totalEntregues += 1
                    elif novo_estado == "falhada":
                        totalFalhadas += 1
                        anomaliaPedidoId[anomaliasCount] = eventosPedidoId[i]
                        anomaliaEstafetaId[anomaliasCount] = eventosEstafetaId[i]
                        anomaliaData[anomaliasCount] = eventosTimestamp[i]
                        print("Motivo da falha:")
                        anomaliaMotivo[anomaliasCount] = input()
                        anomaliasCount += 1
                    print("Evento editado com sucesso")

                elif escolha == 2:
                    if eventosEstado[i] == "entregue":
                        totalEntregues -= 1
                    elif eventosEstado[i] == "falhada":
                        totalFalhadas -= 1
                        # remover anomalia correspondente
                        found_j = -1
                        for j in range(0, anomaliasCount):
                            if (anomaliaPedidoId[j] == eventosPedidoId[i] and
                                anomaliaEstafetaId[j] == eventosEstafetaId[i] and
                                anomaliaData[j] == eventosTimestamp[i]):
                                found_j = j
                                break
                        if found_j != -1:
                            for k in range(found_j, anomaliasCount - 1):
                                anomaliaPedidoId[k] = anomaliaPedidoId[k + 1]
                                anomaliaEstafetaId[k] = anomaliaEstafetaId[k + 1]
                                anomaliaMotivo[k] = anomaliaMotivo[k + 1]
                                anomaliaData[k] = anomaliaData[k + 1]
                            anomaliaPedidoId[anomaliasCount - 1] = 0
                            anomaliaEstafetaId[anomaliasCount - 1] = 0
                            anomaliaMotivo[anomaliasCount - 1] = ""
                            anomaliaData[anomaliasCount - 1] = ""
                            anomaliasCount -= 1

                    eventosId[i] = -1
                    eventosPedidoId[i] = 0
                    eventosEstafetaId[i] = 0
                    eventosEstado[i] = ""
                    eventosTimestamp[i] = ""
                    eventosLocalizacao[i] = ""
                    eventosDescricao[i] = ""
                    print("Evento removido com sucesso")

                else:
                    print("Escolha inválida")

        if not eventoEncontrado:
            print("Evento não encontrado")

elif option == 6:
    print("Obrigado!")

else:
    print("Opção inválida")