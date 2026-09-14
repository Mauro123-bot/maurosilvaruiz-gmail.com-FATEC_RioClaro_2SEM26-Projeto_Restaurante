# Sistema de Gestão de Restaurante
**Aluno:** Mauro Silva Ruiz  

Este projeto consiste em um sistema de gestão de estoque, comandas e pagamentos desenvolvido como requisito avaliativo para as disciplinas de Estrutura de Dados e Linguagem de Programação II da Fatec Rio Claro.

O objetivo principal é aplicar os conceitos de Orientação a Objetos e estruturas de dados dinâmicas personalizadas, sem a utilização de coleções nativas estruturais da linguagem (como listas ou dicionários embutidos) para a lógica principal do negócio.


# 1. CONCEPÇÃO DO SISTEMA

## 1.1 Premissas de Negócio e Requisitos
* **Tipo de restaurante (Simplificado - Descritivo):** Restaurante familiar de bairro próximo à Fatec, focado em atendimento rápido de almoço para professores e alunos com pouco tempo.[cite: 1]
* **Produtos ofertados (Descritivo):** Pratos Feitos (PFs), sanduíches frios e 3 categorias de bebidas (água, suco e refrigerante de 2 marcas cada, todas padronizadas em volume único de 500ml).[cite: 1]
* **Preços por Categoria:** Preço fixado pela categoria da bebida, independentemente da marca escolhida.[cite: 1]

## 1.2 Arquitetura Geral do Sistema

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


