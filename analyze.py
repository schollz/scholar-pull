import json

titles = []
with open('titles','w') as f2:
    with open('titles2','w') as f3:
        with open('data.json','r') as f:
            for line in f:
                try:
                    j = json.loads(line)
                    for d in j:
                        f2.write(str(d['citations']) + '\t' + str(len(d['title'].split())) + '\n')
                except:
                    pass

