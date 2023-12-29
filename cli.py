import json
import platform
import re
import time
import shutil
import os
import yaml
import glob
from PIL import Image
from tkinter import messagebox 

from colorama import just_fix_windows_console
from rich import print as rprint

from rich.progress import track
from rich.console import Console
from time import sleep


system = platform.system()

if system == "Windows":
    just_fix_windows_console()
console = Console()
class YmlDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(YmlDumper, self).increase_indent(flow, False)
def hitbox(length,width,height):
    da  = []
    for le in range(length):
        for wi in range(width):
            for he in range(height):
                da.append("{ x: "+str(wi)+", y: "+str(he)+", z: "+str(le)+" }")
    return da
# replace text json to oraxen
def replace_text_json(dir,namespce,filename):
  if filename.endswith(".json"):
    with open(dir, 'r') as file :
        filedata = file.read()
    filedata = filedata.replace(namespce+":", namespce+'/')
    with open(dir, 'w') as file:
        file.write(filedata)
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
with console.status("[bold green]Fetching data...") as status:

    # check folder itemadder 
    if not os.path.isdir('./ItemsAdder'):
        os.mkdir('./ItemsAdder') 
        sleep(1)
        console.log(f"[red]Please dropfile to folder ItemsAdder[/red]")
        exit()
    sleep(1)
    console.log(f"[green]check fonder itemadder[/green]")

    # check itemadder emptry
    if len(os.listdir('./ItemsAdder'))<=0:
        console.log(f"[red]Please dropfile to folder ItemsAdder[/red]")              
        exit()
    sleep(1)
    console.log(f"[green]check fonder itemadder empty[/green]")

    # Remove folder Oraxen
    if os.path.isdir('./Oraxen'):
        shutil.rmtree('./Oraxen')
    if not os.path.isdir('./Oraxen'):
        os.mkdir('./Oraxen')             
        os.mkdir('./Oraxen/pack') 
        os.mkdir('./Oraxen/pack/models') 
        os.mkdir('./Oraxen/pack/textures')
    sleep(1)
    console.log(f"[green]Remove folder Oraxen[/green]")

    # backup file itemadder
    itemadder = './ItemsAdder/contents'
    if (os.path.exists(itemadder)):
        if(os.path.exists("./ItemsAdder_old")):
            shutil.rmtree("./ItemsAdder_old")
        shutil.copytree("./ItemsAdder","./ItemsAdder_old")  
    sleep(2)
    console.log(f"[green]Backup file itemadder[/green]")
    for get_conntent in os.listdir(itemadder):
        status.update(f"[bold yellow] Get {get_conntent} >> start")
        status.update(f"[bold yellow] Get {get_conntent} >> orixen model and textrues gen")
        categories = []
        items = []
        for get_config in list(set(glob.glob(itemadder+"/"+get_conntent+"/**/**/*.yml", recursive = True))):
            with open(get_config,encoding="utf-8") as file:
                documents = yaml.full_load(file)
                if  'categories' in documents:
                    for key in list(documents['categories']):
                        categories = documents['categories'][key]['items']
                if  'items' in documents:
                    for key in list(documents['items']):
                        items.append(key)
        for item in items:
            if documents["info"]["namespace"]+":"+item in categories:
                categories.remove(documents["info"]["namespace"]+":"+item)
        if len(categories)>0:    
            messagebox.showerror("Error", "\n".join(categories))          
        status.update(f"[bold yellow] Get {get_conntent} >> ia json to oraxin json")
        for file in list(set(glob.glob(itemadder+"/"+get_conntent+"/**/**/models", recursive = True))):
            path = file.replace('\\','/')
            namespace = path.split('/')[-2]
            shutil.copytree(file,"./Oraxen/pack/models/"+namespace)
            for file_json in glob.glob("./Oraxen/pack/models/"+namespace+"/**/**/*.json", recursive = True):
                get_models = file_json.replace('\\','/')
                status.update(f"[bold yellow] Get {get_conntent} >> ia json to oraxin json >> "+get_models)
                replace_text_json(get_models,namespace,get_models)
            # print(namespace)
        status.update(f"[bold yellow] Get {get_conntent} >> ia textures to oraxin textures")
        sleep(1)
        for file in list(set(glob.glob(itemadder+"/"+get_conntent+"/**/**/textures", recursive = True))):
            path = file.replace('\\','/')
            namespace = path.split('/')[-2]
            shutil.copytree(file,"./Oraxen/pack/textures/"+namespace)
        
        status.update(f"[bold yellow] Get {get_conntent} >> itemadder config to oraxin config")
        sleep(1)
        for get_config in list(set(glob.glob(itemadder+"/"+get_conntent+"/**/**/*.yml", recursive = True))):
                with open(get_config,encoding="utf-8") as file:
                        documents = yaml.full_load(file)
                        get_namespace = documents['info']['namespace']
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
                                            name_sp = name_sp.replace('_','')
                                            
                                            if(not os.path.exists(f'Oraxen/pack/textures/{get_namespace}/armors')):
                                                os.makedirs(f'Oraxen/pack/textures/{get_namespace}/armors')

                                            armor_part = os.path.dirname(documents['items'][key]['Pack']['textures'][0])
                                            _s_key = documents['items'][key.lower()]['specific_properties']['armor']['slot'].lower()
                                            
                                            os.rename(f"Oraxen/pack/textures/{get_namespace}/"+documents['items'][key]['Pack']['textures'][0],f"Oraxen/pack/textures/{get_namespace}/{armor_part}/{name_sp}_{list_type_arror[_s_key]}.png")
                                            shutil.move(f"Oraxen/pack/textures/{get_namespace}/{armor_part}/{name_sp}_{list_type_arror[_s_key]}.png",f'Oraxen/pack/textures/{get_namespace}/armors')
                                            

                                            
                                            documents['items'][key]['Pack']['parent_model']= "item/generated"
                                            a_text = get_namespace+"/"+f"armors/{name_sp}_{list_type_arror[_s_key]}.png"
                                            # print(a_text)
                                        
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
                                                    # print(name_sp)
                                                    os.rename(f"Oraxen/pack/textures/{get_namespace}/"+documents['armors_rendering'][na]['layer_1']+'.png', f"Oraxen/pack/textures/{get_namespace}/{get_part}/{name_sp}_armor_layer_1.png")
                                                    shutil.move(f"Oraxen/pack/textures/{get_namespace}/{get_part}/{name_sp}_armor_layer_1.png",f'Oraxen/pack/textures/{get_namespace}/armors')
                                                if(os.path.exists(f"Oraxen/pack/textures/{get_namespace}/"+documents['armors_rendering'][na]['layer_2']+'.png')):
                                                    get_part = documents['armors_rendering'][na]['layer_2'].split('/')
                                                    get_part.pop()
                                                    get_part = '/'.join(get_part)
                                                    # print(name_sp)
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
                                                if (not os.path.exists('Oraxen/pack/models/'+get_namespace)):
                                                    os.makedirs('Oraxen/pack/models/'+get_namespace)
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
                                                if (not os.path.exists('Oraxen/pack/models/'+get_namespace)):
                                                    os.makedirs('Oraxen/pack/models/'+get_namespace)
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
                            
                            get_file = os.path.basename(get_config)
                            with open(r'Oraxen\\items\\'+get_conntent+'_'+get_file, 'w') as file:
                                documents = yaml.dump(documents['items'], file, Dumper=YmlDumper, default_flow_style=False)
                            with open(r'Oraxen\\items\\'+get_conntent+'_'+get_file, 'r') as file :
                                filedata = file.read()
                            filedata = filedata.replace("'", '')
                            with open(r'Oraxen\\items\\'+get_conntent+'_'+get_file, 'w') as file:
                                file.write(filedata)

                            
                            status.update(f"[bold yellow] Convet file {get_file}")
                            sleep(1)
                        elif  'font_images' in documents:
                            data_icon = {}
                            get_namespace = documents['info']['namespace']
                            for key in list(documents['font_images']):
                                _emoji = (documents['font_images'][key]['path']+".png").replace(".png.png",".png")
                                
                                im = Image.open('Oraxen/pack/textures/'+get_namespace+"/"+_emoji)
                                width, height = im.size
                                data_icon[key] = {
                                    'height': documents['font_images'][key]['scale_ratio'],
                                    # 'height': height,
                                    'ascent': documents['font_images'][key]['y_position'],                                   
                                    'texture': get_namespace+"/"+_emoji
                                    }
                                if 'scale_ratio' not in  documents['font_images'][key]:
                                    if height<=64:
                                        data_icon[key]['is_emoji']= True
                                    else:
                                        data_icon[key]['height']= height
                                if 'symbol' in documents['font_images'][key]:
                                    data_icon[key]['char'] = documents['font_images'][key]['symbol']

                            if not os.path.exists(r"Oraxen\\glyphs"):
                                os.makedirs(r"Oraxen\\glyphs")
                            glyphs_file = os.path.basename(get_config)
                            g_name_file = (get_conntent+'_'+glyphs_file).replace(get_conntent+"_"+get_conntent,get_conntent)
                            g_name_file = g_name_file.replace(glyphs_file.split("_")[0]+"_"+glyphs_file.split("_")[0],glyphs_file.split("_")[0])
                            with open(r'Oraxen\\glyphs\\'+g_name_file+'.yml', 'w',encoding="utf-8") as file:
                                documents = yaml.dump(data_icon, file, Dumper=YmlDumper, default_flow_style=False, encoding='utf-8', allow_unicode=True)
        # lang file
        for get_config in list(set(glob.glob(itemadder+"/"+get_conntent+"/**/**/*.yml", recursive = True))):
                with open(get_config,encoding="utf-8") as file:
                        documents = yaml.full_load(file)
                        if  'minecraft_lang_overwrite' in documents:
                            for minecraft_lang_config in documents['minecraft_lang_overwrite']:
                                for minecraft_lang_config_button in documents['minecraft_lang_overwrite'][minecraft_lang_config]['entries']:
                                    documents['minecraft_lang_overwrite'][minecraft_lang_config]['entries'][minecraft_lang_config_button] = re.sub(r":offset_(-?\d+):", r"<shift:\1>", documents['minecraft_lang_overwrite'][minecraft_lang_config]['entries'][minecraft_lang_config_button])
                                    for icon_name in data_icon:                                        
                                        documents['minecraft_lang_overwrite'][minecraft_lang_config]['entries'][minecraft_lang_config_button] = documents['minecraft_lang_overwrite'][minecraft_lang_config]['entries'][minecraft_lang_config_button].replace(":"+icon_name+":","§f<glyph:"+icon_name+">§r")

                                if not os.path.exists("Oraxen\\pack\\lang"):
                                    os.makedirs("Oraxen\\pack\\lang")
                                with open(r'Oraxen\\pack\\lang\\en_us.json', 'w',encoding="utf-8") as file:
                                    json.dump(documents['minecraft_lang_overwrite'][minecraft_lang_config]['entries'],file, ensure_ascii=False)
                                with open(r'Oraxen\\pack\\lang\\global.json', 'w',encoding="utf-8") as file:
                                    json.dump(documents['minecraft_lang_overwrite'][minecraft_lang_config]['entries'],file, ensure_ascii=False)

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
        if (os.path.exists('./ItemsAdder')):
            shutil.rmtree("./ItemsAdder")
        time.sleep(2)
        if (os.path.exists('./ItemsAdder_old')):
            os.rename('./ItemsAdder_old','./ItemsAdder')
       
    console.log(f'[bold][red]convert success!')