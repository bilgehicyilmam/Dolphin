## Executive Summary
Group Dolphin is a project group formed by the instructor Suzan Uskudarli for the course SWE 574 Software Engineering as a Team. Its members are, also the students of the course; Bilge Hicyilmam, Hasan Gokce and Kerem Mert Aksoy. The aim of the group, as a project, is to successfully extract information from scientific documents in Medical Domain and process these documents to identify domain specific concepts such as those that relate to anatomy, disease, and patients.
This SRS document is a product of decisions taken throughout the meetings which are both held internally with the team members and externally between our customer – Suzan Uskudarli and the GD (Group Dolphin) team. These meetings are held between 26th of Oct 2020 up to this date; 21st of Nov 2020 and they will continue being held until 1st of Feb 2021. There were 12 internal and 4 external meetings are completed up to this point. 
GD SRS Document contains functional and nonfunctional requirements which will be used by the GD team for the design and development processes of the SWE574 project.

## 1.	Introduction
### 1.1	Objectives and scope

The objective of the document is to describe requirements for GD and the goal of the Software Requirements Specification document is to help GD team throughout the Software Design Process. GD, as a team, aims to follow up agile methodology and considers implementation with development sprints thus this document is always open to be subjected for a change which also labels it as a live document. 

The final product aims to extract information from documents on Pub-Med about the domain requested as Covid-19 and to aggregate and search information from various perspectives. It will automatically annotate the requested content with predefined terms and the annotations will relate the content of articles to ontological concepts. Hence as a vantage point this document describes information about potential users, domains, user stories, functional and non-functional requirements and planned to be updated with the UML class diagrams and use case models during the project timeline. It can be considered as an SRS document with full functional details and its user scenarios can be used to start first development sprints.

### 1.2	Intended Audience and Usage Guidelines

This SRS document is intended for GD team members for future design and development purposes and for reporting purposes to the customer – Suzan Uskudarli to control the process in the right way possible. 



## 2.Target

This chapter includes the target audience and the application domains of the system.

### 2.1 Users

The users of the system can be grouped into 2 categories: end-user and developer.

**Name:** End-user

**Description:** End-users use the system to search for articles in the Covid 19 medical domain.

**Name:** Developer

**Description:** Developers provide applications, necessary updates by receiving feedback from the end-users. They are responsible for retrieving new articles to the system periodically.

### 2.2. Areas and Domains

The system targets a medical domain, in particular Covid 19. The articles are about domain-specific concepts such as those that relate to anatomy, disease, and patients. 

| __#__  | __Description__ | 
|-----------------|---------------|
|  **Area** |  **Data Analysis (Text Analysis)** |  
|  Description |  Since the amount of data is huge in the biomedical field, it is possible to derive meaningful information with proper data analysis. Efficient analysis and interpretation of complex data can improve public health. With the purpose of revolutionizing the medical treatments for Covid 19, the system focuses on giving insight into the disease. |  
|  Domain |  Medicine |  
|  **Area** |  **Search Data** |  
|  Description |  To support research during the Covid 19 outbreak, we aim to provide the latest scientific articles about the field. Researchers can find any Covid 19 related publications by typing queries into the search field. The system targets to enhance productivity for the biomedical field by systematically delivering critical information. |  
|  Domain |  Medicine |  



## 3. Functional Requirements

This chapter describes the functional requirements of the application. First, we described the content of the data. Next, we described the search functionalities of the application and finally, the presentation way of the results.




#### 3.1 Search

**3.1.1.** The system shall take input data from the search field.

**3.1.2.** The system shall be able to fetch articles based on search terms by querying abstracts and titles.

**3.1.3.** The system shall provide another search field for user to expand the search on the new dimensions.

**3.1.4.** The system shall be able to display created dimensions on the screen.

**3.1.5.** The system shall provide delete option for the desired dimensions.

**3.1.6.** The system shall provide adding multiple words with comma on dimensions and main query.

**3.1.7.** The system shall be able to delete words on dimensions.

**3.1.8.** The system shall provide a faceted search based on publication date, location.

**3.1.9.** The system shall check for query term's synonyms and it's childrens from annotation and ontology database respectively and it shall retrieve articles based on the query term, its synonym and its child classes. 

**3.1.10** The system shall omit stop words like "and", "or", "but" from the searched terms while doing search but uppercase "AND", "OR", "BUT" words shall not be omitted considering abbreviations. 

**3.1.11** The system shall make search based on search window size (between 0-4 words are permitted in between a query term with multiple words) and search term's order shall be taken into consideration. 

**3.1.12** The system shall be able to query search terms with its word boundaries. (if searched for "bound"; "bound" shall be retrieved, not "rebound" )

#### 3.2. Articles

