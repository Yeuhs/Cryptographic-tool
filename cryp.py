# -*- coding: utf-8 -*-

import collections
import re
import sys
import traceback
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, ttk

# ==================== АЛФАВІТИ ТА ЧАСТОТИ ====================
UA_32 = "АБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
UA_33 = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
EN_25 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
EN_26 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

UA_FREQ = {
    'О': 0.094, 'А': 0.072, 'Н': 0.065, 'І': 0.062, 'И': 0.061, 'В': 0.052,
    'Р': 0.047, 'Т': 0.046, 'Е': 0.045, 'С': 0.041, 'К': 0.035, 'Л': 0.035,
    'М': 0.031, 'Д': 0.030, 'П': 0.029, 'З': 0.023, 'У': 0.021, 'Я': 0.020,
    'Б': 0.017, 'Г': 0.016, 'Ч': 0.014, 'Х': 0.012, 'Ь': 0.012, 'Ц': 0.010,
    'Ж': 0.009, 'Ї': 0.008, 'Є': 0.008, 'Й': 0.008, 'Ш': 0.007, 'Ю': 0.007,
    'Щ': 0.005, 'Ф': 0.003, 'Ґ': 0.001,
}
EN_FREQ = {
    'E': 0.127, 'T': 0.090, 'A': 0.081, 'O': 0.075, 'I': 0.070, 'N': 0.067,
    'S': 0.063, 'H': 0.061, 'R': 0.060, 'D': 0.042, 'L': 0.040, 'C': 0.028,
    'U': 0.027, 'M': 0.024, 'W': 0.023, 'F': 0.022, 'G': 0.020, 'Y': 0.019,
    'P': 0.019, 'B': 0.015, 'V': 0.009, 'K': 0.007, 'J': 0.001, 'X': 0.001,
    'Q': 0.001, 'Z': 0.001,
}

ALPH_CODES = ["UA32", "UA33", "EN"]
POLY_ALPHABETS = {"UA32": UA_32, "UA33": UA_33, "EN": EN_25}
ALPHABETS = {"UA32": UA_32, "UA33": UA_33, "EN": EN_26}
FREQS = {"UA32": UA_FREQ, "UA33": UA_FREQ, "EN": EN_FREQ}
EXPECTED_IC = {"UA32": 0.056, "UA33": 0.056, "EN": 0.0667}

# ==================== КОЛЬОРОВА ПАЛІТРА ====================
C_BG = "#070925"
C_PANEL = "#0e1140"
C_PANEL2 = "#171b5c"
C_FIELD = "#090c30"
C_TEXT = "#e9edff"
C_MUTED = "#9ba6ec"
C_CYAN = "#19e3ff"
C_MAGENTA = "#ff3b8d"
C_PURPLE = "#8a5cff"
C_BLUE = "#2f7bff"
C_ORANGE = "#ffb23b"
C_BTN = "#10154f"

