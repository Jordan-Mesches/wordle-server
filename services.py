import datetime
from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, computed_field
from security import safe_requests


class ValidWordChecker:
    _valid_words: list[str] = []

    def __init__(self, words: Optional[list[str]] = None):
        if not words:
            words = []

        ValidWordChecker._valid_words.extend(words)

    @classmethod
    def load_from_file(cls, path) -> "ValidWordChecker":
        words = []
        with open(path, "r") as f:
            for line in f:
                words.append(line.strip())

        return cls(words=words)

    @classmethod
    def check(cls, word) -> bool:
        return word in cls._valid_words and len(word) == 5

@dataclass
class WordleAnswer:
    word: str
    date: datetime.datetime

    @property
    def is_current(self) -> bool:
        """
        Check if the wordle answer is for the current date.
        :return: True if the wordle answer is for the current date, False otherwise.
        """
        return self.date.date() == datetime.datetime.now().date()


def get_wordle_answer() -> WordleAnswer:
    current_date = datetime.datetime.now()
    response = safe_requests.get(f"https://www.nytimes.com/svc/wordle/v2/{current_date.strftime("%Y-%m-%d")}.json")

    return WordleAnswer(
        word=response.json()["solution"],
        date=current_date
    )

class WordleLetter(BaseModel):
    letter: str
    in_word: bool
    in_correct_spot: bool

    @property
    def is_correct(self) -> bool:
        return self.in_word and self.in_correct_spot


class WordleWord(BaseModel):
    letters: list[WordleLetter]

    @computed_field
    @property
    def is_correct(self) -> bool:
        return all(letter.is_correct for letter in self.letters)

class WordleValidator:
    _wordle_answer: WordleAnswer = None

    def __init__(self):
        if not WordleValidator._wordle_answer or not WordleValidator._wordle_answer.is_current:
            WordleValidator._wordle_answer = get_wordle_answer()

    def validate(self, word: str) -> WordleWord:
        answer = self._wordle_answer.word

        letters = []
        for i, letter in enumerate(word):
            in_word = letter in answer
            in_correct_spot = letter == answer[i]
            letters.append(WordleLetter(letter=letter, in_word=in_word, in_correct_spot=in_correct_spot))

        return WordleWord(letters=letters)

