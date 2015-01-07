# -*- coding: utf-8 -*-
#
#                               Módulo de parsing
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

u"""Módulo de parsing.

Este módulo contém métodos que extraem informações disponíveis em sites da
instituição e as retorna em estruturas devidamente aninhados.

xkcd relevante: http://xkcd.com/1421/
"""

import urllib2
from bs4 import BeautifulSoup
from campi import *
from sanitizer import *


class ParsersRU(object):

    u"""Extrai informações contidas no site do Restaurante Universitário."""

    def __init__(self, campus = 'santa-monica'):
        u"""Inicializa o objeto com o nome do campus, e a URL de extração.

        Arguments:

            campus (str): Nome do campus normalizado. (default santa-monica)
        """
        self.campus = verifica_campus(campus)
        self.url = 'http://localhost/'

    def parse_cardapios(self):

        u"""Interpreta as tabelas de cardápio no site do restaurante"""

        pagina = urllib2.urlopen(self.url+self.campus).read()
        soup = BeautifulSoup(pagina)
        list_cardapios = []

        # Percorre as refeições e suas respectivas tabelas de cardápio

        section = soup.find('section', id='post-content')
        nomes_refeicoes = section.find_all('h2')
        tabelas_cardapios = section.find_all('table')

        for ref, tab in zip(nomes_refeicoes, tabelas_cardapios):

            refeicao = normaliza_chave(ref.string).replace('-'+self.campus, '')

            # Percorre todos os dias disponíveis

            nome_colunas = tab.find_all('th')
            dias = tab.find_all('tr', class_=True)

            for dia in dias:

                dia_repetido = False  # Para controlar a repetição

                dict_temp_refeicao = {refeicao: {}}
                dict_temp = {'data': '', 'refeicoes': {}}

                # Percorre cada dado

                celulas = dia.find_all('td')

                for meta, dado in zip(nome_colunas, celulas):

                    meta = normaliza_chave(meta.string)

                    if dado.string is None:  # Se for campo dia

                        dado = dado.span.string.encode('utf-8').strip()
                        transl = 'aábcçdefghijklmnopqrstuvzwxyz- ,'
                        dado = dado.translate(None, transl)

                    else:
                        dado = dado.string.strip()

                    if meta == 'data':

                        if not list_cardapios:
                            dict_temp['data'] = dado

                        else:
                            for r in list_cardapios:
                                if r['data'] == dado:
                                    dia_repetido = True
                                    r['refeicoes'].update(dict_temp_refeicao)
                                    break

                            else:
                                dict_temp['data'] = dado

                    else:
                        dict_temp_refeicao[refeicao].update({meta: dado})
                        dict_temp['refeicoes'].update(dict_temp_refeicao)

                if not dia_repetido:
                    list_cardapios.append(dict_temp)

        # Junta as refeições vegetarianas no mesmo cardápio que as outras

        for r in list_cardapios:
            for s in r['refeicoes'].keys():
                if '-vegetariano' in s:
                    veg = {}
                    for t in r['refeicoes'][s].keys():
                        if not '-vegetariano' in t:
                            veg.update({t + '-vegetariano': r['refeicoes'][s][t]})

                        else:
                            veg.update({t: r['refeicoes'][s][t]})

                    sem_sufixo = s.replace('-vegetariano', '')
                    r['refeicoes'][sem_sufixo].update(veg)

            for u in r['refeicoes'].keys():
                if '-vegetariano' in u:
                    del r['refeicoes'][u]

        return dict({'campus': self.campus, 'cardapios': list_cardapios})

    def parse_comunicados(self):
        pass

    def parse_informacoes(self):

        """Interpreta as informações gerais no site do restaurante"""

        pass
        