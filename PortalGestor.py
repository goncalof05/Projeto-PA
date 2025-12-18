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
