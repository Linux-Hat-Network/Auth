from requests import get, post

#1
print("#1")
post("http://localhost:8081/api/new/user", json={"name":"admin", "password":"lollol", "is_admin":1}).json()
#2
print("#2")
post("http://localhost:8081/api/new/user", json={"name":"test", "password":"lollol", "is_admin":0}).json()