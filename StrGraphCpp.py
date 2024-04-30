import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt


class BaseNode(object):
    def __init__(self, dag, name, call, param=None, input=None) -> None:
        self.dag = dag
        self.name = name
        self.call = call
        self.dag.add_node(name, call=call, param=param, input=input)


class Node(BaseNode):
    def __init__(self, dag, name, call, param=None, input=None) -> None:
        super().__init__(dag, name, call, param, input)

    def __rshift__(self, other: BaseNode):
        self.dag.add_edge(self.name, other.name)
        return other


class StrGraphCpp(object):
    def __init__(self, name=None) -> None:
        self.name = name
        self.dag = nx.DiGraph()
        self.nodes = []
        self.result = {}

    def addNode(self, name, call, param=None, input=None):
        node = Node(self.dag, name, call, param, input)
        self.nodes.append(node)
        return node

    def show(self):
        pos = graphviz_layout(self.dag, prog='dot')
        nx.draw_networkx(self.dag, pos, arrows=True, with_labels=True)
        plt.show()

    def check_has_cycle(self):
        # check if diagram is directed acyclic graph after add new edge
        if not nx.is_directed_acyclic_graph(self.dag):
            print("Cannot add edge. The graph contains cycles.")
            cycles = list(nx.simple_cycles(self.dag))
            for cycle in cycles:
                print(cycle)
            return True
        return False

    def check_is_missing_init_value(self):
        # check if first level nodes has initial input string
        flag = False
        for node in self.dag.nodes():
            if len(list(self.dag.predecessors(node))) == 0 and self.dag.nodes()[node]['input'] == None:
                print(f'Node {node} is missing init value')
                flag = True
        return flag

    def run(self):
        if self.check_has_cycle():
            return False
        if self.check_is_missing_init_value():
            return False
        nodes = self.dag.nodes()
        try:
            topological_order = nx.topological_sort(self.dag)
            for name in topological_order:
                node = nodes[name]
                pre_nodes = list(self.dag.predecessors(name))
                call = node['call']
                param = node['param']
                if len(pre_nodes) == 0:
                    # The first level nodes only support one input value at most and one or zero paramter
                    if param is None:
                        output = call(node['input'])
                    else:
                        output = call(node['input'], param)
                else:
                    # The next level nodes support more than one input value and one or zero paramter
                    inputs = [self.result[k] for k in pre_nodes]
                    if param is not None:
                        inputs.append(param)
                    output = call(*inputs)

                self.result[name] = output

        except Exception as e:
            print(e)
