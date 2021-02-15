
# 1. Dimensional Search

	combination_results = {empty dictionary}

	if there is a get request:
	
		if "main query" in get request:
			split query from comma and append to first empty query list (query_0)
		if "first dimension" in get request:
			split query from comma and append to second empty query list (query_1)
		if "second dimension" in get request:
			split query from comma and append to third empty query list (query_2)
		if "fourth dimension" in get request:
			split query from comma and append to fourth empty query list (query_3)
		if "fifth dimension" in get request:
			split query from comma and append to fifth empty query list (query_4)
			
		if there are more than or equal to one element in main query list(query_0):
		
			for each element in query list, call count function 
			append query term and related count to combination results in order 
		
		if there are more than or equal to one element in first dimension list(query_1):
		
			for each element in main query list (query_0) and first dimension list (query_1):
				get the element from the the main query list and get the element from the first dimension list and give 
				these elements as parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order

		if there are more than or equal to one element in second dimension list(query_2):
		
			for each element in main query list (query_0) and second dimension list (query_2):
				get the element from the the main query list and get the element from the second dimension list and give 
				these elements as parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to one element in third dimension list(query_3):
		
			for each element in main query list (query_0) and third dimension list (query_3):
				get the element from the the main query list and get the element from the third dimension list and give 
				these elements as parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to one element in fourth dimension list(query_4):
		
			for each element in main query list (query_0) and fourth dimension list (query_4):
				get the element from the the main query list and get the element from the fourth dimension list and give 
				these elements as parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to two elements in main query list(query_0):
		
			take the element from the first index of the main query list and append to the end of a list
			
			if there are more than or equal to one element in first dimension list(query_1):
			
				for each element in main query list (query_0) and first dimension list (query_1):
					get the element from the the main query list and get the element from the first dimension list
					and give these elements as parameters to count function by calling count function 
					get the result of count function which is the total number of articles
					append query term and related count to combination results in order
					
			if there are more than or equal to one element in second dimension list(query_2):
			
				for each element in main query list (query_0) and second dimension list (query_2):
				
					get the element from the the main query list and get the element from the second dimension list 
					and give these elements as parameters to count function by calling count function 
					get the result of count function which is the total number of articles
					append query term and related count to combination results in order 
				
			if there are more than or equal to one element in third dimension list(query_3):
			
				for each element in main query list (query_0) and third dimension list (query_3):
					get the element from the the main query list and get the element from the third dimension list 
					and give these elements as parameters to count function by calling count function 
					get the result of count function which is the total number of articles
					append query term and related count to combination results in order 
				
			if there are more than or equal to one element in fourth dimension list(query_4):
			
				for each element in main query list (query_0) and fourth dimension list (query_4):
					get the element from the the main query list and get the element from the fourth dimension list 
					and give these elements as parameters to count function by calling count function 
					get the result of count function which is the total number of articles
					append query term and related count to combination results in order 
					
		if there are more than or equal to three elements in main query list(query_0):
		
			take the element from the first index of main query list and append to the end of a list
			
			if there are more than or equal to one element in first dimension list(query_1):
			
				for each element in main query list (query_0) and first dimension list (query_1):
				
					get the element from the the main query list and get the element from the first dimension list 
					and give these elements as parameters to count function by calling count function 
					get the result of count function which is the total number of articles
					append query term and related count to combination results in order
					
			if there are more than or equal to one element in second dimension list(query_2):
			
				for each element in main query list (query_0) and second dimension list (query_2):
				
					get the element from the the main query list and get the element from the second dimension list 
					and give these elements as parameters to count function by calling count function 
					get the result of count function which is the total number of articles
					append query term and related count to combination results in order 
				
			if there are more than or equal to one element in third dimension list(query_3):
			
				for each element in main query list (query_0) and third dimension list (query_3):
				
					get the element from the the main query list and get the element from the third dimension list 
					and give these elements as parameters to count function by calling count function 
					get the result of count function which is the total number of articles
					append query term and related count to combination results in order 
				
			if there are more than or equal to one element in fourth dimension list(query_4):
			
				for each element in main query list (query_0) and fourth dimension list (query_4):
				
					get the element from the the main query list and get the element from the fourth dimension list 
					and give these elements as parameters to count function by calling count function 
					get the result of count function which is the total number of articles
					append query term and related count to combination results in order 
					
					
		if there are more than or equal to one element in first dimension list (query_1) and more than or equal to one element in 
		second dimension list (query_2):
		
			for each element in main query list (query_0) and first dimension list (query_1) and second dimension list (query_2):
			
				get the element from the the main query list, get the element from the first dimension list and get the 
				element from the second dimension list and give these elements as parameters to count function by calling 
				count function 
			        get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to two elements in first dimension list(query_1) and more than or equal to one element in 
		second dimension list(query_2):
		
			take the element from the first index of first dimension list (query_1) and append to the end of a list
			
			for each element in main query list (query_0) and first dimension list (query_1) and second dimension list (query_2):
			
				get the element from the the main query list, get the element from the first dimension list and get the 
				element from the second dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to three elements in first dimension list(query_1) and more than or equal to one element in 
		second dimension list(query_2):
		
			take the element from the first index of first dimension list (query_1) and append to the end of a list
			
			for each element in main query list (query_0) and first dimension list (query_1) and second dimension list (query_2):
			
				get the element from the the main query list, get the element from the first dimension list and get the 
				element from the second dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to four elements in first dimension list(query_1) and more than or equal to one element 
		in second dimension list(query_2):
		
			take the element from the first index of first dimension list (query_1) and append to the end of a list
			
			for each element in main query list (query_0) and first dimension list (query_1) and second dimension list (query_2):
			
				get the element from the the main query list, get the element from the first dimension list and get the 
				element from the second dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to two elements in second dimension list(query_2) and more than or equal to one element in 
		first dimension list(query_1):
		
			take the element from the first index of second dimension list (query_2) and append to the end of a list
			
			for each element in main query list (query_0) and first dimension list (query_1) and second dimension list (query_2):
			
				get the element from the the main query list, get the element from the first dimension list and get the
				element from the second dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to three elements in second dimension list(query_2) and more than or equal to one element in 
		first dimension list(query_1):
		
			take the element from the first index of second dimension list (query_2) and append to the end of a list
			
			for each element in main query list (query_0) and first dimension list (query_1) and second dimension list (query_2):
				get the element from the the main query list, get the element from the first dimension list and get the 
				element from the second dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to four elements in second dimension list(query_2) and more than or equal to one element
		in first dimension list(query_1):
		
			take the element from the first index of second dimension list (query_2) and append to the end of a list
			
			for each element in main query list (query_0) and first dimension list (query_1) and second dimension list (query_2):
				get the element from the the main query list, get the element from the first dimension list and get the 
				element from the second dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order
				
		if there are more than or equal to one element in third dimension list(query_3):
		
			for each element in main query list (query_0) and first dimension list (query_1) and third dimension list (query_3):
				get the element from the the main query list, get the element from the first dimension list and get the 
				element from the third dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
			for each element in main query list (query_0) and second dimension list (query_2) and third dimension list (query_3):
				get the element from the the main query list, get the element from the second dimension list and get the
				element from the third dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to two elements in third dimension list(query_3):
		
			take the element from the first index of third dimension list (query_3) and append to the end of a list
			
			for each element in main query list (query_0) and first dimension list (query_1) and third dimension list (query_3):
				get the element from the the main query list, get the element from the first dimension list and get the 
				element from the third dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
			for each element in main query list (query_0) and second dimension list (query_2) and third dimension list (query_3):
				get the element from the the main query list, get the element from the second dimension list and get the
				element from the third dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to three elements in third dimension list(query_3):
		
			take the element from the first index of third dimension list (query_3) and append to the end of a list
			
			for each element in main query list (query_0) and first dimension list (query_1) and third dimension list (query_3):
				get the element from the the main query list, get the element from the first dimension list and get the 
				element from the third dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
			for each element in main query list (query_0) and second dimension list (query_2) and third dimension list (query_3):
				get the element from the the main query list, get the element from the second dimension list and get the
				element from the third dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to four elements in third dimension list(query_3):
		
			take the element from the first index of third dimension list (query_3) and append to the end of a list
			
			for each element in main query list (query_0) and first dimension list (query_1) and third dimension list (query_3):
				get the element from the the main query list, get the element from the first dimension list and get the 
				element from the third dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
			for each element in main query list (query_0) and second dimension list (query_2) and third dimension list (query_3):
				get the element from the the main query list, get the element from the second dimension list and get the 
				element from the third dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order
				
		if there are more than or equal to one element in fourth dimension list(query_4):
		
			for each element in main query list (query_0) and first dimension list (query_1) and fourth dimension list (query_4):
				get the element from the the main query list, get the element from the first dimension list and get the 
				element from the fourth dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
			for each element in main query list (query_0) and second dimension list (query_2) and fourth dimension list (query_4):
				get the element from the the main query list, get the element from the second dimension list and get the 
				element from the fourth dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
			for each element in main query list (query_0) and third dimension list (query_3) and fourth dimension list (query_4):
				get the element from the the main query list, get the element from the third dimension list and get the 
				element from the fourth dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
			for each element in main query list (query_0) and first dimension list (query_1) and third dimension list (query_3) 
			and fourth dimension list (query_4):
				get the element from the the main query list, get the element from the first dimension list, get the
				element from the third dimension list and get the element from the fourth dimension list and give these 
				elements as parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
			for each element in main query list (query_0) and second dimension list (query_2) and third dimension list (query_3)
			and fourth dimension list (query_4):
				get the element from the the main query list, get the element from the second dimension list, get the 
				element from the third dimension list and get the element from the fourth dimension list and give these 
				elements as parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to two elements in fourth dimension list(query_4):
				
			take the element from the first index of fourth dimension list (query_4) and append to the end of a list
		
			for each element in main query list (query_0) and first dimension list (query_1) and fourth dimension list (query_4):
				get the element from the the main query list, get the element from the first dimension list and get 
				the element from the fourth dimension list and give these elements as parameters to count function by 
				calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
			for each element in main query list (query_0) and second dimension list (query_2) and fourth dimension list (query_4):
				get the element from the the main query list, get the element from the second dimension list and get the 
				element from the fourth dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
			for each element in main query list (query_0) and third dimension list (query_3) and fourth dimension list (query_4):
				get the element from the the main query list, get the element from the third dimension list and get the 
				element from the fourth dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
			for each element in main query list (query_0) and first dimension list (query_1) and third dimension list (query_3) 
			and fourth dimension list (query_4):
				get the element from the the main query list, get the element from the first dimension list, get the 
				element from the third dimension list and get the element from the fourth dimension list and give these 
				elements as parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
			for each element in main query list (query_0) and second dimension list (query_2) and third dimension list (query_3) 
			and fourth dimension list (query_4):
				get the element from the the main query list, get the element from the second dimension list, get the 
				element from the third dimension list and get the element from the fourth dimension list and give these 
				elements as parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
		
		if there are more than or equal to one element in third dimension list(query_3):
			
			for each element in main query list (query_0) and first dimension list (query_1) and second dimension list (query_2)
			and third dimension list (query_3):
				get the element from the the main query list, get the element from the first dimension list, get 
				the element from the second dimension list and get the element from the third dimension list and give 
				these elements as parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
		
		if there are more than or equal to two elements in third dimension list(query_3):
		
			take the element from the first index of third dimension list (query_3) and append to the end of a list
			
			for each element in main query list (query_0) and first dimension list (query_1) and second dimension list (query_2) 
			and third dimension list (query_3):
				get the element from the the main query list, get the element from the first dimension list, get the 
				element from the second dimension list and get the element from the third dimension list and give these 
				elements as parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to three elements in third dimension list(query_3):
		
			take the element from the first index of third dimension list (query_3) and append to the end of a list
			
			for each element in main query list (query_0) and first dimension list (query_1) and second dimension list (query_2) 
			and third dimension list (query_3):
				get the element from the the main query list, get the element from the first dimension list, get the element
				from the second dimension list and get the element from the third dimension list and give these elements as 
				parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to fourth elements in third dimension list(query_3):
		
			take the element from the first index of third dimension list (query_3) and append to the end of a list
			
			for each element in main query list (query_0) and first dimension list (query_1) and second dimension list (query_2) 
			and third dimension list (query_3):
				get the element from the the main query list, get the element from the first dimension list, get the element 
				from the second dimension list and get the element from the third dimension list and give these elements 
				as parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to one element in fourth dimension list(query_4):
			
			for each element in main query list (query_0) and first dimension list (query_1) and second dimension list (query_2) 
			and third dimension list (query_3) and fourth dimension list (query_4):
				get the element from the the main query list, get the element from the first dimension list, get the element 
				from the second dimension list, get the element from the third dimension list and get the element from the 
				fourth dimension list and give these elements as parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
			if there are more than or equal to two elements in third dimension list(query_3):
		
				take the element from the first index of third dimension list (query_3) and append to the end of a list
				
				for each element in main query list (query_0) and first dimension list (query_1) and second dimension list 
				(query_2) and third dimension list (query_3) and fourth dimension list (query_4):
				get the element from the the main query list, get the element from the first dimension list, get the 
				element from the second dimension list, get the element from the third dimension list and get the 
				element from the fourth dimension list and give these elements as parameters to count function by 
				calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
			if there are more than or equal to two elements in second dimension list(query_2):
		
				take the element from the first index of second dimension list (query_2) and append to the end of a list
				
				for each element in main query list (query_0) and first dimension list (query_1) and second dimension list 
				(query_2) and third dimension list (query_3) and fourth dimension list (query_4):
				get the element from the the main query list, get the element from the first dimension list, get the element 
				from the second dimension list, get the element from the third dimension list and get the element from the 
				fourth dimension list and give these elements as parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
			if there are more than or equal to two elements in first dimension list(query_1):
		
				take the element from the first index of first dimension list (query_1) and append to the end of a list
				
				for each element in main query list (query_0) and first dimension list (query_1) and second dimension list 
				(query_2) and third dimension list (query_3) and fourth dimension list (query_4):
				get the element from the the main query list, get the element from the first dimension list, get the element 
				from the second dimension list, get the element from the third dimension list and get the element from the 
				fourth dimension list and give these elements as parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to two elements in fourth dimension list(query_4):
		
			take the element from the first index of fourth dimension list (query_4) and append to the end of a list
			
			for each element in main query list (query_0) and first dimension list (query_1) and second dimension list (query_2)
			and third dimension list (query_3) and fourth dimension list (query_4):
				get the element from the the main query list, get the element from the first dimension list, get the element
				from the second dimension list, get the element from the third dimension list and get the element from the 
				fourth dimension list and give these elements as parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to three elements in fourth dimension list(query_4):
		
			take the element from the first index of fourth dimension list (query_4) and append to the end of a list
			
			for each element in main query list (query_0) and first dimension list (query_1) and second dimension list (query_2) 
			and third dimension list (query_3) and fourth dimension list (query_4):
				get the element from the the main query list, get the element from the first dimension list, get the element 
				from the second dimension list, get the element from the third dimension list and get the element from the 
				fourth dimension list and give these elements as parameters to count function by calling count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
		if there are more than or equal to two elements in main query list and more than or equal to two elements in third dimension
		list(query_3):
		
			take the element from the first index of main query list and append to the end of a list
			
			for each element in main query list (query_0) and first dimension list (query_1) and third dimension list (query_3):
				get the element from the the main query list, get the element from the first dimension list and get the
				element from the third dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order 
				
			for each element in main query list (query_0) and second dimension list (query_2) and third dimension list (query_3):
				get the element from the the main query list, get the element from the second dimension list and get the
				element from the third dimension list and give these elements as parameters to count function by calling 
				count function 
				get the result of count function which is the total number of articles
				append query term and related count to combination results in order
				
				
