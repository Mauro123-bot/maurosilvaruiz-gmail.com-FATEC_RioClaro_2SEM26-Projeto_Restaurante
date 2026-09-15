

Sistema de Gestão de Restaurante 🍽️
Este projeto consiste em um sistema completo de gestão de estoque, comandas, pagamentos e relatórios, desenvolvido como requisito avaliativo para as disciplinas de Estrutura de Dados e Linguagem de Programação 2 da Fatec Rio Claro.
O objetivo principal é aplicar os conceitos de Programação Orientada a Objetos (POO) — com foco em Herança, Encapsulamento e Separação de Responsabilidades (SoC) — e o desenvolvimento de estruturas de dados dinâmicas personalizadas sem a utilização direta de coleções nativas estruturais (como listas ou dicionários embutidos) para a lógica principal do negócio.
________________________________________
Funcionalidades do Sistema
•	Controle de Comandas: Abertura por cliente, inserção e remoção dinâmica de refeições e bebidas antes do fechamento.
•	Controle de Estoque & Lotes: Gestão de lotes perecíveis armazenando produto, quantidade, preços de compra/venda, data de compra e data de vencimento.
•	Regra FIFO / PEPS Segura: Prioridade automática de saída para os lotes mais antigos. O sistema inclui validação prévia de saldo para evitar "falsas baixas" e corrupção de inventário.
•	Edição de Estoque: Permite o ajuste e a correção manual de quantidades de produtos armazenados nos lotes.
•	Controle de Pagamento e Caixa: Fechamento de comandas com suporte a pagamentos via PIX, Cartão, Dinheiro e modalidade de "Confiança".
•	Simulação e Persistência: Geração de dados aleatórios para testes rápidos via biblioteca Faker e armazenamento não volátil via pickle.
•	Relatórios: Emissão automatizada de relatórios de vendas e de consumo.
________________________________________
Premissas de Modelagem e Arquitetura do Sistema
Para atender com rigor técnico ao enunciado do projeto, a arquitetura foi dividida em 4 Blocos Principais integrando a herança de domínio, a gestão de regras de negócio e as travas de segurança:
Arquitetura em Blocos do Projeto
Plaintext
[ SISTEMA DO RESTAURANTE ]
│
├── Bloco 1: O CARDÁPIO E ESTOQUE (Herança, Encapsulamento e FIFO)
│   ├── Produto (Classe Base / Mãe: id, nome, preco_venda)
│   ├── Comida (Classe Filha: peso_g)
│   ├── Bebida (Classe Filha: categoria, volume_ml fixo em 500ml)
│   ├── LoteEstoque (Registra produto, quantidade, preco_compra, dataCompra, dataVencimento)
│   └── Estoque (Baixa PEPS/FIFO e edição manual de quantidade)
│
├── Bloco 2: O FLUXO DE ATENDIMENTO (Comanda e Fila Personalizada)
│   ├── Comanda (Dados do pedido, cliente, refeições/bebidas e status)
│   └── FilaAtendimento (Estrutura FIFO própria para os PFs/Refeições)
│
├── Bloco 3: O CAIXA E HISTÓRICO (Pagamentos e Vendas)
│   ├── Pagamento (Registra valor, data, hora, comanda e forma: Pix, Cartão, Dinheiro, Confiança)
│   └── Caixa (Processa pagamentos e armazena o histórico)
│
└── Bloco 4: REPOSIÇÃO, DADOS E RELATÓRIOS (Gestão e Persistência)
    ├── GerenciadorEstoque (Verifica e repõe mercadoria)
    ├── GerenciadorDados (Gera dados com Faker e persiste com Pickle)
    └── GerenciadorRelatorios (Gera relatórios de vendas e consumo)
Principais Premissas Adotadas
•	Separação entre Preço de Venda e Preço de Compra: O preço de venda pertence ao produto (cardápio). O preço de compra pertence a cada LoteEstoque, visto que os custos de aquisição flutuam a cada remessa com fornecedores.
•	Padronização de Bebidas: As bebidas possuem volume padronizado em 500ml e são categorizadas (ex: Água, Suco, Refrigerante), servindo a própria categoria como nome de produto.
•	Baixa FIFO com Validação em Duas Etapas: Para evitar o bug da "falsa baixa", o método de baixa do estoque primeiro realiza a consulta e soma total do item. A baixa efetiva nos lotes ocorre apenas se houver quantidade total suficiente em estoque.
•	Ordenação Cronológica Automática: A inserção de lotes realiza a ordenação por data de compra (data_compra), garantindo que o consumo do lote mais antigo ocorra independentemente da ordem de digitação das entradas.
________________________________________
Estruturas de Dados Customizadas
Para atender às restrições do projeto e exercitar o encapsulamento, foram desenvolvidas estruturas manuais baseadas em nós (No):
1.	Fila Dinâmica (FilaEstoque / FilaAtendimento): Estruturas encadeadas para o controle de saída de estoque (FIFO) e da ordem dos pedidos na cozinha.
2.	Lista Encadeada (ListaComandas): Gerenciamento dinâmico das comandas abertas e dos itens vinculados a cada cliente.
3.	Lista Encadeada (ListaHistorico): Armazenamento sequencial do histórico de comprovantes e registros de pagamentos efetuados.
________________________________________

Estrutura do Projeto
Plaintext
├── estruturas/         # Implementação manual de No, Fila e Listas Encadeadas
├── modelos/            # Classes de domínio (Produto, Comida, Bebida, LoteEstoque, Comanda, Pagamento)
├── servicos/           # Lógica de negócio (Estoque, Caixa, Gerenciadores e Interface)
├── .gitignore          # Arquivos ignorados (.venv, dados.pkl e caches)
├── main.py             # Ponto de entrada e menu interativo via terminal
├── README.md           # Documentação do projeto
└── requirements.txt    # Dependências do projeto (Faker, etc.)
________________________________________

Como Executar o Projeto
1.	Certifique-se de ter o Python 3 instalado.
2.	Crie e ative o ambiente virtual:
Bash
python -m venv .venv

# No Windows (PowerShell):
.venv\Scripts\Activate.ps1

# No Windows (Git Bash) ou Linux/Mac:
source .venv/bin/activate
3.	Instale as dependências:
Bash
pip install -r requirements.txt
4.	Execute a aplicação:
Bash
python main.py
________________________________________
Desenvolvedor
•	Nome: Mauro Silva Ruiz
•	E-mail: maurosilvaruiz@gmail.com
•	Repositório: maurosilvaruiz-gmail.com-FATEC_RioClaro_2SEM26-Projeto_Restaurante
•	Instituição: Fatec Rio Claro
•	Data de Apresentação: 17/09/2026 às 07h50
