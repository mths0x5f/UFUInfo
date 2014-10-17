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

u"""Módulo de autenticações.

Este módulo contém métodos de log-in e log-out para os sistemas da instituição
que necessitem de autenticação para serem utilizados.
"""

import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup


class UsuarioSenhaIncorretos(Exception):

    u"""Exceção para quando usuário e/ou senha informados estão incorretos."""

    def __str__(self):
        return repr('Usuario e/ou senha estao incorretos, tente novamente.')


class AuthBiblioteca(object):

    u"""Métodos de log-in e log-out para o SISBI, o Sistema de Bibliotecas.

    Note:

        Note que o SISBI **NÃO** suporta HTTPS. As requisições são feitas
        utilizando HTTP, o que expõe a senha a ataques *man-in-the-middle*.

        Por favor, alertar possíveis usuários sobre isso.
    """

    def __init__(self):
        u"""Inicializa o objeto com a URL, uma *cookie jar* e um *opener*."""
        self.url = ('http://babao.dr.ufu.br:8080/auth/login?wicket:'
                    'bookmarkablePage=:com.vtls.chamo.webapp.component.opac.'
                    'OpacLoginPage&wicket:interface=:0:loginPanel:loginForm::'
                    'IFormSubmitListener::')  # HTTP, really?
        self.cookies = cookielib.CookieJar()
        self.cookie_processor = urllib2.HTTPCookieProcessor(self.cookies)
        self.opener = urllib2.build_opener(self.cookie_processor)

    def log_in(self, usuario, senha):
        u"""Método de log-in ao sistema.

        Arguments:

            usuario (str): Usuário cadastrado no SISBI, não há padronização.
            senha (str): Senha do usuário. D'oh!

        Raises:

            urllib2.URLError: Caso o adaptador de rede não estiver conectado.
            UsuarioSenhaIncorretos: Quando usuário e/ou senha estão incorretos.

        Returns:

            Uma instância do "opener" capaz de abrir novas URL com os cookies
            salvos, na sessão aberta.

                .open(): Abre uma nova URL.
                .open().read(): Retorna o código dessa página.
        """
        dados = urllib.urlencode({'username': usuario, 'password': senha})
        pag = self.opener.open(self.url, dados).read()
        soup = BeautifulSoup(pag)

        if soup.find(id='loginForm'):
            raise UsuarioSenhaIncorretos

        return self.opener

    def log_out(self):
        u"""Método de log-out.

        Este método existe apenas por formalidades. Não retorna nada, nem há a
        necessidade de checar se foi exitoso.
        """
        try:
            self.opener.open('http://babao.dr.ufu.br:8080/auth/logout')
        except urllib2.HTTPError:
            pass
        except urllib2.URLError:
            pass
