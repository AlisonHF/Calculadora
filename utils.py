import re



NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')


# Função que checa um número e um ponto
def isNumOrDot(string : str):
    return bool(NUM_OR_DOT_REGEX.search(string))


# Função que checa se é vazio ou não
def isEmpty(string: str):
    return len(string) == 0


# Função que verifica se um número é valido 
def isValidNumber(string: str):
    valid = False
    try:
        float(string)
        valid = True
    except ValueError:
        valid = False
    return valid


# Função que converte um número float que pode ser int
def converToNumber(string: str):
    number = float(string)

    if number.is_integer():
        number = int(number)
        return number
    return number
