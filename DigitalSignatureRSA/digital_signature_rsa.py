import random


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
        p = int(random.uniform(2 ** 8, 2 ** 16))
    return p


def count_result(base, bin_exp, mod):
    res = 1
    a = base
    for position in range(len(bin_exp)):
        if int(bin_exp[position]) != 0:
            res *= (a % mod) * int(bin_exp[position])
        a = (a * a) % mod
    res %= mod
    return res


def general_euclid_algorithm(base, mod):
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


def from_dec_to_reversed_bin(num):
    binary = ''
    while num > 0:
        binary += str(num % 2)
        num //= 2
    return binary


def count_hash(message):
    return message


class Abonent:
    def __init__(self, name):
        self.__P = generate_big_prime()
        self.__Q = generate_big_prime()
        self.__phi = (self.__P - 1) * (self.__Q - 1)
        self.N = self.__P * self.__Q
        self.__c = 0
        self.d = 0
        self.other_d = 0
        self.other_N = 0
        self.name = name
        self.message = 0

    def generate_message(self):
        self.message = int(random.uniform(2 ** 8, self.N))

    def generate_variables(self):
        c = 0
        u = [0, 0, 0]
        while u[0] != 1:
            c = int(random.uniform(2 ** 8, self.__phi))
            u = general_euclid_algorithm(c, self.__phi)
        self.__c = c
        self.d = u[1]

    def set_other_public_variables(self, d, N):
        self.other_d = d
        self.other_N = N

    def share_public_variables(self):
        return self.d, self.N

    def count_message_for_receiver(self):
        for_receiver = []

        print(f"{self.name}\n"
              f"I sent to Bob message: {self.message}\n"
              f"Hash function is h(m) = m\n")
        hash_value = count_hash(self.message)

        reversed_bin_c = from_dec_to_reversed_bin(self.__c)
        sign = count_result(hash_value, reversed_bin_c, self.N)

        for_receiver.append(self.message)
        for_receiver.append(sign)

        return for_receiver

    def check_digital_signature(self, message_and_sign):
        my_sign = count_hash(message_and_sign[0])

        reversed_bin_d = from_dec_to_reversed_bin(self.other_d)
        other_sign = count_result(message_and_sign[1], reversed_bin_d, self.other_N)

        if my_sign == other_sign:
            print(f"{self.name}\n"
                  f"I got message with signature: {message_and_sign}\n"
                  "And this is true message from Alice!\n"
                  f"Because equality is provable: {my_sign} == {other_sign}")
        else:
            print("Message is distorted or its not message from Alice...")


def main():
    alice = Abonent("ALICE")
    bob = Abonent("BOB")

    alice.generate_variables()
    bob.generate_variables()

    alice_d, alice_N = alice.share_public_variables()
    bob.set_other_public_variables(alice_d, alice_N)

    alice.generate_message()

    for_bob = alice.count_message_for_receiver()
    bob.check_digital_signature(for_bob)


if __name__ == '__main__':
    main()
