# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
es = Elasticsearch()
try:
    es.indices.delete('es')
except:
    print('删除失败')
file = open("test.json")
count = 1
for line in file:
    print(count)
    es.index(index="es",body=line)
    count = count + 1
