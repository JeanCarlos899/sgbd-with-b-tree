class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf  # True se o nó for uma folha
        self.keys = []  # Lista de chaves
        self.children = []  # Lista de filhos

    def to_dict(self):
        """Converte o nó em um dicionário para facilitar a serialização JSON."""
        return {
            'leaf': self.leaf,
            'keys': self.keys,
            'children': [child.to_dict() for child in self.children]
        }

    @staticmethod
    def from_dict(data):
        """Reconstrói um nó a partir de um dicionário."""
        node = BTreeNode(leaf=data['leaf'])
        node.keys = data['keys']
        node.children = [BTreeNode.from_dict(
            child) for child in data['children']]
        return node
