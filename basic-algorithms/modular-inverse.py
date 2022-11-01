def count_inverse(mod, base):
    u = [mod, 0]
    v = [base, 1]
    while v[0] != 0:
        q = u[0] // v[0]
        t = [u[0] % v[0], u[1] - q * v[1]]
        u = v
        v = t
    if u[1] < 0:
        u[1] += mod
    return u


if __name__ == '__main__':
    base, mod = map(int, input("Enter base, mod: ").split())

    result = count_inverse(mod, base)

    if result[0] != 1:
        print(f'{base}^(-1)(mod {mod}) != 1\n'
              f'Impossible to find modular inverse')
    else:
        print(f'{base}^(-1)(mod {mod}) = {result}')
