import time
import random
from btree import BTree
import os


def run_performance_tests(btree: BTree, num_tests=1, num_operations=500):
    """Executa testes de desempenho para as operações de inserção, remoção, atualização e deleção."""
    insert_times = []
    delete_times = []
    update_times = []
    search_times = []

    for _ in range(num_tests):
        # Gera dados aleatórios
        data = generate_random_data(num_operations)
        updated_data = generate_random_data(num_operations)

        # Testa a inserção
        start_time = time.time()
        for item in data:
            btree.insert(item)
        insert_times.append(time.time() - start_time)

        # Testa a busca
        start_time = time.time()
        for item in data:
            btree.search(item)
        search_times.append(time.time() - start_time)

        # Testa a atualização
        start_time = time.time()
        for old_item, new_item in zip(data, updated_data):
            btree.update(old_item, new_item)
        update_times.append(time.time() - start_time)

        # Testa a deleção
        start_time = time.time()
        for item in updated_data:
            btree.delete(item)
            # Após cada deleção, verifique se a árvore está vazia
            if btree.root is None:
                btree = BTree(btree.t)  # Recria a árvore se estiver vazia
        delete_times.append(time.time() - start_time)


    # Calcula a média de tempo para cada operação em segundos
    avg_insert_time = sum(insert_times) / num_tests
    avg_search_time = sum(search_times) / num_tests
    avg_update_time = sum(update_times) / num_tests
    avg_delete_time = sum(delete_times) / num_tests

    # Converte os tempos médios para milissegundos (ms)
    avg_insert_time_ms = avg_insert_time * 1000
    avg_search_time_ms = avg_search_time * 1000
    avg_update_time_ms = avg_update_time * 1000
    avg_delete_time_ms = avg_delete_time * 1000

    print("===========================================================")
    print("RESULTADOS DOS TESTES DE DESEMPENHO")
    print(
        f"Nº testes: {num_tests}x | Nº de op.: {num_operations} | Grau mínimo: {btree.t}")
    print("===========================================================")
    print("Tempo médio de inserção: {:.2f} ms".format(avg_insert_time_ms))
    print("Tempo médio de busca: {:.2f} ms".format(avg_search_time_ms))
    print("Tempo médio de atualização: {:.2f} ms".format(
        avg_update_time_ms))
    print("Tempo médio de deleção: {:.2f} ms".format(avg_delete_time_ms))



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
    run_performance_tests(btree)
