from btree_node import BTreeNode
import json


class BTree:
    def __init__(self, t):
        self.root = BTreeNode(leaf=True)
        self.t = t  # Grau mínimo da árvore B

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
            return self.search(k, node.children[i])

    def insert(self, k):
        """Insere uma nova chave k na árvore B."""
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode()
            self.root = temp
            temp.children.insert(0, root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, node: BTreeNode, k):
        """Insere a chave k em um nó não cheio."""
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self._split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], k)

    def _split_child(self, x: BTreeNode, i: BTreeNode):
        """Divide o filho y de x no índice i."""
        t = self.t
        y = x.children[i]
        z = BTreeNode(leaf=y.leaf)
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.children = y.children[t: 2 * t]
            y.children = y.children[0: t]

    def delete(self, k):
        """Remove uma chave k da árvore B."""
        if self.search(k) is None:
            return False

        self._delete(self.root, k)

        # Caso especial: se a raiz ficar vazia e não for folha, devemos ajustá-la
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]

        return True


    def _delete(self, node: BTreeNode, k):
        t = self.t
        i = 0
        # Encontra o índice da chave k ou do filho apropriado
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        if node.leaf:
            # Caso 1: Remover de um nó folha
            if i < len(node.keys) and node.keys[i] == k:
                node.keys.pop(i)
            return

        # Se a chave está no nó não folha
        if i < len(node.keys) and node.keys[i] == k:
            if node.children[i].leaf:
                # Caso 2a: O predecessor está em um nó folha
                node.keys[i] = self._get_predecessor(node, i)
                self._delete(node.children[i], node.keys[i])
            elif node.children[i + 1].leaf:
                # Caso 2b: O sucessor está em um nó folha
                node.keys[i] = self._get_successor(node, i)
                self._delete(node.children[i + 1], node.keys[i])
            else:
                # Caso 2c: Ambos filhos têm pelo menos t chaves
                self._merge(node, i)
                self._delete(node.children[i], k)
        else:
            # Se a chave não está presente, desce para o filho adequado
            if len(node.children[i].keys) < t:
                self._fill(node, i)
            self._delete(node.children[i], k)

    def _get_predecessor(self, node: BTreeNode, i):
        current = node.children[i]
        while not current.leaf:
            current = current.children[-1]
        return current.keys[-1]

    def _get_successor(self, node: BTreeNode, i):
        current = node.children[i + 1]
        while not current.leaf:
            current = current.children[0]
        return current.keys[0]

    def _merge(self, node: BTreeNode, i):
        child = node.children[i]
        sibling = node.children[i + 1]
        child.keys.append(node.keys[i])
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.children.extend(sibling.children)
        node.keys.pop(i)
        node.children.pop(i + 1)

    def _fill(self, node: BTreeNode, i):
        t = self.t
        if i != 0 and len(node.children[i - 1].keys) >= t:
            self._borrow_from_prev(node, i)
        elif i != len(node.keys) and len(node.children[i + 1].keys) >= t:
            self._borrow_from_next(node, i)
        else:
            if i != len(node.keys):
                self._merge(node, i)
            else:
                self._merge(node, i - 1)

    def _borrow_from_prev(self, node: BTreeNode, i):
        child = node.children[i]
        sibling = node.children[i - 1]
        child.keys.insert(0, node.keys[i - 1])
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        node.keys[i - 1] = sibling.keys.pop()

    def _borrow_from_next(self, node: BTreeNode, i):
        child = node.children[i]
        sibling = node.children[i + 1]
        child.keys.append(node.keys[i])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        node.keys[i] = sibling.keys.pop(0)


    def update(self, old_k, new_k):
        """Atualiza uma chave na árvore B."""
        node, index = self.search(old_k)
        if node:
            node.keys[index] = new_k
        else:
            print("Chave não encontrada!")

    def save_to_file(self, filename):
        """Salva a árvore em um arquivo JSON."""
        with open(filename, 'w') as f:
            json.dump(self.root.to_dict(), f)

    def load_from_file(self, filename):
        """Carrega a árvore de um arquivo JSON."""
        with open(filename, 'r') as f:
            data = json.load(f)
            self.root = BTreeNode.from_dict(data)

    def display(self, node=None, level=0):
        """Exibe a árvore (apenas para debug)."""
        if node is None:
            node = self.root
        print('Chaves no nível', level, ':', node.keys)
        if not node.leaf:
            for child in node.children:
                self.display(child, level + 1)
