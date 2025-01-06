
import random
from decimal import Decimal, ROUND_HALF_UP
import time
from multiprocessing import Pool

soul_kinds = []
with open('./soul_kinds.txt','r') as f:
    for s in f.readlines():
        soul_kinds.append(s.rstrip('\n'))

prime_attrs = {
    "speed": 12, "ATK_bonus": 0.1, "Crit": 0.1, "Crit_damage": 0.14,
    "ATK": 81, "DEF": 14, "Health": 342, "DEF_bonus": 0.1, "HP_bonus": 0.1,
    "Resist": 0.1, "ACC": 0.1
}

slot_attr = {
    "1": ['ATK'], "2": ['speed', 'ATK_bonus', 'HP_bonus', 'DEF_bonus'],
    "3": ['DEF'], "4": ['ATK_bonus', 'HP_bonus', 'DEF_bonus', 'ACC', 'Resist'],
    "5": ['Health'], "6": ['ATK_bonus', 'HP_bonus', 'DEF_bonus', 'Crit', 'Crit_damage']
}

prime_increase_per_level = {
    "speed": 3, "ATK_bonus": 0.03, "Crit": 0.03, "Crit_damage": 0.05,
    "ATK": 27, "DEF": 6, "Health": 114, "DEF_bonus": 0.03, "HP_bonus": 0.03,
    "Resist": 0.03, "ACC": 0.03
}

non_prime_attrs = {
    "speed": [2.4, 3.0], "ATK_bonus": [2.4, 3.0], "HP_bonus": [2.4, 3.0],
    "DEF_bonus": [2.4, 3.0], "Crit": [2.4, 3.0], "Crit_damage": [3.2, 4.0],
    "ACC": [3.2, 4.0], "Resist": [3.2, 4.0], "ATK": [21.6, 27.0],
    "DEF": [4.0, 5.0], "Health": [91.2, 114.0]
}

exp_level = {
    0: 0, 1: 3500, 2: 8750, 3: 15750, 4: 24500, 5: 35000,
    6: 47250, 7: 61250, 8: 77000, 9: 94500, 10: 113750,
    11: 134750, 12: 157500, 13: 182000, 14: 208250, 15: 236250
}


class Soul:
    def __init__(self):
        self.name = random.choice(soul_kinds)
        self.slot = random.randint(1, 6)
        probabilities_slot2 = [0.1, 0.3, 0.3, 0.3]
        probabilities_slot46 = [0.3, 0.3, 0.3, 0.05, 0.05]
        if self.slot == 2:
            self.prime = random.choices(slot_attr[str(self.slot)], probabilities_slot2)[0]
        elif self.slot in (4, 6):
            self.prime = random.choices(slot_attr[str(self.slot)], probabilities_slot46)[0]
        else:
            self.prime = slot_attr[str(self.slot)][0]

        self.prime_value = prime_attrs[self.prime]
        self.non_prime_count = random.choice([2, 2, 3, 3, 4])
        self.non_prime = []
        self.non_prime_value = []
        for _ in range(self.non_prime_count):
            while True:
                np = random.choice(list(non_prime_attrs.keys()))
                if np not in self.non_prime:
                    break
            value = Decimal(random.uniform(*non_prime_attrs[np])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            self.non_prime.append(np)
            self.non_prime_value.append(value)
        self.for_boost = self.non_prime.copy()
        self.level = 0
        self.exp = 0


def boost(s: Soul, exp):
    last_lv = s.level
    s.exp += exp
    for k, v in exp_level.items():
        if exp > v:
            continue
        elif exp == v:
            s.level = k
        else:
            s.level = k - 1
            break

    s.prime_value = Decimal(prime_attrs[s.prime] + (s.level - 0) * prime_increase_per_level[s.prime]).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP)

    np_boost_cnt = (s.level - last_lv) // 3
    for _ in range(np_boost_cnt):
        to_boost = random.choice(s.for_boost)
        boost_value = Decimal(random.uniform(*non_prime_attrs[to_boost])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        idx = s.non_prime.index(to_boost)
        s.non_prime_value[idx] += boost_value
        s.for_boost.append(to_boost)


def process_soul(_):
    s = Soul()
    boost(s, 236250)
    if s.prime == 'speed' and 'speed' in s.non_prime:
        idx = s.non_prime.index('speed')
        if s.non_prime_value[idx] >= 15.5:
            return s.non_prime_value[idx]
    return None


if __name__ == "__main__":
    cnt = 0
    results = []
    start_time = time.time()
    with Pool(4) as pool:
        results = pool.map(process_soul, range(50000000))
    valid_results = [r for r in results if r is not None]
    cnt = len(valid_results)
    # with open('./soul_data.txt','w') as f:
    #     for res in valid_results:
    #         f.writelines(str(res) + '\n')

    print(f"Count: {cnt}, Average:{sum(valid_results)/cnt:.2f}, Max:{max(valid_results)}, Time: {time.time() - start_time:.2f} seconds")


