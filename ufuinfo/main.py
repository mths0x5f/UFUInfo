# coding: utf-8

import urllib2
from bs4 import BeautifulSoup

domain = "ufu.br"

page = urllib2.urlopen("http://" + "www.ru." + domain + "/santa-monica").read();
soup = BeautifulSoup(page)

     

resultado = []

''' Percorre as refeições disponíveis e suas respectivas tabelas de cardápio '''

nome_refeicao = soup.find("section", id="post-content").find_all("h2")
tabelas_cardapio = soup.find("section", id="post-content").find_all("table")

for ref, tab in zip(nome_refeicao, tabelas_cardapio):

    refeicao = ref.string.encode('utf-8')
    refeicao = refeicao.replace("ç", "c").lower().replace(" ", "-")

    ''' Percorre todos os dias disponíveis '''

    nome_colunas = tab.find_all("th")
    linhas = tab.find_all("tr", class_=True) # Linhas de cabeçalho não tem class

    for lin in linhas: # Cada linha é um dia diferente

        dia_repetido = False

        obj_refeicoes = {refeicao: {}}
        obj_temp = {"data": "", "refeicoes": {}}

        ''' Percorre cada dado '''
        
        celulas = lin.find_all("td")
 
        for meta, dado in zip(nome_colunas, celulas):
            
            meta = meta.string.encode('utf-8').strip().replace(" ", "-").lower()
            meta = meta.replace('ç', 'c').replace('õ', 'o').replace('ã', 'a')

            if dado.string is None:
                dado = dado.span.string.encode('utf-8').strip()
                dado = dado.translate(None, "aábcçdefghijklmnopqrstuvzwxyz- ,")
            else:
                dado = dado.string.encode('utf-8').strip()

            if meta == "data":
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
                
                obj_refeicoes[refeicao.replace("-vegetariano", "")].update({meta: dado})
                obj_temp['refeicoes'].update(obj_refeicoes)


        if not dia_repetido:
            resultado.append(obj_temp)
        
        





import json
text_file = open("Output.json", "w")
text_file.write(json.dumps(resultado, ensure_ascii=False))
text_file.close()