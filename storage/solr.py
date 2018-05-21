# coding=UTF-8
from storage import solr_url
import pysolr
import requests


# search intagram username in solr.
def search(mode,key,number):
    client = pysolr.Solr(solr_url)
    try:
        search_result = client.search(mode+':'+key,rows=number)
        return search_result
    except:
        print('search failed.')



def writer(data):
    client = pysolr.Solr(solr_url,timeout=10)
    try:
        client.add(data)
        return 'Success save.'
    except:
        return 'write failed.'
