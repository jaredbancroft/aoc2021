from collections import defaultdict
from itertools import pairwise


class Polymer:
    def __init__(self, filename: str) -> None:
        self.polymer_template: str = ""
        self.insertion_rules: dict[str, str] = {}
        self.polymer_template, self.insertion_rules = self._read_input(
            filename
        )
        self.pair_count = defaultdict(
            self._first_argument_must_be_callable_or_None
        )

    def _first_argument_must_be_callable_or_None(self) -> int:
        return 0

    def polymerize(self, steps: int) -> int:
        last: str = self.polymer_template[-1]

        for pairs in pairwise(self.polymer_template):
            pair = f"{pairs[0]}{pairs[1]}"
            if pair not in self.pair_count:
                self.pair_count[pair] = 1
            else:
                self.pair_count[pair] += 1

        for i in range(0, steps):
            pair_count = defaultdict(
                self._first_argument_must_be_callable_or_None
            )

            for pair in self.pair_count:
                if pair in self.insertion_rules:
                    new_pairs: list[str] = [
                        f"{pair[0]}{self.insertion_rules[pair]}",
                        f"{self.insertion_rules[pair]}{pair[1]}",
                    ]
                    for new_pair in new_pairs:
                        pair_count[new_pair] += self.pair_count[pair]
                else:
                    pair_count[pair] += self.pair_count[pair]
            self.pair_count = pair_count

        counts = defaultdict(self._first_argument_must_be_callable_or_None)
        for pair in self.pair_count:
            counts[pair[0]] += self.pair_count[pair]
        counts[last] += 1

        return max(counts.values()) - min(counts.values())

    def _read_input(self, filename: str) -> tuple[str, dict[str, str]]:
        with open(filename, "r", encoding="utf-8") as f:
            tmp: list[str] = f.readlines()
        polymer_template: str = tmp[0].rstrip()
        insertion_rules: dict[str, str] = {}
        for t in tmp[2:]:
            rule: list[str] = t.rstrip().split(" -> ")
            insertion_rules[rule[0]] = rule[1]
        return polymer_template, insertion_rules
