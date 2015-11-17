from datetime import datetime
from elasticsearch import Elasticsearch
import re
import sys

server = 's2.zserg.net:9200'

def noteparser(text):
    re_tags = r'#([^\s]+)'
    re_title = r'#([^\s]+)'
    tags = re.findall(re_tags,text)
    stat = re.search(re_title,text,re.I|re.M)
    if stat:
       title = stat.group(1)
    else:
       title = '<no_title>'

    note = {
            'title': title,
            'contents': text,
            'published': datetime.now(),
            'tags': tags
    }
    return note



text = ''
for line in sys.stdin:
   text += line

note = noteparser(text)

#print(noteparser(text))

es = Elasticsearch(server)
res = es.index(index="notes", doc_type='note',  body=note)
print(res['created'])

