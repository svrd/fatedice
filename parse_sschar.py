from sys import argv

class Character:
    name = ""
    skills = dict()

    def _parse_skills(self, line):
        skills = line.split(",")
        for skill in skills:
            skill = skill.strip()
            [name, value] = skill.split(" ")
            self.skills[name] = int(value)


    def parse(self, lines):
        for line in range(0, len(lines)):
            lines[line] = lines[line].rstrip()
        line = 0
        self.name = lines[line].rstrip()
        line = 1

        skills_start_line = -1
        talents_start_line = -1
        equipment_start_line = -1

        while True and line < len(lines):
            if lines[line].startswith("FÄRDIGHETER:"):
                start_line = line
                end_line = line + 1
                while end_line < len(lines) and ":" not in lines[end_line]:
                    end_line += 1
                complete_string = ' '.join(lines[start_line:end_line])
                pos = complete_string.find(":") + 1
                complete_string = complete_string[pos:]
                self._parse_skills(complete_string)
                line = end_line

            line += 1
        
    def print(self):
        print(self.name)
        first = True
        skills_line = "FÄRDIGHETER: "
        for skill, value in self.skills.items():
            append = ""
            if not first:
                append = ", "
            skills_line += f"{append}{skill} {value}"
            first = False
        print(skills_line)

if __name__ == '__main__':
    with open(argv[1], 'r') as f:
        lines = f.readlines()
        character = Character()
        character.parse(lines)
        character.print()