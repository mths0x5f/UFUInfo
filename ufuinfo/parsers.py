# -*- coding: utf-8 -*-
#
#                            Módulo de parsing
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

"""Módulo de parsing

"Extratores" de informações disponíveis em sites da instituição que retornam
dictionaries devidamente aninhados. 

Depende da biblioteca Beautiful Soup 4 e Python 2.7

"""

import urllib2
import json ##################### remover ao fim dos testes
from bs4 import BeautifulSoup

class ParserRU:
    
    """Extrai informações contidas no site do Restaurante Universitário."""

    def __init__(self, campus = 'santa-monica'):
        """Inicializa o objeto

        Argumentos:
        campus -- Nome do campus em minúsculas e hífen invés de espaço (default santa-monica)

        """
        self.campus = campus
        self.url = 'http://www.ru.ufu.br/'

    def parse_cardapios(self):

        """Interpreta as tabelas de cardápio no site do restaurante"""

        pag = urllib2.urlopen(self.url + self.campus).read();
        soup = BeautifulSoup(pag)
        resultado = []

        # Percorre as refeições e suas respectivas tabelas de cardápio

        nomes_ref = soup.find('section', id='post-content').find_all('h2')
        tabelas_card = soup.find('section', id='post-content').find_all('table')

        for ref, tab in zip(nomes_ref, tabelas_card):

            refeicao = ref.string.encode('utf-8')
            refeicao = refeicao.replace('ç', 'c').lower().replace(' ', '-')

            # Percorre todos os dias disponíveis

            nome_colunas = tab.find_all('th')
            linhas = tab.find_all('tr', class_=True)

            for lin in linhas: # Cada linha é um dia diferente

                dia_repetido = False # Para controlar a repetição

                obj_refeicoes = {refeicao: {}}
                obj_temp = {'data': '', 'refeicoes': {}}

                # Percorre cada dado
                
                celulas = lin.find_all('td')
         
                for meta, dado in zip(nome_colunas, celulas):
                    
                    meta = meta.string.encode('utf-8').strip()
                    meta = meta.replace(' ', '-').lower()
                    meta = meta.replace('ç', 'c').replace('õ', 'o')
                    meta = meta.replace('ã', 'a')

                    if dado.string is None:
                        dado = dado.span.string.encode('utf-8').strip()
                        dado = dado.translate(None, 'aábcçdefghijklmnopqrstuvzwxyz- ,')

                    else:
                        dado = dado.string.encode('utf-8').strip()

                    if meta == 'data':
                        if not resultado:
                            obj_temp['data'] = dado

                        else:            
                            for r in resultado:
                                if r['data'] == dado:
                                    dia_repetido = True
                                    r['refeicoes'].update(obj_refeicoes)
                                    break

                            else:
                                obj_temp['data'] = dado

                    else:                        
                        obj_refeicoes[refeicao].update({meta: dado})
                        obj_temp['refeicoes'].update(obj_refeicoes)

                if not dia_repetido:
                    resultado.append(obj_temp)
        
        return dict({'campus': self.campus, 'dia-cardapio': resultado})

    def parse_comunicados(self):
        pass

    def parse_informacoes(self):
        pass






































































try:
    jsonstr = json.dumps(ParserRU("umuarama").parse_cardapios(), ensure_ascii=False)
except urllib2.HTTPError, e:
    print "opa"

text_file = open('output.json', 'w')
text_file.write(jsonstr)
text_file.close()