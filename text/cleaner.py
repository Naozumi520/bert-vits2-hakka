import ToJyutping
from ToJyutping.PhonemesList import PhonemesList
from ToJyutping.Jyutping import Jyutping
import unicodedata
from typing import Literal, Tuple, Union
from itertools import starmap
from operator import add

from config import config
from text.symbols import symbols, yue_offset
from text.HakkaSyllable import HakkaSyllable


mode: Literal["standard", "minimal", "ipa"] = config.preprocess_text_config.mode
is_minimal = mode == "minimal"
yue_symbol_id_offsets = (yue_offset + 1,) * (3 if is_minimal else 2) + (0,)
hak_symbol_id_offsets = (yue_offset + 1,) * (4 if is_minimal else 3) + (0,)
j_medial_symbol_id = yue_offset + 20
zero_medial_symbol_id = yue_offset

hak_to_yue_symbol_map = str.maketrans({"v": "w", "y": "j", "a": "aa"} | dict(zip("123456", "543131")))


if mode == "ipa":
    def jyutping_ipa_g2p(self, offset: Union[int, Tuple[int, int, int], Tuple[int, int, int, int]] = 0, *, tone_same_seq = False, minimal = False) -> Union[Tuple[int, int, int], Tuple[int, int, int, int]]:
        raise NotImplementedError()
        return result if not offset else tuple(starmap(add, zip(result, offset)) if is_iterable(offset) else map(offset.__add__, result))
    Jyutping.g2p = jyutping_ipa_g2p


def clean_text(text, language):
    text = unicodedata.normalize("NFC", text)
    if language == "YUE":
        org_phonemes = ToJyutping.g2p(text, minimal=is_minimal, offset=yue_symbol_id_offsets)
        phonemes = PhonemesList((ids[:1] + (j_medial_symbol_id if ids[0] == j_medial_symbol_id else zero_medial_symbol_id,) + ids[1:]) if len(ids) > 1 else ids for ids in org_phonemes)
        lengths = [length + 1 if length > 1 else length for length in org_phonemes.lengths]
    elif language == "HAK":
        text = text.translate(hak_to_yue_symbol_map)
        phonemes = PhonemesList(
            (symbols.index(syllable),) if len(syllable) == 1  # Punctuation
            else HakkaSyllable(syllable).g2p(minimal=is_minimal, offset=hak_symbol_id_offsets)
            for syllable in text.split()
        )
        lengths = _get_lengths(text, phonemes)
    else:
        raise ValueError(f"Invalid language: {language}")
    return text, phonemes.segmentals, phonemes.tones, lengths


def _get_lengths(text, phonemes):
    it = iter(phonemes)
    prev_is_space = True

    def get_length(c):
        nonlocal prev_is_space
        is_space = c.isspace()
        try:
            return len(next(it)) - 1 if prev_is_space and not is_space else 0
        finally:
            prev_is_space = is_space

    return list(map(get_length, text))


if __name__ == "__main__":
    print(clean_text("咩話……你話上個月上堂學法文文法用咗 $50,000！？", "YUE"))
    print(clean_text("依然唔愛", "YUE"))
    print(clean_text("gang1 tien2 lau3 coi1 lam2 di1 boi4 la1 cut5 yit5 kai4 ngiuk5 loi2 ziong3 bin1 geu3 , yi2 miau4 le1 , ciu4 mak5 gai4 du1 mau2 .", "HAK"))
    print(clean_text("yi1 yen2 m1 oi4", "HAK"))
    print(_get_lengths("dnjkdfjk  rsujf es    oesesfklsf   ", [range(1), range(2), range(3), range(4)]))
    print(_get_lengths("  dnjkdfjk  rsujf es    oesesfklsf   ", [range(1), range(2), range(3), range(4)]))
