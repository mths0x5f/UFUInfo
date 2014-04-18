# -*- coding: utf-8 -*-

campi = {
    'santa-monica': [],
    'umuarama': [],
    'monte-carmelo': [],
    'ituiutaba': [],
    'patos-de-minas': [],
    'gloria': []
}

def verifica_campus(campus):
    if campus not in campi.keys():
        raise CampusNaoExiste
    return campus

class CampusNaoExiste(Exception):
    """Exceção lançada quando o nome de campus informado não existe"""     
    def __str__(self):
        return repr('O campus informado não existe.')