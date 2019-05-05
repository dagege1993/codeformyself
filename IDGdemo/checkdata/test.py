payload = "{\r\n    \"param\": {\r\n        \"company\": \"流利说\",\r\n        \"category\": \"课程\",\r\n        \"start\": \"2019-01-13\",\r\n        \"end\": \"2019-09-01\"\r\n    },\r\n    \"data\": [\r\n        {\r\n            \"type\": \"课程数\",\r\n            \"dt\": \"2019-01-13\",\r\n            \"data\": 75\r\n        },\r\n        {\r\n            \"type\": \"课程数\",\r\n            \"dt\": \"2019-01-14\",\r\n            \"data\": 101\r\n        }\r\n    ]\r\n}"
import json

result = json.loads(payload)
print(result)
