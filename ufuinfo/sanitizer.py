# -*- coding: utf-8 -*-


import codecs
from unidecode import unidecode


def remove_espaco(string):
    pass

    
def remove_espaco_extra(string):
    """Remove espaço duplicado, tabs e outros *white-space* em strings.

    Arguments:

        string (str): A string a ser modificada.

    Returns:

        A string modificada.
    """
    return ' '.join(string.split())


def remove_especiais(string):
    """Substitui caracteres especiais em strings.

    Arguments:

        string (str): A string a ser modificada.

    Returns:

        A string modificada.
    """
    return unidecode(codecs.decode(string))


def normaliza_dict(dictionary):
    pass
