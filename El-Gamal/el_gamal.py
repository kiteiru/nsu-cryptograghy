import random


def count_result(binary, base, mod):
    res = 1
    a = base
    for position in range(len(binary)):
        if int(binary[position]) != 0:
            res *= (a % mod) * int(binary[position])
        a = (a * a) % mod
    res %= mod
    return res


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


def from_base10_to_reversed_base2(num):
    binary = ''
    while num > 0:
        binary += str(num % 2)
        num //= 2
    return binary


class Abonent:
    def __init__(self, name):
        self.name = name
        self.p = 30803
        self.g = 2
        self.__c = int(random.uniform(2, self.p - 1))
        self.d = count_result(from_base10_to_reversed_base2(self.__c), self.g, self.p)
        self.other_d = 0
        self.r = int(random.uniform(2, self.p - 1))
        self.k = 0
        self.__original_message = ""
        self.encoded_message = []

    def set_other_d_public_variable(self, d):
        self.other_d = d

    def share_d_public_variable(self):
        return self.d

    def set_k_value(self, k):
        self.k = k

    def share_k_value(self):
        return self.k

    def read_message_from_file(self, path):
        with open(path, "r") as f:
            self.__original_message = f.read()

    def write_message_in_file(self, path):
        with open(path, "w") as f:
            for char in [chr(num) for num in self.__original_message]:
                f.write(str(char))

    def encode_message(self):
        self.encoded_message = [ord(symbol) for symbol in self.__original_message]

    def count_message_for_receiver(self):
        for_receiver = []
        if self.name == "alice":
            binary_exp = from_base10_to_reversed_base2(self.r)
            for symbol in self.encoded_message:
                for_receiver.append((symbol * count_result(binary_exp, self.other_d, self.p)) % self.p)
        elif self.name == "bob":
            binary_exp = from_base10_to_reversed_base2(-self.__c + (self.p - 1))
            for symbol in self.encoded_message:
                for_receiver.append((symbol * count_result(binary_exp, self.k, self.p)) % self.p)
        return for_receiver

    def set_original_message(self, message):
        self.__original_message = message


def main():
    alice = Abonent("alice")
    bob = Abonent("bob")

    FILEPATH_TO_SEND = "Alice.txt"
    FILEPATH_TO_RECEIVE = "Bob.txt"

    alice.set_other_d_public_variable(bob.share_d_public_variable())

    alice.read_message_from_file(FILEPATH_TO_SEND)
    alice.encode_message()

    alice.k = count_result(from_base10_to_reversed_base2(alice.r), alice.g, alice.p)

    bob.encoded_message = alice.count_message_for_receiver()
    bob.set_k_value(alice.share_k_value())

    bob.set_original_message(bob.count_message_for_receiver())
    bob.write_message_in_file(FILEPATH_TO_RECEIVE)

    print(f"Bob has received message from Alice!\n"
          f"Check out files {FILEPATH_TO_SEND} and {FILEPATH_TO_RECEIVE}")


if __name__ == '__main__':
    main()
