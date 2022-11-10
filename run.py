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
    os.mkdir('./ItemsAdder/data') 
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
        if get_models.endswith(".png") or get_models.endswith(".png.mcmeta"):
            shutil.copy(itemadder+"/"+get_namespace+"/textures/"+get_models,"./Oraxen/pack/textures/"+get_namespace)
            print("copy "+itemadder+"/"+get_namespace+"/textures/"+get_models)
        elif not get_models.endswith("."):
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
                    documents['items'][key]['Pack']['generate_model'] = documents['items'][key]['Pack'].pop('generate')
                    if documents['items'][key]['Pack']['generate_model'] == False:
                        documents['items'][key]['material'] = documents['items'][key]['Pack'].pop('material')
                        
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
                                if 'hitbox' in documents['items'][key]['Mechanics']['furniture'] :
                                    documents['items'][key]['Mechanics']['furniture'].pop('hitbox')
                                if 'placeable_on' in documents['items'][key]['Mechanics']['furniture'] :
                                    documents['items'][key]['Mechanics']['furniture'].pop('placeable_on')
                                if 'fixed_rotation' in documents['items'][key]['Mechanics']['furniture'] :
                                    documents['items'][key]['Mechanics']['furniture'].pop('fixed_rotation')
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
                        
                    else:
                        if 'armor' in documents['items'][key]['specific_properties']:
                            documents['items'][key]['Pack']['parent_model']= "item/generated"
                            a_text = get_namespace+"/"+documents['items'][key]['Pack']['textures'][0]
                            documents['items'][key]['Pack']['textures'] = [a_text,a_text]

                            list_type_arror = {"chest":"chestplate","legs":"leggings","feet":"boots"}
                            
                            documents['items'][key]['material'] = "LEATHER_"+list_type_arror[documents['items'][key]['specific_properties']['armor']['slot']].upper()
               
                            vv = documents['items'].pop(key)
                            nv = a_text.split("/")[2].split("_")[0]
                            nk = nv+'_'+list_type_arror[vv['specific_properties']['armor']['slot']]
                            documents['items'][nk] = vv
                            documents['items'][nk].pop('specific_properties')
                            
                            


                            # replace name armor
                            if os.path.exists(f"Oraxen/pack/textures/{get_namespace}/armor/{nv}_chestplate.png"):
                                old_file = os.path.join(f"Oraxen/pack/textures/{get_namespace}/armor", f"{nv}_chestplate.png")
                                new_file = os.path.join(f"Oraxen/pack/textures/{get_namespace}/armor", f"{nv}_armor_layer_1.png")
                                os.rename(old_file, new_file)
                            if os.path.exists(f"Oraxen/pack/textures/{get_namespace}/armor/{nv}_leggings.png"):
                                old_file_2 = os.path.join(f"Oraxen/pack/textures/{get_namespace}/armor", f"{nv}_leggings.png")
                                new_file_2 = os.path.join(f"Oraxen/pack/textures/{get_namespace}/armor", f"{nv}_armor_layer_2.png")
                                os.rename(old_file_2, new_file_2)
                            
                                
                            # set armor 128x32 config
                            if not os.path.exists(f"Oraxen/settings.yml"):
                                shutil.copy(f"Oraxen/Oraxen_settings.yml", f"Oraxen/settings.yml")
                            # documents['items'][key]['Pack']['textures'].append(a_text)
                with open(r'Oraxen\\items\\'+get_file, 'w') as file:
                    documents = yaml.dump(documents['items'], file)
                print("Convet file "+get_file) 