from submarine.systems.syntax import SyntaxChecker


def solution(day):
    s = SyntaxChecker(f"inputs/{day}.txt")
    return s.calculate_incomplete_error_score()
