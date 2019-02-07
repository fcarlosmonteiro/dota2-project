import json

json_file='heroStats.json'
json_data=open(json_file)
dataset = json.load(json_data)

atkmin = 100000
for data in dataset:
	if data['move_speed'] < atkmin:
		atkmin=data['move_speed']
print(atkmin)

#para 5 heros
#atk min 11 (55 for 5 heros) e max 70 (350 for 5 heros)
#move min 270 (1350 for 5 heros) e max 335 (1675 for 5 heros)
#roles min -5 e max 10
#gankFitMin = 320
#gankFitMax = 2075