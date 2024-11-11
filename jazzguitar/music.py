import itertools
from dataclasses import dataclass
from typing import Self

_names_sharps = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
_names_flats = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
_PITCH_COUNT = 12


@dataclass
class Pitch:
    name: str
    distance_from_c: int

    def __init__(self, name: str, distance_from_c: int):
        self.name = name
        self.distance_from_c = distance_from_c

    @staticmethod
    def of(name: str):
        if name in _names_sharps:
            return Pitch(name=name, distance_from_c=_names_sharps.index(name))
        elif name in _names_flats:
            return Pitch(name=name, distance_from_c=_names_flats.index(name))
        else:
            raise ValueError(f"Unknown pitch: {name}")

    def above(self, num: int = 1, flat: bool = False) -> Self:
        if num == 0:
            return self
        assert num >= 1
        new_distance = (self.distance_from_c + num) % _PITCH_COUNT
        name_lookup_table = _names_flats if flat else _names_sharps
        return Pitch(name=name_lookup_table[new_distance], distance_from_c=new_distance)

    def below(self, num: int = 1, sharp: bool = False) -> Self:
        if num == 0:
            return self
        assert num >= 1
        new_distance = (self.distance_from_c - num) % _PITCH_COUNT
        name_lookup_table = _names_sharps if sharp else _names_flats
        return Pitch(name=name_lookup_table[new_distance], distance_from_c=new_distance)

    @property
    def is_sharp(self) -> bool:
        return "#" in self.name

    @property
    def is_flat(self) -> bool:
        return "b" in self.name

    @property
    def letter(self) -> str:
        return self.name.replace("#", "").replace("b", "")


@dataclass
class Scale:
    pitches: list[Pitch]

    def __init__(self, key: str, pattern: list[int]):
        self.pitches = self._find_pitches(key, pattern)[:-1]

    @staticmethod
    def major(key: str):
        return Scale(key=key, pattern=[2, 2, 1, 2, 2, 2, 1])

    @staticmethod
    def _is_correct_pattern(pitches: list[Pitch]) -> bool:
        letters = {pitch.letter for pitch in pitches[:-1]}
        return len(letters) == len(pitches) - 1 and pitches[-1] == pitches[0]

    @classmethod
    def _find_pitches(cls, key: str, pattern: list[int]) -> list[Pitch]:
        tonic = Pitch.of(key)

        offsets = [0] + list(itertools.accumulate(pattern))

        sharp_pitches = [tonic.above(offset, flat=False) for offset in offsets]
        if cls._is_correct_pattern(sharp_pitches):
            return sharp_pitches

        flat_pitches = [tonic.above(offset, flat=True) for offset in offsets]
        if cls._is_correct_pattern(flat_pitches):
            return flat_pitches

        raise ValueError(f"Invalid scale: {key}, pattern: {pattern}")
