def detail_check(result):
    answer = ""
    if result <= 4:
        answer = "Ilska"
    elif result == 5:
        answer = "Sorg"
    elif result == 6:
        answer = "Rädsla"
    elif result == 7:
        answer = "Missgynna tråd"
    elif result == 8:
        answer = "Missgynna rollperson"
    elif result == 9:
        answer = "Fokus spelledarperson"
    elif result == 10:
        answer = "Gynna spelledarperson"
    elif result == 11:
        answer = "Fokus rollperson"                        
    elif result == 12:
        answer = "Missgynna spelledarperson"
    elif result == 13:
        answer = "Fokus tråd"
    elif result == 14:
        answer = "Gynna rollperson"
    elif result == 15:
        answer = "Gynna tråd"
    elif result == 16:
        answer = "Mod"
    elif result == 17:
        answer = "Glädje"
    else:
        answer = "Lugn"
    return answer