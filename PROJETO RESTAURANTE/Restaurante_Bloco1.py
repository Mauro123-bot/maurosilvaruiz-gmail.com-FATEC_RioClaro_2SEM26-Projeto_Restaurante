from datetime import datetime, date
from collections import deque
import pickle
import random

# ==============================================================================
# BLOCO 1 - PRODUTOS E CONTROLE DE ESTOQUE
# ==============================================================================

class Produto:
    """Classe base para os produtos do cardápio."""
    def __init__(self, id_produto, nome, preco_venda):
        self.id_produto = id_produto
        self.nome = nome
        self.preco_venda = preco_venda

    def __repr__(self):
        return f"{self.__class__.__name__}(ID: {self.id_produto}, Nome: {self.nome}, Venda: R${self.preco_venda:.2f})"


class Comida(Produto):
    """Especialização de Produto para itens alimentícios."""
    def __init__(self, id_produto, nome, preco_venda, peso_g):
        super().__init__(id_produto, nome, preco_venda)
        self.peso_g = peso_g


class Bebida(Produto):
    """Especialização de Produto para bebidas com volume fixo."""
    def __init__(self, id_produto, categoria, preco_venda):
        super().__init__(id_produto, categoria, preco_venda)
        self.categoria = categoria
        self.volume_ml = 500


class LoteEstoque:
    """Representa um lote específico de mercadoria armazenada."""
    def __init__(self, produto, quantidade, preco_compra, data_compra, data_vencimento):
        self.produto = produto
        self.quantidade = quantidade
        self.preco_compra = preco_compra
        self.data_compra = data_compra
        self.data_vencimento = data_vencimento

    def __repr__(self):
        return (f"Lote(Produto: {self.produto.nome}, Qtd: {self.quantidade}, "
                f"Compra: R${self.preco_compra:.2f}, Vencimento: {self.data_vencimento})")


class Estoque:
    """Gerencia a entrada, alteração e baixa FIFO/PEPS dos lotes."""
    def __init__(self):
        self.lotes = []

    def adicionar_lote(self, lote):
        self.lotes.append(lote)
        self.lotes.sort(key=lambda l: l.data_compra)

    def editar_quantidade(self, lote, nova_quantidade):
        if nova_quantidade < 0:
            print("[ERRO] Quantidade de estoque não pode ser negativa.")
            return
        lote.quantidade = nova_quantidade
        print(f"[MANUTENÇÃO] Lote de {lote.produto.nome} retificado para {nova_quantidade} unidades.")

    def consultar_quantidade_total(self, id_produto):
        return sum(lote.quantidade for lote in self.lotes if lote.produto.id_produto == id_produto)

    def dar_baixa_fifo(self, id_produto, quantidade_desejada):
        qtd_disponivel = self.consultar_quantidade_total(id_produto)
        
        if qtd_disponivel < quantidade_desejada:
            print(f"[ERRO DE INVENTÁRIO] Solicitado: {quantidade_desejada} | Disponível: {qtd_disponivel}")
            return False

        qtd_restante = quantidade_desejada
        for lote in self.lotes:
            if lote.produto.id_produto == id_produto and lote.quantidade > 0:
                if lote.quantidade <= qtd_restante:
                    qtd_restante -= lote.quantidade
                    lote.quantidade = 0
                else:
                    lote.quantidade -= qtd_restante
                    qtd_restante = 0
                if qtd_restante == 0:
                    break
        
        print(f"[SUCESSO ESTOQUE] Baixa de {quantidade_desejada} unidade(s) processada.")
        return True