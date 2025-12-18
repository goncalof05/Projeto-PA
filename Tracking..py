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
