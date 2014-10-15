from ufuinfo.parsers import *
from ufuinfo.campi import *
import json

ru = ParsersRU("santa-monica")
jj = json.dumps(ru.parse_cardapios())

print jj

open('saida.json', 'w').write(jj)
