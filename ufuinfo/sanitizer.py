# -*- coding: utf-8 -*-
#
#                       Módulo de normalização e limpeza
#
#  This file is part of UFUInfo
#
#  Copyright (C) 2014  Matheus Silva Santos
#
#  UFUInfo is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  UFUInfo is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with UFUInfo.  If not, see <http://www.gnu.org/licenses/>.
#

u"""Módulo de normalização e limpeza.

Este módulo contém funções de limpeza de strings e normalização de estruturas
de dados utilizadas no projeto.
"""

from unidecode import unidecode


def trata_espaco_extra(string):
    u"""Remove espaço duplicado, tabs e outros *white-space*.

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
    u"""Substitui espaço pelo caractere '-' (hífen, menos).

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
    u"""Substitui caracteres especiais pelos seus equivalentes.

    Arguments:

        string (str): A string a ser modificada.

    Returns:

        A string modificada.
    """
    try:
        return unidecode(string.decode('utf-8'))  # utf-8
    except UnicodeEncodeError:
        return unidecode(string)  # pure unicode


def normaliza_chave(string):
    u"""Normaliza/padroniza uma dada string, substituindo espaços e especiais.

    Arguments:

        string (str): A string a ser modificada.

    Returns:

        A string modificada.
    """
    string = trata_espaco_extra(string)
    string = trata_espaco(string)
    string = trata_especiais(string)

    return string.lower()


normaliza_id = normaliza_chave  # Alias para a função normaliza_chave


def normaliza_dict(dictionary):
    u"""Normaliza/padroniza um dado dictionary.

    Arguments:

        dictionary (dict): O dicionário a ser modificado.

    Returns:

        O dictionary modificado.
    """
    print dictionary.keys()


if __name__ == '__main__':
    print normaliza_dict({'teste':'', 'hoje': {'ontem':{'manhã':1}}})
