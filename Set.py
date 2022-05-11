import numpy as np

class Set:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        # self.weight = weight
        self.end.next = self.start
        self.start.next = None
        self.nodes = []
        self.nodes.append(start)
        self.nodes.append(end)

    def add(self, start, end):
        succeed = True

        if end not in self.nodes and start == self.nodes[-1]:
            # end.next = self.start
            print("gets heress")
            self.nodes.append(end)
            return succeed
        elif start not in self.nodes and end == self.nodes[-1]:
            # end.next = self.start
            print("gets heress")
            self.nodes.append(start)
            return succeed
        elif end not in self.nodes and start == self.nodes[0]:
            # self.nodes[0].next = end
            print("gets heress")
            self.nodes.insert(0, end)
            return succeed
        elif start not in self.nodes and end ==  self.nodes[0]:
            # self.nodes[0].next = start
            print("gets heress")
            self.nodes.insert(0, start)
            return succeed


        else:
            # print('cannot insert the start and end nodes')
            print(start, end, self.nodes[0], self.nodes[-1], end in self.nodes )
            return not succeed

    def __str__(self):
        line = 'Set0:'
        for node in self.nodes:
            line += str(node.id) + ' '
        # print(self.nodes)
        return line

    # def add_all(self, start, nodes):
    #     for node in nodes:
    #         if node is nodes:
    #             print('node already in the nodes.  ')
    #
    #     if start is self.nodes[-1]:
    #         for i in range(len(nodes) - 1):
    #             self.nodes.append(nodes[i + 1])


