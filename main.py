from btree import BTree
import random
import time
import psutil
import os


def generate_random_data(n, range_start=1, range_end=None):
    """Gera uma lista de n números inteiros aleatórios entre range_start e range_end."""
    if range_end is None:
        range_end = n + 1

    return random.sample(range(range_start, range_end), n)


def measure_execution_time(btree: BTree, data, operation):
    """Mede o tempo de execução de uma operação na árvore B."""
    start_time = time.time()
    if operation == 'insert':
        for item in data:
            btree.insert(item)
    elif operation == 'delete':
        for item in data:
            deleted = btree.delete(item)
            if not deleted:
                print(f"Valor {item} não encontrado na árvore.")
            else:
                print(f"Valor {item} removido da árvore.")
    elif operation == 'search':
        for item in data:
            btree.search(item)
    end_time = time.time()
    return end_time - start_time


def measure_memory():
    """Mede o uso de memória atual do processo."""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss  # Retorna o uso de memória residente


def main_menu():
    print("\n=== Menu Principal ===")
    print("1. Inserir dados na Árvore B\t\t5. Gerar dados aleatórios")
    print("2. Buscar dados na Árvore B\t\t6. Avaliar desempenho (tempo e memória)")
    print("3. Atualizar dados na Árvore B\t\t7. Exibir Árvore B")
    print("4. Remover dados da Árvore B\t\t8. Salvar Árvore B em arquivo")
    print("0. Sair\t\t\t\t\t9. Carregar Árvore B de arquivo")


def main():
    t = int(input("Digite o grau mínimo da Árvore B (t): "))
    btree = BTree(t)

    while True:
        main_menu()
        choice = input("Escolha uma opção: ")

        if choice == '1':
            k = int(input("Digite o valor a ser inserido: "))

            start_time = time.time()
            btree.insert(k)
            end_time = time.time()

            time_elapsed = end_time - start_time
            print(
                f"Valor {k} inserido na árvore em {time_elapsed * 1000:.4f} ms.")

        elif choice == '2':
            k = int(input("Digite o valor a ser buscado: "))

            start_time = time.time()
            result = btree.search(k)
            end_time = time.time()

            time_elapsed = end_time - start_time
            if result:
                print(
                    f"Valor {k} encontrado na árvore em {time_elapsed * 1000:.4f} ms.")
            else:
                print(f"Valor {k} não encontrado na árvore.")

        elif choice == '3':
            old_k = int(input("Digite o valor a ser atualizado: "))
            new_k = int(input("Digite o novo valor: "))

            start_time = time.time()
            btree.update(old_k, new_k)
            end_time = time.time()

            time_elapsed = end_time - start_time

            print(
                f"Valor {old_k} atualizado para {new_k} em {time_elapsed * 1000:.4f} ms.")

        elif choice == '4':
            k = int(input("Digite o valor a ser removido: "))

            start_time = time.time()
            deleted = btree.delete(k)
            end_time = time.time()

            time_elapsed = end_time - start_time

            if deleted:
                print(
                    f"Valor {k} removido da árvore em {time_elapsed * 1000:.4f} ms.")
            else:
                print(f"Valor {k} não encontrado na árvore.")

        elif choice == '5':
            n = int(input("Quantos dados aleatórios deseja gerar? "))
            range_start = int(
                input("Digite o início do intervalo de valores: "))
            range_end = int(input("Digite o fim do intervalo de valores: "))
            data = generate_random_data(n, range_start, range_end)
            for value in data:
                btree.insert(value)
            print("Dados inseridos na árvore B.")

        elif choice == '6':
            operation = input(
                "Qual operação deseja medir (insert/delete/search)? ")
            n = int(input("Quantos dados aleatórios para a operação? "))
            data = generate_random_data(n)
            execution_time = measure_execution_time(btree, data, operation)
            memory_usage = measure_memory()
            print(
                f"Tempo de execução para {operation}: {execution_time * 1000:.4f} ms")
            print(f"Uso de memória: {memory_usage / (1024 ** 2):.2f} MB")

        elif choice == '7':
            btree.display()

        elif choice == '8':
            btree.save_to_file('database/btree.json')
            print(f"Árvore B salva em 'database/btree.json'.")

        elif choice == '9':
            btree.load_from_file('database/btree.json')
            print(f"Árvore B carregada de 'database/btree.json'.")

        elif choice == '0':
            print("Saindo do programa.")
            break

        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    main()
