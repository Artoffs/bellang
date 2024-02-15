import basicbellang

while True:
    text = input(">")
    result, error = basicbellang.run("<stdin1>", text)

    if error:
        print(error.as_string())
    else:
        print(result)
