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


def get_by_id():
    handle = Entrez.efetch(db="pubmed", id=['33220640', '33220632', '33220631', '33220618', '33220615', '33220602', '33220575', '33220549', '33220478', '33220456', '33220455', '33220447', '33220442', '33220441', '33220440', '33220439', '33220398', '33220390', '33220384', '33220366', '33220354', '33220349', '33220345', '33220338', '33220296', '33220289', '33220283', '33220249', '33220209', '33220208', '33220207', '33220206', '33220195', '33220194', '33220193', '33220192', '33220184', '33220171', '33220155', '33220127'], retmode="xml")
    records = Entrez.read(handle)
    for record in records["PubmedArticle"]:
      # print("PMID: \n" + str(record["MedlineCitation"]["PMID"]) + "\n")
      # print("Title: \n" + str(record["MedlineCitation"]["Article"]["ArticleTitle"]) + "\n")
      pmid = record["MedlineCitation"]["PMID"]
      title = record["MedlineCitation"]["Article"]["ArticleTitle"]
      title = title.encode('utf-8').decode('utf-8')
      abstract = record["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]
        print("Abstract: \n" + str(record["MedlineCitation"]["Article"]["Abstract"]['AbstractText']) + "\n")
      abstract = ' '.join(map(str, abstract))
      abstract =  abstract.encode('utf8')


      print(pmid)
      print(title)
      print(abstract)



id_list = search("sars-cov-2 or covid 19")

print("Id list: ")
print(id_list)

# get_by_id("22909249")
get_by_id()
