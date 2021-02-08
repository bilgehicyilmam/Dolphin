# User Test Cases and Testing Results

## Basic Search

**Title:** Open homepage and do basic search.

**Description:** A user should be able to enter query terms into search field by entering comma between the words, and the system should be able to search these terms in articles. (The basic search should be able to gather articles based on **AND** search)

**Precondition:** None

**Test Steps:**

1. Navigate to the webpage.
2. In the 'query' field, enter the query terms by putting comma between the words.
3. Click ‘Search’.

**Test Data:**

* lung, breath

**Expected Result:** A page displaying the total 111 articles that includes lung AND breath together. Synonym form popup should be displayed as well that includes the synonyms and children of query terms.

**Actual Result:** As expected

**Result:** Pass

## Faceted Search with Date

**Title:** Open homepage and do faceted search with dates.

**Description:** A user should be able to enter query terms into search field by entering comma between the words. On the other hand, the user should be able to pick start date and end date. The system should be able to search these terms in articles by checking the dates of the articles. 

**Precondition:** None

**Test Steps:**

1. Navigate to the webpage.
2. In the 'query' field, enter the query terms by putting comma between the words.
3. In the dates field, choose start date/ end date preferably.
4. Click ‘Search’.

**Test Data:**

* lung, breath
* 2020-04-01 / 2020-11-30

**Expected Result:** A page displaying the total 97 articles that includes lung AND breath together between the dates of 2020-04-01 and 2020-11-30. Synonym form popup should be displayed as well that includes the synonyms and children of query terms.

**Actual Result:** As expected

**Result:** Pass

## Faceted Search with Country

**Title:** Open homepage and do faceted search with country data.

**Description:** A user should be able to enter query terms into search field by entering comma between the words. On the other hand, the user should be able to pick country. The system should be able to search these terms in articles by checking the country information of the articles. 

**Precondition:** None

**Test Steps:**

1. Navigate to the webpage.
2. In the 'query' field, enter the query terms by putting comma between the words.
3. In the country field, choose country.
4. Click ‘Search’.

**Test Data:**

* lung, breath
* Italy

**Expected Result:** A page displaying the total 8 articles that includes lung AND breath together in Italy. Synonym form popup should be displayed as well that includes the synonyms and children of query terms.

**Actual Result:** As expected

**Result:** Pass

## Dimensional Search

**Title:** Open homepage and do dimensional search.

**Description:** A user should be able to enter query terms into search field by entering comma between the words. On the other hand, the user should be able to add new dimensions to main query. The system shall also allow to remove dimensions. The search result must show summary table that includes the total counts of the combinations of query terms with the terms in dimensions.

**Precondition:** None

**Test Steps:**

1. Navigate to the webpage.
2. Click on Dimensional Search button under the basic search field.
3. Navigate to the dimensional search page.
4. In the 'query' field, enter the query terms by putting comma between the words.
5. Click on Add Dimension button to add a new dimension.
6. Enter new query terms with comma between them.
7. Click ‘Search’.

**Test Data:**

* lung
* woman, man
* breath, cough

**Expected Result:** A page displaying the summary table that shows the total counts of articles for the combinations of query terms. Synonym form popup should be displayed as well that includes the synonyms and children of query terms.

* lung: 3390
* lung, woman: 49
* lung, man: 58
* lung, breath: 111
* lung, cough: 240
* lung, woman, breath: 4
* lung, man, cough: 17
* lung, man, breath: 8
* lung, woman, cough: 13

**Actual Result:** As expected

**Result:** Pass

## Search with Graphs

**Title:**  Navigation to related articles with graphs.

**Description:** The user should be able to click on the graph that shows the counts of articles and navigate to the related search results. 

**Precondition:** Search result is displayed.

**Test Steps:**

1. Click on some part of a country graph. For example, Italy that includes the total 474 articles. (prefererably)
2. Click on some part of a date graph. For example, 2019-June that includes the total 6 articles. (prefererably)

**Test Data:**

* lung

**Expected Result:** Navigation to the page displaying the total 474 articles **OR** Navigation to the page displaying the total 6 articles.

**Actual Result:** As expected

**Result:** Pass

## Article with Annotations

**Title:** The user should be able to view annotations for medical terms on the article details page.

**Description:** The user should be able to click on pubmed id of an article and navigate to the related article's details such as title or abstract. When the user is navigated to the related article, medical terms should be shown as annotated. When the user clicks on the word, annotation should be displayed as popup.

**Precondition:** Search result is displayed.

**Test Steps:**

1. Click on pubmed id of an article.

**Test Data:**

* lung

**Expected Result:** A page displaying the title, pubmed id, abstract, keywords, publication date, DOI link, authors, conclusions, results, copyrights, journals if exist.
Medical terms such as lung should be annotated on the page as well. When the user click on a word, a popup should be displayed that includes the explanation of the medical term lung.

**Actual Result:** As expected

**Result:** Pass
