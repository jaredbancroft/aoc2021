class BingoSubsystem:
    def __init__(self, filepath):
        self.filepath = filepath
        self.cards = []
        self.store_input()

    def set_numbers(self, fh):
        numbers = fh.readline().rstrip()
        self.numbers = numbers.split(",")

    def set_cards(self, fh):
        while True:
            line = fh.readline()
            if not line:
                break
            if line == "\n":
                card = BingoCard()
                self.cards.append(card)
            else:
                card.set_line(line)

    def store_input(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            self.set_numbers(f)
            self.set_cards(f)

    def init_game(self):
        for card in self.cards:
            card.init_card()

    def play(self, outcome):
        self.init_game()
        if outcome == "win":
            return self.play_to_win()
        else:
            return self.play_to_lose()

    def play_to_win(self):
        winner = False
        for number in self.numbers:
            for card in self.cards:
                winner = card.check_lines(number)
                if winner:
                    return int(number) * card.unmarked_total

    def play_to_lose(self):
        winning_cards = []
        for number in self.numbers:
            for card in self.cards:
                if card.check_lines(number):
                    winning_cards.append(card)
            if len(winning_cards) > 0:
                for winner in winning_cards:
                    if len(self.cards) == 1:
                        return int(number) * winner.unmarked_total
                    self.cards.remove(winner)
                winning_cards = []


class BingoCard:
    def __init__(self):
        self.lines = []
        self.unmarked_total = 0

    def set_line(self, line):
        ll = line.split(",")
        self.lines.append(ll[0].split())

    def print(self):
        for line in self.lines:
            print(line)

    def init_card(self):
        for line in self.lines:
            self.unmarked_total += sum([int(x) for x in line])

    def check_winner(self, line):
        if line == ["", "", "", "", ""]:
            return True
        return False

    def check_horizontal(self):
        for line in self.lines:
            if self.check_winner(line):
                return True
        return False

    def check_vertical(self):
        line_length = len(self.lines[0])
        vlines = []
        for i in range(0, line_length):
            vline = []
            for line in self.lines:
                vline.append(line[i])
            vlines.append(vline)
        for vl in vlines:
            if self.check_winner(vl):
                return True
        return False

    def update_card(self, number):
        for line in self.lines:
            if number in line:
                idx = line.index(number)
                line[idx] = ""
                self.unmarked_total -= int(number)

    def check_lines(self, number):
        self.update_card(number)
        horizontal = self.check_horizontal()
        vertical = self.check_vertical()
        return horizontal or vertical
