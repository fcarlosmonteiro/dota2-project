import json

json_file='heroStats.json'
json_data=open(json_file)
dataset = json.load(json_data)
fitvalue=0
for id_hero in range(1,10):
	for data in dataset:
		if data['id']==id_hero:
			fitvalue = fitvalue + data['base_agi']
			for r in data['roles']:
				print (r)
#print (fitvalue)