# ==================== ЛОКАЛІЗАЦІЯ (UA / EN) ====================
LANG_DATA = {
    "UA": {
        "title": "Cryptographic Tool",
        "lang_label": "Мова / Language",
        "nav_encrypt": "🔒  Зашифрувати",
        "nav_decrypt": "🔓  Розшифрувати",
        "nav_analyze": "🔍  Аналіз шифрів",
        "nav_clear": "🧹  Очистити все",
        "nav_help": "❓  Довідка",
        "poly_title": "Квадрат Полібія",
        "caesar_title": "Шифр / Криптоаналіз Цезаря",
        "vig_title": "Шифр / Криптоаналіз Віженера",
        "io_title": "Вхідний текст",
        "alphabet": "Алфавіт:",
        "rows": "Рядки:",
        "cols": "Стовпчики:",
        "keyword": "Ключове слово:",
        "mode": "Режим:",
        "coords": "Координати (РядСтовп - без ключа)",
        "shift": "Зсув вниз на 1 (з ключем)",
        "update_matrix": "Оновити матрицю",
        "output_text": "Результат:",
        "encrypt": "🔒 Зашифрувати",
        "decrypt": "🔓 Розшифрувати",
        "paste": "📋 Вставити",
        "copy": "📄 Копіювати",
        "copy_res": "📄 Копіювати результат",
        "caesar_input": "Текст для Цезаря:",
        "caesar_mode_nokey": "Без ключового слова (класичний Цезар)",
        "caesar_mode_key": "З ключовим словом (підстановка)",
        "caesar_shift": "Зсув (числовий ключ):",
        "caesar_kw_lbl": "Ключове слово:",
        "caesar_enc": "🔒 Зашифрувати Цезарем",
        "caesar_dec": "🔓 Розшифрувати Цезарем",
        "caesar_analyze_btn": "🔍 Авто-криптоаналіз (без ключа)",
        "vig_input": "Текст для Віженера:",
        "vig_break": "Розкрити ключ і розшифрувати",
        "vig_key": "Ключ:",
        "vig_len": "Довжина ключа (0 = авто):",
        "vig_enc_key": "Зашифрувати ключем",
        "vig_dec_key": "Розшифрувати ключем",
        "alph_ua32": "UA32 (Українська, 32 літери, без Ґ)",
        "alph_ua33": "UA33 (Українська, 33 літери, з Ґ)",
        "alph_en25": "EN (Англійська, 25 літер, J=I)",
        "alph_en26": "EN (Англійська, 26 літер)",
        "tooltip_UA32": "Українська 32 літери (без Ґ). Матриця 8x4 або 4x8",
        "tooltip_UA33": "Українська 33 літери (з Ґ). Матриця 7x5 або 6x6",
        "tooltip_EN": "Англійський алфавіт (25 літер, J=I). Матриця 5x5",
        "code_warning_title": "Увага: виявлено код/скрипт!",
        "code_warning_msg": "Текст у буфері схожий на код!\n\nВи дійсно бажаєте його вставити?",
        "cut": "Вирізати",
        "select_all": "Виділити все",
        "undo": "Скасувати",
        "redo": "Повторити",
        "clear_field": "Очистити поле",
        "warn": "Увага",
        "err": "Помилка",
        "err_dims": "Некоректні розміри матриці.",
        "err_capacity": "Матриця {r}x{c} вміщує {cap} символів, а алфавіт має {need}.",
        "capacity_warn": "⚠ Матриця замала: {cap} клітинок, потрібно ≥ {need}",
        "copied": "✔ Скопійовано в буфер обміну",
        "nothing_copy": "Немає що копіювати",
        "cleared": "Усі поля очищено",
        "short_text": "Текст занадто короткий для аналізу.",
        "no_key": "Введіть ключ (літери вибраного алфавіту).",
        "no_text": "Введіть текст.",
        "caesar_header": "=== НАЙВІРОГІДНІШІ ВАРІАНТИ (ОЦІНКА ЧАСТОТ) ===",
        "shift_lbl": "Зсув",
        "score_lbl": "Бал",
        "best_mark": "◄ найімовірніший",
        "vig_len_found": "Знайдена довжина ключа: {k}{forced}",
        "vig_forced": " (задана вручну)",
        "vig_ic": "Індекс збігів (очікується ≈ {exp:.3f}) для довжин:",
        "vig_key_found": "Відновлений ключ: {key}",
        "vig_decrypted": "Розшифрований текст:",
        "vig_hint": "Підказка: текст короткий ({n} літер), аналіз може помилятись.",
        "vig_result_enc": "Результат шифрування Віженера:",
        "vig_result_dec": "Результат дешифрування Віженера:",
        "help_text": (
            "ГАРЯЧІ КЛАВІШІ (у будь-якій розкладці):\n"
            "  Ctrl+C — копіювати     Ctrl+V — вставити\n"
            "  Ctrl+X — вирізати      Ctrl+A — виділити все\n"
            "  Ctrl+Z — скасувати     Ctrl+Y / Ctrl+Shift+Z — повторити\n\n"
            "ПОЛІБІЙ:\n"
            "  • Без ключа (Координати) — кожна літера → Пара РядСтовп.\n"
            "  • З ключем (Зсув вниз) — заміна літерою знизу у матриці.\n\n"
            "ЦЕЗАР:\n"
            "  • Перемикач дозволяє шифрувати з ключовим словом або без нього.\n"
            "  • Кнопка криптоаналізу здійснює автоматичний підбір зсуву.\n\n"
            "ВІЖЕНЕР: розкриття ключа за критерієм Хі-квадрат та індексом Фрідмана."
        ),
    },
    "EN": {
        "title": "Cryptographic Tool",
        "lang_label": "Language / Мова",
        "nav_encrypt": "🔒  Encrypt",
        "nav_decrypt": "🔓  Decrypt",
        "nav_analyze": "🔍  Analyze ciphers",
        "nav_clear": "🧹  Clear all",
        "nav_help": "❓  Help",
        "poly_title": "Polybius Square",
        "caesar_title": "Caesar Cipher & Analysis",
        "vig_title": "Vigenere Cipher & Analysis",
        "io_title": "Input Text",
        "alphabet": "Alphabet:",
        "rows": "Rows:",
        "cols": "Columns:",
        "keyword": "Keyword:",
        "mode": "Mode:",
        "coords": "Coordinates (RowCol - no key)",
        "shift": "Shift down by 1 (with key)",
        "update_matrix": "Update Matrix",
        "output_text": "Result:",
        "encrypt": "🔒 Encrypt",
        "decrypt": "🔓 Decrypt",
        "paste": "📋 Paste",
        "copy": "📄 Copy",
        "copy_res": "📄 Copy Result",
        "caesar_input": "Text for Caesar:",
        "caesar_mode_nokey": "Without keyword (Classic Caesar)",
        "caesar_mode_key": "With keyword (Keyed substitution)",
        "caesar_shift": "Shift (numeric key):",
        "caesar_kw_lbl": "Keyword:",
        "caesar_enc": "🔒 Encrypt Caesar",
        "caesar_dec": "🔓 Decrypt Caesar",
        "caesar_analyze_btn": "🔍 Auto Cryptanalysis (no key)",
        "vig_input": "Text for Vigenere:",
        "vig_break": "Recover Key & Decrypt",
        "vig_key": "Key:",
        "vig_len": "Key length (0 = auto):",
        "vig_enc_key": "Encrypt with key",
        "vig_dec_key": "Decrypt with key",
        "alph_ua32": "UA32 (Ukrainian, 32 letters, no Ґ)",
        "alph_ua33": "UA33 (Ukrainian, 33 letters, with Ґ)",
        "alph_en25": "EN (English, 25 letters, J=I)",
        "alph_en26": "EN (English, 26 letters)",
        "tooltip_UA32": "Ukrainian 32 letters (without Ґ). Matrix 8x4 or 4x8",
        "tooltip_UA33": "Ukrainian 33 letters (with Ґ). Matrix 7x5 or 6x6",
        "tooltip_EN": "English alphabet (25 letters, J=I). Matrix 5x5",
        "code_warning_title": "Warning: code/script detected!",
        "code_warning_msg": "The clipboard text looks like code!\n\nAre you sure you want to paste it?",
        "cut": "Cut",
        "select_all": "Select All",
        "undo": "Undo",
        "redo": "Redo",
        "clear_field": "Clear field",
        "warn": "Warning",
        "err": "Error",
        "err_dims": "Invalid matrix size.",
        "err_capacity": "A {r}x{c} matrix holds {cap} symbols, alphabet has {need}.",
        "capacity_warn": "⚠ Matrix too small: {cap} cells, need ≥ {need}",
        "copied": "✔ Copied to clipboard",
        "nothing_copy": "Nothing to copy",
        "cleared": "All fields cleared",
        "short_text": "Text is too short for analysis.",
        "no_key": "Enter a key (letters of selected alphabet).",
        "no_text": "Enter some text.",
        "caesar_header": "=== MOST LIKELY VARIANTS (FREQUENCY SCORE) ===",
        "shift_lbl": "Shift",
        "score_lbl": "Score",
        "best_mark": "◄ most likely",
        "vig_len_found": "Key length found: {k}{forced}",
        "vig_forced": " (set manually)",
        "vig_ic": "Index of coincidence (expected ≈ {exp:.3f}) per length:",
        "vig_key_found": "Recovered key: {key}",
        "vig_decrypted": "Decrypted text:",
        "vig_hint": "Hint: text is short ({n} letters), frequency analysis may err.",
        "vig_result_enc": "Vigenere encryption result:",
        "vig_result_dec": "Vigenere decryption result:",
        "help_text": (
            "HOTKEYS (any keyboard layout):\n"
            "  Ctrl+C — copy       Ctrl+V — paste\n"
            "  Ctrl+X — cut        Ctrl+A — select all\n"
            "  Ctrl+Z — undo       Ctrl+Y / Ctrl+Shift+Z — redo\n\n"
            "POLYBIUS:\n"
            "  • Without key (Coordinates) — letter → RowCol pair.\n"
            "  • With key (Shift down) — replaces letter with one below.\n\n"
            "CAESAR:\n"
            "  • Toggle enables Caesar with or without keyword.\n"
            "  • Cryptanalysis button performs auto frequency search.\n\n"
            "VIGENERE: Key recovery via Chi-square statistic and Friedman Index."
        ),
    },
}

# ==================== ДЕТЕКТОР СКРИПТІВ ТА КОДУ ====================
_CODE_PATTERNS = [
    r"<\s*script\b",
    r"</?\s*(html|body|div|span|iframe|script|style)\b[^>]*>",
    r"^\s*(def|class)\s+\w+.*:\s*$",
    r"^\s*(import\s+[\w.]+|from\s+[\w.]+\s+import\s+\w+)",
    r"\b(function\s*\w*\s*\(|console\.log\s*\(|document\.\w+|window\.\w+)",
    r"^\s*(const|let|var)\s+\w+\s*=",
    r"#include\s*<.*?>",
    r"^\s*(public|private)\s+(static\s+)?\w+\s+\w+\s*\(",
    r"[{};]\s*$",
]

def is_code_or_script(text: str) -> bool:
    for pattern in _CODE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
            return True
    return False

# ==================== КРИПТОЛОГІЧНІ АЛГОРИТМИ ====================

# --- 1. КВАДРАТ ПОЛІБІЯ ---
def build_polybius_matrix(rows, cols, key="", lang="UA32"):
    base_alph = list(POLY_ALPHABETS[lang])
    extras = [' ', '.', ',', '-', '!', '?'] + list("0123456789")
    capacity = rows * cols

    key_clean = []
    for c in key.upper():
        if lang == "EN" and c == "J":
            c = "I"
        if (c in base_alph or c in extras) and c not in key_clean:
            key_clean.append(c)

    full_list = key_clean + [c for c in base_alph if c not in key_clean]
    if len(full_list) < capacity:
        for ex in extras:
            if ex not in full_list:
                full_list.append(ex)
            if len(full_list) == capacity:
                break
    full_list = full_list[:capacity]
    while len(full_list) < capacity:
        full_list.append("·")
    return [full_list[r * cols:(r + 1) * cols] for r in range(rows)]

