import json

json_file='heroStats.json'
json_data=open(json_file)
dataset = json.load(json_data)

base =-100000
for data in dataset:
	if data['base_str'] > base:
		base=data['base_str']
		print(base)
print(base*5)

#para 5 heros
#atk min 55 e max 350
#move min 1350 e max 1675
#roles min -25 e max 50
#FitMin = 1380
#FitMax = 2075

#base_str min = 60 e base_str max = 150
#atk_rate min = 6.5 e atk_rate max = 10
#roles min -25 e max 50
#FitMin = 41,5
#FitMax = 210

#base_agi min = 0 e base_str max = 180
#roles min -25 e max 10
#primary_attr min = 1 e primary_attr max = 20
#FitMin = 1
#FitMax = 190