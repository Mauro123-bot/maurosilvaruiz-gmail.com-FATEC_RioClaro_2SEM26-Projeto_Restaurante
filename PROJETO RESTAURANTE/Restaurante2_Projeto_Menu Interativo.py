from datetime import datetime, date
from collections import deque
import pickle
import random

#####################################################################################################
# BLOCO 1 - PRODUTOS E CONTROLE DE ESTOQUE
######################################################################################################

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


######################################################################################################
# BLOCO 2 - COMANDAS, PEDIDOS E FILA DA COZINHA
######################################################################################################

class ItemPedido:
    """Item solicitado dentro de uma comanda."""
    def __init__(self, produto, quantidade, observacao=""):
        self.produto = produto
        self.quantidade = quantidade
        self.observacao = observacao

    def calcular_subtotal(self):
        return self.produto.preco_venda * self.quantidade

    def __repr__(self):
        obs = f" ({self.observacao})" if self.observacao else ""
        return f"{self.quantidade}x {self.produto.nome}{obs} = R${self.calcular_subtotal():.2f}"


class Comanda:
    """Gerencia a conta de um cliente ou mesa."""
    def __init__(self, id_comanda, mesa):
        self.id_comanda = id_comanda
        self.mesa = mesa
        self.itens = []
        self.status = "Aberta"

    def adicionar_item(self, produto, quantidade, observacao=""):
        if self.status == "Fechada":
            print(f"[ERRO] Comanda #{self.id_comanda} está fechada.")
            return False
        
        item = ItemPedido(produto, quantidade, observacao)
        self.itens.append(item)
        print(f"[COMANDA #{self.id_comanda}] Adicionado: {item}")
        return True

    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.itens)

    def fechar_comanda(self):
        self.status = "Fechada"
        print(f"[COMANDA #{self.id_comanda}] Encerrada. Total: R${self.calcular_total():.2f}")

    def __repr__(self):
        return f"Comanda(ID: {self.id_comanda}, Mesa: {self.mesa}, Status: {self.status}, Total: R${self.calcular_total():.2f})"


class FilaCozinha:
    """Gerencia a fila de preparo da cozinha (FIFO)."""
    def __init__(self):
        self._fila = deque()

    def enfileirar_pedido(self, comanda, item):
        if isinstance(item.produto, Bebida):
            print(f"[AUTOATENDIMENTO] {item.produto.nome} é bebida. Não vai para a cozinha.")
            return False
        self._fila.append((comanda.id_comanda, item))
        comanda.status = "Em Preparo"
        print(f"[COZINHA] Pedido da Comanda #{comanda.id_comanda} entra na fila: {item.quantidade}x {item.produto.nome}")
        return True

    def desenfileirar_proximo(self):
        if not self._fila:
            print("[COZINHA] Nenhum pedido pendente na fila.")
            return None
        
        id_comanda, item = self._fila.popleft()
        print(f"[COZINHA] Preparando pedido da Comanda #{id_comanda}: {item.quantidade}x {item.produto.nome}")
        return id_comanda, item

    def visualizar_fila(self):
        print("\n--- FILA ATUAL DA COZINHA (FIFO) ---")
        if not self._fila:
            print("Fila vazia.")
            return
        for idx, (id_cmd, item) in enumerate(self._fila, 1):
            print(f"{idx}. Comanda #{id_cmd} -> {item}")


###################################################################################################
# BLOCO 3 - CAIXA E HISTÓRICO DE PAGAMENTOS
###################################################################################################

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


######################################################################################################
# BLOCO 4 - REPOSIÇÃO, RELATÓRIOS, PERSISTÊNCIA E SIMULAÇÃO
######################################################################################################

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
        print("\n----------------------------------------")
        print("         RELATÓRIO FINANCEIRO             ")
        print("------------------------------------------")
        total_faturado = sum(p.valor_pago for p in caixa.historico)
        print(f"Total de Transações: {len(caixa.historico)}")
        print(f"Faturamento Total  : R${total_faturado:.2f}")
        
        # Detalhamento por Forma de Pagamento
        formas = {}
        for p in caixa.historico:
            formas[p.forma_pagamento] = formas.get(p.forma_pagamento, 0) + p.valor_pago
        
        for forma, total in formas.items():
            print(f"  - {forma}: R${total:.2f}")
        print("----------------------------------------\n")


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


