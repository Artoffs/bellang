import basicbellang

while True:
    text = input("BelLang>>>")
    result, error = basicbellang.run("<праграмма>", text)

    if error:
        print(error.as_string())
    elif result:
        print(result)
