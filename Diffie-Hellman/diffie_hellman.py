import random


class Abonent:
    def __init__(self, name):
        self.name = name
        self.p = 30803
        self.g = 2
        self.__secret_key = int(random.uniform(2, self.p - 1))
        self.public_key = self.count_key(self.g, self.__secret_key, self.p)

    def get_public_key(self):
        return self.public_key

    def count_common_key(self, received_key):
        return self.count_key(received_key, self.__secret_key, self.p)

    def count_result(self, binary, base, mod):
        res = 1
        a = base
        for position in range(len(binary)):
            if int(binary[position]) != 0:
                res *= (a % mod) * int(binary[position])
            a = (a * a) % mod
        res %= mod
        return res

    def from_base10_to_reversed_base2(self, num):
        binary = ''
        while num > 0:
            binary += str(num % 2)
            num //= 2
        return binary

    def count_key(self, base, exp, mod):
        binary_exp = self.from_base10_to_reversed_base2(exp)
        return self.count_result(binary_exp, base, mod)


def main():
    alice = Abonent("Alice")
    bob = Abonent("Bob")

    alice_common_key = alice.count_common_key(bob.get_public_key())
    bob_common_key = bob.count_common_key(alice.get_public_key())

    print(f'{alice.name} public key = {alice.public_key}\n'
          f'{bob.name} public key = {bob.public_key}\n')

    print(f'{alice.name} common key = {alice_common_key}\n'
          f'{bob.name} common key = {bob_common_key}\n\n'
          f'Common keys are equal!')


if __name__ == "__main__":
    main()
