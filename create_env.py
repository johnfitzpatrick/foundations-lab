import requests


params = {'name':'mocking_service','url':'http://mockbin.org'}
r = requests.post('http://localhost:8001/services',data = params)
print(r.status_code)

params = {'name':'mocking','hosts':'localhost','paths[]':'/mock'}
r = requests.post('http://localhost:8001/services/mocking_service/routes',data = params)
print(r.status_code)

params = {'username':'Jane'}
r = requests.post('http://localhost:8001/consumers',data = params)
print(r.status_code)


params = {'name':'rate-limiting','config.minute':5,'config.policy':'local'}
r = requests.post('http://localhost:8001/plugins',data = params)
print(r.status_code)


print(r.status_code)