**3.2.1** The system shall be able to retrieve abstracts, titles, keywords, DOI Link, publication date, conclusion, PubMed ID, Conclusions, Results, Journals, CopyRights related to the searched input from the user and display them on article detail page.

**3.2.2.** The system shall retrieve articles related to all desired dimensions.

**3.2.3.** The system shall link the retrieved PubMed ID's to their full abstracts.

**3.2.4.** The system shall direct the user to the webpage where the full article is published if the user clicks on the DOI Link from the full abstract page.

**3.2.6.** The system shall be able to list 10 articles per page and depict the number of all found abstracts at the top of each page.

**3.2.7.** The system shall be able to list all the searched articles based on the clicked year from the graphical visualization.

**3.2.8.** The system shall be able to list all the searched articles based on the location of affiliation countries of the authors from the graphical visualization.

#### 3.3. Ontology and Annotation

**3.3.1.** The system shall auto-annotate the medical terms, their synonyms, and all related medical words on article abstracts and titles.

**3.3.2.** Medical ontology database shall be built by parsing a selected ontology (Covid-19 ontology from https://bioportal.bioontology.org/ontologies/COVID-19) and saved to the database.

**3.3.3.** Ontology data shall be parsed into its Class, SubClassOf, Synonyms, Labels and Definitions and shall be saved on the database.

**3.3.4.** Article abstracts shall be annotated by using the Ontology data.

**3.3.5.** System shall auto-annotate new articles.

**3.3.6.** Annotated terms on the article's detail page shall be displayed as a pop-up with its class and definition field.

**3.3.7.** Every single annotation item shall be retrieved as a seperate entity from the annotation server.

#### 3.4. Visualization

**3.4.1.** The system shall be able to provide a graphical visualization of the articles based on their publication date.

**3.4.2.** The system shall be able to provide a link on the year info of the graphical visual



## 4. Non-functional Requirements

### 4.1. Development

**4.1.1** Main programming language shall be Python, external libraries shall be used for API search and frontend design.

**4.1.2.** System shall be able to handle errors.

**4.1.3.** System shall have unit tests to provide software quality.

**4.1.4.** Annotations shall be presented in JSON-LD (JSON Linked Data) format.

### 4.2. Data Source

**4.2.1.** System shall retrieve data from Entrez and Pubmed.

**4.2.2.** System shall use UMLS for annotations.

### 4.3. Availability

**4.3.1.**  Application should be available online for an ordinary web browser with a well-designed user interface.

**4.3.2.** An average user shall be able to use all features of the application.

### 4.4. Environment

**4.4.1.** System shall be available via AWS and Heroku servers. 

#### 4.5 Database Content

**4.5.1** The system shall provide only Covid-19 articles from PubMed and ontology data from Bioontology.

**4.5.2** The system shall make automatic daily updates for new articles.

**4.5.3** The system shall provide annotations in a different database than articles and ontologies.

### 4.6. Standards

**4.6.1.** System shall use W3C Web Annotation Data Model.

## 5. User Stories

### Scenario #1

**User Role:** End-User

**User Role Description:** Hayal is a third-year undergraduate student in the Department of Medicine at Istanbul University. She is 20 years old. As a medical student, she is fascinated by the working of the human body.  She loves helping people to live healthier and happier lives. Unfortunately, she is very anxious about Covid 19, since the coronavirus pandemic has caused more than a million deaths. That’s why she wants to analyze coronavirus and the long term effects in detail. She wants to learn the effects on the lungs.

**User Story:** As a user, I want to open a search engine and search the effects of coronavirus on just the lungs. Also, I want to read the full article.

**Precondition:** The user has opened the web page.

**Title:** The user searches the Covid 19 article that is about "lungs", and reads the full text.
1.	She writes “lungs” into the search bar, and clicks on the search button.
2.	She glanced at the abstract of the first article which includes serious pneumonia, the case of lungs filled with fluid and debris.
3.	She clicks on the article.
4.	After the full abstract opens on the page, she clicks on the "read full article" button.
5. She reads the article that includes author list, publication date, references, publication journal as well.
6. After reading the full article, she returns back to the homepage.
7. She makes a new search for nails.
8. Since "nails" don't exist in the word dictionary for our concept Covid 19, she sees a warning "no publications found".


**Acceptance Criteria**

I can see all the articles that include just the lungs about Covid 19, and I can open the full article to read it. I can not see the articles that include "nails".

### Scenario #2 Rebecca

**Rebecca's Story:**

I am an American business magnate, software developer, and philanthropist. Thinking of the humanities future is a big part of my life; besides climate change, there are more dangerous challenges such as epidemics. The idea of contributing to humanity makes me more connected to the world.

I regularly talk to my co-workers about how we quickly respond to a pandemic. We're constantly looking for the big-picture to create a world-wide plan, but lately, it seems a little tough to do that. Everything seems to have an "information pollution" and needs to spend too much time to visualize the data, and therefore, we keep the argument with excel tables.

I really enjoy finding new articles that match my working areas. I wish there were a way to find more related articles in the quickest way and more visualization relating to those articles without waiting for new visual reports.

**User Role:** End-User.

**Preconditions:** 
* User is at work in her free time.
* User is on the main page of the web application.
* User uses a notebook, not a mobile device.

**Steps:**
1. User types on the search box "T cell"
2. User press the enter button.
3. User sees selected articles and choose a year to narrow the result.
4. To be sure if an article is related to the topic, she clicks on annotations which are highlighted in the abstract; thus, she can be sure that the searched item is in the correct wording form considering the terminology.
5. User clicks on the first article.
6. User retrieves full abstract with annotations.
7. User clicks "read full article" button.

**Acceptance Criteria**

User can see T-cell related publications and auto-annotations.

### Scenario #3

**User Role:** End-User.

**User Role Description:** Ahmet is a nurse who is frequently working with obstetricians. Since the Covid-19 has become a pandemic, more and more children are born with their mother's already are being infected by Covid-19. Although obstetricians are researching about Covid-19 effects and preventions on new-borns, as a nurse, Ahmet also wants to gain knowledge about it to be aware of this phenomena as a professional. 

**User Story:** He wants to learn more about Personal Protective Equipments (PPEs) to be confident about when to wear yellow isolation gowns or blue isolation gowns etc. He, obviously, cares about hygiene but he is also wondering what is more can be done during the Covid-19 pandemic to protect the newborns. He also wonders the effects of Covid-19 infected mother on between premature babies and the newborn normal babies, to learn more and be certain if any different treatment is needed on premature babies. And finally he personally wonders whether if a Covid-19 infected mother should give a normal birth or cesarian birth. 


**Preconditions:** 
* User can do research during his free hours on shift at the hospital since he does not have any internet access at home.
* He uses a computer which is connected to hospital's network.
* He already typed Covid 19 on the search field and clicked on the search button this retrieved around 70k documents.


**Steps:**
1. User has selected all available texts and publication day from 2010 to 2018
2. User typed again "Covid 19" on the search field.
3. User recognized that very few studies (18) have been done about Covid-19 between 2010 and 2018/
4. User checks these studies and become certain that they are not related to Covid 19. (This gives an insight to the user that almost all studies regarding Covid 19 are done after 2019.)
5. User enters "PPE, Covid-19 and obstetrics" with spaces on the search field, selected all texts, clicked on the button and retrieved searched documents. The search retrieves 43 abstract results. Only 3 of them are directly related to all 3 items. Mostly retrieved documents are about Covid-19 and obstetrics. Few documents are directly related only to PPEs.
6. User clicks on the 2nd article (out of 3 articles which are related to all searched items) and gain knowledge.
7. User wants to make another search and returns back to the home page.
8. User enters "Covid 19, hygiene and newborn" on the search field and enters the search button.
9. 21 article abstracts are returned. Most of them are related to searched items and user clicks on article titles.
10. User opens the abstracts on new tab and returns to the home page.
11. User enters "premature birth covid-19" on the search field and enters the search button.
12. 55 article abstracts are return and only 2 of them were related to "premature birth and covid-19".
13. User was not satisfied with the article concepts, and considers to change search items to reach the desired search.
14. User enters "early birth cases covid-19" on search field and clicked button.
15. User still was not satisfied with the search and gives up on it.
16. User typed "cesarian birth covid-19" on search field and clicked search button.
17. No documents were retrieved.
18. User recognizes he made a typo and typed "cesarean birth covid-19" on search field and clicked the search button.
19. User was not satisfied with the 73 results, and recognizes on one abstract that cesarean section is used.
20. User typed "cesarean section covid-19" on search field and clicked the search button.
21. 107 articles were retrieved and interested ones are right clicked and opened in new tab.


**Acceptance Criteria**

User made 4 searches about his interested questions, and on 2 of his searches he found more related articles about his search and on his 2 searches he founds less articles.

# Mockups

Mockups can be reached from this [link](https://xd.adobe.com/view/59b2b062-214f-4a29-8813-6b9e3fd4a621-0ce1/) as well.

## Mockup #1
![Web 1920 – 1](https://user-images.githubusercontent.com/25805267/99155453-240c4d00-26c9-11eb-8494-767f7abfea06.png)
## Mockup #2
![Web 1920 – 2](https://user-images.githubusercontent.com/25805267/99155454-25d61080-26c9-11eb-9c2b-45b16f6ffb57.png)
## Mockup #3
![Web 1920 – 3](https://user-images.githubusercontent.com/25805267/99155457-27073d80-26c9-11eb-9e4a-a9478aba0a74.png)
## Mockup #4
![Web 1920 – 4](https://user-images.githubusercontent.com/25805267/99155459-28d10100-26c9-11eb-9f15-bc3ac7195914.png)
## Mockup #5
![Web 1920 – 7](https://user-images.githubusercontent.com/25805267/99155463-2c648800-26c9-11eb-9c66-78ee093ead49.png)
## Mockup #6
![Web 1920 – 8](https://user-images.githubusercontent.com/25805267/99155464-2ec6e200-26c9-11eb-8250-a90c901ba084.png)
## Mockup #7
![Web 1920 – 5](https://user-images.githubusercontent.com/25805267/99155460-2b335b00-26c9-11eb-9443-dc4a6aabeaf4.png)
## Mockup #8
![Web 1920 – 6](https://user-images.githubusercontent.com/25805267/99155461-2bcbf180-26c9-11eb-95c6-63701f306a20.png)
## Mockup #9
![Web 1920 – 9](https://user-images.githubusercontent.com/25805267/99901066-f6c12f80-2cc4-11eb-8f1c-00d4418c0996.png)
## Mockup #10
![Web 1920 – 10](https://user-images.githubusercontent.com/25805267/99901069-f9238980-2cc4-11eb-9c9b-1e131517fc5b.png)
## Mockup #11
![Web 1920 – 10](https://user-images.githubusercontent.com/25805267/100637091-84df8a80-3343-11eb-9c1e-3876fec821ae.png)
## Mockup #12
![Web 1920 – 9](https://user-images.githubusercontent.com/25805267/100637096-8610b780-3343-11eb-87b0-39d1c4ff4d96.png)


## 6. Conclusion

The main purpose of this document is to define requirements for Group Dolphin. Since the SRS document is labeled as live document, these specified requirements are subject to change within the project life cycle. This document will also be a source both in the Design and Development processes of Group Dolphin. 

## 7. Appendix : Glossary

**GD:** Group Dolhin

**Customer:** Dr. Suzan Uskudarli

**SRS:** Sofrware Requirements Specification

**Developers:** Group Dolphin

**Designers:** Group Dolhin

**Domain:** Constrained interest/work area of a subject

**Document:** Scientific abstract and article

**Anatomy:** The branch of biology concerned with the study of the structure of organisms and their parts

**Disease:** A particular abnormal condition that negatively affects the structure or function of all or part of an organism

**Patient:** A person receiving or registered to receive medical treatment

**Internal Meeting:** Meeting within GD

**External Metting:** Meeting with the customer Dr Suzan Uskudarli

**Functional requirement:** A function of a system or its component, where a function is described as a specification of behavior between outputs and inputs

**Nonfunctional requirement:** A requirement that specifies criteria that can be used to judge the operation of a system, rather than specific behaviors. They are contrasted with functional requirements that define specific behavior or functions.

**Design:** The process by which an agent creates a specification of a software artifact intended to accomplish goals, using a set of primitive components and subject to constraints

**Development:** The process of conceiving, specifying, designing, programming, documenting, testing, and bug fixing involved in creating and maintaining applications, frameworks, or other software components 

**Agile Methodology:**  A type of project management process, mainly used for software development, where demands and solutions evolve through the collaborative effort of self-organizing and cross-functional teams and their customers

**Implementation:** The process of putting a decision or plan into effect; execution

**Development Sprint:**  A set period of time during which specific work has to be completed and made ready for review

**End-user:** A person who ultimately uses or is intended to ultimately use a product

**Application:** A software program that runs on your computer

**Target Audience:** A particular group at which a product is aimed

**Annotation:** A note by way of explanation or comment added to a text or diagram

**UML:** Unified Modelling Language

**PubMed:** A free search engine accessing primarily the MEDLINE database of references and abstracts on life sciences and biomedical topics

**Entrez:** NCBI’s (National Center for Biotechnology Information) primary text search and retrieval system that integrates the PubMed database of biomedical literature with 38 other literature and molecular databases including DNA and protein sequence, structure, gene, genome, genetic variation and gene expression

**UMLS:** Unified Medical Language System

**Medical treatment:**  The management and care of a patient to combat disease or disorder

**Data Analysis:** A process of inspecting, cleansing, transforming and modeling data with the goal of discovering useful information, informing conclusions and supporting decision-making

**Data:** The quantities, characters, or symbols on which operations are performed by a computer, which may be stored and transmitted in the form of electrical signals and recorded on magnetic, optical, or mechanical recording media

**System Requirements:** A statement that identifies the functionality that is needed by a system in order to satisfy the customer's requirements

**User Requirements:** A document usually used in software engineering that specifies what the user expects the software to be able to do

**Covid-19:** A disease caused by a new strain of coronavirus. 'CO' stands for corona, 'VI' for virus, and 'D' for disease. Formerly, this disease was referred to as '2019 novel coronavirus' or '2019-nCoV.'
