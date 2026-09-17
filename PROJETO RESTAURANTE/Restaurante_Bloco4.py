# BLOCO 4 - REPOSIÇÃO, RELATÓRIOS, PERSISTÊNCIA E SIMULAÇÃO
# ==============================================================================

class ReposicaoEstoque:
    """Gerencia alertas de reposição de estoque baixo e ordens de compra."""
    def __init__(self, estoque, limite_minimo=5):
        self.estoque = estoque
        self.limite_minimo = limite_minimo

    def verificar_e_repor(self, produto, quantidade_compra, preco_compra):
        total_atual = self.estoque.consultar_quantidade_total(produto.id_produto)
        if total_atual < self.limite_minimo:
            print(f"[ALERTA REPOSIÇÃO] {produto.nome} está abaixo do limite ({total_atual}/{self.limite_minimo}). Repondo...")
            novo_lote = LoteEstoque(
                produto=produto,
                quantidade=quantidade_compra,
                preco_compra=preco_compra,
                data_compra=date.today(),
                data_vencimento=date(2026, 12, 31)
            )
            self.estoque.adicionar_lote(novo_lote)
            print(f"[REPOSIÇÃO CONCLUÍDA] Adicionado lote de {quantidade_compra} unidades de {produto.nome}.")
        else:
            print(f"[ESTOQUE OK] {produto.nome} possui saldo suficiente: {total_atual} unidades.")


class Relatorios:
    """Consolida os dados de vendas, faturamento e ocupação."""
    @staticmethod
    def gerar_relatorio_financeiro(caixa):
        print("\n==========================================")
        print("         RELATÓRIO FINANCEIRO             ")
        print("==========================================")
        total_faturado = sum(p.valor_pago for p in caixa.historico)
        print(f"Total de Transações: {len(caixa.historico)}")
        print(f"Faturamento Total  : R${total_faturado:.2f}")
        
        # Detalhamento por Forma de Pagamento
        formas = {}
        for p in caixa.historico:
            formas[p.forma_pagamento] = formas.get(p.forma_pagamento, 0) + p.valor_pago
        
        for forma, total in formas.items():
            print(f"  - {forma}: R${total:.2f}")
        print("==========================================\n")


class Persistencia:
    """Realiza a gravação e leitura do estado do sistema em disco com Pickle."""
    @staticmethod
    def salvar_sistema(objeto_sistema, nome_arquivo="restaurante_dados.pkl"):
        try:
            with open(nome_arquivo, "wb") as f:
                pickle.dump(objeto_sistema, f)
            print(f"[PERSISTÊNCIA] Dados salvos com sucesso em '{nome_arquivo}'.")
        except Exception as e:
            print(f"[ERRO PERSISTÊNCIA] Falha ao salvar: {e}")

    @staticmethod
    def carregar_sistema(nome_arquivo="restaurante_dados.pkl"):
        try:
            with open(nome_arquivo, "rb") as f:
                dados = pickle.load(f)
            print(f"[PERSISTÊNCIA] Dados carregados com sucesso de '{nome_arquivo}'.")
            return dados
        except FileNotFoundError:
            print(f"[PERSISTÊNCIA] Arquivo '{nome_arquivo}' não encontrado. Iniciando novo estado.")
            return None


def simular_atendimento_faker(estoque, cozinha, caixa, produtos):
    """Simula movimentações de atendimento e vendas automatizadas."""
    print("\n--- INICIANDO SIMULAÇÃO DE VENDAS AUTOMÁTICA ---")
    for i in range(1, 4):
        comanda = Comanda(id_comanda=300 + i, mesa=i)
        prod_sorteado = random.choice(produtos)
        qtd = random.randint(1, 3)
        
        comanda.adicionar_item(prod_sorteado, qtd)
        estoque.dar_baixa_fifo(prod_sorteado.id_produto, qtd)
        
        if isinstance(prod_sorteado, Comida):
            cozinha.enfileirar_pedido(comanda, comanda.itens[0])
            cozinha.desenfileirar_proximo()
            
        forma = random.choice(["Pix", "Cartão", "Dinheiro"])
        val_entregue = comanda.calcular_total() + 10.0 if forma == "Dinheiro" else None
        caixa.processar_pagamento(comanda, forma_pagamento=forma, valor_entregue=val_entregue)