# USER’S MANUAL

### Overview
The User Manual provides End Users with a detailed operational description of the Dolphin COVID-19 Publication Search System and its associated tools, 
such as the search procedures and manipulation of data on search results.

### 1.	GENERAL
#### 1.1	Introduction and Purpose

Scientific documents embody knowledge across time, disciplines, and regions. Authors refer to the same concepts with alternative terminology and have different
styles of writing. It is important to be able to extract information from repositories of documents to aggregate and search information from various perspectives. 
This project concerns extracting information from scientific documents in Medical Domain. These documents will be processed to identify domain specific concepts 
such as those that relate to anatomy, disease, and patients. One can see significant terms such as amygdala (and, importantly with the qualifier "left" amygdala), 
neurons, orbitofrontal cortex, parahippocampal cortex, entorhinal cortex, hippocampus, animal, human, neurosurgical patients, These terms will be automatically 
annotated by associating them with predefined terms in ontologies. Also, multi word terms must be carefully processed. For example, when both words are not taken 
into consideration together annotations that are not relevant to the search “left amygdala” can be seen. This application will harvest information from PubMed 
specifically on COVID-19 topic and automatically annotate the content with predefined terms. The annotations will relate the content of articles to ontological concepts.

* The Dolphin Web Application can be reached via:  http://ec2-3-122-230-119.eu-central-1.compute.amazonaws.com/

### 2	USER MANUAL OVERVIEW

#### 2.1	Basic Search

Home screen of the application is where the user can also apply the basic search. There is a search text field where the user can be able to input her/his query term 
and search for the articles on PubMed on COVID-19 domain. There is also dimensional search option provided under search text field which will be detailed in the 
next step (2.2). Search terms shall either be applied as one single term like: “Brain cancer” or multiple search terms are also welcomed with the comma rule: “Brain 
cancer, infectious disease”. The comma rule basically takes these 2 terms separately and searches the articles where these 2 terms can be seen together in the articles 
(and rule). If the user wants to search for the articles where multiple terms are seen together, then s/he can apply the comma rule and enter multiple search terms to 
her/his query. The application searches for entered search terms on the PubMed COVID database and retrieves articles based on the search term. Other than basic text 
search on the articles, it also searches synonyms and sub-classes (i.e. liver is the sub-class of organ) of the articles through the ontology database. The user can also 
be able to apply filters on her/his search term via the date and location selection fields. User can be able to see the number of articles found based on her/his search 
(either with or without filters), the graphical visualization of the affiliation countries/locations of the publication’s authors and the graphical visualization of the 
publication dates of the searched articles. These graphical visualizations are navigatable so if the user likes to retrieve the details about the information provided 
from the graphical visualizations, s/he can simply click on the interested (location or date data) bars or pin-points on graphical visualizations and filter through 
her/his search results. Up to 10 search results are displayed on the screen and user can navigate through the result pages at the bottom of the result’s screen. 
A shortened version of the searched article’s abstract and keywords alongside with the article’s title and PubMed id can be observed on the results page. 
Navigation to the details of the desired article based on the searched criteria can be applied through the link on the searched article’s PubMed id. To call back the 
basic search screen “Dolphin” option on the top left of the navigation bar can be clicked.


