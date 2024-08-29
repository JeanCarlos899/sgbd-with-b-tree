import json
import os
import uuid


class BTreeNode:
    def __init__(self, leaf=False, node_id=None):
        self.leaf = leaf  # True se o nó for uma folha
        self.keys = []  # Lista de chaves
        self.children = []  # Lista de IDs dos filhos
        # Gerar um UUID único para cada nó se não for fornecido
        self.node_id = node_id or str(uuid.uuid4())

    def to_dict(self):
        """Converte o nó em um dicionário para facilitar a serialização JSON."""
        return {
            'leaf': self.leaf,
            'keys': self.keys,
            'children': self.children,  # Salva apenas os IDs dos filhos
            'node_id': self.node_id
        }

    @staticmethod
    def from_dict(data):
        """Reconstrói um nó a partir de um dicionário."""
        node = BTreeNode(leaf=data['leaf'], node_id=data['node_id'])
        node.keys = data['keys']
        node.children = data['children']  # Armazena apenas os IDs dos filhos
        return node

    def save_to_disk(self):
        """Salva o nó em um arquivo com o nome do seu identificador."""
        # Certifique-se de que o diretório 'database' existe
        if not os.path.exists('database'):
            os.makedirs('database')

        with open(f'database/{self.node_id}.json', 'w') as f:
            json.dump(self.to_dict(), f)

    @staticmethod
    def load_from_disk(node_id):
        """Carrega o nó de um arquivo."""
        file_path = f'database/{node_id}.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                return BTreeNode.from_dict(data)
        return None
