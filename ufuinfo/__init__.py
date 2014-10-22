# -*- coding: utf-8 -*-
#
#                              Módulo de __init__
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

u"""UFUInfo.

UFUInfo é uma biblioteca Python (2.7) capaz de recuperar informações disponí-
veis nos sites da UFU, a Universidade Federal de Uberlândia. Seus parsers
retornam dictionaries devidamente aninhados, seguindo os padrões definidos pela
documentação.

Ela é constituída por esses arquivos:

    - campi.py - Módulo com funções de informação e validação de campus.
    - parsers.py - Módulo dos parsers de informações.
    - sanitizer.py - Módulo responsável pela limpeza e padronização dos dicts.
    - auths.py - Módulo de métodos de autenticação aos sistemas da UFU.
    - actions.py - Módulo de ações e requisições aos sistemas da UFU.

Todas as classes, métodos e funções estão documentadas em seu próprio código
para a melhor compreensão sobre o uso desta biblioteca. Documentação adicional
pode ser obtida na página do projeto no GitHub: github.com/mths0x5f/UFUInfo
"""
