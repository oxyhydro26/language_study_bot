import random
import re

FILE_LINE_END = 7541

class WordDB:
    def __init__(self, db_file_path: str):
        self.db: list[tuple[str, str]] = []
        db_file = open(db_file_path, "r")
        for line in db_file.readlines():
            line = re.sub("\n", "", line)
            self.db.append(tuple(line.split("::")))

    def get_one_random(self):
        index = random.randint(0, FILE_LINE_END)
        return self.db[index]


if __name__ == "__main__":
    db = WordDB("word_db.txt")
    db.get_one_random()
