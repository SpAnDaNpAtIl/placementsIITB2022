import json

#for reseting everything, simply delete res.json and run file = open('res.json', 'w') file.close()

with open('res.json') as f:
    data = json.load(f)

g_min = 1600000
ctc_min = 2000000

for i in data:
    if i['compDet'][0].get('gross')>g_min and i['compDet'][0].get('ctc')>ctc_min and 'soft' not in i['title'].lower():
        print(i.get('title'), i.get('company').get('name'), i['compDet'][0].get('gross'), i['compDet'][0].get('ctc'))


print(data[0])