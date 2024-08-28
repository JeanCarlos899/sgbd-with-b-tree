# Sistema Gerenciador de Banco de Dados Simples Utilizando Árvores B - ESTRUTURA DE DADOS II

Este repositório contém o código-fonte e a documentação de um Sistema Gerenciador de Banco de Dados (SGBD) simples, desenvolvido para realizar operações básicas de CRUD (Create, Read, Update, Delete) utilizando a estrutura de dados Árvore B para indexação.

## Objetivo

O objetivo deste projeto é demonstrar a compreensão dos conceitos de Sistemas Gerenciadores de Banco de Dados (SGBDs), estruturas de dados e algoritmos, além de aplicar esses conhecimentos na prática através da implementação de uma Árvore B.

## Funcionalidades

- **Inserção (INSERT)**: Insere novos registros no banco de dados, indexando-os na Árvore B.
- **Busca (SELECT)**: Busca registros específicos no banco de dados utilizando a Árvore B como índice.
- **Atualização (UPDATE)**: Atualiza registros existentes no banco de dados.
- **Remoção (DELETE)**: Remove registros do banco de dados e atualiza a Árvore B.
- **Geração de Dados Aleatórios**: Cria um conjunto de dados aleatórios para testar o sistema.
- **Avaliação de Desempenho**: Mede o tempo de execução e o consumo de memória das operações CRUD.

## Estrutura do Repositório

- `btree.py`: Implementação da classe BTree, que representa a árvore B e suas operações.
- `btree_node.py`: Implementação da classe BTreeNode, que representa os nós da árvore B.
- `main.py`: Código principal para interação com o usuário, incluindo um menu para operações CRUD e testes de desempenho.
- `database/`: Diretório onde o arquivo JSON da árvore B é salvo e carregado.
- `README.md`: Este arquivo.

## Como Usar

1. **Clone o Repositório:**

    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2. **Instale as Dependências:** Certifique-se de que você tenha o Python instalado. Este projeto requer a biblioteca psutil, que pode ser instaladas via pip.

    ```bash
    pip install psutil
    ```

3. **Execute o Programa:**

    ```bash
    python main.py
    ```
