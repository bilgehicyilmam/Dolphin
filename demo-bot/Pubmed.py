from Bio import Entrez

class Pubmed(object):
    """Creates pubmed objects for fetching and saving data ."""
    db_name = "pubmed"
    email = 'bilge.hicyilmam@boun.edu.tr'
    retmax = 100000
    count = 0
    record = []


    def __init__(self, search_term):
        self.search_term = search_term
        Entrez.email = self.email

    def search(self):
        print(self.search_term)
        handle = Entrez.esearch(db=self.db_name, term=self.search_term, retmax=self.retmax )
        record = Entrez.read(handle)
        id_list = record["IdList"]
        self.record = record
        self.count = record['Count']
        handle.close()
        return id_list

    def handle_encoding(self):
        pass


#   Initialize
pubmed = Pubmed("sars cov 2 or covid 19")
pubmed.search()
print(pubmed.count)
print(pubmed.record['QueryTranslation'])


