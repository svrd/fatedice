from random import randint

d6_stats = [0, 0, 0, 0, 0, 0]

def add_stat(die, value):
    d6_stats[value-1] += 1

def read_stats():
    try:
        with open("t6_stat.txt", "r+") as f:
            line = f.readline()
            start_pos = 0
            for die in range(6):
                line = line[start_pos:]
                end_pos = line.find(";")
                number_string = line[:end_pos]
                d6_stats[die] = int(number_string)
                start_pos = end_pos + 1
    except IOError:
        print("No T6 stat file")
    print(f"d6_stat.txt: {d6_stats}")


def write_stats():
    line = ""
    for i in range(6):
        line += f"{d6_stats[i]};"
    with open("t6_stat.txt", "w+") as f:
        f.write(line)


def get_stats():
    the_sum = sum(d6_stats)
    result = "<table border=1><tr>"
    print(the_sum)
    print(d6_stats)
    for i in range(6):
        if the_sum == 0:
            percent = 0.0
        else:
            percent = (d6_stats[i] / the_sum) * 100
        result += f"<td>{i+1}: {d6_stats[i]} ({percent:.2f}%)</td>"
    result += "</tr></table>"
    return result


if __name__ == '__main__':
    read_stats()
    for i in range(1000):
        r = randint(1,6)
        add_stat(6, r)
    print(get_stats())
    write_stats()