def polybius_encrypt(text, matrix, lang, mode):
    rows, cols = len(matrix), len(matrix[0])
    char_map = {matrix[i][j]: (i, j) for i in range(rows) for j in range(cols)}
    out = []
    for ch in text.upper():
        if lang == "EN" and ch == "J":
            ch = "I"
        if mode == "coords":
            if ch in char_map:
                r, c = char_map[ch]
                out.append(f"{r + 1}{c + 1}")
            elif ch == " ":
                out.append("/")
            elif ch == "\n":
                out.append("\n")
            else:
                out.append(ch)
        else:
            if ch in char_map:
                r, c = char_map[ch]
                res_char = matrix[(r + 1) % rows][c]
                out.append(res_char if ch.isupper() else res_char.lower())
            else:
                out.append(ch)
    return " ".join(out).replace(" \n ", "\n") if mode == "coords" else "".join(out)

def polybius_decrypt(text, matrix, lang, mode):
    rows, cols = len(matrix), len(matrix[0])
    if mode == "coords":
        out = []
        for line in text.split("\n"):
            chars = []
            tokens = line.split()
            for tok in tokens:
                if tok == "/":
                    chars.append(" ")
                elif tok.isdigit():
                    if len(tok) == 2:
                        r, c = int(tok[0]) - 1, int(tok[1]) - 1
                        chars.append(matrix[r][c] if 0 <= r < rows and 0 <= c < cols else tok)
                    elif len(tok) % 2 == 0:
                        for idx in range(0, len(tok), 2):
                            pair = tok[idx:idx + 2]
                            r, c = int(pair[0]) - 1, int(pair[1]) - 1
                            chars.append(matrix[r][c] if 0 <= r < rows and 0 <= c < cols else pair)
                    else:
                        chars.append(tok)
                else:
                    chars.append(tok)
            out.append("".join(chars))
        return "\n".join(out)
    else:
        char_map = {matrix[i][j]: (i, j) for i in range(rows) for j in range(cols)}
        out = []
        for ch in text:
            ch_u = ch.upper()
            if lang == "EN" and ch_u == "J":
                ch_u = "I"
            if ch_u in char_map:
                r, c = char_map[ch_u]
                res_char = matrix[(r - 1) % rows][c]
                out.append(res_char if ch.isupper() else res_char.lower())
            else:
                out.append(ch)
        return "".join(out)

# --- 2. ШИФР ЦЕЗАРЯ ---
def make_caesar_alphabet(base_alph, keyword=""):
    key_clean = []
    for c in keyword.upper():
        if c in base_alph and c not in key_clean:
            key_clean.append(c)
    rem = [c for c in base_alph if c not in key_clean]
    return key_clean + rem

def caesar_cipher_transform(text, shift, keyword="", code="UA33", decrypt=False):
    base_alph = ALPHABETS[code]
    n = len(base_alph)
    has_kw = bool(keyword.strip())
    sub_alph = make_caesar_alphabet(base_alph, keyword) if has_kw else base_alph

    out = []
    for ch in text:
        ch_u = ch.upper()
        if ch_u in base_alph:
            if not decrypt:
                if has_kw:
                    idx = base_alph.index(ch_u)
                    res_char = sub_alph[(idx - shift) % n]
                else:
                    idx = base_alph.index(ch_u)
                    res_char = base_alph[(idx + shift) % n]
            else:
                if has_kw:
                    idx = sub_alph.index(ch_u)
                    res_char = base_alph[(idx + shift) % n]
                else:
                    idx = base_alph.index(ch_u)
                    res_char = base_alph[(idx - shift) % n]
            out.append(res_char if ch.isupper() else res_char.lower())
        else:
            out.append(ch)
    return "".join(out)

def caesar_analyze(text, code):
    alph, freq = ALPHABETS[code], FREQS[code]
    n = len(alph)
    results = []
    for shift in range(n):
        dec_chars = []
        letters = []
        for c in text:
            cu = c.upper()
            if cu in alph:
                res_char = alph[(alph.index(cu) - shift) % n]
                dec_chars.append(res_char if c.isupper() else res_char.lower())
                letters.append(res_char)
            else:
                dec_chars.append(c)
        dec = "".join(dec_chars)
        score = 0.0
        if letters:
            for ch, cnt in collections.Counter(letters).items():
                score += (cnt / len(letters)) * freq.get(ch, 0.0)
        results.append((score, shift, dec))
    results.sort(key=lambda x: x[0], reverse=True)
    return results

# --- 3. ШИФР ВІЖЕНЕРА ---
def vigenere_crypt(text, key, code, decrypt=False):
    alph = ALPHABETS[code]
    n = len(alph)
    key_alph = [k.upper() for k in key if k.upper() in alph]
    if not key_alph:
        return None
    shifts = [alph.index(k) for k in key_alph]
    out, j = [], 0
    for ch in text:
        ch_u = ch.upper()
        if ch_u in alph:
            s = shifts[j % len(shifts)]
            idx = alph.index(ch_u)
            res_idx = (idx - s) % n if decrypt else (idx + s) % n
            res_char = alph[res_idx]
            out.append(res_char if ch.isupper() else res_char.lower())
            j += 1
        else:
            out.append(ch)
    return "".join(out)

def _ic(seq):
    n = len(seq)
    if n < 2:
        return 0.0
    return sum(v * (v - 1) for v in collections.Counter(seq).values()) / (n * (n - 1))

