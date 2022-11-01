import random
import numpy as np


def is_prime(num):
    if num % 2 == 0:
        return False
    else:
        for div in range(3, int(num ** 0.5) + 1, 2):
            if num % div == 0:
                return False
    return True


def generate_big_prime():
    p = 2
    while not is_prime(p):
        p = int(random.uniform(2 ** 3, 2 ** 12))
    return p


def from_dec_to_reversed_bin(num):
    binary = ''
    while num > 0:
        binary += str(num % 2)
        num //= 2
    return binary


def count_result(base, bin_exp, mod):
    res = 1
    a = base
    for position in range(len(bin_exp)):
        if int(bin_exp[position]) != 0:
            res *= (a % mod) * int(bin_exp[position])
        a = (a * a) % mod
    res %= mod
    return res


def generate_equation():
    a = int(random.uniform(2 ** 2, 2 ** 5))
    p = generate_big_prime()
    y = int(random.uniform(2 ** 2, 2 ** 7))
    return y, a, p


def main():
    y, a, p = generate_equation()
    n = int(random.uniform(np.sqrt(p) + 1, np.sqrt(p) * 2))
    m = int(random.uniform(np.sqrt(p) + 1, np.sqrt(p) * 2))
    print(f"Generated expression:\n"
          f"{y} = {a} ^ x (mode {p})\n")
    print(f"Generated numbers:\n"
          f"n = {n}, m = {m}\n")

    first_row = [((y * (count_result(a, from_dec_to_reversed_bin(i), p))) % p, i, 1) for i in range(0, n + 1)]
    second_row = [(count_result(a, from_dec_to_reversed_bin(m * j), p), j, 2) for j in range(1, n + 1)]

    sorted_together = sorted(first_row + second_row, key=lambda x: x[0])

    i, j = 0, 0
    for k in range(len(sorted_together) - 1):
        if sorted_together[k][0] == sorted_together[k + 1][0] and sorted_together[k][2] != sorted_together[k + 1][2]:
            if sorted_together[k][2] == 1:
                i = sorted_together[k][1]
                j = sorted_together[k + 1][1]
            else:
                i = sorted_together[k + 1][1]
                j = sorted_together[k][1]
            break

    x = j * m - i

    if count_result(a, from_dec_to_reversed_bin(x), p) == y:
        print(f"Such x exists!\n"
              f"x = {x}")
    else:
        print("Such x doesnt exist!")


if __name__ == '__main__':
    main()
