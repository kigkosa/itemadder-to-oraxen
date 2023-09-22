import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox 
import shutil
import os
import yaml
import glob
from PIL import Image

class App:
    def __init__(self, root):


        #setting title
        root.title("Convert Itemadder to Oraxen")
        icon = """
        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
    """
        img = tk.PhotoImage(data=icon)
        root.tk.call('wm', 'iconphoto', root._w, img)
        
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


        # add progress bar
        self.progress = tk.ttk.Progressbar(root, orient = tk.HORIZONTAL, length = 100, mode = 'determinate')
        self.progress.place(x=10,y=0,width=230,height=10)





    def GButton_674_command(self):
        if not os.path.isdir('./ItemsAdder'):
            os.mkdir('./ItemsAdder') 
            messagebox.showinfo("Info", "Please dropfile to folder ItemsAdder")
        # if not os.path.isdir('./Oraxen_settings.yml'):
        #     with open('Oraxen_settings.yml', 'wb') as f:
        #         f.write(requests.get('https://raw.githubusercontent.com/kigkosa/itemadder-to-oraxen/master/Oraxen_settings.yml').content)
        self.progress['value'] = 0
        if len(os.listdir('./ItemsAdder'))<=0:
            messagebox.showinfo("Info", "Please dropfile to folder ItemsAdder")                
            return 0
        self.progress['value'] = 10
        if os.path.isdir('./Oraxen'):
            shutil.rmtree('./Oraxen')
        if not os.path.isdir('./Oraxen'):
            os.mkdir('./Oraxen') 
            
            os.mkdir('./Oraxen/pack') 
            os.mkdir('./Oraxen/pack/models') 
            os.mkdir('./Oraxen/pack/textures')

        itemadder = './ItemsAdder/contents'

        for get_conntent in os.listdir(itemadder):
            # print(get_conntent)
            ia_resoure_part = itemadder+"/"+get_conntent+"/resourcepack/"
            if os.path.exists(ia_resoure_part+"/assets"):
                ia_resoure_part = ia_resoure_part+"/assets"
            for get_namespace in os.listdir(ia_resoure_part):               
                
                if not os.path.isdir('./Oraxen/pack/models/'+get_namespace):
                    os.mkdir('./Oraxen/pack/models/'+get_namespace)
                    os.mkdir('./Oraxen/pack/textures/'+get_namespace)
                #get all sound
                if os.path.isdir(ia_resoure_part+"/"+get_namespace+"/sounds"):
                    os.mkdir('./Oraxen/pack/assets')
                    os.mkdir('./Oraxen/pack/assets/'+get_namespace)
                    shutil.copytree(ia_resoure_part+"/"+get_namespace+"/sounds","./Oraxen/pack/assets/"+get_namespace+"/sounds")
                    shutil.copy(ia_resoure_part+"/"+get_namespace+"/sounds.json","./Oraxen/pack/assets/"+get_namespace)

                        
                # get all model json replace
                for file in glob.glob(ia_resoure_part+"/"+get_namespace+"/models/"+"**/*.json", recursive = True):
                    get_models = file.replace('\\','/')
                    replace_text_json(get_models,get_namespace,get_models)


                # get all model json coppy
                if os.path.isdir("./Oraxen/pack/models/"+get_namespace):
                    shutil.rmtree("./Oraxen/pack/models/"+get_namespace)
                if os.path.isdir(ia_resoure_part+"/"+get_namespace+"/models"):
                    shutil.copytree(ia_resoure_part+"/"+get_namespace+"/models","./Oraxen/pack/models/"+get_namespace)

                # coppy textures
                if os.path.isdir("./Oraxen/pack/textures/"+get_namespace):
                    shutil.rmtree("./Oraxen/pack/textures/"+get_namespace)
                if os.path.isdir(ia_resoure_part+"/"+get_namespace+"/textures"):
                    shutil.copytree(ia_resoure_part+"/"+get_namespace+"/textures","./Oraxen/pack/textures/"+get_namespace)
                self.progress['value'] = 30
            # check namespace config file
            ia_config_name = itemadder+"/"+get_conntent+"/configs"
            for get_config_name in os.listdir(ia_config_name):
                if not get_config_name.endswith('.yml'):
                    ia_config_name = ia_config_name+"/"+get_config_name
            for get_config in os.listdir(ia_config_name):
                with open(ia_config_name+"/"+get_config) as file:
                        documents = yaml.full_load(file)

                        if  'items' in documents:
                            if not os.path.exists("./Oraxen/items"):
                                os.mkdir('./Oraxen/items') 
                            for key in list(documents['items']):
                                documents['items'][key]['Pack'] = documents['items'][key].pop('resource')
                                documents['items'][key]['displayname'] = "\"<White>"+color_to_hex(documents['items'][key].pop('display_name').title() )+"\""
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

                                    documents['items'][key]['material'] = documents['items'][key]['Pack'].pop('material').upper()

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
                                            documents['items'][key]['Mechanics']['furniture']['type'] = 'ITEM_FRAME'
                                            documents['items'][key]['Mechanics']['furniture']['drop'] = {'silktouch': False,'loots':[{'oraxen_item':key}]}
                                                

                                            if 'fixed_rotation' in documents['items'][key]['Mechanics']['furniture'] :
                                                documents['items'][key]['Mechanics']['furniture'].pop('fixed_rotation')
                                            if 'furniture_sit' in documents['items'][key]['Mechanics']:
                                                furniture_sit = documents['items'][key]['Mechanics'].pop('furniture_sit')
                                                documents['items'][key]['Mechanics']['furniture']['seat'] = {'height':round(furniture_sit['sit_height']-1,1)}
                                                documents['items'][key]['Mechanics']['furniture']['barrier'] = True
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
                                    if  'material' in documents['items'][key]:
                                        
                                        if 'SHIELD' in documents['items'][key]['material'].upper():
                                            documents['items'][key]['Pack']['blocking_model'] = get_namespace+"/"+documents['items'][key]['Pack']['model']+'_blocking'
                                        elif 'CROSSBOW' in documents['items'][key]['material'].upper():

                                            gnd = get_namespace+"/"+documents['items'][key]['Pack']['model']
                                            documents['items'][key]['Pack']['firework_model'] = gnd+'_firework'
                                            documents['items'][key]['Pack']['charged_model'] = gnd+'_charged'
                                            documents['items'][key]['Pack']['pulling_models'] = [gnd+'_0',gnd+'_1',gnd+'_2']                            
                                        elif 'BOW' in documents['items'][key]['material'].upper():
                                            gnd = get_namespace+"/"+documents['items'][key]['Pack']['model']
                                            


                                            documents['items'][key]['Pack']['pulling_models'] = [
                                                gnd+'_0',
                                                    gnd+'_1',
                                                    gnd+'_2'
                                            ]
                                            

                                        elif 'FISHING_ROD' in documents['items'][key]['material'].upper():
                                            gnd = get_namespace+"/"+documents['items'][key]['Pack']['model']

                                            documents['items'][key]['Pack']['cast_model'] = gnd+'_cast'



                                    documents['items'][key]['Pack']['model'] = get_namespace+"/"+documents['items'][key]['Pack']['model']
                                    
                                else:
                                    if 'specific_properties' in documents['items'][key]:
                                        if 'model_id' in documents['items'][key]['Pack']:
                                            documents['items'][key]['Pack']['custom_model_data'] = documents['items'][key]['Pack'].pop('model_id')
                                        
                                        if 'armor' in documents['items'][key]['specific_properties']:
                                            
                                            namespace_split = get_namespace.split("_")[0]

                                            list_type_arror = {"chest":"chestplate","legs":"leggings","feet":"boots","head":"helmet"}
                                            name_sp = key
                                            for x_list_type_arror,key_x_list_type_arror in list_type_arror.items():
                                                name_sp = name_sp.replace(key_x_list_type_arror,'')
                                                name_sp = name_sp.replace(x_list_type_arror,'')
                                            # namespace_split = name_sp

                                            # print(f"Oraxen/pack/textures/{get_namespace}/armor/{namespace_split}_{list_type_arror[documents['items'][key]['specific_properties']['armor']['slot']]}.png")
                                            
                                            
                                            if(not os.path.exists(f'Oraxen/pack/textures/{get_namespace}/armors')):
                                                os.makedirs(f'Oraxen/pack/textures/{get_namespace}/armors')

                                            armor_part = os.path.dirname(documents['items'][key]['Pack']['textures'][0])
                                            _s_key = documents['items'][key.lower()]['specific_properties']['armor']['slot'].lower()
                                            
                                            os.rename(f"Oraxen/pack/textures/{get_namespace}/"+documents['items'][key]['Pack']['textures'][0],f"Oraxen/pack/textures/{get_namespace}/{armor_part}/{name_sp}_{list_type_arror[_s_key]}.png")
                                            shutil.move(f"Oraxen/pack/textures/{get_namespace}/{armor_part}/{name_sp}_{list_type_arror[_s_key]}.png",f'Oraxen/pack/textures/{get_namespace}/armors')
                                            

                                            
                                            documents['items'][key]['Pack']['parent_model']= "item/generated"
                                            a_text = get_namespace+"/"+f"armors/{name_sp}_{list_type_arror[_s_key]}.png"
                                            print(a_text)
                                        
                                            documents['items'][key]['Pack']['textures'] = [a_text,a_text]

                                            
                                            
                                            documents['items'][key]['material'] = "LEATHER_"+list_type_arror[_s_key].upper()
                                            
                                            nv = a_text.split("/")[2].split("_")[0]

                                                 
        
                                            # replace name armor
                                            colors = [] 
                                            texture_size = 16
                                            for na in documents['armors_rendering']:
                                                hex = documents['armors_rendering'][na]['color'].lstrip('#')
                                                colors = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))


                                                if(os.path.exists(f"Oraxen/pack/textures/{get_namespace}/"+documents['armors_rendering'][na]['layer_1']+'.png')):
                                                    get_part = documents['armors_rendering'][na]['layer_1'].split('/')
                                                    get_part.pop()
                                                    get_part = '/'.join(get_part)
                                                    print(name_sp)
                                                    os.rename(f"Oraxen/pack/textures/{get_namespace}/"+documents['armors_rendering'][na]['layer_1']+'.png', f"Oraxen/pack/textures/{get_namespace}/{get_part}/{name_sp}_armor_layer_1.png")
                                                    shutil.move(f"Oraxen/pack/textures/{get_namespace}/{get_part}/{name_sp}_armor_layer_1.png",f'Oraxen/pack/textures/{get_namespace}/armors')
                                                if(os.path.exists(f"Oraxen/pack/textures/{get_namespace}/"+documents['armors_rendering'][na]['layer_2']+'.png')):
                                                    get_part = documents['armors_rendering'][na]['layer_2'].split('/')
                                                    get_part.pop()
                                                    get_part = '/'.join(get_part)
                                                    print(name_sp)
                                                    os.rename(f"Oraxen/pack/textures/{get_namespace}/"+documents['armors_rendering'][na]['layer_2']+'.png', f"Oraxen/pack/textures/{get_namespace}/{get_part}/{name_sp}_armor_layer_2.png")
                                                    shutil.move(f"Oraxen/pack/textures/{get_namespace}/{get_part}/{name_sp}_armor_layer_2.png",f'Oraxen/pack/textures/{get_namespace}/armors')
                                                                                               

                                            documents['items'][key]['color'] = f"{colors[0]}, {colors[1]}, {colors[2]}"
                                            
                                            
                                            if os.path.exists(f"Oraxen/pack/textures/{get_namespace}/{armor_part}/{namespace_split}_armor_layer_1.png"):
                                                mode_to_bpp = {"1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32, "CMYK": 32, "YCbCr": 24, "LAB": 24, "HSV": 24, "I": 32, "F": 32}
                                                im = Image.open(f"Oraxen/pack/textures/{get_namespace}/{armor_part}/{namespace_split}_armor_layer_1.png") 
                                                texture_size = mode_to_bpp[im.mode]
                                            
                                            for del_fd in os.listdir(f"Oraxen/pack/textures/{get_namespace}"):
                                                if os.path.isdir(f"Oraxen/pack/textures/{get_namespace}/{del_fd}"):  
                                                    di = os.listdir(f"Oraxen/pack/textures/{get_namespace}/{del_fd}")
                                                    if len(di) == 0:
                                                        shutil.rmtree(f"Oraxen/pack/textures/{get_namespace}/{del_fd}")

                                        
                                            # "Oraxen/settings.yml" red file yml
                                            # if not os.path.exists(f"Oraxen/settings.yml"):
                                            #     with open("Oraxen_settings.yml",'r') as f:
                                            #         data = yaml.load(f, Loader=yaml.FullLoader)
                                            #         data['Pack']['generation']['armor_resolution'] = texture_size
                                            #     with open(f"Oraxen/settings.yml",'w') as f:
                                            #         yaml.dump(data, f)
                                        
                                    else:
                                        
                                        # gen 2d item
                                        if 'model_id' in documents['items'][key]['Pack']:
                                            documents['items'][key]['Pack']['custom_model_data'] = documents['items'][key]['Pack'].pop('model_id')
                                        documents['items'][key]['material'] = documents['items'][key]['Pack'].pop('material').upper()
                                        for tr in range(len(documents['items'][key]['Pack']['textures'])):
                                            documents['items'][key]['Pack']['textures'][tr] = get_namespace+'/'+documents['items'][key]['Pack']['textures'][tr]
                                        if 'SHIELD' in documents['items'][key]['material'].upper():
                                            documents['items'][key]['Pack']['blocking_model'] = documents['items'][key]['Pack']['textures'][0]+'_blocking'
                                            documents['items'][key]['Pack']['parent_model'] = "item/shield"
                                            with open(f"Oraxen/pack/models/{documents['items'][key]['Pack']['blocking_model']}.json", "w") as f:
                                                f.write('{"parent":"builtin/entity","gui_light":"front","textures":{"particle":"'+documents['items'][key]['Pack']['blocking_model']+'"},"display":{"thirdperson_righthand":{"rotation":[45,135,0],"translation":[3.51,11,-2],"scale":[1,1,1]},"thirdperson_lefthand":{"rotation":[45,135,0],"translation":[13.51,3,5],"scale":[1,1,1]},"firstperson_righthand":{"rotation":[0,180,-5],"translation":[-15,5,-11],"scale":[1.25,1.25,1.25]},"firstperson_lefthand":{"rotation":[0,180,-5],"translation":[5,5,-11],"scale":[1.25,1.25,1.25]},"gui":{"rotation":[15,-25,-5],"translation":[2,3,0],"scale":[0.65,0.65,0.65]}}}')
                                        elif 'CROSSBOW' in documents['items'][key]['material'].upper():
                                            gnd = documents['items'][key]['Pack']['textures'][0]
                                            documents['items'][key]['Pack']['charged_model'] = gnd+'_charged'
                                            documents['items'][key]['Pack']['firework_model'] = gnd+'_firework'
                                            documents['items'][key]['Pack']['pulling_models'] = [gnd+'_0',gnd+'_1',gnd+'_2']       

                                            documents['items'][key]['Pack']["parent_model"] = "item/crossbow"
                                            for tr in documents['items'][key]['Pack']['pulling_models']:
                                                with open(f"Oraxen/pack/models/{tr}.json", "w") as f:
                                                    f.write('{"parent":"minecraft:item/crossbow","textures":{"layer0":"'+tr+'"}}')

                                        elif 'BOW' in documents['items'][key]['material'].upper():
                                            gnd = documents['items'][key]['Pack']['textures'][0]
                                            documents['items'][key]['Pack']["parent_model"] = "item/bow"
                                            documents['items'][key]['Pack']['pulling_models'] = [
                                                gnd+'_0',
                                                    gnd+'_1',
                                                    gnd+'_2'
                                            ]
                                            for tr in documents['items'][key]['Pack']['pulling_models']:
                                                with open(f"Oraxen/pack/models/{tr}.json", "w") as f:
                                                    f.write('{"parent":"minecraft:item/bow","textures":{"layer0":"'+tr+'"}}')

                                        elif 'FISHING_ROD' in documents['items'][key]['material'].upper():
                                            gnd = documents['items'][key]['Pack']['textures'][0]
                                            documents['items'][key]['Pack']['cast_model'] = gnd+'_cast'
                                            documents['items'][key]['Pack']["parent_model"] = "item/handheld_rod"
                                            with open(f"Oraxen/pack/models/{gnd}_cast.json", "w") as f:
                                                f.write('{"parent":"minecraft:item/fishing_rod","textures":{"layer0":"'+gnd+'_cast"}}')
                                                
                                            
                            for key in list(documents['items']):
                                if 'specific_properties' in documents['items'][key]:
                                    if 'armor' in documents['items'][key]['specific_properties']:
                                            vv = documents['items'].pop(key)
                                            nv = a_text.split("/")[2].split("_")[0]
                                            nk = name_sp+'_'+list_type_arror[vv['specific_properties']['armor']['slot'].lower()]
                                            documents['items'][nk] = vv
                                            documents['items'][nk].pop('specific_properties')
                            get_file = get_config
                            with open(r'Oraxen\\items\\'+get_conntent+'_'+get_file, 'w') as file:
                                documents = yaml.dump(documents['items'], file, Dumper=YmlDumper, default_flow_style=False)
                            with open(r'Oraxen\\items\\'+get_conntent+'_'+get_file, 'r') as file :
                                filedata = file.read()
                            filedata = filedata.replace("'", '')
                            with open(r'Oraxen\\items\\'+get_conntent+'_'+get_file, 'w') as file:
                                file.write(filedata)

                            print("Convet file "+get_file) 
                            self.GLabel_225["text"] = "Convet file "+get_file
                        elif  'font_images' in documents:
                            data_icon = {}
                            get_namespace = documents['info']['namespace']
                            for key in list(documents['font_images']):
                                _emoji = (documents['font_images'][key]['path']+".png").replace(".png.png",".png")
                                
                                im = Image.open('Oraxen/pack/textures/'+get_namespace+"/"+_emoji)
                                width, height = im.size
                               
                                data_icon[key] = {
                                    # 'height': height,
                                    'ascent': documents['font_images'][key]['y_position'],                                   
                                    'texture': get_namespace+"/"+_emoji
                                    }
                                if height<=64:
                                    data_icon[key]['is_emoji']= True
                                else:
                                    data_icon[key]['height']= height

                            if not os.path.exists(r"Oraxen\\glyphs"):
                                os.makedirs(r"Oraxen\\glyphs")
                            with open(r'Oraxen\\glyphs\\'+get_conntent+'_'+get_config, 'w') as file:
                                documents = yaml.dump(data_icon, file, Dumper=YmlDumper, default_flow_style=False)

            # r"Oraxen\\pack\\models" check file count 0
            if os.path.exists(r"Oraxen\\pack\\models"):
                if len(os.listdir(r"Oraxen\\pack\\models"))==0:
                    shutil.rmtree(r"Oraxen\\pack\\models")
           
            # mege file
            data  = ''
            for get_file_ox in glob.glob(r'Oraxen\\items\\'+get_conntent+"_**.yml"):
                with open(get_file_ox, 'r') as file :
                        data += file.read()
                os.remove(get_file_ox)
                with open(r'Oraxen\\items\\'+get_conntent+".yml", 'w') as file:
                    file.write(data)   
            self.progress['value'] = 100
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
    
    root = tk.Tk()
    app = App(root)
    root.mainloop()
