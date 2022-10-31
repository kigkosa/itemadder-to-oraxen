
import shutil
import os
import yaml


# replace text json to oraxen
def replace_text_json(dir,namespce,filename):
  if filename.endswith(".json"):
    with open(dir, 'r') as file :
        filedata = file.read()
    filedata = filedata.replace(namespce+":", namespce+'/')
    with open(dir, 'w') as file:
        file.write(filedata)
    print("replace "+dir)

def rename_keys(dict_, new_keys):
    d1 = dict( zip( list(dict_.keys()), new_keys) )
    return {d1[oldK]: value for oldK, value in dict_.items()}
if not os.path.isdir('./ItemsAdder'):
    os.mkdir('./ItemsAdder') 
if not os.path.isdir('./Oraxen'):
    os.mkdir('./Oraxen') 
    os.mkdir('./Oraxen/items') 
    os.mkdir('./Oraxen/pack') 
    os.mkdir('./Oraxen/pack/models') 
    os.mkdir('./Oraxen/pack/textures')

itemadder = './ItemsAdder/data/resource_pack/assets'
for get_namespace in os.listdir(itemadder):

    if not os.path.isdir('./Oraxen/pack/models/'+get_namespace):
        os.mkdir('./Oraxen/pack/models/'+get_namespace)
        os.mkdir('./Oraxen/pack/textures/'+get_namespace)

    # get all model json replace
    for get_models in os.listdir(itemadder+"/"+get_namespace+"/models"):
        replace_text_json(itemadder+"/"+get_namespace+"/models/"+get_models,get_namespace,get_models)
        if not get_models.endswith(".json"):
           for get_models_2 in os.listdir(itemadder+"/"+get_namespace+"/models/"+get_models):
                replace_text_json(itemadder+"/"+get_namespace+"/models/"+get_models+"/"+get_models_2,get_namespace,get_models_2)
    # get all model json coppy
    for get_models in os.listdir(itemadder+"/"+get_namespace+"/models"):
        if get_models.endswith(".json"):
            shutil.copy(itemadder+"/"+get_namespace+"/models/"+get_models,"./Oraxen/pack/models/"+get_namespace)
            print("copy "+itemadder+"/"+get_namespace+"/models/"+get_models)
        elif not get_models.endswith(".json"):
           for get_models_2 in os.listdir(itemadder+"/"+get_namespace+"/models/"+get_models):
                if not os.path.isdir("./Oraxen/pack/models/"+get_namespace+"/"+get_models):
                    os.mkdir("./Oraxen/pack/models/"+get_namespace+"/"+get_models)
                shutil.copy(itemadder+"/"+get_namespace+"/models/"+get_models+"/"+get_models_2,"./Oraxen/pack/models/"+get_namespace+"/"+get_models+"/"+get_models_2)
                print("copy "+itemadder+"/"+get_namespace+"/models/"+get_models+"/"+get_models_2)
    for get_models in os.listdir(itemadder+"/"+get_namespace+"/textures"):
        if get_models.endswith(".png"):
            shutil.copy(itemadder+"/"+get_namespace+"/textures/"+get_models,"./Oraxen/pack/textures/"+get_namespace)
            print("copy "+itemadder+"/"+get_namespace+"/textures/"+get_models)
        elif not get_models.endswith(".png"):
           for get_models_2 in os.listdir(itemadder+"/"+get_namespace+"/textures/"+get_models):
                if not os.path.isdir("./Oraxen/pack/textures/"+get_namespace+"/"+get_models):
                    os.mkdir("./Oraxen/pack/textures/"+get_namespace+"/"+get_models)
                shutil.copy(itemadder+"/"+get_namespace+"/textures/"+get_models+"/"+get_models_2,"./Oraxen/pack/textures/"+get_namespace+"/"+get_models+"/"+get_models_2)
                print("copy "+itemadder+"/"+get_namespace+"/textures/"+get_models+"/"+get_models_2)

# item pack to oraxen
itemadder = './ItemsAdder/data/items_packs'
for get_namespace in os.listdir(itemadder):
    for get_file in os.listdir(itemadder+"/"+get_namespace):
        
        with open(itemadder+"/"+get_namespace+"/"+get_file) as file:
            documents = yaml.full_load(file)
            if  'items' in documents:
                for key in documents['items']:
                    documents['items'][key]['Pack'] = documents['items'][key].pop('resource')
                    documents['items'][key]['displayname'] = documents['items'][key].pop('display_name')
                    documents['items'][key]['material'] = documents['items'][key]['Pack'].pop('material')
                    
                    documents['items'][key]['Pack']['generate_model'] = documents['items'][key]['Pack'].pop('generate')
                    if 'behaviours' in documents['items'][key]:
                        if 'furniture' in documents['items'][key]['behaviours']:
                            documents['items'][key]['Mechanics'] = documents['items'][key].pop('behaviours')
                            # print(documents['items'][key]['Mechanics']['furniture']['solid'])
                            if 'solid' in documents['items'][key]['Mechanics']['furniture'] :
                                if documents['items'][key]['Mechanics']['furniture']['solid'] == True:
                                    documents['items'][key]['Mechanics']['furniture']['barrier'] = documents['items'][key]['Mechanics']['furniture']['solid']
                                    documents['items'][key]['Mechanics']['furniture'].pop('solid')
                                else:
                                    documents['items'][key]['Mechanics']['furniture']['barrier'] = False
                            else:
                                documents['items'][key]['Mechanics']['furniture']['barrier'] = False
                            documents['items'][key]['Mechanics']['furniture']['facing'] = 'UP'
                            documents['items'][key]['Mechanics']['furniture']['rotation'] = 90

                    if 'model_id' in documents['items'][key]['Pack']:
                        documents['items'][key]['Pack']['custom_model_data'] = documents['items'][key]['Pack'].pop('model_id')
                    if 'model_path' in documents['items'][key]['Pack']:
                        documents['items'][key]['Pack']['model'] = documents['items'][key]['Pack'].pop('model_path')
                    if 'hat' in documents['items'][key]:
                        documents['items'][key]['hat'] = {'enabled': True}
                        # documents['items'][key].pop('hat')
                        
                    documents['items'][key]['Pack']['model'] = get_namespace+"/"+documents['items'][key]['Pack']['model']
                with open(r'Oraxen\\items\\'+get_file, 'w') as file:
                    documents = yaml.dump(documents['items'], file)
                print("Convet file "+get_file)
      


