class Graph:
    def __init__(self):
        self.nodes = []

    def append_nodes(self, status):
        """
        Function to add nodes in my graph.
        Obs: nodes won't be added if they're already in the graph
        """
        if not node_in_graph(status, self.nodes):
            self.nodes.append(status)


def node_in_graph(status, graph):
    for node in graph:
        if node.representation() == status.representation():
            return True

    return False
