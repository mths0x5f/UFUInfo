# -*- coding: utf-8 -*-


from unidecode import unidecode


def trata_espaco_extra(string):
    """Remove espaço duplicado, tabs e outros *white-space* em strings.

    Arguments:

        string (str): A string a ser modificada.

    Returns:

        A string modificada.
    """
    try:
        return ' '.join(string.decode('utf-8').split())  # utf-8
    except UnicodeEncodeError:
        return ' '.join(string.split())  # pure unicode


def trata_espaco(string):
    """Substitui espaço pelo caractere '-' (hífen, menos) em strings.

    Arguments:

        string (str): A string a ser modificada.

    Returns:

        A string modificada.
    """
    try:
        return string.decode('utf-8').replace(' ', '-')  # utf-8
    except UnicodeEncodeError:
        return string.replace(' ', '-')  # pure unicode


def trata_especiais(string):
    """Substitui caracteres especiais pelos seus equivalentes em strings.

    Arguments:

        string (str): A string a ser modificada.

    Returns:

        A string modificada.
    """
    try:
        return unidecode(string.decode('utf-8'))  # utf-8
    except UnicodeEncodeError:
        return unidecode(string)  # pure unicode


def normaliza_chave(chave):

    chave = trata_espaco_extra(chave)
    chave = trata_espaco(chave)
    chave = trata_especiais(chave)

    return chave.lower()


def normaliza_dict(dictionary):
    pass


if __name__ == '__main__':
    print normaliza_chave('Santa          Mônica')
