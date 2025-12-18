username = [""] * (200)
zone = [""] * (200)
pedidocimento = [0] * (200)
pedidoareia = [0] * (200)
pedidotijolo = [0] * (200)
estafeta = [""] * (200)

stockcimento = 1000
stockareia = 1000
stocktijolo = 1000
qtencomendas = 0
continuar = "sim"
while continuar == "sim":
    i = qtencomendas
    print("username:")
    username[i] = input()
    if username[i] != "":
        print("zona:")
        zone[i] = input()
        if zone[i] == "N" or zone[i] == "S" or zone[i] == "C" or zone[i] == "n" or zone[i] == "s" or zone[i] == "c":
            print("Quantidade de cimento:")
            pedidocimento[i] = int(input())
            print("Quantidade de areia")
            pedidoareia[i] = int(input())
            print("Quantidade de tijolo:")
            pedidotijolo[i] = int(input())
            if pedidocimento[i] <= stockcimento and pedidoareia[i] <= stockareia and pedidotijolo[i] <= stocktijolo:
                estadoencomenda = "aprovada"
                if zone[i] == "N" or zone[i] == "n":
                    estafeta[i] = "estafeta1"
                else:
                    if zone[i] == "C" or zone[i] == "c":
                        estafeta[i] = "estafeta2"
                    else:
                        estafeta[i] = "estafeta3"
                stockcimento = stockcimento - pedidocimento[i]
                stockareia = stockareia - pedidoareia[i]
                stocktijolo = stocktijolo - pedidotijolo[i]
                print("Encomenda aprovada e atribuída a ")
                print(estafeta[i])
            else:
                estadoencomenda = "pendente"
                print("Encomenda pendente, falta de stock.")
                estafeta[i] = ""
        else:
            estadoencomenda = "rejeitada"
            print("Encomenda rejeitada")
            estafeta[i] = ""
    qtencomendas = qtencomendas + 1
    print("Deseja criar outra encomenda?")
    continuar = input()
continuarConsulta = "sim"
while continuarConsulta == "sim":
    print("indique o id da sua encomenda para a acompanhar")
    id = int(input())
    if id >= 0 and id < qtencomendas:
        print("Detalhes encomenda:")
        print("Username: ")
        print(username[id])
        print("Zona: ")
        print(zone[id])
        print("Cimento pedido: ")
        print(pedidocimento[id])
        print("Areia pedida: ")
        print(pedidoareia[id])
        print("Tijolo pedido: ")
        print(pedidotijolo[id])
        print("Estafeta atribuída: ")
        print(estafeta[id])
    else:
        print("ID inválido. Não existe nenhuma encomenda com esse ID.")
    print("Pretende consultar outra encomenda pelo ID?")
    continuarConsulta = input()