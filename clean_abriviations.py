with open('german_abbreviations.txt', 'r', encoding='utf-8') as fin:
    words = fin.read().split('\n')

new_words = []

for each_word in words:
    if '.' in each_word:
        new_words.append(each_word)

with open('german_abbreviation_new.txt', 'w', encoding='utf-8') as fout:
    fout.write('\n'.join(new_words))