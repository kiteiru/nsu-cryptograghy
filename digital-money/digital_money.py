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


def count_result(base, bin_exp, mod):
    res = 1
    a = base
    for position in range(len(bin_exp)):
        if int(bin_exp[position]) != 0:
            res *= (a % mod) * int(bin_exp[position])
        a = (a * a) % mod
    res %= mod
    return res


class Bank:
    def __init__(self, name):
        self.name = name
        self.banknotes = []
        self.__P = None
        self.__Q = None
        self.__phi = None
        self.__c = None
        self.N = None
        self.d = None
        self.customer_n = None
        self.customer_account = None
        self.good = None
        self.store_account = None
        self.customer_banknote = None
        self.message = None

    def generate_variables(self):
        self.__P = generate_big_prime()
        self.__Q = generate_big_prime()
        c = 0
        u = [0, 0, 0]
        while u[0] != 1:
            self.__phi = (self.__P - 1) * (self.__Q - 1)
            c = int(random.uniform(2 ** 8, self.__phi))
            u = general_euclid_algorithm(c, self.__phi)
        self.__c = c
        self.d = u[1]
        self.N = self.__P * self.__Q
        return self.N, self.d

    def set_variables_from_customer(self, public_n, customer_account, good):
        self.customer_n = public_n
        self.customer_account = customer_account
        self.good = good

    def count_public_s(self):
        reversed_bin_c = from_dec_to_reversed_bin(self.__c)
        public_s = count_result(self.customer_n, reversed_bin_c, self.N)
        return public_s

    def set_variables_from_store(self, banknote, store_account):
        self.customer_banknote = banknote
        self.store_account = store_account

    def check_customer_banknote(self, banknote, store_account):
        print(f"{self.name}:\n"
              f"I am checking customer banknote: <n, sign>")
        self.store_account = store_account
        reversed_bin_d = from_dec_to_reversed_bin(self.d)
        if banknote[0] not in self.banknotes and count_result(banknote[1], reversed_bin_d, self.N) == banknote[0]:
            self.customer_account -= self.good[1]
            self.store_account += self.good[1]
            self.message = True
            print(f"Banknote successfully checked!\n")
        else:
            self.message = False
            print(f"Banknote failed validation!\n")

    def share_variables_after_purchase(self):
        return self.message, self.customer_account, self.store_account


class Store:
    def __init__(self, name, money):
        self.name = name
        self.account = money
        self.goods = {"sweather": 32,
                      "skirt": 12,
                      "socks": 3,
                      "t-shirt": 5,
                      "jeans": 25}
        self.customer_banknote = None
        self.chosen_good = None

    def share_goods(self):
        print(f"{self.name}:\n"
              f"I sale such goods: {self.goods}\n")
        return self.goods

    def set_chosen_good(self, chosen_good):
        self.chosen_good = chosen_good

    def set_customer_banknote(self, banknote):
        self.customer_banknote = banknote

    def share_variables_to_bank(self):
        return self.customer_banknote, self.account

    def get_message_from_bank(self, message):
        if message:
            self.goods.pop(self.chosen_good[0])
            print(f"{self.name}:\n"
                  f"I sell {self.chosen_good[0]} to customer\n")
            return True
        else:
            print(f"{self.name}:\n"
                  f"I havent sell {self.chosen_good[0]} to customer\n"
                  f"Its banknote failed validation!")
            return False

    def set_money_account(self, account):
        print(f"{self.name}:\n"
              f"Before purchase i had {self.account}$ on my account")
        self.account = account
        print(f"After purchase i have {self.account}$ on my account\n")


class Customer:
    def __init__(self, name, money):
        self.name = name
        self.account = money
        self.good = None
        self.__n = None
        self.__k = None
        self.__k_inverse = None
        self.N = None
        self.d = None
        self.public_n = None
        self.sign = None
        self.banknote = None
        self.purchase = None

    def choose_good(self, goods):
        self.good = random.choice(list(goods.items()))
        print(f"{self.name}:\n"
              f"I choose {self.good[0]} for {self.good[1]}$\n")
        return self.good

    def set_public_variables(self, N, d):
        self.N = N
        self.d = d

    def generate_private_variables(self):
        self.__n = int(random.uniform(2, self.N))
        k = 0
        u = [0, 0, 0]
        while u[0] != 1:
            k = int(random.uniform(2 ** 8, self.N))
            u = general_euclid_algorithm(k, self.N)
        self.__k = k
        self.__k_inverse = u[1]

    def count_public_n(self):
        reversed_bin_d = from_dec_to_reversed_bin(self.d)
        self.public_n = (self.__n * count_result(self.__k, reversed_bin_d, self.N)) % self.N

    def share_variables_to_bank(self):
        return self.public_n, self.account, self.good

    def count_sign(self, public_s):
        self.sign = (public_s * self.__k_inverse) % self.N

    def form_banknote(self):
        self.banknote = [self.__n, self.sign]
        return self.banknote

    def get_message_from_store(self, is_successful_purchase):
        if is_successful_purchase:
            self.purchase = self.good
            print(f"{self.name}:\n"
                  f"I got {self.good[0]} from store!\n")
        else:
            print(f"{self.name}:\n"
                  f"I havent got {self.good[0]} from store!\n")

    def set_money_account(self, account):
        print(f"{self.name}:\n"
              f"Before purchase i had {self.account}$ on my account")
        self.account = account
        print(f"After purchase i have {self.account}$ on my account\n")


def main():
    STORE_MONEY = int(random.uniform(2 ** 12, 2 ** 20))
    CUSTOMER_MONEY = int(random.uniform(2 ** 6, 2 ** 10))

    bank = Bank("BANK")
    store = Store("STORE", STORE_MONEY)
    customer = Customer("CUSTOMER", CUSTOMER_MONEY)

    goods = store.share_goods()

    chosen_good = customer.choose_good(goods)

    store.set_chosen_good(chosen_good)

    N, d = bank.generate_variables()

    customer.set_public_variables(N, d)
    customer.generate_private_variables()
    customer.count_public_n()
    public_n, customer_account, good = customer.share_variables_to_bank()

    bank.set_variables_from_customer(public_n, customer_account, good)
    public_s = bank.count_public_s()

    customer.count_sign(public_s)
    banknote = customer.form_banknote()

    store.set_customer_banknote(banknote)
    banknote, store_account = store.share_variables_to_bank()

    bank.check_customer_banknote(banknote, store_account)
    message, customer_account, store_account = bank.share_variables_after_purchase()

    is_successful_purchase = store.get_message_from_bank(message)

    customer.get_message_from_store(is_successful_purchase)

    store.set_money_account(store_account)

    customer.set_money_account(customer_account)


if __name__ == "__main__":
    main()