![image](https://user-images.githubusercontent.com/61224886/106474076-95cc8980-64b5-11eb-8336-ca12a1688adc.png)


#### 2.2	Dimensional Search

If the user wants to apply dimensional search on her/his results, s/he can navigate there from the basic search screen by clicking “Dimensional Search” option under 
the search text field. When dimensional search screen showed up, the search text field can be observed as it was in basic search but also there are “Add Dimension” and “Remove Dimension” buttons
under the “main query” search term which enables user’s to add and remove dimensions to her/his search. What are these dimensions? Basically they provide the user to add 
new dimensions on her/his main query. When the dimensions are applied and search is made, the result screen displays the combinations of the searched terms entered on both 
the main query and the dimensions. Main query is where the user should enter her/his most interested area of concept to search for and with the help of the dimensions the
user can search (filter out) the wide number of articles possible on the main query concept into a more vertical search to the specific part of the main concept where 
s/he wants to retrieve. For example; “lung cancer” can be a main query where the user wants to find the articles related to brain cancer but if s/he is more interested 
in lung cancer in women, s/he can basically add dimension as “women” to give more insight to her/his search. Multiple terms can also be applied on dimensional search 
with the comma rule* but please recall that it does not have the same logic as it does on basic search. Dimensional search is more for retrieving the searched term 
combinations and the article numbers found for these combinations, thus it provides the user to find out the best search combination (possibly the highest number of 
article found) in a single search if the user is not sure what to search for exactly to retrieve the right articles or interested in statistical data based on different 
queries searched. 

Here is a pseudo example to dimensional search; the user can enter multiple search terms on the main query field **(up to 3 terms)**. On the dimensions, searh terms **(up to 5 terms)** can be entered. On the other hand, the system can calculate the combinations of searh terms **(up to 6 dimensions)**. (It takes at least 30 -40 minutes to calculate the results.)
If the user enters “lung cancer, liver cancer” on the main query field this means that the user is interested on 2 main domains separately; lung cancer and liver cancer. 
Then if the user wants to add dimension on these 2 domains, s/he simply clicks “Add Dimension” button to add dimension and enters “women, men”. When the user searches for 
“lung cancer, liver cancer” on the main query and the “women, men” on the first dimension, the results will show the combination of dimensions on the main queries such as:

-	Lung cancer (each main query itself)
-	Lung cancer - woman (each main query with the possibilities on dimension)
-	Lung cancer - man (each main query with the possibilities on dimension)
-	Lung cancer - children (each main query with the possibilities on dimension)
-	Lung cancer - breath (each main query with the possibilities on dimension)
-	Lung cancer - cough (each main query with the possibilities on dimension)
-	Lung cancer - fever (each main query with the possibilities on dimension)
-	Lung cancer - woman - breath (each main query with the possibilities on dimension)
-	Lung cancer - woman - cough (each main query with the possibilities on dimension)
-	Lung cancer - woman - fever (each main query with the possibilities on dimension)
-	Lung cancer - man - breath (each main query with the possibilities on dimension)
-	Lung cancer - man - cough (each main query with the possibilities on dimension)
-	Lung cancer - man - fever (each main query with the possibilities on dimension)
-	Lung cancer - children - breath (each main query with the possibilities on dimension)
-	Lung cancer - children - cough (each main query with the possibilities on dimension)
-	Lung cancer - children - fever (each main query with the possibilities on dimension)

Also the number of articles found for each combination will be displayed on the screen. This page is simply called “summary page” of your search combinations 
where you can have insight of your search. The search here to retrieve the count of the combinations is done with the same logic as in basic search, it searches 
for the combination results based on the searched terms, then it also searches for searched term’s synonyms and sub-classes from ontology to retrieve the number 
of articles found for the combinations. The combination results are displayed after search is done. Filtering on date or location while applying the search is also 
possible for the dimensional search. Number of articles displayed on the results is found with the and rule (for ex: the total number articles where “lung cancer” 
and “men” are found together with their synonyms and sub-classes). User can be able to click on the article numbers found for the combinations to navigate to the 
articles of the desired combination. User can also check for the synonyms and sub-classes found for the dimensional query made on the left bottom of the screen.

![image](https://user-images.githubusercontent.com/61224886/106474218-bbf22980-64b5-11eb-8714-ba383e6863a1.png)

![image](https://user-images.githubusercontent.com/61224886/106474456-ffe52e80-64b5-11eb-8cbe-6ca25bc60d54.png)

![image](https://user-images.githubusercontent.com/61224886/106474553-14c1c200-64b6-11eb-9533-4839ea439a7c.png)

![image](https://user-images.githubusercontent.com/61224886/106474649-30c56380-64b6-11eb-9af3-3ee006a6680e.png)

The user can navigate to the related articles by clicking on the numbers on the summary table. Under the search box field, graph based on countries (by authors) and the graph based on the dates can be found. Under the graphs, articles can be found. The user can navigate to these articles by clicking on their pubmed id's as well. 

![image](https://user-images.githubusercontent.com/61224886/106474947-78e48600-64b6-11eb-8792-c26c75d03230.png)

![image](https://user-images.githubusercontent.com/61224886/106475130-a7626100-64b6-11eb-8250-731378065240.png)

![image](https://user-images.githubusercontent.com/61224886/106475199-bd702180-64b6-11eb-9f6f-c203cc592bf8.png)



#### 2.3	Article Detail Page

When the user clicks on the PubMed id of the searched results, it navigates to the details page of the selected article where if available the PubMed id, title, 
abstract, keywords, conclusions, authors, publication date, DOI Link (where article can be found if open to access), results, journals and copyrights info of the 
article is displayed. Medical terms on the article’s title, keywords and the abstract can be found as annotated and highlighted. If navigated on these annotated words, 
the definition of the term can be seen on the screen with its source where the definition is taken from so that if the user desires the check the details about the 
annotated term, s/he can navigate to the ontology where the term is founded from and make a detailed search on the term via the source link provided.

![image](https://user-images.githubusercontent.com/61224886/106475348-e55f8500-64b6-11eb-8410-aabc6a288f18.png)



