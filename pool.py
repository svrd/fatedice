from random import randint
from dicestatistics import add_stat, read_stats, write_stats, get_stats

def rand_d6():
    value = randint(1,6)
    add_stat(6, value)
    return value


def roll_pool(baseValue, skillValue, itemValue, artifactDice):
        base_result = ""
        skill_result = ""
        item_result = ""
        artifact_result = ""
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

        for artifactDie in artifactDice:
            artifact_result += f"A{artifactDie}:{randint(1, artifactDie)} "

        result += base_result + skill_result + item_result + artifact_result
        return result


def push_roll(result):
    pushed_result = ""
    results = result.split(" ")
    print(results)
    for roll in results:
        i = 0
        if roll == '':
            continue
        elif roll[i] == 'B':
            i += 1
            if roll[i] == '1' or roll[i] == '6':
                pushed_result += f"B{roll[i]} "
            else:
                pushed_result += f"B{rand_d6()} "
        elif roll[i] == 'S':
            i += 1
            if roll[i] == '6':
                pushed_result += f"S{roll[i]} "
            else:
                pushed_result += f"S{rand_d6()} "
        elif roll[i] == 'I':
            i += 1
            if roll[i] == '1' or roll[i] == '6':
                pushed_result += f"I{roll[i]} "
            else:
                pushed_result += f"I{rand_d6()} "
        elif roll[i] == 'A':
            i += 1
            die_and_result = roll[i:].split(":")
            artifact_die = int(die_and_result[0])
            int_result = int(die_and_result[1])
            if int_result > 0 and int_result < 6:
                pushed_result += f"A{artifact_die}:{randint(1, artifact_die)} "
            else:
                pushed_result += f"A{artifact_die}:{int_result} "

    return pushed_result


if __name__ == '__main__':
    read_stats()
    result = roll_pool(4, 3, 1, [8, 10, 12])
    pushed_result = push_roll(result)
    print("Result: " + result)
    print("Pushed: " + pushed_result)
    write_stats()
    print(get_stats())