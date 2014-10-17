# -*- coding: utf-8 -*-
from ufuinfo.parsers import *
from ufuinfo.campi import *
import json


## Instanciar um objeto de parsers de um determinado campus

ru = ParsersRU(raw_input('campus: ')) # 'santa-monica' é o padrão, 

##	Gerar um arquivo .json

open('saida.json', 'w').write(json.dumps(ru.parse_cardapios()))
