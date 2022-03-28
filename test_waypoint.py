from Waypoint import Waypoint
import random
a = Waypoint(20.291, 28.862, 12)
b = Waypoint(10.45, 11, 12)
c = Waypoint(10.45, 11.2, 12)
d = Waypoint(10.45, 11.2, 12.1)
#
# l = [b, c, d, a]
# l.append(b)
#
# origins = {1: b}
# uav = 2
# origins[uav] = a
#
# print('len of origins', len(origins), random.random() * 5 - 10)
#
# print(origins)
#
# print(a in l)
# for ll in l:
#     print(ll.x, ll.y, ll.z)
#
# print('after sort')
# l2 = l.sort()
# for ll in l:
#     print(ll.x, ll.y, ll.z)
#
#
# print(l.index(a))
# print(l.index(b))
#
#
ab = {1: a, 2: b, 3: c}
print(ab[0])
for aa in ab:
    print(ab[aa])
# print(list(ab.values()).index('uav2'))
# # print(ab.values())
#
# for i in range(4):
#     print(i + 1)
