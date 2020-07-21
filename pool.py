from random import randint

def roll_pool(baseValue, skillValue, itemValue, artefactDie):
        base_result = ""
        skill_result = ""
        item_result = ""
        result = ""
        if int(baseValue) > 0:
            for i in range(0, int(baseValue)):
                base_result += f"B{randint(1,(int(6)))} "

        if int(skillValue) > 0:
            for i in range(0, int(skillValue)):
                skill_result += f"S{randint(1,(int(6)))} "

        if int(itemValue) > 0:
            for i in range(0, int(itemValue)):
                item_result += f"I{randint(1,(int(6)))} "

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
                pushed_result += f"B{randint(1,(int(6)))} "
        elif result[i] == 'S':
            i += 1
            if result[i] == '6':
                pushed_result += f"S{result[i]} "
            else:
                pushed_result += f"S{randint(1,(int(6)))} "
        elif result[i] == 'I':
            i += 1
            if result[i] == '1' or result[i] == '6':
                pushed_result += f"I{result[i]} "
            else:
                pushed_result += f"I{randint(1,(int(6)))} "

    return pushed_result


if __name__ == '__main__':
    result = roll_pool(4, 3, 1, 0)
    pushed_result = push_roll(result)
    print("Result: " + result)
    print("Pushed: " + pushed_result)