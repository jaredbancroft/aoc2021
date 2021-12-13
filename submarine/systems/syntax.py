from __future__ import annotations
from typing import Generic, TypeVar


T = TypeVar("T")


class SyntaxChecker:
    def __init__(self, filename: str) -> None:
        self.chunks: list[list[str]] = self._load_nav_subsystem_data(filename)
        self.opening_chars: list[str] = ["(", "[", "{", "<"]
        self.closing_chars: list[str] = [")", "]", "}", ">"]
        self.score_lut: dict[str, int] = {
            ")": 3,
            "]": 57,
            "}": 1197,
            ">": 25137,
        }
        self.autocomplete_lut: dict[str, int] = {
            ")": 1,
            "]": 2,
            "}": 3,
            ">": 4,
        }

    def _load_nav_subsystem_data(self, filename) -> list[list[str]]:
        chunks: list[list[str]] = []
        with open(filename, "r", encoding="utf-8") as f:
            while True:
                tmp: str = f.readline().rstrip()
                if not tmp:
                    break
                chunk: list[str] = list(tmp)
                chunks.append(chunk)
        return chunks

    def _process_chunk(self, chunk: list[str]) -> str:
        stack: Stack[str] = Stack()
        autocomplete: list[str] = []
        index: int
        previous_char: str
        for char in chunk:
            if char in self.opening_chars:
                stack.push(char)
            elif char in self.closing_chars:
                index = self.closing_chars.index(char)
                if stack.is_empty():
                    return char
                previous_char = stack.pop()
                if previous_char != self.opening_chars[index]:
                    return char
            else:
                return "Invalid character"
        while not stack.is_empty():
            previous_char = stack.pop()
            index = self.opening_chars.index(previous_char)
            char = self.closing_chars[index]
            autocomplete.append(char)
        return "".join(autocomplete)

    def calculate_incomplete_error_score(self) -> int:
        scores: list[int] = []
        for chunk in self.chunks:
            output: str = self._process_chunk(chunk)
            if len(output) > 1:
                score: int = 0
                for char in output:
                    score = (score * 5) + self._look_up_autocomplete(char)
                scores.append(score)
        middle_index: int = int((len(scores) - 1) / 2)
        scores.sort()
        return scores[middle_index]

    def calculate_syntax_error_score(self) -> int:
        score: int = 0
        for chunk in self.chunks:
            output = self._process_chunk(chunk)
            score += self._look_up_score(output)
        return score

    def _look_up_score(self, key: str) -> int:
        if key in self.score_lut.keys():
            return self.score_lut[key]
        return 0

    def _look_up_autocomplete(self, key: str) -> int:
        return self.autocomplete_lut[key]


class Stack(Generic[T]):
    def __init__(self) -> None:
        self.items: list[T] = []

    def is_empty(self) -> bool:
        return self.items == []

    def push(self, item: T):
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()

    def peek(self) -> T:
        return self.items[len(self.items) - 1]

    def size(self) -> int:
        return len(self.items)
