import numpy as np
import os

hobbies_factor = {
    "cooking": 5.5,
    "drawing": 5.0,
    "music": 6.0,
    "dating": 2.0,
    "hanging with friends": 5.0,
    "biking/treadmill": 3.0,
    "3d modeling": 2.0,
    "vball/rock climbing": 0.5,
    "yoga": 3.0,
    "photography": 5.0,
    "cleaning": 5.0,
    "programming": 4.0,
}


def norm(l):
    r = {}
    s = sum(l.values())
    for key, value in l.items():
        r[key] = value / s
    return r


def read_last(f):
    old_last = None
    last = f.readline()
    old_last = last
    while last:
        old_last = last
        last = f.readline()
    return old_last


def main():
    hobbies_factor_norm = norm(hobbies_factor)

    hobbies_history = {}
    try:
        with open("history.txt", "r") as f:
            for line in f:
                if line in hobbies_history:
                    hobbies_history[line] += 1
                else:
                    hobbies_history[line] = 1
    except:
        print("No history file found. Creating...")
        with open("history.txt", "w") as f:
            f.write("\n")
    for hobby in hobbies_factor.keys():
        if hobby not in hobbies_history:
            hobbies_history[hobby] = 1
    hobbies_history_sum = sum(hobbies_history.values())

    hobbies_scaled_prob = {}
    for hobby, factor in hobbies_factor_norm.items():
        hobby_count = hobbies_history[hobby]
        hobby_history_norm = hobby_count / hobbies_history_sum
        hobbies_scaled_prob[hobby] = factor * (1 / hobby_history_norm)
    hobbies_scaled_prob_norm = norm(hobbies_scaled_prob)

    last = ""
    with open("history.txt", "r") as f:
        last = read_last(f)

    with open("history.txt", "a") as f:
        p = np.array(list(hobbies_scaled_prob_norm.values()))
        v = np.array(list(hobbies_scaled_prob_norm.keys()))
        result = np.random.choice(v, p=p)
        while result == last:
            result = np.random.choice(v, p=p)
        print(f"Wheel says: you should do some {result}.")
        f.write(f"{result}\n")


if __name__ == "__main__":
    main()

