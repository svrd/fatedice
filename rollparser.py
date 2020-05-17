from sys import argv
import random

def parse_roll(roll):
    pos = 0
    total_result = 0
    result_string = ""
    number = 0
    no_of_sides = 0
    no_of_dice = 0
    is_addition = True
    while pos < len(roll):
        if roll[pos].isdigit():
            number = 0
            begin = pos
            while pos < len(roll) and roll[pos].isdigit():
                pos += 1
            end = pos
            number = int(roll[begin:end])
            print(f"Number: {number}")

        if pos < len(roll) and roll[pos] == "T" and number != 0:
            no_of_dice = number
            print(f"Dice: {no_of_dice}")
            number = 0
        
        if no_of_dice > 0 and number > 0:
                no_of_sides = number
                print(f"Sides: {no_of_sides}")
                number = 0
        elif number > 0:
            modifier = number
            number = 0
            print(f"Modifier: {modifier}")
            if is_addition is True:
                total_result += modifier
                if result_string != "":
                    result_string += f"+"
            else:
                total_result -= modifier
                result_string += f"-"
            result_string += f"{modifier}"


        
        # Roll Dice
        if no_of_dice > 0 and no_of_sides > 0:
            while no_of_dice > 0:
                result = random.randint(1,(int(no_of_sides)))
                if is_addition is True:
                    total_result += result
                    if result_string != "":
                        result_string += f"+"
                else:
                    total_result -= result
                    result_string += f"-"
                result_string += f"{result}"
                no_of_dice -= 1
            no_of_sides = 0

        if pos < len(roll) and roll[pos] == "+":
            is_addition = True
        if pos < len(roll) and roll[pos] == "-":
            is_addition = False               

        pos += 1
    
    result_string += f"={total_result}"
    return result_string


if __name__ == '__main__':
    print(parse_roll(argv[1]))