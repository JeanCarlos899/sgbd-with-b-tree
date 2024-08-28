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
            self.split_child(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)

    def insert_non_full(self, node: BTreeNode, k):
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
                self.split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self.insert_non_full(node.children[i], k)

    def split_child(self, x: BTreeNode, i: BTreeNode):
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
        self.delete_internal(self.root, k)

        # Se a raiz tiver 0 chaves e não for uma folha, substituímos a raiz
        if len(self.root.keys) == 0:
            if not self.root.leaf:
                self.root = self.root.children[0]
            else:
                self.root = BTreeNode(leaf=True)

    def delete_internal(self, node: BTreeNode, k):
        """Função recursiva para remover uma chave da árvore B."""
        t = self.t
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        if i < len(node.keys) and node.keys[i] == k:
            # Caso 1: A chave a ser removida está em um nó folha
            if node.leaf:
                node.keys.pop(i)
            else:
                # Caso 2: A chave a ser removida está em um nó interno
                y = node.children[i]
                z = node.children[i + 1]
                if len(y.keys) >= t:
                    node.keys[i] = self.get_predecessor(y)
                    self.delete_internal(y, node.keys[i])
                elif len(z.keys) >= t:
                    node.keys[i] = self.get_successor(z)
                    self.delete_internal(z, node.keys[i])
                else:
                    self.merge(node, i)
                    self.delete_internal(y, k)
        elif node.leaf:
            # A chave não está na árvore
            print("A chave {} não está presente na árvore.".format(k))
            return
        else:
            # A chave a ser removida não está presente neste nó
            if len(node.children[i].keys) < t:
                if i != 0 and len(node.children[i - 1].keys) >= t:
                    self.borrow_from_prev(node, i)
                elif i != len(node.keys) and len(node.children[i + 1].keys) >= t:
                    self.borrow_from_next(node, i)
                else:
                    if i != len(node.keys):
                        self.merge(node, i)
                    else:
                        self.merge(node, i - 1)
            self.delete_internal(node.children[i], k)

    def get_predecessor(self, node: BTreeNode):
        """Obtém o predecessor de uma chave."""
        while not node.leaf:
            node = node.children[len(node.keys)]
        return node.keys[-1]

    def get_successor(self, node: BTreeNode):
        """Obtém o sucessor de uma chave."""
        while not node.leaf:
            node = node.children[0]
        return node.keys[0]

    def borrow_from_prev(self, node: BTreeNode, idx):
        """Empresta uma chave do filho anterior de node.children[idx]."""
        child = node.children[idx]
        sibling = node.children[idx - 1]
        child.keys.insert(0, node.keys[idx - 1])
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        node.keys[idx - 1] = sibling.keys.pop()

    def borrow_from_next(self, node: BTreeNode, idx):
        """Empresta uma chave do próximo filho de node.children[idx]."""
        child = node.children[idx]
        sibling = node.children[idx + 1]
        child.keys.append(node.keys[idx])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        node.keys[idx] = sibling.keys.pop(0)

    def merge(self, node: BTreeNode, idx):
        """Funde node.children[idx] com node.children[idx+1]."""
        child = node.children[idx]
        sibling = node.children[idx + 1]
        child.keys.append(node.keys.pop(idx))
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.children.extend(sibling.children)
        node.children.pop(idx + 1)

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
