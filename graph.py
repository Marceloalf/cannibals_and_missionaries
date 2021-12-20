class Graph:
    def __init__(self):
        self.nodes = []
        self.objective = None
        self.init = None

    def append_nodes(self, status):
        """
        Function to add nodes in my graph.
        Obs: nodes won't be added if they're already in the graph
        """
        if not node_in_graph(status, self.nodes):
            self.nodes.append(status)

    def create_graph(self):
        graph_representation = {}

        for node in self.nodes:
            graph_representation[node] = []
            for adjacency in node.adjacency:
                graph_representation[node].append(adjacency["node"])

        return graph_representation

    def generate_path(self, path):
        if path[-1] == self.init:
            yield path
            return

        for adjacency in self.create_graph()[path[-1]]:
            if adjacency in path:
                continue
            for bigger_path in self.generate_path(path + [adjacency]):
                yield bigger_path


def node_in_graph(status, graph):
    for node in graph:
        if node.representation() == status.representation():
            return True

    return False
