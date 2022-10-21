import random


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


def count_result(base, bin_exp, mod):
    res = 1
    a = base
    for position in range(len(bin_exp)):
        if int(bin_exp[position]) != 0:
            res *= (a % mod) * int(bin_exp[position])
        a = (a * a) % mod
    res %= mod
    return res


def generate_g(p, q):
    g = int(random.uniform(2, p - 1))
    result = count_result(g, from_dec_to_reversed_bin(q), p)
    while result == 1:
        g = int(random.uniform(2, p - 1))
        result = count_result(g, from_dec_to_reversed_bin(q), p)
    return g


def is_prime(num):
    if num % 2 == 0:
        return False
    else:
        for div in range(3, int(num ** 0.5) + 1, 2):
            if num % div == 0:
                return False
    return True


def generate_p_prime():
    p = 2
    q = 2
    while not is_prime(q) and not is_prime(p):
        q = int(random.uniform(2 ** 8, 2 ** 16))
        p = 2 * q + 1
    return p, q


def from_dec_to_reversed_bin(num):
    binary = ''
    while num > 0:
        binary += str(num % 2)
        num //= 2
    return binary


def count_hash(message):
    return message


class Abonent:
    def __init__(self, name, p, g):
        self.p = p
        self.g = g
        self.x = int(random.uniform(2, self.p - 1))
        self.y = count_result(self.g, from_dec_to_reversed_bin(self.x), self.p)
        self.k = 0
        self.other_y = 0
        self.name = name
        self.message = 0

    def generate_message(self):
        self.message = int(random.uniform(2 ** 8, self.p))

    def set_other_public_variables(self, y):
        self.other_y = y

    def share_public_variables(self):
        return self.y

    def get_k_inverse(self, k):
        u = [0, 0, 0]
        while u[0] != 1:
            u = general_euclid_algorithm(k, self.p - 1)
        return u[1]

    def generate_k_variable(self):
        k = 0
        u = [0, 0, 0]
        while u[0] != 1:
            k = int(random.uniform(2, self.p - 1))
            u = general_euclid_algorithm(k, self.p - 1)
        return k

    def count_message_for_receiver(self):
        for_receiver = []

        print(f"{self.name}\n"
              f"I sent to Bob message: {self.message}\n"
              f"Hash function is h(m) = m\n")
        hash_value = count_hash(self.message)

        self.k = self.generate_k_variable()

        reversed_bin_k = from_dec_to_reversed_bin(self.k)
        r = count_result(self.g, reversed_bin_k, self.p)
        u = (hash_value - self.x * r) % (self.p - 1)
        k_inverse = self.get_k_inverse(self.k)
        s = (k_inverse * u) % (self.p - 1)

        for_receiver.append(self.message)
        for_receiver.append(r)
        for_receiver.append(s)

        return for_receiver

    def check_digital_signature(self, message_and_sign):
        my_hash = count_hash(message_and_sign[0])

        left_expr = (self.other_y ** message_and_sign[1]) * (message_and_sign[1] ** message_and_sign[2]) % self.p
        right_expr = count_result(self.g, from_dec_to_reversed_bin(my_hash), self.p)

        if left_expr == right_expr:
            print(f"{self.name}\n"
                  f"I got message with signature: {message_and_sign}\n"
                  "And this is true message from Alice!\n"
                  f"Because equality is provable: {left_expr} == {right_expr}")
        else:
            print("Message is distorted or its not message from Alice...")
            print(left_expr, right_expr)


def main():
    p, q = generate_p_prime()
    g = generate_g(p, q)
    alice = Abonent("ALICE", p, g)
    bob = Abonent("BOB", p, g)

    alice_y = alice.share_public_variables()
    bob.set_other_public_variables(alice_y)

    alice.generate_message()

    for_bob = alice.count_message_for_receiver()
    bob.check_digital_signature(for_bob)


if __name__ == '__main__':
    main()
