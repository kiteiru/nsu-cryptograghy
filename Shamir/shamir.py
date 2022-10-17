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
    def __init__(self):
        self.gcd = 0
        self.__c = 0
        self.__d = 0
        self.p = 30803
        self.__original_message = ""
        self.encoded_message = []

    def set_private_variables(self):
        while self.gcd != 1:
            self.__c = int(random.uniform(2 ** 2, 2 ** 6))
            inverse = count_inverse(self.p - 1, self.__c)
            self.gcd = inverse[0]
            self.__d = inverse[1]

    def read_message_from_file(self, path):
        with open(path, "r") as f:
            self.__original_message = f.read()

    def write_message_in_file(self, path):
        with open(path, "w") as f:
            for char in [chr(num) for num in self.__original_message]:
                f.write(str(char))

    def encode_message(self):
        self.encoded_message = [ord(symbol) for symbol in self.__original_message]

    def count_message_for_receiver(self, symbol):
        for_receiver = []
        binary_exp = 0
        if symbol == "c":
            binary_exp = from_base10_to_reversed_base2(self.__c)
        elif symbol == "d":
            binary_exp = from_base10_to_reversed_base2(self.__d)
        for symbol in self.encoded_message:
            for_receiver.append(count_result(binary_exp, int(symbol), self.p))
        return for_receiver

    def set_original_message(self, message):
        self.__original_message = message


def main():
    alice = Abonent()
    bob = Abonent()

    FILEPATH_TO_SEND = "Alice.txt"
    FILEPATH_TO_RECEIVE = "Bob.txt"

    alice.set_private_variables()
    bob.set_private_variables()

    alice.read_message_from_file(FILEPATH_TO_SEND)
    alice.encode_message()

    bob.encoded_message = alice.count_message_for_receiver("c")

    alice.encoded_message = bob.count_message_for_receiver("c")

    bob.encoded_message = alice.count_message_for_receiver("d")

    bob.set_original_message(bob.count_message_for_receiver("d"))
    bob.write_message_in_file(FILEPATH_TO_RECEIVE)

    print(f"Bob has received message from Alice!\n"
          f"Check out files {FILEPATH_TO_SEND} and {FILEPATH_TO_RECEIVE}")


if __name__ == '__main__':
    main()
