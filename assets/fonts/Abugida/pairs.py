from itertools import product
from tqdm import tqdm
import os

# Phonemes dictionary with consonants and vowels, now with illegal combinations as strings
_ = ''
phonemes = {
    'vowels': {
        'i': '',
        'e': '',
        'o': '',
        'é': '',
        'a': 'éú',
        'á': '',
        'ó': 'é',
        'ú': '',
        'u': ''
    },
    'consonants': {
        'x': '',
        'h': 'wy',
        'w': '',
        'y': '',
        'p': 'wylr',
        'c': 'wr',
        't': 'wy',
        'þ': '',
        'f': 'wy',
        'k': 'wylr',
        's': 'wyptklmnr',
        'ś': 'wypr',
        'ź': 'w',
        'l': '',
        'm': 'wy',
        'n': 'y',
        'r': '',
        'ŋ': '',
        'b': 'wylr',
        'j': '',
        'd': 'wy',
        'ð': 'wy',
        'v': 'wylr',
        'g': 'wylr',
        'z': 'wr'
    }
}

def getPairs(phoneme_type, label):
    output = f"\n## {label}\n### "
    phonemes_data = phonemes[phoneme_type]
    
    pairSet = set()  # Use a set to prevent duplicates
    
    for x in phonemes_data:
        pairSet.add(x)  # Add individual phonemes
        illegal = True  
        addEntry = ""
        for y in phonemes_data:
            if x == y:
                continue
            if y in phonemes_data[x]:  # Check illegal combinations
                addEntry += f"`{x.upper()}{y.upper()}` "
                pairSet.add(f"{x}{y}")  # Add the pair
                illegal = False
        if not illegal:
            output += addEntry
    return output, sorted(pairSet)  # Convert set to sorted list before returning


markdown = "# Doubles"
vowelPairs, vowelPairList = getPairs('vowels','Diphthongs (Vowel Pairs)')
markdown += vowelPairs
consonantPairs, consonantPairList = getPairs('consonants','Clusters (Consonant Pairs)')
markdown += consonantPairs

cvPairList = []
cPrev = None
vPrev = None

consonantPairList.append("")
consonantPairList.sort()
vowelPairList.sort()

cvPairList.sort()

for c in consonantPairList:
    for v in vowelPairList:
        if c != cPrev and cPrev is not None:
            if c != "":
                cvPairList.append(f'\n## {c}\n### ')
        if c != "":
            cvPairList.append(f'`{c}{v}` ')
        cPrev = c

syllables = "# Consonant-Vowel Pairs\n"

for cv in cvPairList:
    syllables += cv.upper()

def getFileData(size):
    sizeList = [
        'B',
        'KB',
        'MB',
        'GB',
        'TB',
        'PB',
        'EB',
        'ZB'
    ]
    sizeRange = 1
    sizeIndex = 0
    formattedFileSize = size
    while size >= sizeRange * 1000 and sizeIndex < len(sizeList) - 1:
        sizeRange *= 1000
        sizeIndex += 1
    formattedFileSize = size / sizeRange
    fileSizeUnit = sizeList[sizeIndex]
    file = f'{formattedFileSize.__round__(2):,} {fileSizeUnit}'
    return file

def genWords(file_path):
    print()
    syl = 1000
    while syl > 3:
        syl = 2# int(input('How Many Syllables? '))
        if syl > 3:
            n = 900 ** syl
            print(f'''
WARNING: Quantum Computer Not Detected.
This Process Will Crash Your Computer.
{str(n)[0]}e{len(str(n-1))} ({(n):,}) Is Too Many Characters.
{getFileData(n)} Is Too Large
Avoid.
''')
        else:
            continue
    if "" in consonantPairList:
        consonantPairList.remove("")
    syllableList = []
    for c in consonantPairList:
        syllableList.append(c)
        for v in vowelPairList:
            syllableList.append(c + v)
    total_words = 0
    for i in range(syl):
        total_words += len(syllableList) ** (syl - (i))
    with open(file_path,'w',encoding='utf-8') as f:
        with tqdm(total=total_words, desc="Processing", unit="word", ascii="->", bar_format="{l_bar}{bar} {n_fmt} {unit}s [{remaining}, {rate_fmt}]") as pbar:
            iteration = 0
            for i in range(syl + 1):
                if i > 0:
                    for word in product(syllableList, repeat=i):
                        iteration += 1
                        word_str = ''.join(word).upper()

                        # Skip words with double consonants or double vowels
                        skip_word = False
                        for j in range(len(word_str) - 1):
                            if (word_str[j] == word_str[j + 1] and 
                                (word_str[j] in phonemes['consonants'] or word_str[j] in phonemes['vowels'])):
                                skip_word = True
                                break  # No need to check further

                        # Ensure 'X' only appears at the start
                        if 'X' in word_str and word_str.index('X') != 0:
                            skip_word = True  # Mark word as invalid

                        if skip_word:
                            continue  # Skip writing this word

                        newWord = '\n' if iteration != 1 else ''
                        newWord += f'{word_str}  '
                        f.write(newWord)
                        pbar.update(1)

with open('assets/fonts/Abugida/markdown.md', 'w', encoding='utf-8') as f:
    f.write(markdown)

with open('assets/fonts/Abugida/syllables.md', 'w', encoding='utf-8') as f:
    f.write(syllables)

fileTypes = [
    'txt',
    'md'
]

for i in fileTypes:
    genWords(f'assets/fonts/Abugida/output.{i}')