from btree_node import BTreeNode
import uuid
import json
import os


class BTree:
    def __init__(self, t):
        self.t = t  # Grau mínimo da árvore B
        self.cache = {}  # Cache para nós carregados
        self.max_cache_size = 100  # Limite para o cache

        # Tenta carregar o UUID da raiz da árvore de root.json
        self.root = self.load_root()

        if self.root:
            self.root = self.load_node(self.root) or BTreeNode(leaf=True)
        else:
            # Se não há raiz, cria uma nova árvore B
            self.root = BTreeNode(leaf=True)
            self.save_root(self.root.node_id)
            self.save_node(self.root)

    def load_root(self):
        """Carrega o UUID do nó raiz de root.json."""
        try:
            with open('database/root.json', 'r') as f:
                data = json.load(f)
                return data['root_id']
        except FileNotFoundError:
            return None

    def save_root(self, root_id):
        """Salva o UUID do nó raiz em root.json."""
        with open('database/root.json', 'w') as f:
            json.dump({'root_id': root_id}, f)

    def load_node(self, node_id):
        """Carrega um nó do cache ou do disco, se necessário."""
        if node_id in self.cache:
            return self.cache[node_id]
        else:
            node = BTreeNode.load_from_disk(node_id)
            if node:
                self.cache[node_id] = node
                self._ensure_cache_limit()
            return node

    def save_node(self, node):
        """Salva um nó no disco e no cache."""
        self.cache[node.node_id] = node
        if node.keys:  # Salva o nó apenas se houver chaves
            node.save_to_disk()
        else:
            # Se o nó está vazio e é folha, podemos remover o arquivo se ele existir
            if node.leaf:
                file_path = f'database/{node.node_id}.json'
                # Verifica se o arquivo existe antes de remover
                if os.path.exists(file_path):
                    os.remove(file_path)
        self._ensure_cache_limit()

    def _ensure_cache_limit(self):
        """Garante que o cache não exceda seu tamanho máximo."""
        if len(self.cache) > self.max_cache_size:
            node_id_to_evict = next(iter(self.cache))
            self.cache[node_id_to_evict].save_to_disk()
            del self.cache[node_id_to_evict]

    def insert(self, k):
        """Insere uma nova chave k na árvore B."""
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            # A raiz está cheia, criar uma nova raiz e dividir
            new_root = BTreeNode(leaf=False)
            new_root.children.append(root.node_id)  # Referência ao antigo root
            # Gera um novo UUID para o novo nó raiz
            new_root.node_id = str(uuid.uuid4())
            self.root = new_root
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, k)
            self.save_root(new_root.node_id)  # Atualiza o UUID da nova raiz
            self.save_node(new_root)  # Salva a nova raiz
        else:
            self._insert_non_full(root, k)
        self.save_node(self.root)

    def _insert_non_full(self, node: BTreeNode, k):
        """Insere a chave k em um nó não cheio."""
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
            self.save_node(node)
        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            child = self.load_node(node.children[i])
            if len(child.keys) == (2 * self.t) - 1:
                self._split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_non_full(self.load_node(node.children[i]), k)

    def _split_child(self, parent: BTreeNode, index):
        """Divide o filho no índice especificado."""
        t = self.t
        child_id = parent.children[index]
        child = self.load_node(child_id)
        new_child = BTreeNode(leaf=child.leaf)
        new_child.node_id = str(uuid.uuid4())  # Novo ID único para o novo nó

        # Mover as chaves e filhos apropriados para o novo nó
        parent.keys.insert(index, child.keys[t - 1])
        parent.children.insert(index + 1, new_child.node_id)

        # Chaves e filhos do novo nó
        new_child.keys = child.keys[t:(2 * t) - 1]
        child.keys = child.keys[:t - 1]

        if not child.leaf:
            new_child.children = child.children[t:(2 * t)]
            child.children = child.children[:t]

        # Salvar nós no disco após a divisão
        self.save_node(child)
        self.save_node(new_child)
        self.save_node(parent)

    def search(self, k, node=None):
        """Busca uma chave k na árvore B."""
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and k == node.keys[i]:
            return (node, i)
        elif node.leaf:
            return None
        else:
            return self.search(k, self.load_node(node.children[i]))

    def update(self, old_k, new_k):
        """Atualiza uma chave na árvore B."""

        deleted = self.delete(old_k)  # Remove a chave antiga
        if deleted:
            self.insert(new_k)  # Insere a chave nova
            print(f"Chave {old_k} atualizada para {new_k} na árvore.")
        else:
            print(f"Chave {old_k} não encontrada na árvore.")

    def delete(self, k):
        """Remove uma chave k da árvore B."""
        if self.search(k) is None:
            print(f"Chave {k} não encontrada na árvore.")
            return False

        self._delete(self.root, k)

        # Após a exclusão, se a raiz está vazia e não é uma folha, promove o primeiro filho para a raiz
        if len(self.root.keys) == 0 and not self.root.leaf:
            # Salva o antigo UUID da raiz para possível exclusão
            old_root_id = self.root.node_id

            # O novo nó raiz é o único filho da raiz atual
            self.root = self.load_node(self.root.children[0])
            self.save_root(self.root.node_id)  # Atualiza o UUID da nova raiz

            # Remove o antigo nó raiz se ele ainda existir
            if old_root_id != self.root.node_id:
                self._remove_node_from_disk(old_root_id)

        elif len(self.root.keys) == 0 and self.root.leaf:
            # Se a raiz está vazia e é uma folha, a árvore está vazia, não há mais chaves
            self.root = None
            os.remove('database/root.json')

        if self.root:
            self.save_node(self.root)

        print(f"Chave {k} deletada da árvore.")
        return True

    def _remove_node_from_disk(self, node_id):
        """Remove o nó do disco se ele existir."""
        file_path = f'database/{node_id}.json'
        if os.path.exists(file_path):
            os.remove(file_path)

    def _delete(self, node: BTreeNode, k):
        t = self.t
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        if node.leaf:
            # Se o nó é uma folha e contém a chave, remove a chave
            if i < len(node.keys) and node.keys[i] == k:
                node.keys.pop(i)
                self.save_node(node)
            return

        child = self.load_node(node.children[i])

        if i < len(node.keys) and node.keys[i] == k:
            if len(child.keys) >= t:
                node.keys[i] = self._get_predecessor(node, i)
                self._delete(self.load_node(node.children[i]), node.keys[i])
            elif len(self.load_node(node.children[i + 1]).keys) >= t:
                node.keys[i] = self._get_successor(node, i)
                self._delete(self.load_node(
                    node.children[i + 1]), node.keys[i])
            else:
                self._merge(node, i)
                self._delete(self.load_node(node.children[i]), k)
        else:
            # Verifica se o filho a ser descido tem o mínimo de chaves
            if len(child.keys) < t:
                self._fill(node, i)
            # Corrige o carregamento do nó após possível fusão
            if i < len(node.children):
                self._delete(self.load_node(node.children[i]), k)
            else:
                self._delete(self.load_node(node.children[i - 1]), k)

    def _get_predecessor(self, node: BTreeNode, i):
        current = self.load_node(node.children[i])
        while not current.leaf:
            current = self.load_node(current.children[-1])
        return current.keys[-1]

    def _get_successor(self, node: BTreeNode, i):
        current = self.load_node(node.children[i + 1])
        while not current.leaf:
            current = self.load_node(current.children[0])
        return current.keys[0]

    def _merge(self, node: BTreeNode, i):
        child = self.load_node(node.children[i])
        sibling = self.load_node(node.children[i + 1])

        # Mover chave do nó pai para o nó filho
        child.keys.append(node.keys[i])
        child.keys.extend(sibling.keys)

        if not child.leaf:
            child.children.extend(sibling.children)

        node.keys.pop(i)
        node.children.pop(i + 1)

        self.save_node(child)
        self.save_node(node)

        # Remover nó irmão do disco
        os.remove(f'database/{sibling.node_id}.json')

    def _fill(self, node: BTreeNode, i):
        t = self.t
        if i != 0 and len(self.load_node(node.children[i - 1]).keys) >= t:
            self._borrow_from_prev(node, i)
        elif i != len(node.keys) and len(self.load_node(node.children[i + 1]).keys) >= t:
            self._borrow_from_next(node, i)
        else:
            if i != len(node.keys):
                self._merge(node, i)
            else:
                self._merge(node, i - 1)

    def _borrow_from_prev(self, node: BTreeNode, i):
        child = self.load_node(node.children[i])
        sibling = self.load_node(node.children[i - 1])
        child.keys.insert(0, node.keys[i - 1])
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        node.keys[i - 1] = sibling.keys.pop()
        self.save_node(child)
        self.save_node(sibling)
        self.save_node(node)

    def _borrow_from_next(self, node: BTreeNode, i):
        child = self.load_node(node.children[i])
        sibling = self.load_node(node.children[i + 1])
        child.keys.append(node.keys[i])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        node.keys[i] = sibling.keys.pop(0)
        self.save_node(child)
        self.save_node(sibling)
        self.save_node(node)

    def display(self, node=None, level=0):
        """Exibe a árvore (apenas para debug)."""
        if node is None:
            node = self.root
        print('Chaves no nível', level, ':', node.keys)
        if not node.leaf:
            for child_id in node.children:
                self.display(self.load_node(child_id), level + 1)
