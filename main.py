import numpy as np
import os

# some change

# hobby: how much desire / how much time
hobbies_factor = {
    "cooking": 5.5 / 1,
    "drawing": 5.0 / 1,
    "music": 6.0 / 1,
    "dating": 3.0 / 1.5,
    "hanging with friends": 5.0 / 1.5,
    "biking/treadmill": 3.0 / 1,
    "3d modeling": 1.0 / 1,
    "vball/rock climbing": 0.5 / 1.7,
    "yoga": 3.0 / 1,
    "photography": 5.0 / 1.4,
    "cleaning": 5.0 / 1,
    "programming": 4.0 / 1,
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
    return old_last.strip()


def spin():
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

    last = ""
    with open("history.txt", "r") as f:
        last = read_last(f)

    hobbies_scaled_prob = {}
    for hobby, factor in hobbies_factor_norm.items():
        if hobby == last:
            # Note that this doesn't make it impossible, because post-normalization
            # there's still a slight chance.
            hobbies_scaled_prob[hobby] = 0
            continue

        hobby_count = hobbies_history[hobby]
        hobby_history_norm = hobby_count / hobbies_history_sum
        hobbies_scaled_prob[hobby] = factor * (1 / hobby_history_norm)
    hobbies_scaled_prob_norm = norm(hobbies_scaled_prob)

    for hobby, prob in hobbies_scaled_prob_norm.items():
        print(f"{hobby} -> {prob}")

    with open("history.txt", "a") as f:
        p = np.array(list(hobbies_scaled_prob_norm.values()))
        v = np.array(list(hobbies_scaled_prob_norm.keys()))
        result = np.random.choice(v, p=p)
        f.write(f"{result}\n")
        f.flush()
        return result


def main():
    result = spin()
    print(f"Wheel says: you should do some {result}.")


if __name__ == "__main__":
    main()

