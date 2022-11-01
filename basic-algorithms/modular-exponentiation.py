def count_result(binary, base, mod):
    res = 1
    a = base
    for position in range(len(binary)):
        if int(binary[position]) != 0:
            res *= (a % mod) * int(binary[position])
        a = (a * a) % mod
    res %= mod
    return res


def from_base10_to_reversed_base2(num):
    binary = ''
    while num > 0:
        binary += str(num % 2)
        num //= 2
    return binary


if __name__ == '__main__':
    base, exp, mod = map(int, input("Enter base, exp, mod: ").split())

    binary_exp = from_base10_to_reversed_base2(exp)
    result = count_result(binary_exp, base, mod)

    print(f'{base}^{exp}(mod {mod}) = {result}')
