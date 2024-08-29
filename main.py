from btree import BTree
import random
import time
import psutil
import os


def generate_random_data(n):
    """Gera uma lista de n números inteiros aleatórios"""
    return random.sample(range(1, 2*n), n)


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
    print("2. Buscar dados na Árvore B\t\t6. Exibir Árvore B")
    print("3. Atualizar dados na Árvore B\t\t7. Deletar database")
    print("4. Remover dados da Árvore B\t\t0. Sair")


def main():
    # Cria o diretório 'database' se não existir
    if not os.path.exists('database'):
        os.makedirs('database')

    t = 100
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
            mem_usage = measure_memory()

            print("===========================================================")
            print(
                f"Valor {k} inserido na árvore em {time_elapsed * 1000:.3f} ms.")
            print(f"Uso de memória: {mem_usage / (1024 ** 2):.2f} MB")
            print("===========================================================")

        elif choice == '2':
            k = int(input("Digite o valor a ser buscado: "))

            start_time = time.time()
            result = btree.search(k)
            end_time = time.time()

            time_elapsed = end_time - start_time
            mem_usage = measure_memory()

            if result:
                print("===========================================================")
                print(
                    f"Valor {k} encontrado na árvore em {time_elapsed * 1000:.3f} ms.")
                print(f"Uso de memória: {mem_usage / (1024 ** 2):.2f} MB")
                print("===========================================================")
            else:
                print(f"Valor {k} não encontrado na árvore.")

        elif choice == '3':
            old_k = int(input("Digite o valor a ser atualizado: "))
            new_k = int(input("Digite o novo valor: "))

            start_time = time.time()
            updated = btree.update(old_k, new_k)
            end_time = time.time()

            time_elapsed = end_time - start_time
            mem_usage = measure_memory()

            if updated:
                print("===========================================================")
                print(
                    f"Valor {old_k} atualizado para {new_k} em {time_elapsed * 1000:.3f} ms.")
                print(f"Uso de memória: {mem_usage / (1024 ** 2):.2f} MB")
                print("===========================================================")
            else:
                print(f"Valor {old_k} não encontrado na árvore.")

        elif choice == '4':
            k = int(input("Digite o valor a ser removido: "))

            start_time = time.time()
            deleted = btree.delete(k)
            end_time = time.time()

            time_elapsed = end_time - start_time
            mem_usage = measure_memory()

            if deleted or deleted is None:
                if deleted is None:
                    btree = BTree(t)
                print("===========================================================")
                print(
                    f"Valor {k} removido da árvore em {time_elapsed * 1000:.3f} ms.")
                print(f"Uso de memória: {mem_usage / (1024 ** 2):.2f} MB")
                print("===========================================================")
            else:
                print(f"Valor {k} não encontrado na árvore.")

        elif choice == '5':
            n = int(input("Quantos dados aleatórios deseja gerar? "))
            data = generate_random_data(n)
            for value in data:
                btree.insert(value)
            print("Dados inseridos na árvore B.")

        elif choice == '6':
            btree.display()

        elif choice == '7':
            for file in os.listdir('database'):
                file_path = os.path.join('database', file)
                os.remove(file_path)
            print("Arquivos de banco de dados removidos.")

            # criar uma nova árvore B
            btree = BTree(t)

        elif choice == '0':
            print("Saindo do programa.")
            break

        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    main()
