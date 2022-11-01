def gcd(a, b):
    if b > a:
        a, b = b, a
    while b != 0:
        residue = a % b
        a = b
        b = residue
    return a


if __name__ == '__main__':
    first, second = map(int, input('Enter two numbers: ').split())
    print(f'gcd({first}, {second}) = {gcd(first, second)}')