from argparse import Namespace
import shutil
import os
import yaml

def replace_text_json(dir,namespce,filename):
  if filename.endswith(".json"):
    with open(dir, 'r') as file :
        filedata = file.read()
    filedata = filedata.replace(namespce+":", namespce+'/')
    with open(dir, 'w') as file:
        file.write(filedata)

itemadder = './ItemsAdder/data/resource_pack/assets'
for get_namespace in os.listdir(itemadder):
    for get_models in os.listdir(itemadder+"/"+get_namespace+"/models"):
        replace_text_json(itemadder+"/"+get_namespace+"/models/"+get_models,get_namespace,get_models)
        if not get_models.endswith(".json"):
           for get_models_2 in os.listdir(itemadder+"/"+get_namespace+"/models/"+get_models):
                replace_text_json(itemadder+"/"+get_namespace+"/models/"+get_models+"/"+get_models_2,get_namespace,get_models_2)
           


