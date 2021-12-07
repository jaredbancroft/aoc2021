from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class FastModel:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.fish_counts = {
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0,
            "8": 0,
        }
        self.init()

    def init(self) -> None:
        with open(self.filepath, "r", encoding="utf-8") as f:
            line = f.read()
        timers = line.split(",")
        for timer in timers:
            self.fish_counts[timer] += 1

    def run(self, days: int) -> int:
        for _ in range(0, days):
            new_fish = self.fish_counts["0"]
            self.cycle_fish(new_fish)
        return sum(self.fish_counts.values())

    def cycle_fish(self, new_fish: int) -> None:
        for i in range(0, len(self.fish_counts) - 1):
            self.fish_counts[str(i)] = self.fish_counts[str(i + 1)]
        self.fish_counts["8"] = new_fish
        self.fish_counts["6"] += new_fish


class BreedingModel:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.init()

    def init(self) -> None:
        with open(self.filepath, "r", encoding="utf-8") as f:
            line = f.read()
        timers = line.split(",")
        self.date = DateChange()
        for timer in timers:
            self.date.attach(LanternFish(int(timer)))

    def run(self, days: int) -> int:
        for _ in range(1, days + 1):
            self.date.increment_day()
        return len(self.date._observers)


class Observer(ABC):
    @abstractmethod
    def update(self, subject: Subject) -> bool:
        pass


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class DateChange(Subject):
    _state: int = 0
    _observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        new_fish: int = 0
        for observer in self._observers:
            if observer.update(self):
                new_fish += 1
        if new_fish > 0:
            for _ in range(0, new_fish):
                self.attach(LanternFish(8))

    def increment_day(self) -> None:
        self._state += 1
        self.notify()


class LanternFish(Observer):
    def __init__(self, timer: int) -> None:
        self.timer = timer

    def update(self, subject: Subject) -> bool:
        if self.timer != 0:
            self.timer -= 1
            return False
        else:
            self.timer = 6
            return True
