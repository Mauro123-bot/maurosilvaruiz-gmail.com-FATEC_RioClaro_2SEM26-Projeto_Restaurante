# Projeto Restaurante
**Aluno:** Mauro Silva Ruiz  
**Disciplina:** Linguagem de Programação II  

Seguem os documentos para acompanhamento:

---

# 1. CONCEPÇÃO DO SISTEMA

## 1.1 Premissas de Negócio e Requisitos
* **Tipo de restaurante (Simplificado - Descritivo):** Restaurante familiar de bairro próximo à Fatec, focado em atendimento rápido de almoço para professores e alunos com pouco tempo.[cite: 1]
* **Produtos ofertados (Descritivo):** Pratos Feitos (PFs), sanduíches frios e 3 categorias de bebidas (água, suco e refrigerante de 2 marcas cada, todas padronizadas em volume único de 500ml).[cite: 1]
* **Preços por Categoria:** Preço fixado pela categoria da bebida, independentemente da marca escolhida.[cite: 1]

## 1.2 Abstração e Modelagem Orientada a Objetos
* **Herança:** A estrutura de herança (`Produto`: `Comida` / `Bebida`) alinha-se adequadamente com a abstração do cardápio.[cite: 1]
* **Controle Financeiro:** A gestão do Caixa suporta as formas exigidas (Pix, Cartão, Dinheiro).[cite: 1]
* **Uso da Fila (FIFO):** O fluxo de atendimento por ordem de chegada do pedido alinha-se com a estrutura FIFO pretendida.[cite: 1]

## 1.3 Arquitetura Geral do Sistema

```text
[ SISTEMA DO RESTAURANTE ]
|
+--- Bloco 1: O CARDÁPIO E ESTOQUE (Herança, Encapsulamento e FIFO)
|    |--- Produto (Classe Base / Mãe)
|    |--- Comida (Classe Filha)
|    |--- Bebida (Classe Filha)
|    |--- LoteEstoque (Registra quantidade, dataCompra e dataVencimento)
|    +--- Estoque (Baixa PEPS/FIFO: consome lotes mais velhos primeiro)
|
+--- Bloco 2: O FLUXO DE ATENDIMENTO (Comanda e Fila Personalizada)
|    |--- Comanda (Dados do pedido, cliente e status)
|    +--- FilaAtendimento (Estrutura FIFO própria para os PFs)
|
+--- Bloco 3: O CAIXA E HISTÓRICO (Pagamentos e Vendas)
|    |--- Pagamento (Registra valor, data e forma: Pix, Cartão, Dinheiro)
|    +--- Caixa (Processa pagamentos e armazena o histórico)
|
+--- Bloco 4: REPOSIÇÃO, DADOS E RELATÓRIOS (Gestão e Persistência)
     |--- GerenciadorEstoque (Verifica e repõe mercadoria)
     |--- GerenciadorDados (Gera dados com Faker e persiste com Pickle)
     +--- GerenciadorRelatorios (Gera relatórios de vendas e consumo)
```[cite: 1]

### 1.3.1 Detalhamento dos Módulos Funcionais

**1. Bloco 1: Estoque e Validade**
* **LoteEstoque:** Armazena as entradas de mercadorias com quantidade, `dataCompra` e `dataVencimento`.[cite: 1]
* **Estoque:** Mantém a lista de lotes e contém a regra `darBaixa()`, que ordena os lotes por vencimento para dar baixa nos itens mais velhos primeiro (regra PEPS/FIFO).[cite: 1]

**2. Bloco 2: Atendimento**
* **FilaAtendimento:** Classe que constrói a estrutura de dados de fila do zero (sem bibliotecas prontas), com os métodos `enfileirar(comanda)` e `desenfileirar()`.[cite: 1]

**3. Bloco 3: Caixa**
* **Pagamento & Caixa:** Guarda cada transação finalizada em uma lista de histórico, permitindo consultar vendas e pagamentos posteriormente.[cite: 1]

**4. Bloco 4: Gestão, Dados e Relatórios**
* **GerenciadorDados:** Responsável pela carga inicial de teste usando a biblioteca *Faker* e por salvar/carregar todo o estado do restaurante em arquivo usando *pickle*.[cite: 1]
* **GerenciadorRelatorios:** Lê os dados acumulados no Caixa e no Estoque para emitir o relatório de vendas e o relatório de consumo.[cite: 1]
