# -*- coding: utf-8 -*-
#
#                            Módulo de autenticações
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


import sanitizer


campi = {
    'santa-monica': [],
    'umuarama': [],
    'monte-carmelo': [],
    'ituiutaba': [],
    'patos-de-minas': [],
    'gloria': []
}


class CampusNaoExiste(Exception):

    """Exceção lançada quando o nome de campus informado não existe"""

    def __str__(self):
        return repr('O campus informado nao existe.')


def verifica_campus(campus):
    u"""Verifica a existência de um dado campus.

    Arguments:

        campus (str): O nome de um possível campus da UFU.

    Raises:

        CampusNaoExiste: Quando o campus informado não existir.

    Returns:

        campus: A própria chave, tratada.
    """
    campus = sanitizer.trata_especiais(campus)
    if campus not in campi.keys():
        raise CampusNaoExiste

    return campus
