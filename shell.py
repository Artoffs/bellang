import basicbellang

file = open('code.txt', encoding="utf-8")
text_full = file.read().split('\n')


for line in text_full:
    result, error = basicbellang.run("<праграмма>", line)

while True:
    text = str(input("BELLANG>>> "))

    result, error = basicbellang.run("<праграмма>", text)

    if error:
        print(error.as_string())
    elif result:
        print(result)
