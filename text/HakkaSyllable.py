from typing import Literal, Tuple, Union, overload
from itertools import starmap
from dataclasses import dataclass
from operator import add
import re
import warnings

def is_iterable(o):
	try:
		iter(o)
	except TypeError:
		return False
	return True

onset = ['', 'b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'ng', 'gw', 'kw', 'w', 'h', 'z', 'c', 's', 'j']
nucleus = ['aa', 'a', 'e', 'i', 'o', 'u']  
rhyme = ['oe', 'oen', 'oeng', 'oet', 'oek', 'eoi', 'eon', 'eot', 'yu', 'yun', 'yut', 'm', 'ng']
coda = ['', 'i', 'u', 'm', 'n', 'ng', 'p', 't', 'k']

regex = re.compile('^([gk]w?|ng|[bpmfvdtnlhwzcsj]?)((?:i(?!(?:ng|[iumnptk]?)[1-6]?$))?)(?![1-6]?$)((aa?|oe?|eo?|y?u|i?)(ng|[iumnptk]?))([1-6]?)$')

_minimal_mapping_nucleus_map = { 'oe': 26, 'eo': 26, 'yu': 27 }
_minimal_mapping_nucleus_to_onset = { 3: 19, 5: 14 }
_minimal_mapping_coda_to_onset = [0, 19, 14, 3, 7, 11, 1, 5, 9]
_minimal_mapping_rhyme_to_nucleus = {
	**{ i: _minimal_mapping_nucleus_map[r[:2]] for i, r in enumerate(rhyme[:-2], 54) },
	19: 23, 32: 23, 35: 23, 38: 25, 50: 25, 53: 25, 65: 0, 66: 0
}
_minimal_mapping_rhyme_to_coda = {
	**{ i: _minimal_mapping_coda_to_onset[coda.index(r[2:])] for i, r in enumerate(rhyme[:-2], 54) },
	0: 20, 9: 21, 18: 22, 27: 19, 36: 24, 45: 14, 54: 26, 62: 27, 65: 3, 66: 11
}

@dataclass(frozen=True)
class HakkaSyllable:
	id: int
	onset_id: int
	onset: str
	medial_id: int
	medial: str
	rhyme_id: int
	rhyme: str
	tone_id: int
	tone: str
	jyutping: str

	def __init__(self, x: Union[str, int]):
		if type(x) == int:
			raise NotImplementedError()
		else:
			object.__setattr__(self, "jyutping", x)
			match = re.match(regex, x)
			if not match: raise ValueError(f"Invalid jyutping: {x!r}")
			_onset, _medial, _rhyme, _nucleus, _coda, _tone = match.groups()
			if _onset == "v": _onset = "w"
			object.__setattr__(self, "onset", _onset)
			object.__setattr__(self, "onset_id", onset.index(_onset))
			object.__setattr__(self, "medial", _medial)
			object.__setattr__(self, "medial_id", int(bool(_medial or _onset == "j")))
			object.__setattr__(self, "rhyme", _rhyme)
			try:
				object.__setattr__(self, "rhyme_id", rhyme.index(_rhyme) + 54)
			except ValueError:
				object.__setattr__(self, "rhyme_id", coda.index(_coda) + nucleus.index(_nucleus) * 9)
			object.__setattr__(self, "tone", _tone)
			object.__setattr__(self, "tone_id", int(_tone) - 1)
			object.__setattr__(self, "id", self.tone_id + self.rhyme_id * 6 + self.medial_id * 402 + self.onset_id * 804)

	def __str__(self):
		return self.jyutping

	def __eq__(self, other):
		return isinstance(other, HakkaSyllable) and self.id == other.id
	
	def __hash__(self):
		return hash(self.id)

	@overload
	def g2p(self, offset: Union[int, Tuple[int, int, int, int]] = 0, *, tone_same_seq = False, minimal: Literal[False] = False) -> Tuple[int, int, int, int]: ...

	@overload
	def g2p(self, offset: Union[int, Tuple[int, int, int, int, int]] = 0, *, tone_same_seq = False, minimal: Literal[True]) -> Tuple[int, int, int, int, int]: ...

	def g2p(self, offset: Union[int, Tuple[int, int, int, int], Tuple[int, int, int, int, int]] = 0, *, tone_same_seq = False, minimal = False) -> Union[Tuple[int, int, int, int], Tuple[int, int, int, int, int]]:
		if minimal:
			warnings.warn('`minimal` is an experimental feature and is subject to changes or removal in the future.')
			necleus = _minimal_mapping_rhyme_to_nucleus.get(self.rhyme_id, _minimal_mapping_nucleus_to_onset.get(self.rhyme_id // 9, self.rhyme_id // 9 + 20))
			result = (
				self.onset_id,
				self.medial_id * 19 or -1,
				necleus or -1,
				_minimal_mapping_rhyme_to_coda.get(self.rhyme_id, _minimal_mapping_coda_to_onset[self.rhyme_id % 9]),
				self.tone_id + (28 if tone_same_seq else 1),
			)
		else:
			result = (self.onset_id, self.medial_id * 19 or -1, self.rhyme_id + 20, self.tone_id + (87 if tone_same_seq else 1))
		return result if not offset else tuple(starmap(add, zip(result, offset)) if is_iterable(offset) else map(offset.__add__, result))
