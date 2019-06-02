import json

json_filelol='championsStats.json'
json_datalol=open(json_filelol)
datasetlol = json.load(json_datalol)

for data in datasetlol:
    championId = data['id']
    f = open('counters/' + str(championId) + ".txt", 'r')
    print('-------------------')
    print('Champion: ' + data['localized_name'])    
    counter1 = f.readline()
    counter2 = f.readline()
    counter3 = f.readline()
    f.close()
    counters = [counter1, counter2, counter3]
    data['counters'] = counters

json.dump(datasetlol, open('championsStatsCounters.json', 'w'))