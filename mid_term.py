import numpy as np
def subRoutine(m):
    j = 0
    t = m
    while j < m:
        for l in range(m, j - 1, -1):
            t += j
        j += 1
    return t

def main(n):
    i = 1
    s = 1
    while i <= n:
        i = 2 * i
        s = s + subRoutine(i)
    h = subRoutine(s)
    print('s', s)
    # print(h)

def verify_main(n):
    if n <= 0:
        return 1

    ans = 1
    k = int(np.floor(np.log2(n)) + 1)
    print('k', k)
    for j in range(1, k + 1, 1):
        m = np.power(2, j)
        print('m', m, j)
        temp = 0
        for i in range(0, m, 1):
            temp += (m - i)*(i + 1)
        ans += temp
            # print('hh',ans, i, 2^j, j, i)
    print('verified s', ans)
    return ans

def verify_subroutine(m):
    if m <= 0:
        return m
    t = 0
    for i in range(0, m, 1):
        t += (m - i) * (i + 1)
    return t

n = 10
main(n)
verify_main(n)

m = -1
print('sub', subRoutine(m))
print('verified sub', verify_subroutine(m))

print(np.log2(2))

# t = subRoutine(3)
# print(t)
# # main(1)
