import requests

BASE = "http://127.0.0.1:5000/"

response1 = requests.put(BASE + "video/1",{"name":"mandom","views":90,"likes":23})
response2 = requests.get(BASE+ "video/12112")

print(response1.json())
print(response2.json())
