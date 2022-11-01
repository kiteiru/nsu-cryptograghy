import random


def is_prime(num):
    if num % 2 == 0:
        return False
    else:
        for div in range(3, int(num ** 0.5) + 1, 2):
            if num % div == 0:
                return False
    return True


def generate_common_big_prime():
    p = 2
    while not is_prime(p):
        p = int(random.uniform(2 ** 8, 2 ** 16))
    return p


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


def from_dec_to_reversed_bin(num):
    binary = ''
    while num > 0:
        binary += str(num % 2)
        num //= 2
    return binary


class Abonent:
    def __init__(self, p, name):
        self.p = p
        self.name = name
        self.common_alpha = format(0, '02b')
        self.common_beta = format(1, '02b')
        self.common_gamma = format(2, 'b')
        self.my_alpha = 0
        self.my_beta = 0
        self.my_gamma = 0
        self.c = 0
        self.d = 0

    def generate_my_cards(self):
        self.my_alpha = int(format(int(random.uniform(2, self.p / 4)), 'b') + self.common_alpha, base=2)
        self.my_beta = int(format(int(random.uniform(2, self.p / 4)), 'b') + self.common_beta, base=2)
        self.my_gamma = int(format(int(random.uniform(2, self.p / 4)), 'b') + self.common_gamma, base=2)
        return self.my_alpha, self.my_beta, self.my_gamma

    def set_my_cards(self, alpha, beta, gamma):
        self.my_alpha = alpha
        self.my_beta = beta
        self.my_gamma = gamma

    def generate_private_variables(self):
        c = 0
        u = [0, 0, 0]
        while u[0] != 1:
            c = int(random.uniform(2 ** 8, self.p - 1))
            u = general_euclid_algorithm(c, self.p - 1)
        self.c = c
        self.d = u[1]

    def count_u_card_list_for_sending(self):
        reversed_bin_c = from_dec_to_reversed_bin(self.c)
        u_list = []
        u_list.append(count_result(self.my_alpha, reversed_bin_c, self.p))
        u_list.append(count_result(self.my_beta, reversed_bin_c, self.p))
        u_list.append(count_result(self.my_gamma, reversed_bin_c, self.p))
        u_list = random.sample(u_list, len(u_list))
        return u_list

    def count_v_card_list_for_sending(self, u_list):
        reversed_bin_c = from_dec_to_reversed_bin(self.c)
        v_list = []
        v_list.append(count_result(u_list[0], reversed_bin_c, self.p))
        v_list.append(count_result(u_list[1], reversed_bin_c, self.p))
        v_list = random.sample(v_list, len(v_list))
        return v_list

    def choose_one_card(self, u_list):
        send_idx = int(random.uniform(0, 3))
        v_list = self.count_v_card_list_for_sending([u_list[i] for i in range(len(u_list)) if i != send_idx])
        v_list = random.sample(v_list, len(v_list))
        return u_list[send_idx], v_list

    def get_my_card_back(self, card):
        reversed_bin_d = from_dec_to_reversed_bin(self.d)
        my_card = count_result(card, reversed_bin_d, self.p)
        my_cards = {"alpha": self.my_alpha,
                    "beta": self.my_beta,
                    "gamma": self.my_gamma}
        print(f"{self.name} has such cards:\n"
              f"{my_cards}\n"
              f"=============================")
        for elem in my_cards:
            if my_card == my_cards[elem]:
                print(f"{self.name} received card {my_card} which is [{elem}]\n")
                break

    def count_w_card(self, cards):
        reversed_bin_d = from_dec_to_reversed_bin(self.d)
        send_idx = int(random.uniform(0, 2))
        w = count_result(cards[send_idx], reversed_bin_d, self.p)
        return w


def main():
    p = generate_common_big_prime()

    alice = Abonent(p, "Alice")
    bob = Abonent(p, "Bob")

    alpha, beta, gamma = alice.generate_my_cards()
    bob.set_my_cards(alpha, beta, gamma)

    alice.generate_private_variables()
    bob.generate_private_variables()

    u_list = alice.count_u_card_list_for_sending()
    u_card, v_list = bob.choose_one_card(u_list)
    w_card = alice.count_w_card(v_list)

    alice.get_my_card_back(u_card)
    bob.get_my_card_back(w_card)


if __name__ == "__main__":
    main()
