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
from time import *
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
        self.url = 'http://www.ru.ufu.br/'

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
            
            refeicao = (normaliza_chave(ref.text)
                        .replace('-'+self.campus, '')
                        .replace('-(link-mobile)', ''))

            # Percorre todos os dias disponíveis

            nome_colunas = tab.find_all('th')
            dias = tab.find_all('tr', class_=True)

            for dia in dias:

                dia_repetido = False  # Para controlar a repetição

                dict_temp_refeicao = {refeicao: {}}
                dict_temp = {'data': '', 'refs_dict': {}}

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
                                    r['refs_dict'].update(dict_temp_refeicao)
                                    break

                            else:
                                dict_temp['data'] = dado

                    else:
                        dict_temp_refeicao[refeicao].update({meta: dado})
                        dict_temp['refs_dict'].update(dict_temp_refeicao)

                if not dia_repetido:
                    list_cardapios.append(dict_temp)

        # Junta as refeições vegetarianas no mesmo cardápio que as outras

        for r in list_cardapios:
            for s in r['refs_dict'].keys():
                if '-vegetariano' in s:
                    veg = {}
                    for t in r['refs_dict'][s].keys():
                        if not '-vegetariano' in t:
                            veg.update({t + '-vegetariano': r['refs_dict'][s][t]})

                        else:
                            veg.update({t: r['refs_dict'][s][t]})

                    sem_sufixo = s.replace('-vegetariano', '')
                    r['refs_dict'][sem_sufixo].update(veg)

            for u in r['refs_dict'].keys():
                if '-vegetariano' in u:
                    del r['refs_dict'][u]

        # Um ano depois (15/02/2015): Esse patch converte a estrutura de dicts
        # das refeicoes, para o uso de lists. Faço isso porque é muita perda
        # de tempo eu reescrever todo o método para usar lists. Deal with it.
        # Também, aproveito para converter a data para ISO 8601.

        for r in list_cardapios:
            r.update({'refeicoes': []})
            for s in r['refs_dict'].values():
                r['refeicoes'].append(s)
            del r['refs_dict']
            r['data'] = strftime("%Y-%m-%d", strptime(r['data'], "%d/%m/%y"))

        return dict({'cardapios-por-dia': list_cardapios})

    @staticmethod
    def parse_comunicados():

        u"""Interpreta os comunicados no site do restaurante"""

        pagina = urllib2.urlopen('http://www.ru.ufu.br/comunicados').read()
        soup = BeautifulSoup(pagina)
        list_comunicados = []

        section = soup.find('section', id='post-content')
        tabela = section.find('table')
        comunicados = tabela.find_all('tr', class_=True)

        for com, i in zip(comunicados, xrange(100)):

            dict_temp = {}
            dict_temp['assunto'] = trata_espaco_extra(com.td.text)
            dict_temp['link'] = 'http://www.ru.ufu.br'+com.td.a['href']

            pagina = urllib2.urlopen(dict_temp['link']).read()
            cont = BeautifulSoup(pagina).find('div', class_='field-name-body')
            dict_temp['conteudo'] = cont.text.replace('Att.,','').replace('\t','').replace('\n\n','')

            # Esse método para a obtenção da data é muito mais confiável e 
            # eficiente. Substituir algum dia o antigo por este.
            dado = com.find('td', class_="views-field-field-comunicado-data")
            dict_temp['data'] = dado.span['content'][:10]

            list_comunicados.append(dict_temp)

            if i == 2:  # Limita a resposta aos 3 últimos comunicados
                break

        return dict({'comunicados': list_comunicados})

    def parse_informacoes(self):

        """Interpreta as informações gerais no site do restaurante"""

        # Na verdade, por agora, este método apenas retorna um dict estático,
        # já que seus valores dificilmente mudarão em um futuro próximo. Fora
        # implementado assim para evitar a gastura. Feel free to contribute.

        info = dict({'valor-reais': 3.00,
                     'funcionamento-ru': [
                        {
                            'abertura': '10:30',
                            'fechamento': '13:30'
                        },
                        {
                            'abertura': '17:45',
                            'fechamento': '19:15'
                        }
                     ],
                     'funcionamento-caixa': [
                        {
                            'abertura': '10:15',
                            'fechamento': '13:15'
                        },
                        {
                            'abertura': '17:30',
                            'fechamento': '19:00'
                        }
                     ]})

        return info
