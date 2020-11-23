from Bio import Entrez

Entrez.email = 'bilge.hicyilmam@boun.edu.tr'

def search(search_term):
  handle = Entrez.esearch(db="pubmed", term=search_term, retmax="40" )
  record = Entrez.read(handle)
  print (record)
  print ("")
  print("The first 20 are:\n{}".format(record["IdList"]))
  id_list = record["IdList"]
  return id_list


def get_by_id(id_list):
    handle = Entrez.efetch(db="pubmed", id=id_list, retmode="xml")
    records = Entrez.read(handle)
    i = 0
    for record in records["PubmedArticle"]:
      pmid = record["MedlineCitation"]["PMID"]
      title = record["MedlineCitation"]["Article"]["ArticleTitle"]
      title = title.encode('utf-8').decode('utf-8')
      abstract = record["MedlineCitation"]["Article"].get("Abstract", None)
      i += 1

      if pmid and title:
        print(str(i) + ".\n")
        print(pmid)
        print(title)
      if abstract:
        print("******* Abstract Exist ********")
        abstract = abstract['AbstractText']
        abstract = ' '.join(map(str, abstract))
        abstract = abstract.encode('utf-8').decode('ascii', 'ignore')
        print(abstract)

      else:
        print("***** This article doesn't have an abstract.")


id_list = search("sars-cov-2 or covid 19")
get_by_id(id_list)
