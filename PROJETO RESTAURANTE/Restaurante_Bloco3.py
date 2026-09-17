# ==============================================================================
# BLOCO 3 - CAIXA E HISTÓRICO DE PAGAMENTOS
# ==============================================================================

class Pagamento:
    """Comprovante de pagamento registrado no caixa."""
    def __init__(self, id_pagamento, comanda, forma_pagamento, valor_pago):
        self.id_pagamento = id_pagamento
        self.comanda = comanda
        self.forma_pagamento = forma_pagamento
        self.valor_pago = valor_pago
        self.data_hora = datetime.now()

    def __repr__(self):
        data_formatada = self.data_hora.strftime("%d/%m/%Y %H:%M:%S")
        return (f"Pagamento #{self.id_pagamento} | Comanda #{self.comanda.id_comanda} | "
                f"Forma: {self.forma_pagamento} | Valor: R${self.valor_pago:.2f} | Data: {data_formatada}")


class Caixa:
    """Processa pagamentos e armazena o histórico financeiro."""
    FORMAS_ACEITAS = ["Pix", "Cartão", "Dinheiro", "Confiança"]

    def __init__(self):
        self.historico = []
        self._contador_pagamentos = 1

    def processar_pagamento(self, comanda, forma_pagamento, valor_entregue=None):
        forma_normalizada = forma_pagamento.capitalize()
        if forma_normalizada not in self.FORMAS_ACEITAS and forma_pagamento.upper() != "PIX":
            print(f"[ERRO] Forma de pagamento '{forma_pagamento}' inválida. Opções: {self.FORMAS_ACEITAS}")
            return None

        if comanda.status == "Fechada":
            print(f"[ERRO] Comanda #{comanda.id_comanda} já está fechada.")
            return None

        total_comanda = comanda.calcular_total()
        troco = 0.0

        if forma_normalizada == "Dinheiro":
            if valor_entregue is None or valor_entregue < total_comanda:
                print(f"[ERRO] Valor fornecido (R${valor_entregue if valor_entregue else 0:.2f}) "
                      f"é insuficiente para pagar R${total_comanda:.2f}.")
                return None
            troco = valor_entregue - total_comanda

        novo_pagamento = Pagamento(
            id_pagamento=self._contador_pagamentos,
            comanda=comanda,
            forma_pagamento=forma_normalizada if forma_normalizada in self.FORMAS_ACEITAS else "Pix",
            valor_pago=total_comanda
        )

        self.historico.append(novo_pagamento)
        self._contador_pagamentos += 1
        comanda.fechar_comanda()

        if troco > 0:
            print(f"[CAIXA] Pagamento efetuado. Troco a devolver: R${troco:.2f}")
        else:
            print(f"[CAIXA] Pagamento da Comanda #{comanda.id_comanda} finalizado com sucesso.")

        return novo_pagamento

    def visualizar_historico(self):
        print("\n--- HISTÓRICO DE VENDAS E CAIXA ---")
        if not self.historico:
            print("Nenhum pagamento registrado.")
            return
        for pagamento in self.historico:
            print(pagamento)


# ==============================================================================
# SCRIPT DE TESTE INTEGRADO (BLOCOS 1, 2 E 3)
# ==============================================================================

if __name__ == "__main__":
    print("=== INICIALIZANDO O SISTEMA DO RESTAURANTE ===")
    
    # 1. Configuração do Estoque (Bloco 1)
    estoque = Estoque()
    hamburguer = Comida(id_produto=1, nome="X-Burger", preco_venda=25.00, peso_g=300)
    suco = Bebida(id_produto=2, categoria="Suco", preco_venda=7.00)

    lote_hamb = LoteEstoque(hamburguer, quantidade=10, preco_compra=12.00, data_compra=date(2026, 9, 1), data_vencimento=date(2026, 10, 1))
    lote_suco = LoteEstoque(suco, quantidade=15, preco_compra=3.50, data_compra=date(2026, 9, 2), data_vencimento=date(2026, 10, 5))

    estoque.adicionar_lote(lote_hamb)
    estoque.adicionar_lote(lote_suco)

    # 2. Atendimento ao Cliente (Bloco 2)
    comanda1 = Comanda(id_comanda=101, mesa=5)
    cozinha = FilaCozinha()

    comanda1.adicionar_item(hamburguer, quantidade=2, observacao="Sem cebola")
    comanda1.adicionar_item(suco, quantidade=1)

    # Processamento de saída de estoque e cozinha
    for item in comanda1.itens:
        estoque.dar_baixa_fifo(item.produto.id_produto, item.quantidade)
        if isinstance(item.produto, Comida):
            cozinha.enfileirar_pedido(comanda1, item)

    cozinha.visualizar_fila()
    cozinha.desenfileirar_proximo()

    # 3. Pagamento e Liquidação no Caixa (Bloco 3)
    caixa = Caixa()
    print("\n--- PROCESSAMENTO NO CAIXA ---")
    caixa.processar_pagamento(comanda1, forma_pagamento="Dinheiro", valor_entregue=60.00)

    # Exibição do histórico acumulado
    caixa.visualizar_historico()

