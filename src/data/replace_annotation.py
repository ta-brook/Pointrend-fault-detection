import json
import os

outcrop_path ='data/raw/resized/'
seismic_path = 'data/raw/seismic/anno/'
save_path = 'data/raw/seismic/resized/'

# # TODO access to annotation
outcrop_data_path = [file for file in os.listdir(outcrop_path) if file.endswith('.json')]
seismic_data_path = [file for file in os.listdir(seismic_path) if file.endswith('.json')]

for data in outcrop_data_path:
     with open(outcrop_path + data) as i:
          outcrop_annotation = json.loads(i.read())
     with open(seismic_path + data.replace('fault','seismic')) as j:
          seismic_annotation = json.loads(j.read())

     seismic_annotation['shapes'] = outcrop_annotation['shapes']

     with open(save_path + data.replace('fault','seismic'), 'w', encoding='utf-8') as f:
          json.dump(seismic_annotation, f, ensure_ascii=False, indent=4)

     print(data)
