from config import config

# Follows the order in ToJyutping.g2p
punctuation = ["…", ".", ",", "!", "?", "-", "'"]
pu_symbols = punctuation  # + ["SP", "UNK"]
pad = "_"

# Cantonese: Symbols are already mapped internally in ToJyutping.g2p
# Generates identity mappings for `len(symbols)` to work correctly
yue_symbols = list(range({"standard": 88, "minimal": 29, "ipa": 0}[config.preprocess_text_config.mode]))
num_yue_tones = 6

# combine all symbols
symbols = [pad] + pu_symbols
yue_offset = len(symbols)  # For use by ToJyutping.g2p in cleaner.py
symbols += yue_symbols

# combine all tones
num_tones = num_yue_tones

# language maps
language_id_map = {"YUE": 0, "HAK": 0}
num_languages = 1

language_tone_start_map = {
    "YUE": 0,
    "HAK": 0,
}
