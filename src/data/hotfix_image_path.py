import json
import os

outcrop_path ='data/annotation/outcrop/json_new/'
save_path = 'data/annotation/outcrop/json_new/'

# # TODO access to annotation
outcrop_data_path = [file for file in os.listdir(outcrop_path) if file.endswith('.json')]

for data in outcrop_data_path:
    with open(outcrop_path + data) as i:
         outcrop_annotation = json.loads(i.read())
         
    print(outcrop_annotation['imagePath'])
    outcrop_annotation['imagePath'] = outcrop_annotation['imagePath'].replace('json','png')
    print(outcrop_annotation['imagePath'])

    with open(save_path + data, 'w', encoding='utf-8') as f:
         json.dump(outcrop_annotation, f, ensure_ascii=False, indent=4)

    print(data)
