import json

titles = []
with open('titles.txt','w') as f4:
    with open('titles','w') as f2:
        with open('titles2','w') as f3:
            with open('data.json','r') as f:
                for line in f:
                    try:
                        j = json.loads(line)
                        for d in j:
                            if 'plos' in d['url']:
                                f3.write(str(d['citations']) + '\t' + str(len(d['title'].split())) + '\n')
                            else:
                                f4.write(d['title'] + '.\n')
                                f2.write(str(d['citations']) + '\t' + str(len(d['title'].split())) + '\n')
                    except:
                        pass

