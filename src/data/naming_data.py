import os
import json
from pathlib import Path
from PIL import Image
from collections import defaultdict




def indexing_name(image_path, save_path, outcrop_data_path):
    
    log_path = Path(image_path + "log.txt")

    if os.path.exists(log_path):
        os.remove(log_path)
        print("The file has been deleted successfully")
    else:
        print("The file does not exist!")
        
    # old_img_lst = []
    old_img_dict = defaultdict()
    count_num = 1
    count_old = 0
    f = open(image_path + "log.txt", "w")

    for data in outcrop_data_path:
        print(data)
        img = Image.open(image_path + data)
        
        if count_num < 10:
            new_name = f'00{count_num}_fault_data.png'
            img.save(f'{save_path}{new_name}')
            # os.remove(f'{image_path}{data}')
            print(f'save {data} image as {new_name}')
        else:
            new_name = f'0{count_num}_fault_data.png'
            img.save(f'{save_path}{new_name}')
            # os.remove(f'{image_path}{data}')
            print(f'save {data} image as {new_name}')

        if 'fault_data' in data:
            old_img_dict[data[:-4]] = new_name[:-4]
            print(f'found old format name :{data} renamed to {new_name}')
            count_old += 1
        
        print(f'old name is : {data} || new name is {new_name} \n---------------')
        count_num += 1
        f.write(f'old name is : {data} || new name is {new_name} \n')

    f.close()
    print('old images is {}'.format(count_old))
    print('total images is {}'.format(count_num))
    print(old_img_dict)

    return old_img_dict

def rename_old_to_new(path, json_path, save_path, old_dict):
    print(path)
    for data in path:
        print(data)
        if data[:-5] in old_dict.keys(): # hash table here 
            new_name = old_dict[data[:-5]] +'.json'
            print(f'open {json_path + data}')

            with open(json_path + data) as i:
                annotation = json.loads(i.read())

            # print(f'delete {json_path + data}')
            # os.remove(json_path + data)
            annotation['imagePath'] = new_name
            print(f'{data} renamed to {new_name} and annotated as {annotation["imagePath"]}')
            print(f'save {save_path + new_name}')

            with open(save_path + new_name, 'w', encoding='utf-8') as f:
                json.dump(annotation, f, ensure_ascii=False, indent=4)
        else:
            print(f'this one is not duplicate {data}')

        print(f'---------------')


def rename_fault_to_seismic(path, save_path):
    for data in path:
         with open(path + data) as i:
            annotation = json.loads(i.read())

            annotation['imagePath'] = annotation['imagePath'].replace('fault', 'seismic')
            data = data.replace('fault', 'seismic')

            print(data)
            print(annotation['imagePath'])


            with open(save_path + data, 'w', encoding='utf-8') as f:
                json.dump(annotation, f, ensure_ascii=False, indent=4)

# image
image_path = 'data/raw/outcrop/'
image_save_path = 'data/raw/test/'

# json
seismic_path = 'data/annotation/seismic/json/'
save_path_seis = 'data/annotation/seismic/json/'
outcrop_path = 'data/annotation/outcrop/json/'
save_path_outcrop = 'data/annotation/outcrop/json_new/'



outcrop_image_path = [file for file in os.listdir(image_path) if file.endswith(('.png', '.jpg'))]
seismic_data_path = [file for file in os.listdir(seismic_path) if file.endswith('.json')]
outcrop_data_path = [file for file in os.listdir(outcrop_path) if file.endswith('.json')]

if __name__ == '__main__':
    print('start...')
    old_dict = indexing_name(image_path, image_save_path, outcrop_image_path)
    print('finish first function')
    rename_old_to_new(outcrop_data_path, outcrop_path, save_path_outcrop, old_dict)
    print('done...')