####################################################################################################
# MENU INTERATIVO PARA ENTRADA MANUAL DE DADOS
#####################################################################################################

if __name__ == "__main__":
    # 1. Inicialização do Sistema
    estoque = Estoque()
    cozinha = FilaCozinha()
    caixa = Caixa()

    # Cadastro inicial de produtos para o cardápio
    hamburguer = Comida(id_produto=1, nome="X-Burger", preco_venda=25.00, peso_g=300)
    suco = Bebida(id_produto=2, categoria="Suco", preco_venda=7.00)
    
    # Abastecendo estoque inicial
    estoque.adicionar_lote(LoteEstoque(hamburguer, quantidade=10, preco_compra=10.00, data_compra=date(2026, 9, 1), data_vencimento=date(2026, 10, 1)))
    estoque.adicionar_lote(LoteEstoque(suco, quantidade=15, preco_compra=3.00, data_compra=date(2026, 9, 2), data_vencimento=date(2026, 10, 5)))

    comanda_atual = None

    while True:
        print("\n----------------------------------------")
        print("    SISTEMA DE RESTAURANTE - PAINEL       ")
        print("------------------------------------------")
        print("1 - Criar/Abrir Comanda")
        print("2 - Adicionar Item na Comanda")
        print("3 - Processar Fila da Cozinha")
        print("4 - Fechar Comanda e Receber Pagamento")
        print("5 - Ver Relatório Financeiro")
        print("6 - Rodar Simulação Automática (Aleatória)")
        print("0 - Sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            num_comanda = int(input("Número da Comanda: "))
            num_mesa = int(input("Número da Mesa: "))
            comanda_atual = Comanda(id_comanda=num_comanda, mesa=num_mesa)
            print(f"[OK] Comanda #{num_comanda} aberta para a mesa {num_mesa}!")

        elif opcao == "2":
            if not comanda_atual:
                print("[ERRO] Abra uma comanda primeiro (Opção 1).")
                continue
            
            print("\nCardápio Disponível:")
            print("1 - X-Burger (R$ 25,00)")
            print("2 - Suco (R$ 7,00)")
            escolha = input("Escolha o produto (1 ou 2): ")
            qtd = int(input("Quantidade: "))
            
            prod = hamburguer if escolha == "1" else suco
            
            # Tenta dar baixa no estoque antes de colocar na comanda
            if estoque.dar_baixa_fifo(prod.id_produto, qtd):
                obs = input("Observação (ex: Sem picles): ") if escolha == "1" else ""
                comanda_atual.adicionar_item(prod, qtd, obs)
                
                # Se for comida, manda para a fila da cozinha
                if isinstance(prod, Comida):
                    cozinha.enfileirar_pedido(comanda_atual, comanda_atual.itens[-1])

        elif opcao == "3":
            cozinha.desenfileirar_proximo()

        elif opcao == "4":
            if not comanda_atual or not comanda_atual.itens:
                print("[ERRO] Não há comanda aberta ou comanda sem itens.")
                continue

            print(f"\nTotal da Comanda #{comanda_atual.id_comanda}: R${comanda_atual.calcular_total():.2f}")
            forma = input("Forma de Pagamento (Pix / Cartao / Dinheiro): ")
            val_entregue = None
            
            if forma.capitalize() == "Dinheiro":
                val_entregue = float(input("Valor pago pelo cliente: R$ "))

            pagamento = caixa.processar_pagamento(comanda_atual, forma, val_entregue)
            if pagamento:
                comanda_atual = None  # Libera para abrir uma nova

        elif opcao == "5":
            Relatorios.gerar_relatorio_financeiro(caixa)

        elif opcao == "6":
            simular_atendimento_faker(estoque, cozinha, caixa, [hamburguer, suco])

        elif opcao == "0":
            print("\nEncerrando o sistema...")
            break
        else:
            print("Opção inválida!")