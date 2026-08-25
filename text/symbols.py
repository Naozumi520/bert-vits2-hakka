punctuation = ["!", "?", "…", ",", ".", "'", "-"]
pu_symbols = punctuation + ["SP", "UNK"]
pad = "_"
silent = "#"

# hakka

hakka_symbols = [
    "a",
    "aa",
    "aai",
    "aak",
    "aam",
    "aan",
    "aang",
    "aap",
    "aat",
    "aau",
    "ai",
    "ak",
    "am",
    "an",
    "ang",
    "ap",
    "at",
    "au",
    "b",
    "c",
    "d",
    "e",
    "ei",
    "ek",
    "eng",
    "eoi",
    "eon",
    "eot",
    "eu",
    "em",
    "en",
    "ep",
    "et",
    "f",
    "g",
    "gw",
    "h",
    "i",
    "ik",
    "im",
    "in",
    "ing",
    "ip",
    "it",
    "iu",
    "y",
    "k",
    "kw",
    "l",
    "m",
    "n",
    "ng",
    "o",
    "oe",
    "oek",
    "oeng",
    "oi",
    "ok",
    "on",
    "ong",
    "ot",
    "ou",
    "p",
    "s",
    "sil",
    "sp",
    "spl",
    "t",
    "u",
    "ui",
    "uk",
    "un",
    "ung",
    "ut",
    "v",
    "w",
    "yu",
    "yun",
    "yut",
    "z",
]
num_hakka_tones = 7

# combine all symbols
normal_symbols = sorted(set(hakka_symbols))
symbols = [pad] + normal_symbols + pu_symbols + [silent]
symbols = symbols + sorted((set(hakka_symbols) - set(symbols)))
sil_phonemes_ids = [symbols.index(i) for i in pu_symbols]

# combine all tones
num_tones = num_hakka_tones

# language maps
language_id_map = {"HAKKA": 0}
num_languages = len(language_id_map.keys())

language_tone_start_map = {
    "HAKKA": 0,
}

if __name__ == "__main__":
    a = set(hakka_symbols)
    print(sorted(a))
