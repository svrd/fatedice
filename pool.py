from random import randint
from dicestatistics import add_stat, read_stats, write_stats, get_stats

def rand_d6():
    value = randint(1,6)
    add_stat(6, value)
    return value


def roll_pool(baseValue, skillValue, itemValue, artifactDie):
        base_result = ""
        skill_result = ""
        item_result = ""
        result = ""
        if int(baseValue) > 0:
            for i in range(0, int(baseValue)):
                base_result += f"B{rand_d6()} "

        if int(skillValue) > 0:
            for i in range(0, int(skillValue)):
                skill_result += f"S{rand_d6()} "

        if int(itemValue) > 0:
            for i in range(0, int(itemValue)):
                item_result += f"I{rand_d6()} "

        result += base_result + skill_result + item_result
        return result

def push_roll(result):
    pushed_result = ""
    for i in range(0, len(result)):
        if result[i] == ' ':
            continue
        elif result[i] == 'B':
            i += 1
            if result[i] == '1' or result[i] == '6':
                pushed_result += f"B{result[i]} "
            else:
                pushed_result += f"B{rand_d6()} "
        elif result[i] == 'S':
            i += 1
            if result[i] == '6':
                pushed_result += f"S{result[i]} "
            else:
                pushed_result += f"S{rand_d6()} "
        elif result[i] == 'I':
            i += 1
            if result[i] == '1' or result[i] == '6':
                pushed_result += f"I{result[i]} "
            else:
                pushed_result += f"I{rand_d6()} "

    return pushed_result


if __name__ == '__main__':
    read_stats()
    result = roll_pool(4, 3, 1, 0)
    pushed_result = push_roll(result)
    print("Result: " + result)
    print("Pushed: " + pushed_result)
    write_stats()
    print(get_stats())