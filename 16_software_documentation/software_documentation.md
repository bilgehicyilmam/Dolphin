# Software Documentation

### 1. Dimensional Search


def dimensional search():

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
			get the element from the the main query list and get the element from the first dimension list and give these elements as parameters to count function by calling count function 
			get the result of count function which is the total number of articles
			append query term and related count to combination results in order

	if there are more than or equal to one element in second dimension list(query_2):
		for each element in main query list (query_0) and first dimension list (query_2):
			get the element from the the main query list and get the element from the second dimension list and give these elements as parameters to count function by calling count function 
			get the result of count function which is the total number of articles
			append query term and related count to combination results in order 
			
	if there are more than or equal to one element in second dimension list(query_3):
		for each element in main query list (query_0) and first dimension list (query_3):
			get the element from the the main query list and get the element from the second dimension list and give these elements as parameters to count function by calling count function 
			get the result of count function which is the total number of articles
			append query term and related count to combination results in order 
			
	if there are more than or equal to one element in second dimension list(query_4):
		for each element in main query list (query_0) and first dimension list (query_4):
			get the element from the the main query list and get the element from the second dimension list and give these elements as parameters to count function by calling count function 
			get the result of count function which is the total number of articles
			append query term and related count to combination results in order 
			
	
	
	
