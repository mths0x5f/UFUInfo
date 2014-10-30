# -*- coding: utf-8 -*-
from ufuinfo.parsers import *
from ufuinfo.campi import *
from ufuinfo.sanitizer import *
import json


## Instanciar um objeto de parsers de um determinado campus

ru = ParsersRU('Santa Mônica') # 'santa-monica' é o padrão, 

d = sanitizer.normaliza_dict(ru.parse_cardapios())

##	Gerar um arquivo .json

open('saida.json', 'w').write(json.dumps(d))