# 2. Helper Functions

```
def synonyms():

	synonyms = [empty list to hold all synonym words]
	the query = add word boundary to the query
	request the synonym (object) of the query from the database (ontologies_ontology collection)
	for each synonym word of the query:
		append to an empty list of synonyms 
		return synonyms list
```
			
```
def parent_child():

	child_words = [empty list to hold all child words]
	the query = add word boundary to the query
	request rdfs class of the query from the database (ontologies_ontology collection)
	if the result is not None:
		request subclass of the rdfs class
		for each subclass of the result:
			append to an empty list of child_words
		get the unique values from the child words list
	return child_words list
	
```

# 3. Basic Search
```
total articles count = get the count of total articles
query = get the request which is the query term for search that is searched in abstract and title if the article
start_date = get the start date of the query entered by the user
end_date = get the end date of the query entered by the user
country = get the country of the query entered by the user
invalid characters = (to be able to ignore these synonym words in search)

if there is a get request:
	synonym index = 0
	queris = split the query term by comma
	queris = remove the blank terms from the list
	replace all "," with "-" and all blanks with "0"
	
	counter = 0
	articles = [empty list]
	
	remove all "and, or" words from the query
	
		for each item in the query list:
		
			remove "and, or" and make word boundary
			
			check the following words if it is 4 word far away from the first word 
			check if includes "ed, ing" to be able to retrieve the actual word
			
			send request to MongoDB to search in abstract, title along with publication date 
			and country information

			synonym words = [empty list]
			
			find the synonym words with the help of synonym function and add it to empty list 
			synonym words
			
			temporary_synonym_list = [empty list]
			
			for each item in synonym words list:
			
				if there is any invalid characters return to for loop again
				otherwise make word boundary for the synonym word
				
				send request to MongoDB for that synonym word to search in abstract,
				title along with publication date and country information 
				append all the articles into the temporary_synonym_list
				
			child words = [empty list]
			
			find the child words with the help of parent_child function and add it to empty list 
			child words
			
			temporary_children_list = [empty list]
			
			for each item in child words list:
			
				if there is any invalid characters return to for loop again
				otherwise make word boundary for the child word
				
				send request to MongoDB for that child word to search in abstract,
				title along with publication date and country information 
				append all the articles into the temporary_children_list
				 
			if length of articles list is equal to zero:
				
				add the result of MongoDB into the articles list
				
				for each item in temporary_synonym_list:
					if the item exist in articles list do not append to articles list
					otherwise add the article to articles list
					
				for each item in temporary_children_list:
					if the item exist in articles list do not append to articles list
					otherwise add the article to articles list
					
			temporay articles list = [empty list]
					
			if length of articles list is not equal to zero:
			
				get the result of MongoDB and check if the articles exist in articles list already
				
				if exist append to temporay articles list
				
				for each item in temporary_synonym_list:
					if the item exist in articles list append to temporay articles list
					
				for each item in temporary_children_list:
					if the item exist in articles list append to temporay articles list
					
			articles = temporay articles list
					
	return articles
```	
				
				
				
				
				
		
		





					
					
					
					
					
					
					
					
					
			
					
				
			
				
			
						
						
		
		
		
