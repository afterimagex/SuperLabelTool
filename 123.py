



words_file = './words.txt'
words_map = {}
with open(words_file, 'r', encoding='UTF-8') as wf:
    for _line in wf.readlines():
        line = _line.strip().split('|')
        key = line[1]
        value = line[2:]
        words_map[key] = value
        print(value)
