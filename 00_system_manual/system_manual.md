# USER’S MANUAL

#### Overview

The System Manual provides System Personnel with a detailed operational description of the Dolphin COVID-19 Publication Search System and its associated environments, 
such as the search procedures and its technical insights.

## 1.	SYSTEM MANUAL OVERVIEW

### 1.1.	System Overview

 ![class_diagram_annotation-Page-2](https://user-images.githubusercontent.com/25805267/106479428-61f46280-64bb-11eb-97ad-c105cdf80b22.png)


The system provides search service to the end-users. It uses PubMed as the source of the articles and Entrez API to fetch the desired information from the articles. 
Domain of the articles is COVID-19. The W3C Web Annotation Data Model is used to represent the annotations on articles. UMLS is chosen to serve as a common terminology 
for the concepts. MongoDB is chosen as the database and the project is developed as a Django project. Python, Html, Css and Js are applied as programming languages. 
The application is hosted on AWS server and can be reached via:  http://ec2-3-122-230-119.eu-central-1.compute.amazonaws.com/



### 1.2.	Application Installation 

The required packages can be downloaded by default with the project download from GitHub but in case of a problem packages and their versions to install the 
application are listed below:

asgiref==3.3.1

bio==0.2.2

biopython==1.78

bson==0.5.8

certifi==2020.12.5

chardet==3.0.4

dataclasses==0.6

Django==3.1.4

django-crispy-forms==1.10.0

django-filter==2.4.0

djangorestframework==3.12.2

djangotoolbox==1.8.0

#djongo==1.3.3

dnspython==2.0.0

idna==2.10

numpy==1.19.4

pymongo==3.11.2

python-dateutil==2.8.1

pytz==2020.4

requests==2.25.0

six==1.15.0

sqlparse==0.2.4

urllib3==1.26.2

pycountry

It can be also reached as requirements.txt via Dolphin’s github page:

https://github.com/HBilge/Dolphin/



All required packages can be installed as:

pip install -r requirements.txt
 
Recall that the djongo version 1.3.3 (should be at least 1.3.4) is not compatible with the django version 3.1.4. To overcome this problem run the following command:

pip install –no-dependencies djongo==1.3.3



### 1.3.	Data Process
Stopwords are the words that should be omitted from the query to retrieve better results.
Stopwords parameter is set to: “and”, “or”, “but”. If needed it can be edited on views.py

Window size is the number of words that is permitted in between the 2 words of the same query term. If “lung cancer” is searched for then articles that include 
“lung and liver cancer” can also be retrieved for since “and” and “liver” is summed up to 2 words and 2 is in between of 0 and 4. (Recall that “and” in this sentence 
will be omitted hence the number of words in between the words searched for is 1) Window Size can be updated on regex defined in views.py {0,4}

### 1.4.	System Resources

Minimum system Resources required for the application server is demonstrated below:


OS Name: Microsoft Windows Server 2019

Version: 10.0.17763 Build 17763

Processor: Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz, 2400 Mhz, 1 Core(s), 

Logical Processor(s)

BIOS Version/Date: Xen 4.2.amazon, 8/24/2006

Installed Physical Memory (RAM): 1.00 GB

Total Physical Memory: 1.00 GB

Available Physical Memory: 118 MB

Total Virtual Memory: 2.00 GB

Available Virtual Memory: 599 MB

Page File Space: 1.00 GB


