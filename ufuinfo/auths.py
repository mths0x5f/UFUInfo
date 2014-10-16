# -*- coding: utf-8 -*-
#
#                         Módulo de autenticações
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

"""Módulo de autenticações

Métodos de log-in e log-out para os sistemas da instituição que necessitem
de autenticação.

Depende da biblioteca Beautiful Soup 4 e Python 2.7

"""

import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup

class AuthBiblioteca:

    """Métodos de log-in e log-out para o SISBI, Sistema de Bibliotecas da UFU.

    O Sistema de Bibliotecas incrivelmente NÃO suporta HTTPS. As requisições tem
    de serem feitas utilizando HTTP, que expõe a senha a ataques man-in-the-middle.

    Por favor, alertar possíveis usuários sobre isso.
    """

    def __init__(self):

        """Inicializa o objeto com a URL do form, uma cookie jar e um opener"""

        self.url = 'http://babao.dr.ufu.br:8080/auth/login?wicket:bookmarkablePage'+\
        '=:com.vtls.chamo.webapp.component.opac.OpacLoginPage&wicket:interface=:0:'+\
        'loginPanel:loginForm::IFormSubmitListener::'
        self.cookies = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))


    def log_in(self, usuario, senha):

        """Método de login

        Argumentos:

        usuario -- Usuário do SISBI
        senha -- Senha do SISBI

        """

        dados = urllib.urlencode({'username': usuario, 'password': senha})
        pag = self.opener.open(self.url, dados).read()
        soup = BeautifulSoup(pag)

        if soup.find(id='loginForm'):
            raise UsuarioSenhaIncorretos

        return self.opener


    def log_out(self):
        """Método de log-out"""
        self.opener.open('http://babao.dr.ufu.br:8080/auth/logout?theme=system')


class UsuarioSenhaIncorretos(Exception):
    """Exceção lançada quando usuário e/ou senha informados estão incorretos"""
    def __str__(self):
        return repr('Usuário e/ou senha estão incorretos, tente novamente.')
