import random
import sys
import os.path

def random_list(list_names):
    items = []
    for list_name in list_names:
        filename = list_name + ".txt"
        if os.path.isfile(filename):
            with open(filename, "r") as file:
                list = file.read().splitlines()
                item = random.choice(list)
                items.append(item)
        else:
            print(f"{filename} does not exit")
    print(items)
    return items