# -*- coding: utf-8 -*-
from ufuinfo.parsers import *
from ufuinfo.campi import *
from ufuinfo.sanitizer import *
import json


## Instanciar um objeto de parsers de um determinado campus

ru = ParsersRU('santa-monica') # 'santa-monica' é o padrão, 

d = sanitizer.normaliza_estrutura(ru.parse_cardapios())

##	Gerar um arquivo .json

jj = json.dumps(d, separators=(',',':'))


open('saida.json', 'w').write(jj)
