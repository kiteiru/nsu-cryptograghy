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
    def __init__(self, P, Q, d, name):
        self.__P = P
        self.__Q = Q
        self.__c = 0
        self.d = d
        self.other_d = 0
        self.other_N = 0
        self.name = name
        self.gcd = 0
        self.__original_message = ""
        self.encoded_message = []


    def set_other_public_variables(self, d, N):
        self.other_d = d
        self.other_N = N

    def share_public_variables(self):
        return self.d, self.__P * self.__Q

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
            binary_exp = from_base10_to_reversed_base2(self.other_d)
            for symbol in self.encoded_message:
                for_receiver.append(count_result(binary_exp, int(symbol), self.other_N))
        elif self.name == "bob":
            while self.gcd != 1:
                common_gcd = count_inverse((self.__P - 1) * (self.__Q - 1), self.d)
                self.__c = common_gcd[1]
                self.gcd = common_gcd[0]
            binary_exp = from_base10_to_reversed_base2(self.__c)
            for symbol in self.encoded_message:
                for_receiver.append(count_result(binary_exp, int(symbol), self.__P * self.__Q))
        return for_receiver

    def set_original_message(self, message):
        self.__original_message = message


def main():
    alice = Abonent(131, 227, 3, "alice")
    bob = Abonent(113, 281, 3, "bob")

    FILEPATH_TO_SEND = "Alice.txt"
    FILEPATH_TO_RECEIVE = "Bob.txt"

    bob_d, bob_N = bob.share_public_variables()
    alice.set_other_public_variables(bob_d, bob_N)

    alice.read_message_from_file(FILEPATH_TO_SEND)
    alice.encode_message()

    bob.encoded_message = alice.count_message_for_receiver()

    bob.set_original_message(bob.count_message_for_receiver())
    bob.write_message_in_file(FILEPATH_TO_RECEIVE)

    print(f"Bob has received message from Alice!\n"
          f"Check out files {FILEPATH_TO_SEND} and {FILEPATH_TO_RECEIVE}")


if __name__ == '__main__':
    main()
