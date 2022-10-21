import random

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

def count_result(base, bin_exp, mod):
    res = 1
    a = base
    for position in range(len(bin_exp)):
        if int(bin_exp[position]) != 0:
            res *= (a % mod) * int(bin_exp[position])
        a = (a * a) % mod
    res %= mod
    return res

def from_dec_to_reversed_bin(num):
    binary = ''
    while num > 0:
        binary += str(num % 2)
        num //= 2
    return binary

class Abonent:
    def __init__(self, p, g):
        self.p = p
        self.g = g
        self.x = None
        self.y = None
        self.bit = None
        self.other_bit = None
        self.k = None
        self.r = None

    def generate_bit(self):
        self.bit = int(random.uniform(0, 2))

    def generate_y(self):
        self.x = int(random.uniform(2, self.p))
        self.y = count_result(self.g, from_dec_to_reversed_bin(self.x), self.p)
        return self.y

    def set_y(self, y):
        self.y = y

    def generate_r(self):
        self.k = int(random.uniform(2, self.p))
        self.r = (count_result(self.y, from_dec_to_reversed_bin(self.bit), self.p) * count_result(self.g, from_dec_to_reversed_bin(self.k), self.p)) % self.p
        return self.r

    def set_r(self, r):
        self.r = r

    def share_bit(self):
        return self.bit

    def set_other_bit(self, bit):
        self.other_bit = bit
        self.bit = bit ^ 1

    def share_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def check(self, sides):
        left_expr = self.r
        right_expr = (count_result(self.y, from_dec_to_reversed_bin(self.other_bit), self.p) * (count_result(self.g, from_dec_to_reversed_bin(self.k), self.p))) % self.p

        if left_expr == right_expr:
            key = int(random.uniform(0, 2))
            print(f"Coin is flipped, we got {sides[key]}!")
            print(f"Alice has chosen: {sides[self.bit]}")
            print(f"Bob has chosen: {sides[self.other_bit]}\n")
            if sides[key] == sides[self.bit]:
                print("Alice won!")
            else:
                print("Bob won!")
        else:
            print("There is channel interruption or cheating of other abonent...")


def main():
    sides = {0: "HEAD", 1: "TAIL"}
    p, q = generate_p_prime()
    g = generate_g(p, q)

    alice = Abonent(p, g)
    bob = Abonent(p, g)

    y = alice.generate_y()

    bob.set_y(y)
    bob.generate_bit()
    r = bob.generate_r()

    alice.set_r(r)
    bob_bit = bob.share_bit()

    alice.set_other_bit(bob_bit)
    alice_bit = alice.share_bit()

    k = bob.share_k()
    bob.set_other_bit(alice_bit)

    alice.set_k(k)
    alice.check(sides)


if __name__ == "__main__":
    main()
