import numpy as np
from Set import Set
class Sets:
    def __init__(self):

        self.sets = []

    def add(self, start, end):

        if not self.sets:
            self.sets.append(Set(start, end))
            print('gers jher')
        else:
            found = False
            for set in self.sets:
                res = set.add(start, end)
                if res is True:
                    found = True
                    break
            # if not found:
            #     self.sets.append(Set(start, end))
        # print(len(self.sets))