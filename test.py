import time
import random
from btree import BTree
import os
import psutil  # Import psutil to measure memory usage


def run_performance_tests(btree: BTree, num_tests, num_operations):
    """Executa testes de desempenho para as operações de inserção, remoção, atualização e deleção."""
    insert_times = []
    delete_times = []
    update_times = []
    search_times = []

    start_test_time = time.time()

    # Get the current process for memory measurement
    process = psutil.Process(os.getpid())

    for _ in range(num_tests):
        # Gera dados aleatórios
        data = generate_random_data(num_operations)
        updated_data = generate_random_data(num_operations)

        # Testa a inserção
        for item in data:
            start_time = time.time()
            btree.insert(item)
            # Registra o tempo de cada inserção
            insert_times.append(time.time() - start_time)

        # Measure memory after all insertions
        mem_after_insertion = process.memory_info().rss

        # Testa a busca
        for item in data:
            start_time = time.time()
            btree.search(item)
            # Registra o tempo de cada busca
            search_times.append(time.time() - start_time)

        # Measure memory after all searches
        mem_after_search = process.memory_info().rss

        # Testa a atualização
        for old_item, new_item in zip(data, updated_data):
            start_time = time.time()
            btree.update(old_item, new_item)
            # Registra o tempo de cada atualização
            update_times.append(time.time() - start_time)

        # Measure memory after all updates
        mem_after_update = process.memory_info().rss

        # Testa a deleção
        for item in updated_data:
            start_time = time.time()
            btree.delete(item)
            # Registra o tempo de cada deleção
            delete_times.append(time.time() - start_time)
            # Após cada deleção, verifique se a árvore está vazia
            if btree.root is None:
                btree = BTree(btree.t)  # Recria a árvore se estiver vazia

        # Measure memory after all deletions
        mem_after_deletion = process.memory_info().rss

    end_test_time = time.time()
    total_test_time = end_test_time - start_test_time

    # Calcula a média de tempo para cada operação individual em segundos
    avg_insert_time = sum(insert_times) / len(insert_times)
    avg_search_time = sum(search_times) / len(search_times)
    avg_update_time = sum(update_times) / len(update_times)
    avg_delete_time = sum(delete_times) / len(delete_times)

    # Converte os tempos médios para milissegundos (ms)
    avg_insert_time_ms = avg_insert_time * 1000
    avg_search_time_ms = avg_search_time * 1000
    avg_update_time_ms = avg_update_time * 1000
    avg_delete_time_ms = avg_delete_time * 1000

    # Convert memory usage to megabytes (MB)
    mem_usage_insertion_mb = mem_after_insertion / (1024 ** 2)
    mem_usage_search_mb = mem_after_search / (1024 ** 2)
    mem_usage_update_mb = mem_after_update / (1024 ** 2)
    mem_usage_deletion_mb = mem_after_deletion / (1024 ** 2)

    print("===========================================================")
    print("RESULTADOS DOS TESTES DE DESEMPENHO")
    print(
        f"Nº testes: {num_tests}x | Nº de op.: {num_operations} | Grau mínimo: {btree.t}")
    print("Tempo total de execução: {:.2f} s".format(total_test_time))
    print("===========================================================")
    print("Tempo médio de inserção por operação: {:.6f} ms".format(
        avg_insert_time_ms))
    print("Tempo médio de busca por operação: {:.6f} ms".format(
        avg_search_time_ms))
    print("Tempo médio de atualização por operação: {:.6f} ms".format(
        avg_update_time_ms))
    print("Tempo médio de deleção por operação: {:.6f} ms".format(
        avg_delete_time_ms))
    print("===========================================================")
    print("Memória total após inserção de {} elementos: {:.2f} MB".format(
        num_operations, mem_usage_insertion_mb))
    print("Memória total após busca de {} elementos: {:.2f} MB".format(
        num_operations, mem_usage_search_mb))
    print("Memória total após atualização de {} elementos: {:.2f} MB".format(
        num_operations, mem_usage_update_mb))
    print("Memória total após deleção de {} elementos: {:.2f} MB".format(
        num_operations, mem_usage_deletion_mb))


def generate_random_data(n):
    """Gera uma lista de n números inteiros aleatórios"""
    return random.sample(range(1, 2*n), n)


if __name__ == "__main__":
    if not os.path.exists('database'):
        os.makedirs('database')

    for file in os.listdir('database'):
        os.remove(f'database/{file}')

    t = 100  # Grau mínimo da árvore B
    btree = BTree(t)

    # será testado uma vez cade operação CRUD por 1000 vezes e ao final
    # será exibido o tempo médio de execução de cada operação em ms.
    run_performance_tests(btree, num_tests=1, num_operations=1000)
