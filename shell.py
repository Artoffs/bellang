import basicbellang

file = open('code.txt', encoding="utf-8")
text_full = file.read()
text_full = text_full.split('\n')

for line in text_full:
    result, error = basicbellang.run("<праграмма>", line)

    if error:
        print(error.as_string())
    elif result:
        print(result)
