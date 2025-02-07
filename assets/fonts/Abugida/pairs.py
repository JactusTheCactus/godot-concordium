from itertools import product
from tqdm import tqdm

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
        if c != cPrev:
            cvPairList.append('\n\n## ')
            if c != "":
                cvPairList.append(f'{c}\n### ')
            else:
                cvPairList.append('Vowels\n### ')
        if c == "":
            cvPairList.append(f"`{v}` ")
        else:
            cvPairList.append(f"`{c}{v}` ")
        cPrev = c

syllables = "# Consonant-Vowel Pairs\n"

for cv in cvPairList:
    if cv.__len__() <= 7:
        syllables += cv.upper()
    else:
        syllables += cv.capitalize()

def genWords(syl):
    print()
    if "" in consonantPairList:
        consonantPairList.remove("")
    syllableList = []
    for c in consonantPairList:
        for v in vowelPairList:
            syllableList.append(c + v)
    total_words = len(syllableList) ** syl  # Calculate total words
    with open('assets/fonts/Abugida/output.txt','w',encoding='utf-8') as f:
        with tqdm(total=total_words, desc="Processing", unit="word", ascii="-=", bar_format="{l_bar}{bar} {n_fmt} {unit}s [{remaining}, {rate_fmt}]") as pbar:
            for word in product(syllableList, repeat=syl):
                newWord = f'{''.join(word).upper()}'
                if newWord != f'{''.join('źwú').upper()}':
                    newWord += '\n'
                f.write(newWord)
                pbar.update(1)
    print(f'''
Number of Possible Syllables: {syllableList.__len__():,}
Length of Words: {syl} Syllables
Number of Words: {syllableList.__len__() ** syl:,}''')

genWords(1)

with open('assets/fonts/Abugida/markdown.md', 'w', encoding='utf-8') as f:
    f.write(markdown)

with open('assets/fonts/Abugida/syllables.md', 'w', encoding='utf-8') as f:
    f.write(syllables)