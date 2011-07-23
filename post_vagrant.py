from jsonrequester import JsonRequester

requester = JsonRequester('http://33.33.33.10')

print requester.post('/record', {'type': 'test'})
