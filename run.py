import shutil
import os
import yaml


class YmlDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(YmlDumper, self).increase_indent(flow, False)
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

def color_to_hex(bb):
    color = {'4':'AA0000','c':'FF5555','6':'FFAA00','e':'FFFF55','2':'00AA00','a':'55FF55','b':'55FFFF','3':'00AAAA','1':'0000AA','9':'5555FF','d':'FF55FF','5':'AA00AA','f':'FFFFFF','7':'AAAAAA','8':'555555','0':'000000'}
    tex = {'l':'bond','k':'obfuscated','m':'strikethrough','n':'underline','o':'italic','r':'reset'}

    h_co_s = {'§'+str(co):'#'+v for co,v in color.items()}   
    h_co_s.update({'§'+str(co):v for co,v in tex.items()})
    h_co_and = {'&'+str(co):'#'+v for co,v in color.items()}   
    h_co_and.update({'&'+str(co):v for co,v in tex.items()})
    
    for v,c in h_co_s.items():        
        bb=bb.replace(v,'<'+c+'>')
    for v,c in h_co_and.items():
        bb=bb.replace(v,'<'+c+'>')
        

    return bb
    # print(color)
if not os.path.isdir('./ItemsAdder'):
    os.mkdir('./ItemsAdder') 
    os.mkdir('./ItemsAdder/data') 
if os.path.isdir('./Oraxen'):
    shutil.rmtree('./Oraxen')
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
                    documents['items'][key]['displayname'] = color_to_hex(documents['items'][key].pop('display_name'))
                    documents['items'][key]['Pack']['generate_model'] = documents['items'][key]['Pack'].pop('generate')
                    if 'lore' in documents['items'][key]:
                        lore = documents['items'][key].pop('lore')
                        l = []
                        for v in lore:
                            l.append(color_to_hex(v))
                        documents['items'][key]['lore'] = l
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
                                documents['items'][key]['material'] = "PAPER"

                        if 'model_id' in documents['items'][key]['Pack']:
                            documents['items'][key]['Pack']['custom_model_data'] = documents['items'][key]['Pack'].pop('model_id')
                        if 'model_path' in documents['items'][key]['Pack']:
                            documents['items'][key]['Pack']['model'] = documents['items'][key]['Pack'].pop('model_path')
                        if 'hat' in documents['items'][key]:
                            documents['items'][key]['hat'] = {'enabled': True}
                            # documents['items'][key].pop('hat')
                        if  'material' in documents['items'][key]:
                            if 'SHIELD' in documents['items'][key]['material']:
                                # documents['items'][key].pop('material')
                                documents['items'][key]['Pack']['blocking_model'] = get_namespace+"/"+documents['items'][key]['Pack']['model']+'_blocking'
                            elif 'CROSSBOW' in documents['items'][key]['material']:
                                # documents['items'][key].pop('material')
                                gnd = get_namespace+"/"+documents['items'][key]['Pack']['model']

                                documents['items'][key]['Pack']['charged_model'] = gnd+'_charged'
                                documents['items'][key]['Pack']['pulling_models'] = [gnd+'_0',gnd+'_1',gnd+'_2']                            
                            elif 'BOW' in documents['items'][key]['material']:
                                # documents['items'][key].pop('material')
                                gnd = get_namespace+"/"+documents['items'][key]['Pack']['model']

                                # documents['items'][key]['Pack']['charged_model'] = gnd+'_pulling_2'
                                documents['items'][key]['Pack']['pulling_models'] = [
                                    gnd+'_0',
                                        gnd+'_1',
                                        gnd+'_2'
                                ]

                            elif 'FISHING_ROD' in documents['items'][key]['material']:
                                # documents['items'][key].pop('material')
                                gnd = get_namespace+"/"+documents['items'][key]['Pack']['model']

                                documents['items'][key]['Pack']['cast_model'] = gnd+'_cast'
                                # documents['items'][key]['pulling_models'] = [gnd+'_pulling_0',gnd+'_pulling_1',gnd+'_pulling_2']



                        documents['items'][key]['Pack']['model'] = get_namespace+"/"+documents['items'][key]['Pack']['model']
                        
                    else:
                        if 'specific_properties' in documents['items'][key]:
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
                                
                                

                                old_file = ''
                                new_file = ''
                                # replace name armor
                                if os.path.exists(f"Oraxen/pack/textures/{get_namespace}/armor/{nv}_chestplate.png"):
                                    old_file = os.path.join(f"Oraxen/pack/textures/{get_namespace}/armor", f"{nv}_chestplate.png")
                                    new_file = os.path.join(f"Oraxen/pack/textures/{get_namespace}/armor", f"{nv}_armor_layer_1.png")
                                    if not os.path.exists(f"Oraxen/pack/textures/{get_namespace}/armor/{nv}_armor_layer_1.png"):
                                        os.rename(old_file, new_file)
                                    if os.path.exists(old_file):
                                        os.remove(old_file)
                                if os.path.exists(f"Oraxen/pack/textures/{get_namespace}/armor/{nv}_leggings.png"):
                                    old_file_2 = os.path.join(f"Oraxen/pack/textures/{get_namespace}/armor", f"{nv}_leggings.png")
                                    new_file_2 = os.path.join(f"Oraxen/pack/textures/{get_namespace}/armor", f"{nv}_armor_layer_2.png")
                                    if not os.path.exists(f"Oraxen/pack/textures/{get_namespace}/armor/{nv}_armor_layer_2.png"):
                                        os.rename(old_file_2, new_file_2)
                                    if os.path.exists(old_file_2):
                                        os.remove(old_file_2)
                                                                
                                # set armor 128x32 config
                                if not os.path.exists(f"Oraxen/settings.yml"):
                                    shutil.copy(f"Oraxen_settings.yml", f"Oraxen/settings.yml")
                            
                with open(r'Oraxen\\items\\'+get_file, 'w') as file:
                    documents = yaml.dump(documents['items'], file, Dumper=YmlDumper, default_flow_style=False)
                print("Convet file "+get_file) 
