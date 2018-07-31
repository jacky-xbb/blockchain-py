import utils


class MerkleNode(object):
    """ Repersents a node of merkle tree.

    Args:
        left (MerkleNode object): a left subtree.
        right (MerkleNode object): a right subtree.
        data (byte): value of node. 

    Attributes:
        left (MerkleNode object): a left subtree.
        right (MerkleNode object): a right subtree.
        data (byte): value of node. 
    """

    def __init__(self, left, right, data):

        if left is None and right is None:
            self.data = utils.sum256_byte(data)
        else:
            self.data = utils.sum256_byte(left.data, right.data)

        self.left = left
        self.right = right


class MerkleTree(object):
    """ Repersents a merkle tree.

    Args:
        data_list (list): a list of data.

    Attributes:
        _root (MerkleNode object): the root of merkle tree.
    """

    def __init__(self, data_list):
        nodes = []

        if len(data_list) % 2 != 0:
            data_list.append(data_list[-1])

        for data in data_list:
            nodes.append(MerkleNode(None, None, data))

        for i in range(len(data_list)//2):
            new_level = []

            for j in range(0, len(nodes), 2):
                node = MerkleNode(nodes[j], nodes[j+1], None)
                new_level.append(node)

            nodes = new_level

        self._root = nodes[0]

    @property
    def root(self):
        return self._root

    @property
    def root_hash(self):
        return self._root.data
