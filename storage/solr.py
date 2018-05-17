from storage import solr_url
import pysolr


# search intagram username in solr.
def search_userID():
    client = pysolr.Solr(solr_url,timeout=10)
    try:
        # search
        search_result = client.search('post_owner')
    except:
        return 'search userID failed.'




def writer(data):
    client = pysolr.Solr(solr_url,timeout=10)
    try:
        client.add(data)
        return 'Success save.'
    except:
        return 'write failed.'
