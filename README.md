# API4
Count the occurrences  of lower, upper and special character in given string
You can also specify what type of data api should return

## Resource URL
http://127.0.0.1:8000

## Endpoints:
/arhive_convert
/convert

# /convert:
Return amount of occurences in given string
##### Response format: JSON, text, xml, CSV
##### Requires authentication: No
##### Request parameters:
message(required) - string provided to calculation
type(required) - type of return message
#### Example of request
{'message': 'teSt', 'type': 'json'}
#### Example of response
{'upper': '1', lower: '3', 'special': '0'}


# /archive_convert:
Convert message to another format
##### Response format: JSON, text, xml, CSV
##### Requires authentication: No
##### Request parameters:
message(required) - string provided to calculation
old_type(required) - type of return message
#### Example of request_1
{'message': 'upper = 1 lower =3 special = 10', 'oldtype': 'txt', new_type': json'}
#### Example of response_1
{'upper': '1', lower: '3', 'special': '10'}
#### Example of request_2
{'message': '{'upper': '1', lower: '3', 'special': '10'}', 'oldtype': 'json', 'new_type': 'csv'}
#### Example of response_2
upper,lower,special
1,3,10

