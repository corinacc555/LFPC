import random
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class ParseTrace:
    steps: List[str]

    def add(self, message: str) -> None:
        self.steps.append(message)


class RegexNode:
    def generate(self, limit: int, rng: random.Random, trace: Optional[ParseTrace] = None) -> str:
        raise NotImplementedError


@dataclass
class Literal(RegexNode):
    value: str

    def generate(self, limit: int, rng: random.Random, trace: Optional[ParseTrace] = None) -> str:
        if trace is not None:
            trace.add(f"Emit literal '{self.value}'")
        return self.value


@dataclass
class Concat(RegexNode):
    parts: List[RegexNode]

    def generate(self, limit: int, rng: random.Random, trace: Optional[ParseTrace] = None) -> str:
        if trace is not None:
            trace.add(f"Concatenation with {len(self.parts)} part(s)")
        return "".join(part.generate(limit, rng, trace) for part in self.parts)


@dataclass
class Alternation(RegexNode):
    options: List[RegexNode]

    def generate(self, limit: int, rng: random.Random, trace: Optional[ParseTrace] = None) -> str:
        idx = rng.randrange(len(self.options))
        if trace is not None:
            trace.add(f"Alternation: choose option {idx + 1} of {len(self.options)}")
        return self.options[idx].generate(limit, rng, trace)


@dataclass
class Repeat(RegexNode):
    node: RegexNode
    min_times: int
    max_times: int

    def generate(self, limit: int, rng: random.Random, trace: Optional[ParseTrace] = None) -> str:
        upper = min(self.max_times, limit)
        if upper < self.min_times:
            upper = self.min_times

        count = rng.randint(self.min_times, upper)
        if trace is not None:
            trace.add(f"Repeat {count} time(s) in range [{self.min_times}, {upper}]")

        return "".join(self.node.generate(limit, rng, trace) for _ in range(count))


class RegexParser:
    """
    Supports: (), |, concatenation, *, +, ?, {n}
    Input grammar is dynamic; there is no hardcoded regex structure.
    """

    def __init__(self, expression: str):
        self.expression = expression
        self.pos = 0

    def parse(self) -> RegexNode:
        node = self._parse_expression()
        if self.pos != len(self.expression):
            raise ValueError(f"Unexpected symbol at index {self.pos}: '{self.expression[self.pos]}'")
        return node

    def _peek(self) -> Optional[str]:
        self._skip_whitespace()
        if self.pos >= len(self.expression):
            return None
        return self.expression[self.pos]

    def _skip_whitespace(self) -> None:
        while self.pos < len(self.expression) and self.expression[self.pos].isspace():
            self.pos += 1

    def _consume(self, expected: Optional[str] = None) -> str:
        ch = self._peek()
        if ch is None:
            raise ValueError("Unexpected end of expression")

        if expected is not None and ch != expected:
            raise ValueError(f"Expected '{expected}' but found '{ch}' at index {self.pos}")

        self.pos += 1
        return ch

    def _parse_expression(self) -> RegexNode:
        terms = [self._parse_term()]
        while self._peek() == "|":
            self._consume("|")
            terms.append(self._parse_term())
        if len(terms) == 1:
            return terms[0]
        return Alternation(terms)

    def _parse_term(self) -> RegexNode:
        factors: List[RegexNode] = []
        while True:
            ch = self._peek()
            if ch is None or ch in ")|":
                break
            factors.append(self._parse_factor())

        if not factors:
            return Literal("")
        if len(factors) == 1:
            return factors[0]
        return Concat(factors)

    def _parse_factor(self) -> RegexNode:
        base = self._parse_primary()

        while True:
            ch = self._peek()
            if ch == "*":
                self._consume("*")
                base = Repeat(base, 0, 5)
            elif ch == "+":
                self._consume("+")
                base = Repeat(base, 1, 5)
            elif ch == "?":
                self._consume("?")
                base = Repeat(base, 0, 1)
            elif ch == "{":
                self._consume("{")
                number = self._parse_number()
                self._consume("}")
                base = Repeat(base, number, number)
            else:
                break

        return base

    def _parse_primary(self) -> RegexNode:
        ch = self._peek()

        if ch == "(":
            self._consume("(")
            inner = self._parse_expression()
            self._consume(")")
            return inner

        if ch is None:
            raise ValueError("Unexpected end of expression")

        if ch in "|)*+?{}":
            raise ValueError(f"Unexpected meta character '{ch}' at index {self.pos}")

        literal = self._consume()
        return Literal(literal)

    def _parse_number(self) -> int:
        start = self.pos
        while self._peek() is not None and self._peek().isdigit():
            self._consume()

        if start == self.pos:
            raise ValueError(f"Expected number at index {self.pos}")

        return int(self.expression[start:self.pos])


def normalize_lab_regex(raw_expression: str) -> str:
    """
    Converts lab notation into parser notation.
    - removes spaces used for visual separation
    - X^(+) -> X+
    - X^5   -> X{5}
    """
    expr = raw_expression
    expr = re.sub(r"\^\(\+\)", "+", expr)
    expr = re.sub(r"\^(\d+)", r"{\1}", expr)
    return expr


class RegexWordGenerator:
    def __init__(self, repetition_limit: int = 5, seed: Optional[int] = None):
        self.repetition_limit = repetition_limit
        self.rng = random.Random(seed)

    def generate_one(self, raw_expression: str, with_trace: bool = False) -> Tuple[str, List[str]]:
        normalized = normalize_lab_regex(raw_expression)
        parser = RegexParser(normalized)
        ast = parser.parse()

        trace = ParseTrace([])
        trace.add(f"Input expression: {raw_expression}")
        trace.add(f"Normalized expression: {normalized}")
        trace.add("Parse to AST and generate one valid word")

        # The parser already hard-limits * and + to 5 by design.
        word = ast.generate(self.repetition_limit, self.rng, trace if with_trace else None)

        if with_trace:
            return word, trace.steps
        return word, []

    def generate_many(self, raw_expression: str, count: int = 10, max_attempts: int = 1000) -> List[str]:
        unique_words = set()
        attempts = 0

        while len(unique_words) < count and attempts < max_attempts:
            attempts += 1
            word, _ = self.generate_one(raw_expression, with_trace=False)
            unique_words.add(word)

        return sorted(unique_words)