def vigenere_analyze(text, code, forced_len=0, max_len=20):
    alph, freq = ALPHABETS[code], FREQS[code]
    n_alph = len(alph)
    letters = [c for c in text.upper() if c in alph]
    n = len(letters)
    if n < 10:
        return None

    limit = max(1, min(max_len, n // 3))
    ic_table = []
    for k in range(1, limit + 1):
        groups = [letters[i::k] for i in range(k)]
        avg_ic = sum(_ic(g) for g in groups) / k
        ic_table.append((k, avg_ic))

    if forced_len and forced_len > 0:
        best_k = min(forced_len, n)
    else:
        best_k = 1
        max_score = -1.0
        for k, ic in ic_table:
            if ic > max_score:
                max_score = ic
                best_k = k

        for k, ic in ic_table:
            if ic >= 0.038 and (best_k % k == 0 or ic >= max_score * 0.90):
                best_k = k
                break

    key_chars = []
    for i in range(best_k):
        group = letters[i::best_k]
        g_len = len(group)
        best_shift = 0
        min_chi2 = float('inf')

        for shift in range(n_alph):
            dec_group = [alph[(alph.index(ch) - shift) % n_alph] for ch in group]
            counts = collections.Counter(dec_group)
            
            chi2 = 0.0
            for ch in alph:
                observed = counts.get(ch, 0)
                expected = g_len * freq.get(ch, 0.0005)
                chi2 += ((observed - expected) ** 2) / expected

            if chi2 < min_chi2:
                min_chi2 = chi2
                best_shift = shift

        key_chars.append(alph[best_shift])

    key = "".join(key_chars)
    return {
        "k": best_k,
        "forced": bool(forced_len),
        "key": key,
        "ic_table": ic_table,
        "n": n,
        "text": vigenere_crypt(text, key, code, decrypt=True),
    }

# ==================== ПОПП-АП ПІДКАЗКИ ====================
class ToolTip:
    def __init__(self, widget, text=""):
        self.widget, self.text, self.tip = widget, text, None
        widget.bind("<Enter>", self.show, add="+")
        widget.bind("<Leave>", self.hide, add="+")

    def set_text(self, text):
        self.text = text

    def show(self, _=None):
        if self.tip or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self.tip = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tk.Label(tw, text=self.text, justify="left", bg=C_PANEL2, fg=C_CYAN,
                 relief="solid", bd=1, padx=6, pady=3).pack()

    def hide(self, _=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None

# ==================== ГОЛОВНИЙ ДОДАТОК (GUI) ====================
class CryptoApp(tk.Tk):
    KEYCODES = {
        "win": {65: "select_all", 67: "copy", 86: "paste", 88: "cut", 90: "undo", 89: "redo"},
        "linux": {38: "select_all", 54: "copy", 55: "paste", 53: "cut", 52: "undo", 29: "redo"},
        "mac": {0: "select_all", 8: "copy", 9: "paste", 7: "cut", 6: "undo", 16: "redo"},
    }
    KEYSYMS = {
        "a": "select_all", "cyrillic_ef": "select_all",
        "c": "copy", "cyrillic_es": "copy",
        "v": "paste", "cyrillic_em": "paste",
        "x": "cut", "cyrillic_che": "cut",
        "z": "undo", "cyrillic_ya": "undo",
        "y": "redo", "cyrillic_en": "redo",
    }
    CTRL_CHARS = {"\x01": "select_all", "\x03": "copy", "\x16": "paste",
                  "\x18": "cut", "\x1a": "undo", "\x19": "redo"}

    def __init__(self):
        super().__init__()
        self.ui_lang = "UA"
        self._i18n = []
        self._combos = []
        self._status_job = None

        fams = set(tkfont.families())
        pick = lambda *n: next((x for x in n if x in fams), "TkDefaultFont")
        self.F = pick("Segoe UI", "Calibri", "Arial", "DejaVu Sans")
        self.FM = pick("Consolas", "DejaVu Sans Mono", "Courier New")

        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w, h = min(1400, sw - 40), min(900, sh - 80)
        self.geometry(f"{w}x{h}+{max(0, (sw - w) // 2)}+{max(0, (sh - h) // 2 - 20)}")
        self.minsize(1100, 700)
        self.configure(bg=C_BG)

        self.setup_styles()
        self.build_layout()
        self.retranslate_ui()

    def t(self, key):
        return LANG_DATA[self.ui_lang].get(key, key)

    def reg(self, widget, key):
        self._i18n.append((widget, key))
        widget.config(text=self.t(key))
        return widget

    def flash(self, msg, color=C_CYAN):
        self.status.config(text=msg, fg=color)
        if self._status_job:
            self.after_cancel(self._status_job)
        self._status_job = self.after(3000, lambda: self.status.config(text=""))

    def setup_styles(self):
        st = ttk.Style(self)
        st.theme_use("clam")
        self.option_add("*TCombobox*Listbox.background", C_FIELD)
        self.option_add("*TCombobox*Listbox.foreground", C_TEXT)
        self.option_add("*TCombobox*Listbox.selectBackground", C_PURPLE)
        self.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")
        self.option_add("*TCombobox*Listbox.font", (self.F, 10))
        st.configure("Neon.TCombobox", fieldbackground=C_FIELD, background=C_PANEL2,
                     foreground=C_TEXT, arrowcolor=C_CYAN, bordercolor=C_PURPLE,
                     lightcolor=C_PURPLE, darkcolor=C_PURPLE, padding=4)
        st.map("Neon.TCombobox",
               fieldbackground=[("readonly", C_FIELD)],
               foreground=[("readonly", C_TEXT)],
               selectbackground=[("readonly", C_FIELD)],
               selectforeground=[("readonly", C_TEXT)],
               bordercolor=[("focus", C_CYAN)],
               background=[("active", C_PURPLE)])
        st.configure("Neon.Vertical.TScrollbar", troughcolor=C_FIELD,
                     background=C_PURPLE, bordercolor=C_FIELD, arrowcolor=C_CYAN,
                     lightcolor=C_PURPLE, darkcolor=C_PURPLE, relief="flat")
        st.map("Neon.Vertical.TScrollbar", background=[("active", C_CYAN)])

    def panel(self, parent, title_key, color=C_PURPLE):
        outer = tk.Frame(parent, bg=C_PANEL, highlightthickness=2,
                         highlightbackground=color, highlightcolor=color)
        head = tk.Label(outer, bg=C_PANEL, fg=C_TEXT, anchor="w",
                        font=(self.F, 14, "bold"), padx=14, pady=5)
        head.pack(fill="x")
        self.reg(head, title_key)
        tk.Frame(outer, bg=color, height=1).pack(fill="x", padx=10)
        body = tk.Frame(outer, bg=C_PANEL)
        body.pack(fill="both", expand=True, padx=12, pady=6)
        return outer, body

    def label(self, parent, key, fg=C_TEXT, bold=False):
        lb = tk.Label(parent, bg=C_PANEL, fg=fg, anchor="w",
                      font=(self.F, 10, "bold" if bold else "normal"))
        return self.reg(lb, key)

    def button(self, parent, key, command, color=C_CYAN, width=None, anchor="center", font_size=10):
        b = tk.Button(parent, command=command, bg=C_BTN, fg=C_TEXT, bd=0,
                      activebackground=color, activeforeground="#000000",
                      relief="flat", highlightthickness=2,
                      highlightbackground=color, highlightcolor=color,
                      cursor="hand2", anchor=anchor, padx=10, pady=4,
                      font=(self.F, font_size, "bold"))
        if width:
            b.config(width=width)
        b.bind("<Enter>", lambda e: b.config(bg=C_PANEL2))
        b.bind("<Leave>", lambda e: b.config(bg=C_BTN))
        return self.reg(b, key)

    def combo(self, parent, kind, width=32):
        cb = ttk.Combobox(parent, state="readonly", width=width,
                          style="Neon.TCombobox", font=(self.F, 10))
        self._combos.append((cb, kind))
        cb["values"] = self.alph_names(kind)
        cb.current(1 if kind == "poly" else 1)
        return cb

    def alph_names(self, kind):
        k = ["alph_ua32", "alph_ua33", "alph_en25" if kind == "poly" else "alph_en26"]
        return [self.t(x) for x in k]

    def entry(self, parent, width=18):
        e = tk.Entry(parent, width=width, bg=C_FIELD, fg=C_TEXT, insertbackground=C_CYAN,
                     selectbackground=C_PURPLE, selectforeground="#ffffff", relief="flat",
                     highlightthickness=1, highlightbackground=C_PURPLE,
                     highlightcolor=C_CYAN, font=(self.FM, 10))
        self.setup_editing(e)
        return e

    def spinbox(self, parent, lo, hi, init, command=None):
        sp = tk.Spinbox(parent, from_=lo, to=hi, width=4, bg=C_FIELD, fg=C_TEXT,
                        buttonbackground=C_PURPLE, insertbackground=C_CYAN,
                        selectbackground=C_PURPLE, relief="flat",
                        highlightthickness=1, highlightbackground=C_PURPLE,
                        highlightcolor=C_CYAN, font=(self.FM, 10), command=command)
        sp.delete(0, tk.END)
        sp.insert(0, str(init))
        if command:
            sp.bind("<KeyRelease>", lambda e: command(), add="+")
        self.setup_editing(sp)
        return sp

    def radio(self, parent, key, var, value, command=None):
        r = tk.Radiobutton(parent, variable=var, value=value, command=command,
                           bg=C_PANEL, fg=C_TEXT, activebackground=C_PANEL,
                           activeforeground=C_CYAN, selectcolor=C_FIELD,
                           highlightthickness=0, bd=0, font=(self.F, 10), cursor="hand2")
        return self.reg(r, key)

    def textbox(self, parent, height):
        box = tk.Frame(parent, bg=C_FIELD, highlightthickness=1,
                       highlightbackground=C_PURPLE, highlightcolor=C_CYAN)
        txt = tk.Text(box, height=height, wrap="word", undo=True, maxundo=-1,
                      autoseparators=True, bg=C_FIELD, fg=C_TEXT,
                      insertbackground=C_CYAN, selectbackground=C_PURPLE,
                      selectforeground="#ffffff", relief="flat", bd=0, padx=6, pady=4,
                      font=(self.FM, 10), exportselection=False)
        sb = ttk.Scrollbar(box, orient="vertical", command=txt.yview,
                           style="Neon.Vertical.TScrollbar")
        txt.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        txt.pack(side="left", fill="both", expand=True)
        txt.bind("<FocusIn>", lambda e: box.config(highlightbackground=C_CYAN), add="+")
        txt.bind("<FocusOut>", lambda e: box.config(highlightbackground=C_PURPLE), add="+")
        self.setup_editing(txt)
        return box, txt

    @staticmethod
    def is_text(w):
        return isinstance(w, tk.Text)

    def setup_editing(self, w):
        if not self.is_text(w):
            w._hist = {"undo": [], "redo": [], "last": w.get()}
            w.bind("<KeyRelease>", lambda e, w=w: self._snap(w), add="+")
        try:
            w.bind("<Control-Key>", self.on_hotkey)
            w.bind("<Command-Key>", self.on_hotkey)
        except tk.TclError:
            pass
        w.bind("<<Paste>>", lambda e: self._do_action("paste", e.widget) or "break")
        w.bind("<Shift-Insert>", lambda e: self._do_action("paste", e.widget) or "break")
        w.bind("<Button-3>", self.show_context_menu)
        w.bind("<Button-2>", self.show_context_menu)

    def detect_action(self, event):
        ks = (event.keysym or "").lower()
        if ks in self.KEYSYMS and len(ks) == 1:
            return self.KEYSYMS[ks]
        if sys.platform.startswith("win"):
            table = self.KEYCODES["win"]
        elif sys.platform == "darwin":
            table = self.KEYCODES["mac"]
        else:
            table = self.KEYCODES["linux"]
        act = table.get(event.keycode) or table.get(event.keycode & 0xFF)
        if act:
            return act
        if ks in self.KEYSYMS:
            return self.KEYSYMS[ks]
        return self.CTRL_CHARS.get(event.char)

    def on_hotkey(self, event):
        if sys.platform.startswith("win") and event.state & 0x20000:
            return None
        act = self.detect_action(event)
        if not act:
            return None
        if act == "undo" and event.state & 0x1:
            act = "redo"
        self._do_action(act, event.widget)
        return "break"

    def get_selection(self, w):
        try:
            if self.is_text(w):
                return w.get("sel.first", "sel.last")
            if w.selection_present():
                return w.selection_get()
        except tk.TclError:
            pass
        return ""

    def delete_selection(self, w):
        try:
            if self.is_text(w):
                w.delete("sel.first", "sel.last")
            elif w.selection_present():
                w.delete("sel.first", "sel.last")
        except tk.TclError:
            pass

    def set_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update_idletasks()

    def _do_action(self, act, w):
        if act == "copy":
            sel = self.get_selection(w)
            if sel:
                self.set_clipboard(sel)
                self.flash(self.t("copied"))
        elif act == "cut":
            sel = self.get_selection(w)
            if sel:
                self.set_clipboard(sel)
                self.delete_selection(w)
                self.flash(self.t("copied"))
        elif act == "paste":
            self.paste_with_check(w)
        elif act == "select_all":
            if self.is_text(w):
                w.tag_add("sel", "1.0", "end-1c")
                w.mark_set("insert", "end-1c")
            else:
                w.select_range(0, tk.END)
                w.icursor(tk.END)
        elif act == "undo":
            self._undo(w, redo=False)
        elif act == "redo":
            self._undo(w, redo=True)
        elif act == "clear":
            self.set_content(w, "")

    def _snap(self, w):
        h = w._hist
        v = w.get()
        if v != h["last"]:
            h["undo"].append(h["last"])
            h["undo"] = h["undo"][-100:]
            h["redo"].clear()
            h["last"] = v

    def _undo(self, w, redo):
        if self.is_text(w):
            try:
                w.edit_redo() if redo else w.edit_undo()
            except tk.TclError:
                pass
            return
        self._snap(w)
        h = w._hist
        src, dst = (h["redo"], h["undo"]) if redo else (h["undo"], h["redo"])
        if not src:
            return
        dst.append(h["last"])
        value = src.pop()
        w.delete(0, tk.END)
        w.insert(0, value)
        h["last"] = value

    def paste_with_check(self, w):
        try:
            text = self.clipboard_get()
        except tk.TclError:
            return
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        if not self.is_text(w):
            text = text.replace("\n", " ")
        if is_code_or_script(text):
            if not messagebox.askyesno(self.t("code_warning_title"), self.t("code_warning_msg")):
                return
        self.delete_selection(w)
        w.insert(tk.INSERT, text)
        if self.is_text(w):
            w.see(tk.INSERT)
            w.edit_separator()
        else:
            self._snap(w)

    def get_content(self, w):
        return w.get("1.0", "end-1c") if self.is_text(w) else w.get()

    def set_content(self, w, value):
        if self.is_text(w):
            w.delete("1.0", tk.END)
            w.insert("1.0", value)
            w.edit_separator()
        else:
            w.delete(0, tk.END)
            w.insert(0, value)
            self._snap(w)

    def copy_all(self, w):
        text = self.get_content(w).strip()
        if text:
            self.set_clipboard(text)
            self.flash(self.t("copied"))
        else:
            self.flash(self.t("nothing_copy"), C_ORANGE)

    def show_context_menu(self, event):
        w = event.widget
        w.focus_set()
        m = tk.Menu(self, tearoff=0, bg=C_PANEL2, fg=C_TEXT, activebackground=C_PURPLE,
                    activeforeground="#ffffff", bd=0, font=(self.F, 10))
        items = [("cut", "cut", "Ctrl+X"), ("copy", "copy", "Ctrl+C"),
                 ("paste", "paste", "Ctrl+V"), ("undo", "undo", "Ctrl+Z"),
                 ("redo", "redo", "Ctrl+Y")]
        for key, act, accel in items:
            label = self.t(key).replace("📋 ", "").replace("📄 ", "")
            m.add_command(label=f"{label}\t{accel}", command=lambda a=act: self._do_action(a, w))
        m.add_separator()
        m.add_command(label=f"{self.t('select_all')}\tCtrl+A", command=lambda: self._do_action("select_all", w))
        m.add_command(label=self.t("clear_field"), command=lambda: self._do_action("clear", w))
        try:
            m.tk_popup(event.x_root, event.y_root)
        finally:
            m.grab_release()
        return "break"

    def build_layout(self):
        self.columnconfigure(1, weight=5, uniform="c")
        self.columnconfigure(2, weight=5, uniform="c")
        self.rowconfigure(1, weight=1)

        self.build_header()
        self.build_sidebar()

        center = tk.Frame(self, bg=C_BG)
        center.grid(row=1, column=1, sticky="nsew", padx=(0, 8), pady=(0, 4))
        center.columnconfigure(0, weight=1)
        center.rowconfigure(1, weight=1)
        self.build_polybius(center)
        self.build_io(center)

        right = tk.Frame(self, bg=C_BG)
        right.grid(row=1, column=2, sticky="nsew", padx=(0, 10), pady=(0, 4))
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)
        self.build_caesar(right)
        self.build_vigenere(right)

        self.status = tk.Label(self, bg=C_BG, fg=C_CYAN, anchor="w",
                               font=(self.F, 10, "bold"), padx=12)
        self.status.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 4))

    def build_header(self):
        head = tk.Frame(self, bg=C_PANEL, highlightthickness=2,
                        highlightbackground=C_BLUE, highlightcolor=C_BLUE)
        head.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=(8, 6))
        head.columnconfigure(1, weight=1)

        logo = tk.Canvas(head, width=46, height=46, bg=C_PANEL, highlightthickness=0)
        logo.grid(row=0, column=0, padx=(12, 6), pady=4)
        logo.create_polygon(23, 2, 42, 9, 40, 29, 23, 44, 6, 29, 4, 9, outline=C_MAGENTA,
                            fill=C_PANEL2, width=2)
        logo.create_rectangle(15, 20, 31, 32, fill=C_MAGENTA, outline="")
        logo.create_arc(17, 10, 29, 25, start=0, extent=180, style="arc", outline=C_MAGENTA, width=2)

        self.lbl_title = tk.Label(head, bg=C_PANEL, fg=C_CYAN, anchor="w", font=(self.F, 20, "bold"))
        self.lbl_title.grid(row=0, column=1, sticky="w")

        box = tk.Frame(head, bg=C_PANEL)
        box.grid(row=0, column=2, padx=12)
        self.lbl_ui_lang = tk.Label(box, bg=C_PANEL, fg=C_MUTED, font=(self.F, 8))
        self.lbl_ui_lang.pack(anchor="e")
        self.combo_ui_lang = ttk.Combobox(box, values=["🇺🇦  Українська", "🇬🇧  English"],
                                          state="readonly", width=15,
                                          style="Neon.TCombobox", font=(self.F, 9))
        self.combo_ui_lang.current(0)
        self.combo_ui_lang.pack()
        self.combo_ui_lang.bind("<<ComboboxSelected>>", self.change_ui_language)

    def build_sidebar(self):
        side = tk.Frame(self, bg=C_PANEL, highlightthickness=2,
                        highlightbackground=C_PURPLE, highlightcolor=C_PURPLE, width=210)
        side.grid(row=1, column=0, sticky="ns", padx=(10, 8), pady=(0, 4))
        side.grid_propagate(False)
        side.pack_propagate(False)
        pad = dict(fill="x", padx=10, pady=5)
        
        self.button(side, "nav_encrypt", self.poly_encrypt, C_MAGENTA, anchor="w", font_size=10).pack(**dict(pad, pady=(12, 5)))
        self.button(side, "nav_decrypt", self.poly_decrypt, C_PURPLE, anchor="w", font_size=10).pack(**pad)
        self.button(side, "nav_analyze", self.analyze_all, C_CYAN, anchor="w", font_size=10).pack(**pad)

        self.copy_label = tk.Label(
            side, text="© Radchenko Illia 2026",
            bg=C_PANEL, fg=C_MUTED, font=(self.F, 8, "bold"),
            wraplength=180, justify="center"
        )
        self.copy_label.pack(side="bottom", pady=(0, 12))

        self.button(side, "nav_help", self.show_help, C_ORANGE, anchor="w", font_size=10).pack(side="bottom", **pad)
        self.button(side, "nav_clear", self.clear_all, C_BLUE, anchor="w", font_size=10).pack(side="bottom", **pad)

    # --- ПАНЕЛЬ ПОЛІБІЯ ---
    def build_polybius(self, parent):
        outer, body = self.panel(parent, "poly_title", C_PURPLE)
        outer.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        r0 = tk.Frame(body, bg=C_PANEL)
        r0.pack(fill="x", pady=2)
        self.label(r0, "alphabet").pack(side="left", padx=(0, 6))
        self.poly_combo = self.combo(r0, "poly", 30)
        self.poly_combo.pack(side="left")
        self.poly_combo.bind("<<ComboboxSelected>>", self.on_poly_lang_change)
        self.poly_tip = ToolTip(self.poly_combo, "")

        r1 = tk.Frame(body, bg=C_PANEL)
        r1.pack(fill="x", pady=2)
        self.label(r1, "rows").pack(side="left")
        self.spin_rows = self.spinbox(r1, 2, 9, 7, self.update_matrix_display)
        self.spin_rows.pack(side="left", padx=(4, 10))
        self.label(r1, "cols").pack(side="left")
        self.spin_cols = self.spinbox(r1, 2, 9, 5, self.update_matrix_display)
        self.spin_cols.pack(side="left", padx=(4, 10))
        self.button(r1, "update_matrix", self.update_matrix_display, C_BLUE, font_size=9).pack(side="right")

        r2 = tk.Frame(body, bg=C_PANEL)
        r2.pack(fill="x", pady=2)
        self.label(r2, "keyword").pack(side="left", padx=(0, 6))
        self.key_var = tk.StringVar()
        self.poly_key = self.entry(r2, 18)
        self.poly_key.config(textvariable=self.key_var)
        self.poly_key.pack(side="left")
        self.key_var.trace_add("write", lambda *a: self.update_matrix_display())
        self.button(r2, "paste", lambda: self.paste_with_check(self.poly_key), C_CYAN, font_size=9).pack(side="left", padx=6)

        r3 = tk.Frame(body, bg=C_PANEL)
        r3.pack(fill="x", pady=2)
        self.label(r3, "mode", C_MUTED).pack(side="left", padx=(0, 6))
        self.mode_var = tk.StringVar(value="coords")
        self.radio(r3, "coords", self.mode_var, "coords").pack(side="left", padx=2)
        self.radio(r3, "shift", self.mode_var, "shift").pack(side="left", padx=2)

        self.lbl_warn = tk.Label(body, bg=C_PANEL, fg=C_MAGENTA, anchor="w", font=(self.F, 8, "bold"))
        self.lbl_warn.pack(fill="x")
        self.matrix_frame = tk.Frame(body, bg=C_PANEL)
        self.matrix_frame.pack(pady=(2, 0))

    def poly_code(self):
        return ALPH_CODES[self.poly_combo.current()]

    def on_poly_lang_change(self, _=None):
        code = self.poly_code()
        dims = {"UA32": (7, 5), "UA33": (7, 5), "EN": (5, 5)}[code]
        for sp, v in zip((self.spin_rows, self.spin_cols), dims):
            sp.delete(0, tk.END)
            sp.insert(0, str(v))
        self.poly_tip.set_text(self.t(f"tooltip_{code}"))
        self.update_matrix_display()

    def poly_params(self, show_error=False):
        try:
            r, c = int(self.spin_rows.get()), int(self.spin_cols.get())
            if not (2 <= r <= 9 and 2 <= c <= 9):
                raise ValueError
        except ValueError:
            if show_error:
                messagebox.showwarning(self.t("warn"), self.t("err_dims"))
            return None
        code = self.poly_code()
        need = len(POLY_ALPHABETS[code])
        if r * c < need:
            if show_error:
                messagebox.showwarning(self.t("warn"), self.t("err_capacity").format(r=r, c=c, cap=r * c, need=need))
            return None
        return build_polybius_matrix(r, c, self.poly_key.get(), code), code

    def update_matrix_display(self, *_):
        for w in self.matrix_frame.winfo_children():
            w.destroy()
        try:
            r, c = int(self.spin_rows.get()), int(self.spin_cols.get())
        except ValueError:
            return
        if not (2 <= r <= 9 and 2 <= c <= 9):
            return
        need = len(POLY_ALPHABETS[self.poly_code()])
        if r * c < need:
            self.lbl_warn.config(text=self.t("capacity_warn").format(cap=r * c, need=need))
            return
        self.lbl_warn.config(text="")
        matrix = build_polybius_matrix(r, c, self.poly_key.get(), self.poly_code())
        hdr = dict(bg=C_PANEL, fg=C_CYAN, font=(self.F, 9, "bold"), width=3)
        for j in range(c):
            tk.Label(self.matrix_frame, text=str(j + 1), **hdr).grid(row=0, column=j + 1, padx=1)
        for i in range(r):
            tk.Label(self.matrix_frame, text=str(i + 1), **hdr).grid(row=i + 1, column=0, padx=1)
            for j in range(c):
                ch = matrix[i][j]
                tk.Label(self.matrix_frame, text="␣" if ch == " " else ch,
                         bg=C_FIELD, fg=C_TEXT, width=3, font=(self.FM, 10, "bold"),
                         highlightthickness=1, highlightbackground=C_PURPLE
                         ).grid(row=i + 1, column=j + 1, padx=1, pady=1)

    def build_io(self, parent):
        outer, body = self.panel(parent, "io_title", C_BLUE)
        outer.grid(row=1, column=0, sticky="nsew")
        body.columnconfigure(0, weight=1)
        body.rowconfigure(1, weight=1)
        body.rowconfigure(4, weight=1)

        top = tk.Frame(body, bg=C_PANEL)
        top.grid(row=0, column=0, sticky="ew")
        self.button(top, "copy", lambda: self.copy_all(self.poly_input), C_CYAN, font_size=8).pack(side="right", padx=(4, 0))
        self.button(top, "paste", lambda: self.paste_with_check(self.poly_input), C_CYAN, font_size=8).pack(side="right")

        box, self.poly_input = self.textbox(body, 2)
        box.grid(row=1, column=0, sticky="nsew", pady=2)

        btns = tk.Frame(body, bg=C_PANEL)
        btns.grid(row=2, column=0, pady=3)
        self.button(btns, "encrypt", self.poly_encrypt, C_CYAN, width=15).pack(side="left", padx=6)
        self.button(btns, "decrypt", self.poly_decrypt, C_MAGENTA, width=15).pack(side="left", padx=6)

        mid = tk.Frame(body, bg=C_PANEL)
        mid.grid(row=3, column=0, sticky="ew")
        self.label(mid, "output_text", C_MUTED, True).pack(side="left")
        self.button(mid, "copy_res", lambda: self.copy_all(self.poly_output), C_CYAN, font_size=8).pack(side="right")

        box, self.poly_output = self.textbox(body, 2)
        box.grid(row=4, column=0, sticky="nsew", pady=2)

    def poly_encrypt(self):
        text = self.get_content(self.poly_input).strip()
        if not text:
            self.flash(self.t("no_text"), C_ORANGE)
            return
        params = self.poly_params(show_error=True)
        if not params:
            return
        matrix, code = params
        self.set_content(self.poly_output, polybius_encrypt(text, matrix, code, self.mode_var.get()))

    def poly_decrypt(self):
        text = self.get_content(self.poly_input).strip()
        if not text:
            self.flash(self.t("no_text"), C_ORANGE)
            return
        params = self.poly_params(show_error=True)
        if not params:
            return
        matrix, code = params
        self.set_content(self.poly_output, polybius_decrypt(text, matrix, code, self.mode_var.get()))

    # --- ПАНЕЛЬ ЦЕЗАРЯ ---
    def build_caesar(self, parent):
        outer, body = self.panel(parent, "caesar_title", C_MAGENTA)
        outer.grid(row=0, column=0, sticky="nsew", pady=(0, 6))
        body.columnconfigure(0, weight=1)
        body.rowconfigure(3, weight=1)
        body.rowconfigure(6, weight=1)

        r0 = tk.Frame(body, bg=C_PANEL)
        r0.grid(row=0, column=0, sticky="ew", pady=1)
        self.label(r0, "alphabet").pack(side="left", padx=(0, 6))
        self.caesar_combo = self.combo(r0, "full", 28)
        self.caesar_combo.pack(side="left")

        r_mode = tk.Frame(body, bg=C_PANEL)
        r_mode.grid(row=1, column=0, sticky="ew", pady=2)
        self.caesar_kw_var = tk.StringVar(value="no_kw")
        self.radio(r_mode, "caesar_mode_nokey", self.caesar_kw_var, "no_kw", self.toggle_caesar_kw).pack(side="left", padx=(0, 8))
        self.radio(r_mode, "caesar_mode_key", self.caesar_kw_var, "with_kw", self.toggle_caesar_kw).pack(side="left")

        r_key = tk.Frame(body, bg=C_PANEL)
        r_key.grid(row=2, column=0, sticky="ew", pady=2)
        self.label(r_key, "caesar_shift").pack(side="left", padx=(0, 4))
        self.caesar_shift_spin = self.spinbox(r_key, 0, 33, 5)
        self.caesar_shift_spin.pack(side="left", padx=(0, 10))

        self.lbl_caesar_kw = self.label(r_key, "caesar_kw_lbl")
        self.lbl_caesar_kw.pack(side="left", padx=(0, 4))
        self.caesar_kw_entry = self.entry(r_key, 12)
        self.caesar_kw_entry.pack(side="left")
        self.caesar_kw_entry.config(state="disabled")

        box, self.caesar_input = self.textbox(body, 2)
        box.grid(row=3, column=0, sticky="nsew", pady=2)

        r_btns = tk.Frame(body, bg=C_PANEL)
        r_btns.grid(row=4, column=0, pady=3)
        self.button(r_btns, "caesar_enc", self.caesar_encrypt, C_CYAN, font_size=9).pack(side="left", padx=3)
        self.button(r_btns, "caesar_dec", self.caesar_decrypt, C_PURPLE, font_size=9).pack(side="left", padx=3)
        self.button(r_btns, "caesar_analyze_btn", self.break_caesar, C_ORANGE, font_size=9).pack(side="left", padx=3)

        r6 = tk.Frame(body, bg=C_PANEL)
        r6.grid(row=5, column=0, sticky="ew")
        self.label(r6, "output_text", C_MUTED, True).pack(side="left")
        self.button(r6, "copy_res", lambda: self.copy_all(self.caesar_output), C_CYAN, font_size=8).pack(side="right")

        box, self.caesar_output = self.textbox(body, 3)
        box.grid(row=6, column=0, sticky="nsew", pady=2)

    def toggle_caesar_kw(self):
        if self.caesar_kw_var.get() == "with_kw":
            self.caesar_kw_entry.config(state="normal")
        else:
            self.caesar_kw_entry.config(state="disabled")

    def caesar_code(self):
        return ALPH_CODES[self.caesar_combo.current()]

    def caesar_encrypt(self):
        text = self.get_content(self.caesar_input).strip()
        if not text:
            self.flash(self.t("no_text"), C_ORANGE)
            return
        try:
            shift = int(self.caesar_shift_spin.get())
        except ValueError:
            shift = 0
        kw = self.caesar_kw_entry.get() if self.caesar_kw_var.get() == "with_kw" else ""
        res = caesar_cipher_transform(text, shift, kw, self.caesar_code(), decrypt=False)
        self.set_content(self.caesar_output, res)

    def caesar_decrypt(self):
        text = self.get_content(self.caesar_input).strip()
        if not text:
            self.flash(self.t("no_text"), C_ORANGE)
            return
        try:
            shift = int(self.caesar_shift_spin.get())
        except ValueError:
            shift = 0
        kw = self.caesar_kw_entry.get() if self.caesar_kw_var.get() == "with_kw" else ""
        res = caesar_cipher_transform(text, shift, kw, self.caesar_code(), decrypt=True)
        self.set_content(self.caesar_output, res)

    def break_caesar(self):
        text = self.get_content(self.caesar_input).strip()
        if not text:
            self.flash(self.t("no_text"), C_ORANGE)
            return
        code = self.caesar_code()
        results = caesar_analyze(text, code)
        lines = [self.t("caesar_header"), ""]
        for i, (score, shift, dec) in enumerate(results):
            mark = f"  {self.t('best_mark')}" if i == 0 else ""
            lines.append(f"[{self.t('shift_lbl')} k = {shift:2d} | "
                         f"{self.t('score_lbl')} = {score:.5f}]: {dec}{mark}")
        self.set_content(self.caesar_output, "\n".join(lines))

    # --- ПАНЕЛЬ ВІЖЕНЕРА ---
    def build_vigenere(self, parent):
        outer, body = self.panel(parent, "vig_title", C_CYAN)
        outer.grid(row=1, column=0, sticky="nsew")
        body.columnconfigure(0, weight=1)
        body.rowconfigure(2, weight=1)
        body.rowconfigure(6, weight=2)

        r0 = tk.Frame(body, bg=C_PANEL)
        r0.grid(row=0, column=0, sticky="ew", pady=1)
        self.label(r0, "alphabet").pack(side="left", padx=(0, 6))
        self.vig_combo = self.combo(r0, "full", 28)
        self.vig_combo.pack(side="left")

        r1 = tk.Frame(body, bg=C_PANEL)
        r1.grid(row=1, column=0, sticky="ew")
        self.label(r1, "vig_input", C_MUTED, True).pack(side="left")
        self.button(r1, "paste", lambda: self.paste_with_check(self.vig_input), C_CYAN, font_size=8).pack(side="right")

        box, self.vig_input = self.textbox(body, 2)
        box.grid(row=2, column=0, sticky="nsew", pady=2)

        r3 = tk.Frame(body, bg=C_PANEL)
        r3.grid(row=3, column=0, sticky="ew", pady=2)
        self.label(r3, "vig_key").pack(side="left", padx=(0, 4))
        self.vig_key = self.entry(r3, 14)
        self.vig_key.pack(side="left")
        self.label(r3, "vig_len").pack(side="left", padx=(10, 4))
        self.vig_len = self.spinbox(r3, 0, 30, 0)
        self.vig_len.pack(side="left")

        r4 = tk.Frame(body, bg=C_PANEL)
        r4.grid(row=4, column=0, pady=3)
        self.button(r4, "vig_break", self.break_vigenere, C_CYAN, font_size=9).pack(side="left", padx=3)
        self.button(r4, "vig_enc_key", lambda: self.vig_apply(False), C_MAGENTA, font_size=8).pack(side="left", padx=3)
        self.button(r4, "vig_dec_key", lambda: self.vig_apply(True), C_PURPLE, font_size=8).pack(side="left", padx=3)

        r6 = tk.Frame(body, bg=C_PANEL)
        r6.grid(row=5, column=0, sticky="ew")
        self.label(r6, "output_text", C_MUTED, True).pack(side="left")
        self.button(r6, "copy_res", lambda: self.copy_all(self.vig_output), C_CYAN, font_size=8).pack(side="right")

        box, self.vig_output = self.textbox(body, 4)
        box.grid(row=6, column=0, sticky="nsew", pady=2)

    def vig_code(self):
        return ALPH_CODES[self.vig_combo.current()]

    def break_vigenere(self):
        text = self.get_content(self.vig_input).strip()
        if not text:
            self.flash(self.t("no_text"), C_ORANGE)
            return
        code = self.vig_code()
        try:
            forced = max(0, int(self.vig_len.get() or 0))
        except ValueError:
            forced = 0
        res = vigenere_analyze(text, code, forced)
        if res is None:
            messagebox.showwarning(self.t("warn"), self.t("short_text"))
            return
        self.set_content(self.vig_key, res["key"])
        top = sorted(res["ic_table"], key=lambda x: x[1], reverse=True)[:5]
        ic_line = ", ".join(f"{k}: {ic:.4f}" for k, ic in top)
        lines = [
            self.t("vig_len_found").format(k=res["k"], forced=self.t("vig_forced") if res["forced"] else ""),
            self.t("vig_ic").format(exp=EXPECTED_IC[code]),
            "  " + ic_line,
            self.t("vig_key_found").format(key=res["key"]),
            "",
            self.t("vig_decrypted"),
            res["text"],
        ]
        if res["n"] < res["k"] * 25:
            lines += ["", self.t("vig_hint").format(n=res["n"])]
        self.set_content(self.vig_output, "\n".join(lines))

    def vig_apply(self, decrypt):
        text = self.get_content(self.vig_input).strip()
        if not text:
            self.flash(self.t("no_text"), C_ORANGE)
            return
        out = vigenere_crypt(text, self.vig_key.get(), self.vig_code(), decrypt)
        if out is None:
            self.flash(self.t("no_key"), C_ORANGE)
            return
        head = self.t("vig_result_dec" if decrypt else "vig_result_enc")
        self.set_content(self.vig_output, f"{head}\n{out}")

    def analyze_all(self):
        if self.get_content(self.caesar_input).strip():
            self.break_caesar()
        if self.get_content(self.vig_input).strip():
            self.break_vigenere()
        if not (self.get_content(self.caesar_input).strip() or self.get_content(self.vig_input).strip()):
            self.flash(self.t("no_text"), C_ORANGE)

    def clear_all(self):
        for w in (self.poly_input, self.poly_output, self.caesar_input,
                  self.caesar_output, self.vig_input, self.vig_output,
                  self.poly_key, self.caesar_kw_entry, self.vig_key):
            self.set_content(w, "")
        self.flash(self.t("cleared"))

    def show_help(self):
        messagebox.showinfo(self.t("nav_help").replace("❓", "").strip(), self.t("help_text"))

    def change_ui_language(self, _=None):
        self.ui_lang = "UA" if self.combo_ui_lang.current() == 0 else "EN"
        self.retranslate_ui()

    def retranslate_ui(self):
        self.title(self.t("title"))
        self.lbl_title.config(text=self.t("title"))
        self.lbl_ui_lang.config(text=self.t("lang_label"))
        for widget, key in self._i18n:
            widget.config(text=self.t(key))
        for cb, kind in self._combos:
            idx = cb.current()
            cb["values"] = self.alph_names(kind)
            cb.current(max(idx, 0))
        self.poly_tip.set_text(self.t(f"tooltip_{self.poly_code()}"))
        self.update_matrix_display()

# ==================== ТОЧКА ВХОДУ ====================
if __name__ == "__main__":
    try:
        app = CryptoApp()
        app.mainloop()
    except Exception as e:
        err_msg = traceback.format_exc()
        print("ПОМИЛКА ПРИ ЗАПУСКУ:\n", err_msg)
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", f"Сталася помилка:\n{e}\n\n{err_msg}")
        except Exception:
            pass