from jsonrequester import JsonRequester

requester = JsonRequester('http://localhost:5000')

print requester.post('/record', {'type': 'test'})
