import sqlite3
from itertools import product
from tqdm import tqdm
import os
import re

# Phonemes dictionary
_ = ''
phonemes = {
    'vowels': {
        'i': '', 'e': '', 'o': '', 'é': '',
        'a': 'éú', 'á': '', 'ó': 'é', 'ú': '', 'u': ''
    },
    'consonants': {
        'x': '', 'h': 'wy', 'w': '', 'y': '',
        'p': 'wylr', 'c': 'wr', 't': 'wy',
        'þ': '', 'f': 'wy', 'k': 'wylr', 's': 'wyptklmnr',
        'ś': 'wypr', 'ź': 'w', 'l': '', 'm': 'wy',
        'n': 'y', 'r': '', 'ŋ': '', 'b': 'wylr',
        'j': '', 'd': 'wy', 'ð': 'wy', 'v': 'wylr',
        'g': 'wylr', 'z': 'wr'
    }
}

# SQLite database path
DB_PATH = 'assets/fonts/Abugida/output.db'

def setup_database():
    """Creates SQLite database and words table with a 'cluster' column."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE,
            cluster TEXT
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS cluster_index ON words(cluster)')
    conn.commit()
    conn.close()

def extract_cluster(word):
    """Extracts the starting consonant cluster from a word."""
    match = re.match(r'^[^AEIOUÉÁÓÚ]+', word)  # Matches the starting consonants
    return match.group(0) if match else word[0]  # If no cluster, return first letter

def insert_word(cursor, word):
    """Inserts a word and its starting cluster into the SQLite database."""
    cluster = extract_cluster(word)
    try:
        cursor.execute("INSERT INTO words (word, cluster) VALUES (?, ?)", (word, cluster))
    except sqlite3.IntegrityError:
        pass  # Skip duplicates

def generate_words():
    """Generates words and saves them to an SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    syllable_list = []
    consonant_pairs = list(phonemes['consonants'].keys())
    vowel_pairs = list(phonemes['vowels'].keys())

    for c in consonant_pairs:
        syllable_list.append(c)
        for v in vowel_pairs:
            syllable_list.append(c + v)

    syl = 2  # Number of syllables per word

    for i in range(1, syl + 1):
        for word_tuple in product(syllable_list, repeat=i):
            word_str = ''.join(word_tuple).upper()
            
            # Skip words with double consonants or vowels
            if any(word_str[j] == word_str[j + 1] for j in range(len(word_str) - 1)):
                continue
            
            # Ensure 'X' only appears at the start
            if 'X' in word_str and word_str.index('X') != 0:
                continue
            
            insert_word(cursor, word_str)

    conn.commit()
    conn.close()

def search_by_cluster(cluster):
    """Retrieves words that start with a specific consonant cluster, sorted alphabetically."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT word FROM words WHERE cluster = ? ORDER BY word", (cluster,))
    results = cursor.fetchall()
    conn.close()
    return [r[0] for r in results if r[0] != 'X']

# Run script
setup_database()
generate_words()

totalWords = len(phonemes['consonants'])
with open('sort/index.html','w',encoding='utf-8') as home:
    home.write('''<style>
body {
    font-family: Verdana;
    padding: 5rem;
    font-size: 3rem;
}
</style>
<h1>Abugida Words, Sorted By The Initial Consonant</h1>''')
for index, consonant in enumerate(phonemes['consonants']):
    if consonant == 'x': fileName = 'vowels'
    else: fileName = consonant.upper() + consonant
    address = 'initialPhonemes/'
    file = f"sort/{address}{fileName}.html"
    with open('sort/index.html','a',encoding='utf-8') as home:
        with open(file, 'w', encoding='utf-8') as f:
            f.write('''<style>
body {
    font-family: Verdana;
    padding: 5rem;
    font-size: 5rem;
}
h1, h2, h3 {
    font-family: Verdana;
}
h3 {
    font-size: 0.5em;
}
p {
    font-size: 2em;
}
b {
    font-family: Abugida;
    font-size: 0.75em;
}
@font-face {
    font-family: Abugida;
    src: url(
        "sort/abugida.ttf"
    )
    format(
        "truetype"
    )
}
</style>
<a href='../index.html'><h3><--Back</h3></a>''')
            words = search_by_cluster(consonant.capitalize())  # Fetch words once per consonant
            f.write(f'\n<h1>{fileName.capitalize()}</h1>')
            for word in words:
                num = f'{(words.index(word) + 1):,}'
                latinWord = word.replace('X','').upper()
                abugidaWord = word.lower()
                f.write(f'\n<p>{latinWord}:<b>{abugidaWord}</b></p>')
        home.write(f"\n<li><a href='{address}{fileName}.html'>{fileName.capitalize()}</a></li>")