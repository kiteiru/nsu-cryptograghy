import random
import string


def generate_key(LENGTH, ALPHABET_SIZE):
    key = []
    for i in range(LENGTH):
        key.append(int(random.uniform(0, ALPHABET_SIZE)))
    return key


class Abonent:
    def __init__(self, name):
        self.name = name
        self.length = None
        self.alphabet_size = None
        self.key = None
        self.message = None
        self.encoded = None
        self.decoded = None

    def set_public_variables(self, LENGTH, ALPHABET_SIZE, key):
        self.length = LENGTH
        self.alphabet_size = ALPHABET_SIZE
        self.key = key

    def form_message(self):
        self.message = [random.choice(string.ascii_lowercase) for i in range(self.length)]

    def encode_message(self):
        head_ascii = ord('a')
        self.encoded = [ord(i) - head_ascii for i in self.message]

    def decode_message(self, decryption):
        head_ascii = ord('a')
        self.decoded = [chr(i + head_ascii) for i in decryption]

    def encrypt_message(self):
        encryption = []
        for i in range(self.length):
            encryption.append((self.encoded[i] + self.key[i]) % self.alphabet_size)
        return encryption

    def decrypt_message(self, encryption):
        decryption = []
        for i in range(self.length):
            decryption.append((encryption[i] - self.key[i]) % self.alphabet_size)
        return decryption

    def print_information(self):
        if self.name == "ALICE":
            print(f"{self.name}:\n"
                  f"I formed message: {''.join(i for i in self.message)}\n")

        elif self.name == "BOB":
            print(f"{self.name}:\n"
                  f"I got message: {''.join(i for i in self.decoded)}\n")


def main():
    LENGTH = int(random.uniform(2 ** 2, 2 ** 4))
    ALPHABET_SIZE = 26
    key = generate_key(LENGTH, ALPHABET_SIZE)

    alice = Abonent("ALICE")
    bob = Abonent("BOB")

    alice.set_public_variables(LENGTH, ALPHABET_SIZE, key)
    bob.set_public_variables(LENGTH, ALPHABET_SIZE, key)

    alice.form_message()
    alice.encode_message()
    encryption = alice.encrypt_message()

    decryption = bob.decrypt_message(encryption)
    bob.decode_message(decryption)

    alice.print_information()
    bob.print_information()


if __name__ == '__main__':
    main()
