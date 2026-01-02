
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
