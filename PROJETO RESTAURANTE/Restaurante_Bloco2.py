# ==============================================================================
# BLOCO 2 - COMANDAS, PEDIDOS E FILA DA COZINHA
# ==============================================================================

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
        for idx, (id_cmd, item) in enumerate(self._fila, 1):
            print(f"{idx}. Comanda #{id_cmd} -> {item}")