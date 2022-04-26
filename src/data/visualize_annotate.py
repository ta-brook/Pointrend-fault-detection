import os

annotation = input(f'annotation path (e.g. outcrop, seismic): ')

data_path = 'data/annotation/'
# data_annotated = data_path + f'{annotation}/json/'
data_annotated = data_path + f'{annotation}/json_replaced/'
save_labelme_directory = data_path + f'{annotation}/{annotation}_visualized/'
save_viz_img = data_path + f'{annotation}/viz_img/'

# TODO mkdir 
if not os.path.exists(save_labelme_directory):
    os.makedirs(save_labelme_directory)
if not os.path.exists(save_viz_img):
    os.makedirs(save_viz_img)

# TODO access to annotation
ls_data_path = [file for file in os.listdir(data_annotated) if file.endswith('.json')]

# TODO visualize and store data
try:
    save_path = []
    for idx, file_name in enumerate(ls_data_path):
        os.system(f'labelme_json_to_dataset {data_annotated + file_name} -o {save_labelme_directory + file_name[:-5]}')
        os.replace(f'{save_labelme_directory + file_name[:-5]}/label_viz.png', f'{save_viz_img}/{file_name}.png')
        print(file_name)

except AssertionError as error:
    print(error)

print(ls_data_path)

# f = '001_fault_data.json'
# print(f[:-5])

