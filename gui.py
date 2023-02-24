import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox 
import shutil
import os
import yaml
import glob
import requests

class App:
    def __init__(self, root):
        if not os.path.isdir('./Oraxen_settings.yml'):
            with open('Oraxen_settings.yml', 'wb') as f:
                f.write(requests.get('https://raw.githubusercontent.com/kigkosa/itemadder-to-oraxen/master/Oraxen_settings.yml').content)
        if not os.path.isdir('./icon.ico'):
            with open('icon.ico', 'wb') as f:
                f.write(requests.get('https://raw.githubusercontent.com/kigkosa/itemadder-to-oraxen/master/icon.ico').content)
        #setting title
        root.title("Itemadder to Oraxen")

        
        root.iconbitmap("icon.ico")
        #setting window size
        width=248
        height=124
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GButton_674=tk.Button(root)
        GButton_674["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_674["font"] = ft
        GButton_674["fg"] = "#000000"
        GButton_674["justify"] = "center"
        GButton_674["text"] = "Generate"
        GButton_674.place(x=40,y=40,width=185,height=61)
        GButton_674["command"] = self.GButton_674_command

        self.GLabel_225=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.GLabel_225["font"] = ft
        self.GLabel_225["fg"] = "#333333"
        self.GLabel_225["justify"] = "center"
        self.GLabel_225["text"] = ""
        self.GLabel_225.place(x=10,y=10,width=249,height=30)

        if not os.path.isdir('./ItemsAdder'):
            os.mkdir('./ItemsAdder') 
            messagebox.showinfo("Info", "Please dropfile to folder ItemsAdder")

    def GButton_674_command(self):
        
        if len(os.listdir('./ItemsAdder'))<=0:
            messagebox.showinfo("Info", "Please dropfile to folder ItemsAdder")                
            return 0
        if os.path.isdir('./ItemsAdder/contents'):
            if os.path.isdir('./ItemsAdder/data'):
                shutil.rmtree('./ItemsAdder/data')
                os.mkdir('./ItemsAdder/data') 
                os.mkdir('./ItemsAdder/data/items_packs')

                
            for get_namespace in os.listdir('./ItemsAdder/contents'):
                shutil.copytree('./ItemsAdder/contents/'+get_namespace+'/configs','./ItemsAdder/data/items_packs/'+get_namespace)
                if os.path.isdir('./ItemsAdder/contents/'+get_namespace+'/resourcepack/assets'):
                    shutil.copytree('./ItemsAdder/contents/'+get_namespace+'/resourcepack','./ItemsAdder/data/resource_pack')
                else:
                    shutil.copytree('./ItemsAdder/contents/'+get_namespace+'/resourcepack','./ItemsAdder/data/resource_pack/assets')

                # print(get_namespace)
            shutil.rmtree('./ItemsAdder/contents')
        # exit()
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
            #get all sound
            if os.path.isdir(itemadder+"/"+get_namespace+"/sounds"):
                os.mkdir('./Oraxen/pack/assets')
                os.mkdir('./Oraxen/pack/assets/'+get_namespace)
                shutil.copytree(itemadder+"/"+get_namespace+"/sounds","./Oraxen/pack/assets/"+get_namespace+"/sounds")
                shutil.copy(itemadder+"/"+get_namespace+"/sounds.json","./Oraxen/pack/assets/"+get_namespace)

                    
            # get all model json replace
            for file in glob.glob(itemadder+"/"+get_namespace+"/models/"+"**/*.json", recursive = True):
                get_models = file.replace('\\','/')
                replace_text_json(get_models,get_namespace,get_models)


            # get all model json coppy
            if os.path.isdir("./Oraxen/pack/models/"+get_namespace):
                shutil.rmtree("./Oraxen/pack/models/"+get_namespace)
            if os.path.isdir(itemadder+"/"+get_namespace+"/models"):
                shutil.copytree(itemadder+"/"+get_namespace+"/models","./Oraxen/pack/models/"+get_namespace)

            # coppy textures
            if os.path.isdir("./Oraxen/pack/textures/"+get_namespace):
                shutil.rmtree("./Oraxen/pack/textures/"+get_namespace)
            if os.path.isdir(itemadder+"/"+get_namespace+"/textures"):
                shutil.copytree(itemadder+"/"+get_namespace+"/textures","./Oraxen/pack/textures/"+get_namespace)


        
        # item pack to oraxen
        itemadder = './ItemsAdder/data/items_packs'
        for get_namespace in os.listdir(itemadder):
            for get_file in os.listdir(itemadder+"/"+get_namespace):
                
                with open(itemadder+"/"+get_namespace+"/"+get_file) as file:
                    documents = yaml.full_load(file)
                    if  'items' in documents:
                        for key in list(documents['items']):
                            documents['items'][key]['Pack'] = documents['items'][key].pop('resource')
                            documents['items'][key]['displayname'] = color_to_hex(documents['items'][key].pop('display_name').title() )
                            documents['items'][key]['Pack']['generate_model'] = documents['items'][key]['Pack'].pop('generate')
                            if 'suggest_in_command' in documents['items'][key] :
                                documents['items'][key].pop('suggest_in_command')
                
                        for key in list(documents['items']):
                            
                
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
                                        if 'entity' in documents['items'][key]['behaviours']['furniture']:
                                            documents['items'][key]['behaviours']['furniture'].pop('entity')

                                        documents['items'][key]['Mechanics'] = documents['items'][key].pop('behaviours')
                                        if 'solid' in documents['items'][key]['Mechanics']['furniture'] :
                                            if documents['items'][key]['Mechanics']['furniture']['solid'] == True:
                                                documents['items'][key]['Mechanics']['furniture']['barrier'] = documents['items'][key]['Mechanics']['furniture']['solid']
                                                documents['items'][key]['Mechanics']['furniture'].pop('solid')
                                            elif documents['items'][key]['Mechanics']['furniture']['solid'] == False:
                                                documents['items'][key]['Mechanics']['furniture']['barrier'] = documents['items'][key]['Mechanics']['furniture']['solid']
                                                documents['items'][key]['Mechanics']['furniture'].pop('solid')                                        
                                            else:
                                                documents['items'][key]['Mechanics']['furniture']['barrier'] = False
                                        else:
                                            documents['items'][key]['Mechanics']['furniture']['barrier'] = False
                                        if 'hitbox' in documents['items'][key]['Mechanics']['furniture'] :
                                            hbt = documents['items'][key]['Mechanics']['furniture'].pop('hitbox')
                                            documents['items'][key]['Mechanics']['furniture']['barriers'] = hitbox(hbt['length'],hbt['width'],hbt['height'])

                                        if 'placeable_on' in documents['items'][key]['Mechanics']['furniture'] :
                                            pn = documents['items'][key]['Mechanics']['furniture'].pop('placeable_on')
                                            documents['items'][key]['Mechanics']['furniture']['limited_placing'] = {}
                                            if 'walls' in pn:
                                                documents['items'][key]['Mechanics']['furniture']['limited_placing']['wall'] = pn['walls']
                                            if 'floor' in pn:
                                                documents['items'][key]['Mechanics']['furniture']['limited_placing']['floor'] = pn['floor'] 
                                            if 'ceiling' in pn:
                                                documents['items'][key]['Mechanics']['furniture']['limited_placing']['roof'] = pn['ceiling'] 

                                            documents['items'][key]['Mechanics']['furniture']['limited_placing']['type'] = 'DENY'
                                            # documents['items'][key]['Mechanics']['furniture']['limited_placing']['block_types'] = ['AIR']
                                            

                                        if 'fixed_rotation' in documents['items'][key]['Mechanics']['furniture'] :
                                            documents['items'][key]['Mechanics']['furniture'].pop('fixed_rotation')
                                        if 'furniture_sit' in documents['items'][key]['Mechanics']:
                                            furniture_sit = documents['items'][key]['Mechanics'].pop('furniture_sit')
                                            documents['items'][key]['Mechanics']['furniture']['seat'] = {'height':round(furniture_sit['sit_height']-1,1)}
                                            documents['items'][key]['Mechanics']['furniture']['barrier'] = True
                                        # documents['items'][key]['Mechanics']['furniture']['facing'] = 'UP'
                                        documents['items'][key]['Mechanics']['furniture']['rotation'] = 90
                                        documents['items'][key]['material'] = "PAPER"


                                        # ROTATION to none
                                        if documents['items'][key]['Mechanics']['furniture']['limited_placing']['wall'] is True:
                                            documents['items'][key]['Mechanics']['furniture']['rotation'] = 'NONE'
                                            documents['items'][key]['Mechanics']['furniture'].pop('barriers')

                                if 'model_id' in documents['items'][key]['Pack']:
                                    documents['items'][key]['Pack']['custom_model_data'] = documents['items'][key]['Pack'].pop('model_id')
                                if 'model_path' in documents['items'][key]['Pack']:
                                    documents['items'][key]['Pack']['model'] = documents['items'][key]['Pack'].pop('model_path')
                                if 'hat' in documents['items'][key]:
                                    documents['items'][key]['Mechanics'] = {}
                                    documents['items'][key]['Mechanics']['hat'] = {'enabled': True}
                                if 'behaviours' in documents['items'][key]:
                                    if 'hat' in documents['items'][key]['behaviours']:
                                        if documents['items'][key]['behaviours']['hat'] == True:
                                            documents['items'][key]['behaviours'].pop('hat')
                                            documents['items'][key].pop('behaviours')
                                            documents['items'][key]['Mechanics'] = {}
                                            documents['items'][key]['Mechanics']['hat'] = {'enabled': True}
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
                                        gnd = get_namespace+"/"+documents['items'][key]['Pack']['model']

                                        documents['items'][key]['Pack']['cast_model'] = gnd+'_cast'



                                documents['items'][key]['Pack']['model'] = get_namespace+"/"+documents['items'][key]['Pack']['model']
                                
                            else:
                                if 'specific_properties' in documents['items'][key]:

                                    
                                    if 'armor' in documents['items'][key]['specific_properties']:
                                        namespace_split = get_namespace.split("_")[0]
                                        list_type_arror = {"chest":"chestplate","legs":"leggings","feet":"boots","head":"helmet"}

                                        # print(list_type_arror[documents['items'][key]['specific_properties']['armor']['slot']])
                                        os.rename(f"Oraxen/pack/textures/{get_namespace}/"+documents['items'][key]['Pack']['textures'][0],f"Oraxen/pack/textures/{get_namespace}/armor/{namespace_split}_{list_type_arror[documents['items'][key]['specific_properties']['armor']['slot']]}.png")
                                        documents['items'][key]['Pack']['parent_model']= "item/generated"
                                        a_text = get_namespace+"/"+f"armor/{namespace_split}_{list_type_arror[documents['items'][key]['specific_properties']['armor']['slot']]}.png"
                                    
                                        documents['items'][key]['Pack']['textures'] = [a_text,a_text]

                                        
                                        documents['items'][key]['material'] = "LEATHER_"+list_type_arror[documents['items'][key]['specific_properties']['armor']['slot']].upper()
                                        
                                        nv = a_text.split("/")[2].split("_")[0]                                

                                        old_file = ''
                                        new_file = ''
                                        # replace name armor
                                        colors = [] 
                                        for na in documents['armors_rendering']:
                                            hex = documents['armors_rendering'][na]['color'].lstrip('#')
                                            colors = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
                                            # tn = documents['armors_rendering'][na]['layer_1'].split("/")
                                            if not os.path.exists(f"Oraxen/pack/textures/{get_namespace}/armor/{namespace_split}_armor_layer_1.png"):
                                                os.rename(f"Oraxen/pack/textures/{get_namespace}/"+documents['armors_rendering'][na]['layer_1']+'.png', f"Oraxen/pack/textures/{get_namespace}/armor/{namespace_split}_armor_layer_1.png")
                                            if not os.path.exists(f"Oraxen/pack/textures/{get_namespace}/armor/{namespace_split}_armor_layer_2.png"):
                                                os.rename(f"Oraxen/pack/textures/{get_namespace}/"+documents['armors_rendering'][na]['layer_2']+'.png', f"Oraxen/pack/textures/{get_namespace}/armor/{namespace_split}_armor_layer_2.png")
                                            if 'emissive_1' in documents['armors_rendering'][na]:
                                                if not os.path.exists(f"Oraxen/pack/textures/{get_namespace}/armor/{namespace_split}_armor_layer_1_e.png"):
                                                    os.rename(f"Oraxen/pack/textures/{get_namespace}/"+documents['armors_rendering'][na]['emissive_1']+'.png', f"Oraxen/pack/textures/{get_namespace}/armor/{namespace_split}_armor_layer_1_e.png")
                                            if 'emissive_2' in documents['armors_rendering'][na]:
                                                if not os.path.exists(f"Oraxen/pack/textures/{get_namespace}/armor/{namespace_split}_armor_layer_2_e.png"):
                                                    os.rename(f"Oraxen/pack/textures/{get_namespace}/"+documents['armors_rendering'][na]['emissive_2']+'.png', f"Oraxen/pack/textures/{get_namespace}/armor/{namespace_split}_armor_layer_2_e.png")

                                        documents['items'][key]['color'] = f"{colors[0]}, {colors[1]}, {colors[2]}"
                                    
                                        

        
                                        # set armor 128x32 config
                                        if not os.path.exists(f"Oraxen/settings.yml"):
                                            shutil.copy(f"Oraxen_settings.yml", f"Oraxen/settings.yml")
                                else:
                                   
                                    
                                    if 'model_id' in documents['items'][key]['Pack']:
                                        documents['items'][key]['Pack']['custom_model_data'] = documents['items'][key]['Pack'].pop('model_id')
                                    documents['items'][key]['material'] = documents['items'][key]['Pack'].pop('material')
                                    for tr in range(len(documents['items'][key]['Pack']['textures'])):
                                        documents['items'][key]['Pack']['textures'][tr] = get_namespace+'/'+documents['items'][key]['Pack']['textures'][tr]
                                    if 'SHIELD' in documents['items'][key]['material']:
                                        documents['items'][key]['Pack']['blocking_model'] = documents['items'][key]['Pack']['textures'][0]+'_blocking'
                                    elif 'CROSSBOW' in documents['items'][key]['material']:
                                        gnd = documents['items'][key]['Pack']['textures'][0]

                                        documents['items'][key]['Pack']['charged_model'] = gnd+'_charged'
                                        documents['items'][key]['Pack']['pulling_models'] = [gnd+'_0',gnd+'_1',gnd+'_2']                            
                                    elif 'BOW' in documents['items'][key]['material']:
                                        gnd = documents['items'][key]['Pack']['textures'][0]
                                        documents['items'][key]['Pack']["model"] = "default/combat_bow"
                                        documents['items'][key]['Pack']['pulling_models'] = [
                                            gnd+'_0',
                                                gnd+'_1',
                                                gnd+'_2'
                                        ]
                                        for tr in documents['items'][key]['Pack']['pulling_models']:
                                            with open(f"Oraxen/pack/models/{tr}.json", "w") as f:
                                                f.write('{"parent":"minecraft:item/bow","textures":{"layer0":"'+tr+'"}}')

                                    elif 'FISHING_ROD' in documents['items'][key]['material']:
                                        gnd = documents['items'][key]['Pack']['textures'][0]

                                        documents['items'][key]['Pack']['cast_model'] = gnd+'_cast'
                        for key in list(documents['items']):
                            if 'specific_properties' in documents['items'][key]:
                                if 'armor' in documents['items'][key]['specific_properties']:
                                        vv = documents['items'].pop(key)
                                        nv = a_text.split("/")[2].split("_")[0]
                                        nk = nv+'_'+list_type_arror[vv['specific_properties']['armor']['slot']]
                                        documents['items'][nk] = vv
                                        documents['items'][nk].pop('specific_properties')
                                    
                        with open(r'Oraxen\\items\\'+get_namespace+'_'+get_file, 'w') as file:
                            documents = yaml.dump(documents['items'], file, Dumper=YmlDumper, default_flow_style=False)
                        with open(r'Oraxen\\items\\'+get_namespace+'_'+get_file, 'r') as file :
                            filedata = file.read()
                        filedata = filedata.replace("'", '')
                        with open(r'Oraxen\\items\\'+get_namespace+'_'+get_file, 'w') as file:
                            file.write(filedata)

                        print("Convet file "+get_file) 
                        self.GLabel_225["text"] = "Convet file "+get_file
        # mege file
        data  = ''
        for get_file in os.listdir(r'Oraxen\\items\\'):
                with open(r'Oraxen\\items\\'+get_file, 'r') as file :
                    data += file.read()
                os.remove(r'Oraxen\\items\\'+get_file)
        with open(r'Oraxen\\items\\'+get_namespace+".yml", 'w') as file:
            file.write(data)   
        messagebox.showinfo("Info", "convert success")           
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
    tex = {'l':'bond','k':'obfuscated','m':'strikethrough','n':'u','o':'italic','r':'reset'}

    h_co_s = {'§'+str(co):'#'+v for co,v in color.items()}   
    h_co_s.update({'§'+str(co):v for co,v in tex.items()})
    h_co_and = {'&'+str(co):'#'+v for co,v in color.items()}   
    h_co_and.update({'&'+str(co):v for co,v in tex.items()})
    
    for v,c in h_co_s.items():        
        bb=bb.replace(v,'<'+c+'>')
    for v,c in h_co_and.items():
        bb=bb.replace(v,'<'+c+'>')
        

    return bb
def hitbox(length,width,height):
    da  = []
    for le in range(length):
        for wi in range(width):
            for he in range(height):
                da.append("{ x: "+str(wi)+", y: "+str(he)+", z: "+str(le)+" }")

    return da
if __name__ == "__main__":
    
        # os.mkdir('./ItemsAdder/data')            
    root = tk.Tk()
    app = App(root)
    root.mainloop()
