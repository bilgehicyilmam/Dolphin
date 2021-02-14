

## annotation popup

```
html = abstractDataFromDb
annotations_of_article = fetch(api_url, pubmed_id_of_article)
prefix = annotations_of_article.prefix
label = annotations_of_article.label
suffix = annotations_of_article.suffix
class = annotations_of_article.class
definition = annotations_of_article.definition

forEach annotations_of_article
    newLabel = '<div class="tooltip">' + label + class + definition + '</div>'
    html = html.replace(prefix + label + suffix, prefix + newLabel + suffix)

return html
```

## creating annotation

```
ontologies = Ontologies.all()
articles = Articles.all()

forEach article in articles
    forEach ontology in ontologies
        if (find(abstract, label))
            save_annotation_to_db(id, source, target, body, creator)
```
