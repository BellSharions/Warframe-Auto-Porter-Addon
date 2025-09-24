bl_info = {
    "name": "Warframe Auto Porter",
    "author": "Bell Sharions",
    "version": (0, 48, 3),
    "blender": (4, 2, 0),
    "location": "3D View > Tool Shelf (Right Panel) > Tool",
    "description": "Imports and configures Warframe models/materials",
    "category": "Import",
}
# Script done by Bell Sharions for Warframe Model Resources
# This is not a "do it all" script, some assebly and tweaks might be required in some cases
                                                                                                    
#                                 @@@@@                                                              
#                             @@@@@#*#%@@@@@@@                                                       
#                         @@@@@%@#+==++*#@@%%@@@                                                     
#                       @@@%#*+++===+++*#%*=+*#%@@@                                                  
#                     @@@%+++==--=++++*#*==+++++*%@@@@@@@@@@@@@@@@@@@                                
#                    @@%*+++=--==+++=-===+++*#%%%%%%%##**#****#****#@@@                              
#                  @@@#++++=--=++++=--=++*#%%%#**+++++===-----=+++++*%@@@                            
#                 @@@#+++++--=+++=--=++*#%%#++++++===---::::--=+++++++*%@@@                          
#                @@%*+++++=--++++=-==+#%#*+++++=---::::::::::-=++++++++++#@@@                        
#               @@%*++++++=--++=----=+*++++++++--::::::::::::-=++++++++++++*%@@                      
#              @@%#+++++++--=++=--==-=++++++++=-:::::::::::::-=++++++++++=--=#@@@@@@                 
#             @@@#++++++++=-=++==++--=++++++++=-::::::::::::-=+++++++++++=--:-+###%%@@@@@@           
#             @@#+++++++++=-=+*#@%*--=++++++++=-::::::::::::-=++++++++++++=--------++*#%@@@@@@       
#            %@%*+++++++++=-=#%#%%#+==++++++++=--::::::::---==++++++++++++++======++++++++**#%@@     
#            @@#+++++*#%@%%#%#-:-+##+==+++++++=--------=====+++++++++++++++++++++++++++++++==+%@@    
#           #@%*+++*%@@@@ @@+:::..-**==+++++++++++++++++++++++++++++++++++++++++++++++++++=-+#@@     
#         --=#%**#@@@@   @%+:....::+#+=++++++++++++++++++++++++++++++++=-==+++++++++++++=--+%@@@@@@@ 
#       =----*%%%%@@    @@+::......-##+=+++++++++++++++++++++++++++===-----+++++++++++==-=*%#****#%@@
#     ------------*    @@*.::::::...-*##+++====++++++++=======---------==--+++++=====--=*%#*+++++==#@
#     -----  ::---  **#@%::::::::::..:+#%*+====--------------======--===--=++==------=+##*+++++++-+%@
#     =----+*=----  *+##*.:::::::::...:+*#%%%%%%%%%%%%%#######****#*+----------==+++++++++++++++==%@@
#      -----:----=  **##=..:::::::.....:====-:::::::::::---===++++=*%##%%%#*+++++++++++++++++++==#@@@
#       ---------  @@@#:.....:::................................:..:-+==--=#%#*++++++++++++++==+%%@@@
#                 @@@#=..................................::::........::.....:+#%#*+++++++++===#%**%@@
#              @@@@%*+=...........      ...............::::::::............ ...:#@#+++++==--+##++*@@ 
#        %%@@@@%%%%%%%%*-..............................::::::::::::............=##+==-----==+++++%@@ 
#     @@@%%#*++++*****##%#=:........::::::::...........::::::::...... .......-*%%#+=-===++++++++*%@  
#    @@@#*=======+++++++**%%=..:=*#%%%%%%%%%%#*=-:..............::... ......+%@@@@@#*++++++++++*%@@  
#   @@%**+=======++++++++++*%#%@%#**+++++*++***#@@%-...........:::::......-+++#@@@@@#++++++++++#@@   
#  @@%*++++====++++++++++++**##***+++++++++++*++**%@%+...........::.....:=++#%@@@@@@#*++++++++*@@@   
#  @%**+*+++*+++====+++++++**++++++++++++++++++++++*#%#-...........::-=+##%@@@@   @@#++++++++*@@@    
# @@#*+++++++*+++====+++++++++++++++++++++++++++++++**%#-:::::--==+++*#%@@@       @%*+++++++*%@@     
# @@#*+++++++++++++++*++++++++++++++++++++++++++++++++#%#+++++++**#%@@@@          @%*++++++#@@@      
# @@#*++*+++++++++**+++++++++++++++++++++++++++++++*++*%%***##%%@@@@@             @%*++++*#@@@       
# @@%*++++++++++++*++++++++++++++++++++++++++++++++*++*%@*****#%@@                @%*+++*%@@         
# @@@#*+++++++++++++++++++++++++++++++++++++++++++++++*%@#*+-:-#@@               -#%#++#@@@          
#  @@@#*+++***++++++++++++++++++++++++++++++++++++++++#%%%@@#*#@@@             =--=#%%%%#            
#   @@@#****+++++++++++++++++++++++++++++++++++++++++*%%#@@@@@@@             =-----*%*=--=           
#    @@@%%%#*++++++++++++++++++++++*#%%%%%%%#**+++++*%@#*#%@@@@             -------  ----=           
#    @@#**%%***+++++++++++++++++++*#%#******##%%#***%@#+====+#@@           =----=    ----=           
#   @@#+++#%%%%*+++++++++++++++++++*%%*++=----=+#%%%%+=======*%@           +----=   =-----           
#  @@#++++++*#%#++++++++++++++++++*#%#+++=-::::=++*#%%#*+====*%@@           +------------            
# @@%*+++++++*%%#*++++++++++++++++*%%*++++=-:::-=++++*#%%#**+*%@@             --:-----=              
# @@#*+++++++++#%#*+++++++++++++++*#%%#*+++=====++++++++#%%%%#%@@              ----=+                
# @@@%#*+++++*#%#*++++++++++++++++++**#%%%#*++++++++++++++*%%#%@@                                    
#   @@@@@@@@@@@@%#*++*+**+++++++++++**#%@@@@#+++++++++++#%**%%%@@                                    
#         @@@  @@@%#*++++++++++***#%%@@@@@ @@#++++**+++*%+:.+%@@                                     
#                @@@@%**+****#%@@@@@@      @@@*+*%%%%%%%%=..=%@@                                     
#                  @@@@@%%@@@@@@@           @@@@@#:.:::::...=%@@                                     
#                      @@@@@@                 @@@%*-:.....:=#@@                                      
#                                               @@@@%#***#%@@@                                       
#                                                    @@@@@@                                          
                                                                                                    
                                                                                                    
from pathlib import Path
import bpy
import os
import ast
import traceback
import time
import re
from collections import OrderedDict
import bmesh
import math
import numpy as np
from fnmatch import fnmatch
from bpy.types import Operator, AddonPreferences, Macro, PropertyGroup
from bpy.props import StringProperty, BoolProperty, PointerProperty, EnumProperty, IntProperty, CollectionProperty
from bpy.app.handlers import persistent

COLOR_SPACE_MAP = {
    'Base Color': 'sRGB',
    'Emission': 'sRGB',
    'Metalness': 'Non-Color',
    'Roughness': 'Non-Color',
    'Specular': 'Non-Color',
    'Normal': 'Non-Color',
    'Alpha': 'Non-Color'
}
EMISSION_FLAGS_FOR_BAKING = ["emission_mask", "multi_tint_and_mask", "emissive_mask"]
shader_exceptions_parameters = [ "Swizzle Vertex Channels" ]
texture_extension_list = [
    ('*.png', 'PNG', 'Use PNG textures'),
    ('*.tga', 'TGA', 'Use TGA textures'),
]
special_reset_rules = {
    'EffectsIntensityStrength': 1,
    'EffectsIntensity X': 1,
    'EffectsIntensity Y': 1,
    'EffectsIntensity Z': 1,
    'EffectsIntensity W': 1,
    'EffectsIntensity2 X': 1,
    'EffectsIntensity2 Y': 1,
    'PanGlobalScale': 1,
    'FPS Value': 30,
    'AOTintColor': tuple([0, 0, 0, 1]),
    'DetailMapDiffuseRange': 100,
    'DetailMapNormalRange': 100,
    'EmissiveTintColor': tuple([1, 1, 1, 1]),
    'EmissiveTintColor Alpha': 1,
    'TimeScalar': 1,
    'UvScale X': 1,
    'UvScale Y': 1,
    'UvScale Z': 1,
    'UvScale W': 1,
    'UVScale01 X': 1,
    'UVScale01 Y': 1,
    'UVScale01 Z': 1,
    'UVScale01 W': 1,
    'UVScale23 X': 1,
    'UVScale23 Y': 1,
    'UVScale23 Z': 1,
    'UVScale23 W': 1,
    'HeightPanScale X': 0,
    'HeightPanScale Y': 0,
    'HeightPanScale Z': 1,
    'HeightPanScale W': 1,
    'AlphaTestValue': 0.5,
    'FacingRoughness': 1,
    'GlancingRoughness': 1,
    'EmissiveFresnelPow': 1,
    'emissiveFade Y': 1,
    'FlickerParam X': 1,
    'GlassColor': tuple([1, 1, 1, 0]),
    'WetBias': -1,
    'Roughness': 0.5,
    'Radius': tuple([1, 0.2, 0.1]),
    'X Scale': 1,
    'Y Scale': 1,
    'HairCapMask X': 1,
    'HairCapMask Y': 1,
    'HairCapMask Z': 1,
    'HairCapMask W': 1,
    'MakeUpMask X': 1,
    'MakeUpMask Y': 1,
    'MakeUpMask Z': 1,
    'MakeUpMask W': 1,
    
}

special_aliases = {
    "TINT_MASK_PACK_MAP_BLEND": "TINT_MASK_PACK_MAP",
}

special_ignores = {
    # "EMISSIVE_COMPRESSION = EC_COMPONENT": "EmissiveTintColor",
}

texture_ignores = [
    "BaseMaterialMetal"
]
extractor_commands = {    
    "Texture": '{0} --extract-textures --texture-format {2} --cache-dir "{1}" --internal-path "{3}" --output-path "{4}"',
    "Material": '{0} --extract-materials --cache-dir "{1}" --internal-path "{2}" --output-path "{3}"'
}
def extract_texture_with_cli(extractor_path, cache_path, texture_format, internal_path, output_dir):
    import subprocess
    import os
    
    cmd = extractor_commands["Texture"].format(
        Path(extractor_path), 
        Path(cache_path),
        texture_format,
        internal_path,
        Path(output_dir)
    )
    
    try:
        print(f"Running command: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Successfully extracted texture: {internal_path}")
            return True
        else:
            print(f"Extractor failed with error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error running extractor: {str(e)}")
        return False

def extract_material_with_cli(extractor_path, cache_path, internal_path, output_dir):
    import subprocess
    import os
    
    cmd = extractor_commands["Material"].format(
        Path(extractor_path), 
        Path(cache_path),
        internal_path,
        Path(output_dir)
    )
    
    try:
        print(f"Running command: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Successfully extracted material: {internal_path}")
            return True
        else:
            print(f"Extractor failed with error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error running extractor: {str(e)}")
        return False
    
def find_shader_material(shader_name, shader_library_path):
    
    shader_files = {}
    for f in os.listdir(shader_library_path):
        if f.endswith('.blend'):
            shader_files[f.lower()] = f
            
    target_file = f"{shader_name}.blend"
    if target_file in shader_files:
        original_filename = shader_files[target_file.lower()]
        return os.path.join(shader_library_path, original_filename), None
    
    for original_filename in shader_files.values():
        if shader_name.lower() in original_filename.lower():
            return os.path.join(shader_library_path, original_filename), None
        
    return None, f"No shader file found for {shader_name}"

def get_best_material_from_blend(blend_path, params):
    materials = []
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        for mat_name in data_from.materials:
            if "stroke" and "dev" not in mat_name.lower():
                materials.append(mat_name)
    
    valid_params = set()
    for key, value in params.items():
        if value == 0 or (isinstance(value, str) and value.upper() == "NONE"):
            continue
        valid_params.add(str(key))
        valid_params.add(str(value))
    
    theoretical_best = []
    parameter_combinations = []
    basic_mats = []
    tint_mask_mats = []
    default_mats = []
    no_paren_mats = []
    
    for mat in materials:
        upper_mat = mat.upper()
        
        if "(" in mat and ")" in mat:
            content = mat.split("(")[1].split(")")[0]
            
            if "+" in content:
                params_in_name = [p.strip() for p in content.split("+")]
                if all(param in valid_params for param in params_in_name):
                    parameter_combinations.append(mat)
                    continue
            
            elif content in valid_params:
                theoretical_best.append(mat)
                continue
        
        if "(BASIC)" in upper_mat:
            basic_mats.append(mat)
        elif "(TINT_MASK)" in upper_mat:
            tint_mask_mats.append(mat)
        elif "(DEFAULT)" in upper_mat:
            default_mats.append(mat)
        elif "(" not in mat or ")" not in mat:
            no_paren_mats.append(mat)
    
    if parameter_combinations:
        return parameter_combinations[0]
    elif theoretical_best:
        return theoretical_best[0]
    elif basic_mats:
        return basic_mats[0]
    elif tint_mask_mats:
        return tint_mask_mats[0]
    elif default_mats:
        return default_mats[0]
    elif no_paren_mats:
        return no_paren_mats[0]
    elif materials:
        return materials[0]
    
    return None

def strtobool (val):
    if not isinstance(val, str):
        return val
    if val.lower() in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif ('none') in val.lower() or   val.lower() in ('none', '', 'no', 'false'):
        return False
    else:
        return False

def get_color_space(source):
    """Determine color space based on source name"""
    if source in COLOR_SPACE_MAP:
        return COLOR_SPACE_MAP[source]
    source_lower = source.lower()
    for key in COLOR_SPACE_MAP:
        if key.lower() in source_lower:
            return COLOR_SPACE_MAP[key]
    return 'sRGB'

def find_internal_path(path):
    index = path.find("Lotus")
    if index == -1:
        return ""
    extracted = path[index:]
    
    last_segment = os.path.basename(extracted)
    if last_segment == '':
        return extracted
        
    if '.' in last_segment:
        parts = last_segment.split('.')
        if len(parts) > 1:
            ext = parts[-1]
            if ext.isalpha() and 1 <= len(ext) <= 5:
                extracted = os.path.dirname(extracted)
    
    return extracted

def find_internal_texture_path(path):
    index = path.find("Lotus")
    if index == -1:
        return ""
    extracted = path[index:]
    
    return extracted

def contains(str1, str2):
    if not isinstance(str1, str) or not isinstance(str2, str):
        return True
    if '=' in str1.lower() or '=' in str2.lower():
        return str1.lower() == str2.lower()
    return str1.lower() in str2.lower()

def containstexture(str1, str2):
    if not isinstance(str1, str) or not isinstance(str2, str):
        return True
    if '=' in str1.lower() or '=' in str2.lower():
        return str1.lower() == str2.lower()
    pattern = re.compile(r'\b' + re.escape(str1.lower()) + r'\b')
    return bool(pattern.search(str2.lower()))

def set_default(input_socket, value):
    if input_socket.type == 'VECTOR':
        input_socket.default_value = tuple(value[:3])
    elif input_socket.type == 'BOOLEAN':
        input_socket.default_value = bool(strtobool(value))
    elif input_socket.type == 'COLOR':
        input_socket.default_value = tuple(value[:3])
    elif input_socket.type == 'RGBA':
        input_socket.default_value = tuple(value[:4])
    elif input_socket.type == 'VALUE':
        input_socket.default_value = float(value)
    elif input_socket.type == 'INT':
        input_socket.default_value = int(value)
        
def reset_default(input_socket):
    socket_name = input_socket.name
    if socket_name in special_reset_rules:
        input_socket.default_value = special_reset_rules[socket_name]
        return
    if input_socket.type == 'VECTOR':
        input_socket.default_value = tuple([0, 0, 0])
    elif input_socket.type == 'BOOLEAN':
        input_socket.default_value = False
    elif input_socket.type == 'COLOR':
        input_socket.default_value = tuple([0.5, 0.5, 0.5])
    elif input_socket.type == 'RGBA':
        input_socket.default_value = tuple([0.5, 0.5, 0.5, 1])
    elif input_socket.type == 'VALUE':
        input_socket.default_value = float(0)
    elif input_socket.type == 'INT':
        input_socket.default_value = int(0)
                
def parse_material_file(filepath):
    material_data = {}
    shader_data = {}
    hierarchy_data = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            
            if not line or line.startswith('#'):
                continue
            if any(ignore in line for ignore in texture_ignores):
                continue
            if '=' not in line and ':' not in line:
                continue
            if ':' in line:
                key, value = line.split(':', 1)
            if '=' in line:
                key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if "shader" in key.lower():
                continue
            if value == '':
                continue
            if '_p.hlsl' in value.lower():
                key = value.lower()
                value = 1
                shader_data[key] = value
                continue
            
            try:
                if value.startswith('[') and value.endswith(']'):
                    value = ast.literal_eval(value)
                else:
                    try: value = float(value) if '.' in value else int(value)
                    except: pass
            except Exception as e:
                pass
            
            material_data[key] = value
            if isinstance(value, str) and not line.startswith('TX:') and "shader" not in line.lower():
                material_data[line.strip()] = 1
                if(line.strip().lower().endswith("= none")):
                    continue
                if(value.strip().lower().startswith("x") and len(value.strip()) == 2):
                    material_data["x"] = int(value.strip()[-1])
                material_data[key] = 1
                material_data[value.strip()] = 1
    
    for key in special_aliases:
        if key in material_data and special_aliases[key] not in material_data:
            material_data[special_aliases[key]] = 1
            
    sorted_material = OrderedDict(sorted(material_data.items(), key=lambda t: t[0]))
    return (sorted_material, shader_data, hierarchy_data)

def connect_textures_and_parameters(material, node_group, parameters, textures, pathToTextures, texture_locations, labeled_reroutes, shader_data, hierarchy_data):
    group_tree = node_group.node_tree
    group_name_lower = group_tree.name.lower()
    if "final tweaks" in group_name_lower:
        return  
     
    if node_group.label.lower() in parameters.keys():
        full_key = None
        for key in parameters.keys():
            if f"{node_group.label.lower()} =" in key:
                full_key = key
                print(full_key)
                break
        
        if full_key:
            search_term = full_key.split('=')[1].strip().lower()
            for nodegroup_to_link in bpy.data.node_groups:
                if search_term in nodegroup_to_link.name.lower():
                    node_group.node_tree = nodegroup_to_link
                    break
                
    if "vertex shader" in group_name_lower:
        for input_socket in node_group.inputs:
            if input_socket.name.lower() in shader_data:
                print(f"Setting Vertex Shader Value: {input_socket} to True")
                set_default(input_socket, True) 
            else:
                print(f"Setting Vertex Shader Value: {input_socket} to False")
                set_default(input_socket, False) 
                  
        return     
    
    for input_socket in node_group.inputs:
        if(input_socket.links):
            current = input_socket.links[0].from_node
            while True:
                if current.name.startswith("Reroute") and (hasattr(current, 'inputs') or current.inputs[0] is None):
                    current = current.inputs[0]
                if current.name.startswith("Input") and (hasattr(current, 'links') or current.links[0] is None):
                    current = current.links[0].from_node
                else:
                    break
            if hasattr(current, 'image'):
                if(bpy.context.scene.warframe_tools_props.EMPTY_IMAGES_BEFORE_SETUP):
                    current.image = None
                selected_list = texture_locations
                for tex_name, filename in selected_list.items():
                    if(isinstance(filename, int)):
                        continue
                    preextfilename = filename
                    if(not filename.endswith(bpy.context.scene.warframe_tools_props.texture_extension.split("*")[1])):
                        filename = filename.split(".")[0] + bpy.context.scene.warframe_tools_props.texture_extension.split("*")[1]
            
                    name = filename.split('/')[-1]
                    if any(containstexture(tex_name, input_socket.name) for link in input_socket.links):
                        try:
                            img = None
                            for img_tex in bpy.data.images:
                                if(img_tex.name in name):
                                    img = img_tex
                            if(img is None):
                                if not os.path.exists(filename) and bpy.context.scene.warframe_tools_props.USE_EXTRACTOR:
                                    props = bpy.context.scene.warframe_tools_props
                                    
                                    internal_path = find_internal_texture_path(preextfilename)
                                    texture_format = props.texture_extension.replace('*.', '').upper()
                                    
                                    success = extract_texture_with_cli(
                                        props.extractor_path,
                                        props.cache_path,
                                        texture_format,
                                        internal_path,
                                        props.root
                                    )
                                    if success:
                                        img = bpy.data.images.load(filename)
                                    else:
                                        print(f"Could not extract texture: {filename}")
                                else:
                                    img = bpy.data.images.load(filename)
                            if '(sRGB)' in input_socket.name:
                                img.colorspace_settings.name = 'sRGB'
                            else:
                                img.colorspace_settings.name = 'Non-Color'
                            print(current.image)
                            if((current.image is None) or (bpy.context.scene.warframe_tools_props.REPLACE_IMAGES and current.image.name not in img.name)):
                                current.image = img
                                print(f"Connected texture: {filename} to {input_socket.name} in {node_group.name}")
                            break
                        except Exception as e:
                            print(f"Texture error: {str(e)}")
                
                continue
        VALID_SOCKET_TYPES = {'BOOLEAN', 'INT', 'COLOR', 'VECTOR', 'VALUE', 'RGBA'}

        input_name = input_socket.name
        input_lower = input_name.lower()
        input_type = input_socket.type
        should_reset = bpy.context.scene.warframe_tools_props.RESET_PARAMETERS
        if input_type not in VALID_SOCKET_TYPES:
            if should_reset:
                reset_default(input_socket)
            continue
        try:
            value = None
            found_match = False
            
            lookup_name = input_lower
            if '/' in input_name:
                base_name, second_part = input_name.split("/", 1)
                base_name_lower = base_name.lower()
                second_part_lower = second_part.lower()
                
                for part in [base_name_lower, second_part_lower]:
                    if part in parameters:
                        value = parameters[part]
                        found_match = True
                        break
            
            if not found_match and any(input_name.endswith(x) for x in ('XYZ', 'X', 'Y', 'Z', 'W', 'Alpha')):
                base_name = input_name.split(" ")[0].lower()
                if base_name in parameters:
                    param_val = parameters[base_name]
                    
                    if input_name.endswith('XYZ'):
                        value = param_val
                    elif input_name.endswith('X'):
                        value = param_val if isinstance(param_val, int) else param_val[0]
                    elif input_name.endswith('Y'):
                        value = param_val if isinstance(param_val, int) else param_val[1]
                    elif input_name.endswith('Z'):
                        value = param_val if isinstance(param_val, int) else param_val[2]
                    elif input_name.endswith(('W', 'Alpha')):
                        value = param_val if isinstance(param_val, int) else param_val[3]
                    found_match = True
            if not found_match:
                if lookup_name in parameters:
                    value = parameters[lookup_name]
                    found_match = True
            if not found_match:
                if input_lower.endswith("= none"):
                    lookup_name = input_lower
                elif '=' in input_lower:
                    lookup_name = input_lower
                else:
                    lookup_name = input_name.split(" ")[0].lower()
                
                if lookup_name in parameters:
                    value = parameters[lookup_name]
                    found_match = True
            
            if found_match:
                print(f"Setting instance parameter: {input_name} = {value}")
                set_default(input_socket, value)
            elif should_reset:
                reset_default(input_socket)

        except Exception as e:
            print(f"Exception processing {input_name}: {str(e)}")
            if should_reset:
                reset_default(input_socket)
                                      
def set_material_properties(material, material_data, pathToTextures, model_path, texture_locations, shader_data, hiearchy_data):
    parameters = {}
    textures = {}
    labeled_reroutes = []
    texture_locations = texture_locations
    path = model_path if bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION else str(pathToTextures)
    if(not path.endswith("/")):
        path += "/"
    for key, value in material_data.items():
        if key.startswith('TX:'):
            result = value
            setone = False
            if(not "/" in result and bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION):
                result = path + result
                setone = True
            if(not result.startswith("/") and "/" in result and bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION and not setone):
                result = path + result
            if(not bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION):
                result = path + result
            textures[key[3:]] = result
        elif ':' in key:
            prefix, param_name = key.split(':', 1)
            parameters[param_name.lower()] = value
        else:
            parameters[key.lower()] = value
    if(bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION):
        root_loc = str(bpy.context.scene.warframe_tools_props.root)
        if(not str(bpy.context.scene.warframe_tools_props.root).endswith("/")):
            root_loc += "/"
        for key, value in textures.items():
            if(os.path.isdir(str(Path(root_loc + value)))):
                if not value.endswith("/"):
                    value += "/"
                onlyfiles = [f for f in os.listdir(str(Path(root_loc + value))) if os.path.isfile(os.path.join(str(Path(root_loc + value)), f))]
                for idx, file in enumerate(onlyfiles):
                    texture_locations[key + " " + str(idx)] = str(Path(root_loc + value + file))
                continue
            texture_locations[key] = str(Path(root_loc + value))
    elif(not bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION):
        for key, value in textures.items():
            if (not str(Path(str(pathToTextures) + value.split("/")[-1])).endswith(bpy.context.scene.warframe_tools_props.texture_extension.split("*")[1])):
                texture_locations[key] = str(Path(os.path.join(pathToTextures, value.split("/")[-1]) + bpy.context.scene.warframe_tools_props.texture_extension.split("*")[1]))
                continue
            texture_locations[key] = os.path.join(pathToTextures, value.split("/")[-1])
            
    for trigger_value, key_to_remove in special_ignores.items():
        if trigger_value.lower() in parameters.keys() and key_to_remove.lower() in parameters:
            del parameters[key_to_remove.lower()]
    
    node_groups = []
    for node in material.node_tree.nodes:
        if node.type == 'REROUTE' and node.label.strip():
            input_unlinked = not node.inputs[0].is_linked
            output_unlinked = not node.outputs[0].is_linked
            
            if input_unlinked or output_unlinked:
                labeled_reroutes.append(node.label)
        if node.type == 'GROUP' and node.node_tree:
            node_groups.append(node)
    node_groups_for_gn = [ng for ng in bpy.data.node_groups if ng.type == 'GEOMETRY' and ng.name.startswith("Gn. ")]
    
    node_group_map = {}
    for ng in node_groups_for_gn:
        base_name = ng.name[4:].split(maxsplit=1)[0]
        node_group_map[base_name.lower()] = ng
    
    for param_name, param_value in (parameters | shader_data).items():
        if param_name.lower() in node_group_map:
            ng = node_group_map[param_name.lower()]
            
            mod = bpy.context.active_object.modifiers.new(name=ng.name, type='NODES')
            mod.node_group = ng
            
            for item in ng.interface.items_tree:
                if item.item_type == 'SOCKET' and item.in_out == 'INPUT':
                    socket_name = item.name
                    if socket_name.lower() in parameters:
                        try:
                            value = parameters[socket_name.lower()]
                            if item.bl_socket_idname == 'NodeSocketBool':
                                    value = bool(value)
                            mod[item.identifier] = value
                            print(f"Setting {mod[item.identifier]} = {parameters[socket_name.lower()]}, {socket_name}")
                        except Exception as e:
                            print(f"Error setting {socket_name}: {str(e)}")
    print(parameters)
    for node in node_groups:  
        if node.type is not 'GEOMETRY':
            connect_textures_and_parameters(material, node, parameters, textures, pathToTextures, texture_locations, labeled_reroutes, shader_data, hiearchy_data)

def get_shader_items(self, context):
    items = []
    if not os.path.exists(bpy.context.scene.warframe_tools_props.pathToShader):
        return items
    with bpy.data.libraries.load(bpy.context.scene.warframe_tools_props.pathToShader, link=False) as (data_from, data_to):
        for mat_name in data_from.materials:
            if "dots stroke" not in mat_name.lower():
                items.append((mat_name, mat_name, ""))
    return items

def get_rig_items(self, context):
    items = []
    if not os.path.exists(bpy.context.scene.warframe_tools_props.rig_path):
        return items
    with bpy.data.libraries.load(bpy.context.scene.warframe_tools_props.rig_path, link=False) as (data_from, data_to):
        for rig_name in data_from.collections:
            print(rig_name)
            if "meta" not in rig_name.lower() and "wgts" not in rig_name.lower():
                items.append((rig_name, rig_name, ""))
    return items

class BakeState:
    """Storage for bake operation state"""
    def __init__(self, material, output_node, orig_socket, image_node, source_socket, renderer_state):
        self.material = material
        self.output_node = output_node
        self.orig_socket = orig_socket
        self.image_node = image_node
        self.source_socket = source_socket
        self.renderer_state = renderer_state

def setup_bake(context, source):
    """Prepare baking for a specific source"""
    material = context.active_object.active_material
    node_tree = material.node_tree
    
    output_node = next((n for n in node_tree.nodes if n.type == 'OUTPUT_MATERIAL'), None)
    if not output_node:
        raise Exception("Material Output node not found")
    orig_socket = None
    if output_node.inputs['Surface'].is_linked:
        orig_socket = output_node.inputs['Surface'].links[0].from_socket
    source_socket = None
    fallback_socket = None
    for node in node_tree.nodes:
        if node.type in {'GROUP', 'GROUP_OUTPUT'}:
            for output in node.outputs:
                if source in output.name:
                    fallback_socket = output
                    if source == "Normal" and "final" in getattr(node.node_tree, 'name', '').lower():
                        continue
                    source_socket = output
                    break
            if source == "Emission":
                for input in node.inputs:
                    if input.name.lower() in EMISSION_FLAGS_FOR_BAKING:
                        input.default_value = False
                        break
        if source_socket:
            break
            
    if not source_socket and fallback_socket:
        source_socket = fallback_socket
    if not source_socket:
        raise Exception(f"Output socket '{source}' not found")

    image_name = f"{material.name}_{source.replace(' ', '')}"
    image = bpy.data.images.new(image_name, *(bpy.context.scene.warframe_tools_props.bake_width, bpy.context.scene.warframe_tools_props.bake_height))
    image.colorspace_settings.name = get_color_space(source)

    image_node = node_tree.nodes.new('ShaderNodeTexImage')
    image_node.image = image
    image_node.location = (output_node.location.x - 300, output_node.location.y + 500)
    
    if output_node.inputs['Surface'].is_linked:
        for link in output_node.inputs['Surface'].links:
            node_tree.links.remove(link)
    node_tree.links.new(source_socket, output_node.inputs['Surface'])
    
    renderer_state = {}
    renderer_state["margin"] = context.scene.render.bake.margin
    renderer_state["use_clear"] = context.scene.render.bake.use_clear
    renderer_state["target"] = context.scene.render.bake.target
    renderer_state["bake_type"] = context.scene.cycles.bake_type
    renderer_state["engine"] = context.scene.render.engine
    renderer_state["samples"] = context.scene.cycles.samples
    renderer_state["device"] = context.scene.cycles.device
    renderer_state["device"] = context.scene.cycles.device
    
    context.scene.render.bake.margin = 3
    context.scene.render.bake.target = 'IMAGE_TEXTURES'
    context.scene.render.bake.use_clear = False
    context.scene.cycles.bake_type = 'EMIT'
    context.scene.render.engine = 'CYCLES'
    context.scene.cycles.samples = 3
        
    prefs = context.preferences
    if prefs.addons.get('cycles'):
        cprefs = prefs.addons['cycles'].preferences
        if hasattr(cprefs, 'devices') and any(device.type == 'CUDA' for device in cprefs.devices):
            context.scene.cycles.device = 'GPU'

    node_tree.nodes.active = image_node
    return BakeState(material, output_node, orig_socket, image_node, source_socket, renderer_state)

def cleanup_bake(state):
    """Restore original node connections after baking"""
    if not state or not state.material:
        return
    bpy.context.scene.render.bake.margin = state.renderer_state["margin"]
    bpy.context.scene.render.bake.use_clear = state.renderer_state["use_clear"]
    bpy.context.scene.render.bake.target = state.renderer_state["target"]
    bpy.context.scene.cycles.bake_type = state.renderer_state["bake_type"]
    bpy.context.scene.render.engine = state.renderer_state["engine"]
    bpy.context.scene.cycles.samples = state.renderer_state["samples"]
    bpy.context.scene.cycles.device = state.renderer_state["device"]
    node_tree = state.material.node_tree
    if not node_tree:
        return
        
    output_surface = state.output_node.inputs['Surface']
    
    if output_surface.is_linked:
        for link in output_surface.links[:]:
            if link.from_socket == state.source_socket:
                node_tree.links.remove(link)
                break
            
    if state.orig_socket:
        try:
            if not output_surface.is_linked:
                node_tree.links.new(state.orig_socket, output_surface)
        except Exception as e:
            print(f"Error restoring connection: {e}")

class OBJECT_OT_BakeTextures(bpy.types.Operator):
    bl_idname = "object.bake_textures"
    bl_label = "Bake Textures"
    bl_options = {'REGISTER', 'UNDO'}

    source: bpy.props.StringProperty(name="Source", default="Base Color")

    def execute(self, context):

        self.sources = [s.strip() for s in self.source.split(',') if s.strip()]
        self.current_index = -1
        self.bake_state = None
        self.baking = False
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if not self.sources:
            return {'FINISHED'}
            
        if self.current_index < 0:
            self.current_index = 0
            self.start_next_bake(context)
            return {'RUNNING_MODAL'}
        
        if self.baking:
            if bpy.app.is_job_running('OBJECT_BAKE'):
                return {'PASS_THROUGH'}
                
            cleanup_bake(self.bake_state)
            print(f"Baked {self.sources[self.current_index]} complete!")
            self.current_index += 1
            self.baking = False
            
        if self.current_index < len(self.sources):
            self.start_next_bake(context)
            return {'RUNNING_MODAL'}
        
        return {'FINISHED'}

    def start_next_bake(self, context):
        source = self.sources[self.current_index]
        print(f"Starting bake: {source}")
        
        try:
            self.bake_state = setup_bake(context, source)
            bpy.ops.object.bake('INVOKE_DEFAULT', type='EMIT')
            self.baking = True
        except Exception as e:
            self.report({'ERROR'}, f"Bake failed: {str(e)}")
            self.current_index = len(self.sources)

def get_color_space(source):
    """Determine color space based on source name"""
    if source in COLOR_SPACE_MAP:
        return COLOR_SPACE_MAP[source]
    
    source_lower = source.lower()
    for key in COLOR_SPACE_MAP:
        if key.lower() in source_lower:
            return COLOR_SPACE_MAP[key]
    
    return 'sRGB'
    
def normal_to_height(normal_img, iterations=5000, damping=0.1):
    """
    Convert normal map to height map using iterative Poisson solver.
    Args:
        normal_img: Blender image object (normal map)
        iterations: Number of solver iterations (higher = more accurate)
        damping: Relaxation factor (0.1-0.5 recommended)
    Returns:
        Height map as 2D numpy array (normalized to 0-1)
    """
    normal_px = np.array(normal_img.pixels).reshape(
        normal_img.size[1], normal_img.size[0], -1
    )
    
    normal_data = normal_px[..., :3].astype(np.float32)
    normal_data = normal_data * 2.0 - 1.0
    
    normal_data[..., 1] *= -1 if bpy.context.scene.warframe_tools_props.invert_green else 1
    
    n_x, n_y, n_z = (
        normal_data[..., 0], 
        normal_data[..., 1], 
        np.clip(normal_data[..., 2], 1.0, 1.0)
    )
    n_z = 1
    dx = -n_x / n_z
    dy = -n_y / n_z
    
    h, w = dx.shape
    f = np.zeros((h, w), dtype=np.float32)
    
    f[1:-1, 1:-1] = 0.5 * (dx[1:-1, 2:] - dx[1:-1, :-2]) + \
                     0.5 * (dy[2:, 1:-1] - dy[:-2, 1:-1])
    
    f[0, :] = dy[0, :]
    f[-1, :] = -dy[-2, :]
    f[:, 0] = dx[:, 0]
    f[:, -1] = -dx[:, -2]

    height = np.zeros((h, w), dtype=np.float32)
    for _ in range(iterations):
        new_height = height.copy()
        new_height[1:-1, 1:-1] = (1 - damping) * height[1:-1, 1:-1] + \
            damping * 0.25 * (
                height[1:-1, :-2] + 
                height[1:-1, 2:] + 
                height[:-2, 1:-1] + 
                height[2:, 1:-1] - 
                f[1:-1, 1:-1]
            )
        
        new_height[0, :] = new_height[1, :]
        new_height[-1, :] = new_height[-2, :]
        new_height[:, 0] = new_height[:, 1]
        new_height[:, -1] = new_height[:, -2]
        height = new_height

    return (height - height.min()) / (height.max() - height.min())

class NormalToHeightOperator(bpy.types.Operator):
    bl_idname = "dprint.normal_to_height"
    bl_label = "Convert Normal to Height"
    
    def execute(self, context):
        normal_img = bpy.data.images.load(bpy.context.scene.warframe_tools_props.normal_to_height_path, check_existing=False) 
        normal_img.colorspace_settings.name = 'Non-Color'
        height_data = normal_to_height(normal_img, iterations=2000)
        
        w, h = normal_img.size
        height_img = bpy.data.images.new(
            name=f"{normal_img.name}_Height",
            width=w,
            height=h,
            alpha=False,
            float_buffer=True
        )
        
        height_rgba = np.zeros((h, w, 4), dtype=np.float32)
        height_rgba[..., 0] = height_data
        height_rgba[..., 1] = height_data
        height_rgba[..., 2] = height_data
        height_rgba[..., 3] = 1.0          
        
        height_img.pixels = height_rgba.ravel()
        
        height_img.pack()
        bpy.context.scene.warframe_tools_props.image_select = height_img.name
        return {'FINISHED'}

class SubDivisionOperator(bpy.types.Operator):
    bl_idname = "dprint.subdivide"
    bl_label = "Add Subdivision Surface Modifier"
    bl_description = "Adds a Catmull-Clark subdivision surface modifier"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None and
            context.active_object.type == 'MESH'
        )

    def execute(self, context):
        props = bpy.context.scene.warframe_tools_props
        obj = context.active_object
        subdiv_levels = props.subdiv_amount
        ram_subdivision = props.ram_subdivision
        ram_amount = props.ram_amount * 1000000
        optimized = props.optimized_subdivision
        if ram_subdivision:
            subdiv_levels = int(max(0, math.floor(math.log(ram_amount / len(obj.data.vertices), 4) - 1) if len(obj.data.vertices) <= ram_amount else 0))
        for mod in obj.modifiers:
            if mod.name.startswith("AutoSubdivision"):
                obj.modifiers.remove(mod)

        if optimized and subdiv_levels > 1:
            base_mod = obj.modifiers.new(name="AutoSubdivision_Base", type='SUBSURF')
            base_mod.subdivision_type = 'SIMPLE'
            base_mod.levels = 1
            base_mod.render_levels = 1
            base_mod.show_expanded = False
            
            detail_mod = obj.modifiers.new(name="AutoSubdivision_Detail", type='SUBSURF')
            detail_mod.subdivision_type = 'CATMULL_CLARK'
            detail_levels = max(0, subdiv_levels - 1)
            detail_mod.levels = detail_levels
            detail_mod.render_levels = detail_levels
            detail_mod.show_expanded = False
            
            self.report({'INFO'}, f"Added optimized subdivision: Simple(1) + Catmull-Clark({detail_levels})")
        
        else:
            mod = obj.modifiers.new(name="AutoSubdivision", type='SUBSURF')
            mod.subdivision_type = 'CATMULL_CLARK'
            mod.levels = subdiv_levels
            mod.render_levels = subdiv_levels
            mod.show_expanded = False
            
            self.report({'INFO'}, f"Added Catmull-Clark subdivision with {subdiv_levels} levels")
        
        return {'FINISHED'} 

class DeformOperator(bpy.types.Operator):
    bl_idname = "dprint.add_height"
    bl_label = "Add Height Map as Deform Modifier"
    bl_description = "Adds displace modifier with selected height map image"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None and
            context.active_object.type == 'MESH'
        )

    def execute(self, context):
        props = bpy.context.scene.warframe_tools_props
        selected_image_name = props.image_select
        
        if selected_image_name == 'NONE' or not selected_image_name:
            self.report({'ERROR'}, "No image selected")
            return {'CANCELLED'}
        
        img = bpy.data.images.get(selected_image_name)
        if not img:
            self.report({'ERROR'}, f"Image '{selected_image_name}' not found")
            return {'CANCELLED'}
        
        obj = context.active_object
        
        texture_name = f"{obj.name}_{img.name}_displace"
        tex = bpy.data.textures.get(texture_name) or bpy.data.textures.new(name=texture_name, type='IMAGE')
        tex.image = img
        tex.use_preview_alpha = True
        
        modifier_name = f"Displace_{img.name}"
        mod = obj.modifiers.get(modifier_name) or obj.modifiers.new(name=modifier_name, type='DISPLACE')
        mod.texture = tex
        mod.strength = 0.01 
        mod.texture_coords = 'UV'
        mod.mid_level = 0.5
        
        self.report({'INFO'}, f"Added displace modifier with {img.name}")
        return {'FINISHED'}


class RunAllOperationsOperator(bpy.types.Operator):
    bl_idname = "dprint.run_all_operations"
    bl_label = "Run All Operations"
    bl_description = "Execute normal map conversion, subdivision, and height deformation"

    def execute(self, context):
        props = bpy.context.scene.warframe_tools_props
        
        try:
            bpy.ops.dprint.normal_to_height()
            
            bpy.ops.dprint.subdivide()
            
            bpy.ops.dprint.add_height()
            
            self.report({'INFO'}, "All operations completed successfully!")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Operation failed: {str(e)}")
            return {'CANCELLED'}

class SHADER_OT_append_material(bpy.types.Operator):
    bl_idname = "shader.append_material"
    bl_label = "Append Shader"
    bl_description = "Append material from shader library"
    bl_property = "material_name"
    bl_options = {'REGISTER', 'UNDO'}

    material_name: bpy.props.EnumProperty(
        name="Materials",
        description="Available materials",
        items=get_shader_items,
    )

    def execute(self, context):
        if not self.material_name:
            return {'CANCELLED'}

        try:
            for obj in context.selected_objects:
                original_base_name = None
                if obj and obj.data and hasattr(obj.data, 'materials') and obj.data.materials:
                    if obj.data.materials[0]:
                        original_base_name = obj.data.materials[0].name.split('.')[0]

                before = set(bpy.data.materials.keys())
                
                before_images = set(bpy.data.images.keys())
                print(os.path.join(context.scene.warframe_tools_props.pathToShader, "Material") + os.sep)
                print(self.material_name)
                bpy.ops.wm.append(
                    directory=os.path.join(context.scene.warframe_tools_props.pathToShader, "Material") + os.sep,
                    filename=self.material_name,
                    do_reuse_local_id=False
                )
                after = set(bpy.data.materials.keys())
                new_material_names = after - before
                
                if not new_material_names:
                    self.report({'ERROR'}, "Failed to append material")
                    return {'CANCELLED'}
                    
                new_material = bpy.data.materials[list(new_material_names)[0]]
                self.report({'INFO'}, f"Appended material: {self.material_name}")

                after_images = set(bpy.data.images.keys())
                new_image_names = after_images - before_images
                
                self.cleanup_textures(new_material, new_image_names)
                gn_node_groups = []
                try:
                    with bpy.data.libraries.load(context.scene.warframe_tools_props.pathToShader, link=False) as (data_from, data_to):
                        gn_node_groups = [name for name in data_from.node_groups if name.startswith("Gn")]
                except Exception as e:
                    self.report({'WARNING'}, f"Could not read node groups: {str(e)}")
                
                for node_group_name in gn_node_groups:
                    if node_group_name not in bpy.data.node_groups:
                        try:
                            bpy.ops.wm.append(
                                directory=os.path.join(context.scene.warframe_tools_props.pathToShader, "NodeTree") + os.sep,
                                filename=node_group_name,
                                do_reuse_local_id=True
                            )
                            self.report({'INFO'}, f"Appended node group: {node_group_name}")
                        except Exception as e:
                            self.report({'WARNING'}, f"Failed to append node group {node_group_name}: {str(e)}")

                if original_base_name:
                    old_materials = [mat for mat in bpy.data.materials 
                                    if mat.name.startswith(original_base_name + '.') or 
                                    mat.name == original_base_name]
                    
                    for old_mat in old_materials:
                        old_mat.user_remap(new_material)
                        
                    for old_mat in old_materials:
                        if old_mat.users == 0 and old_mat != new_material:
                            bpy.data.materials.remove(old_mat)
                    
                    new_material.name = original_base_name
                else:
                    if obj and obj.data:
                        new_name = f"{obj.data.name}_Material"
                        new_material.name = new_name
                        
                        if not obj.data.materials:
                            obj.data.materials.append(new_material)
                        else:
                            obj.data.materials[0] = new_material

        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        return {'FINISHED'}
    def cleanup_textures(self, material, new_image_names):
        """Remove texture files associated with the material"""
        if not material.use_nodes:
            return
        unused_images = new_image_names
        
        for image_name in unused_images:
            image = bpy.data.images.get(image_name)
            if image:
                try:
                    bpy.data.images.remove(image)
                    self.report({'INFO'}, f"Removed unused image: {image_name}")
                except Exception as e:
                    self.report({'WARNING'}, f"Could not remove image {image_name}: {str(e)}")
    def draw(self, context):
        layout = self.layout
        layout.label(text="Select Material to Append")
        layout.prop(self, "material_name", text="")
        layout.separator()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

class RIG_OT_append_rig(bpy.types.Operator):
    bl_idname = "rig.append_rig"
    bl_label = "Append Rig"
    bl_description = "Append rig and do automatic setup"
    bl_property = "rig_name"
    bl_options = {'REGISTER', 'UNDO'}

    rig_name: bpy.props.EnumProperty(
        name="Rigs",
        description="Available rigs",
        items=get_rig_items,
    )

    def execute(self, context):
        if not self.rig_name:
            return {'CANCELLED'}
        original_selection = context.selected_objects
        original_active = context.active_object
        selected = context.selected_objects
        bpy.ops.wm.append(
            directory=os.path.join(bpy.context.scene.warframe_tools_props.rig_path, "Collection") + os.sep,
            filename=self.rig_name
        )
        bpy.ops.wm.append(
            directory=os.path.join(bpy.context.scene.warframe_tools_props.rig_path, "Text") + os.sep,
            filename="Bones Snap"
        )
        self.report({'INFO'}, f"Appended rig: {self.rig_name}")
        obj = bpy.context.object
        new_rig_collection  = bpy.data.collections.get(self.rig_name)
        if new_rig_collection.name not in context.scene.collection.children:
            bpy.context.scene.collection.children.link(new_rig_collection)
        else:
            print("Failed to append rig")
        target_armature = None
        for obj in new_rig_collection.objects:
            print(obj.name)
            if obj.type == 'ARMATURE' and obj.name.lower() in self.rig_name.lower():
                target_armature = obj
                break

        if not target_armature:
            self.report({'ERROR'}, f"Armature '{self.rig_name}' not found in collection")
            return {'CANCELLED'}
        updated_count = 0
        old_armatures = set()
        for obj in selected:
            print(obj)
            for mod in obj.modifiers:
                if mod.type == 'ARMATURE':
                    if mod.object != target_armature:
                        old_armatures.add(mod.object)
                        mod.object = target_armature
                        updated_count += 1
        special_rigs = {"face rig": ["Face Metarig", "MetaRig"], "long arm rig": ["Long Arm Metarig", "Long Arm Metarig"]}
        for sprig in special_rigs:
            if sprig in self.rig_name.lower() and old_armatures:
                face_meta_rig = None
                face_meta_rig = bpy.data.objects.get(special_rigs[sprig][0])
                
                if not face_meta_rig:
                    self.report({'WARNING'}, "Face MetaRig not found in appended collection")
                else:
                    snap_script = bpy.data.texts.get("Bones Snap")
                    if snap_script:
                        print(special_rigs[sprig][1])
                        metacol = bpy.data.collections.get(special_rigs[sprig][1])
                        print(metacol)
                        metacol.hide_viewport = False
                        bpy.ops.object.select_all(action='DESELECT')
                        face_meta_rig.hide_set(False)
                        face_meta_rig.hide_viewport = False
                        face_meta_rig.hide_select = False
                        face_meta_rig.select_set(True)
                        context.view_layer.objects.active = face_meta_rig
                        for old_arm in old_armatures:
                            old_arm.select_set(True)
                            context.view_layer.objects.active = old_arm
                            break
                        try:
                            ctx = {
                                'bpy': bpy,
                                'context': context,
                                'selected_objects': context.selected_objects,
                                'active_object': context.active_object
                            }
                            exec(snap_script.as_string(), ctx)
                        except Exception as e:
                            metacol.hide_viewport = True
                            self.report({'ERROR'}, f"Bone Snap failed: {str(e)}")
                        bpy.ops.object.select_all(action='DESELECT')
                        face_meta_rig.select_set(True)
                        context.view_layer.objects.active = face_meta_rig
                        try:
                            bpy.ops.pose.rigify_generate()
                        except Exception as e:
                            metacol.hide_viewport = True
                            self.report({'ERROR'}, f"Rigify generation failed: {str(e)}")
                            return {'CANCELLED'}
                        metacol.hide_viewport = True
                    else:
                        self.report({'WARNING'}, "Bones Snap script not found")
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Select Rig to Append")
        layout.prop(self, "rig_name", text="")
        layout.separator()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)


def process_object(obj):
    if obj.type != 'MESH':
        return
    me = obj.data
    if me.color_attributes:

        mesh = obj.data
        loops = mesh.loops
        polygons = mesh.polygons
        
        color_attr_names = []
        for att in mesh.color_attributes:
            if att.domain == 'POINT':
                color_attr_names.append(att.name)
        
        if not color_attr_names:
            return

        for attr_name in color_attr_names:
            if attr_name not in mesh.color_attributes:
                continue
                
            color_attr = mesh.color_attributes[attr_name]
            if color_attr.is_internal or color_attr.is_required:
                continue
                
            old_name = color_attr.name
            new_attr = mesh.color_attributes.new(
                name=old_name,
                type=color_attr.data_type,
                domain='CORNER'
            )
            src_data = [0.0] * (len(mesh.vertices) * 4)
            color_attr.data.foreach_get('color', src_data)
            dst_data = [0.0] * (len(loops) * 4)
            for poly in polygons:
                for loop_idx in poly.loop_indices:
                    vert_idx = loops[loop_idx].vertex_index
                    src_idx = vert_idx * 4
                    dst_idx = loop_idx * 4
                    dst_data[dst_idx] = src_data[src_idx]
                    dst_data[dst_idx + 1] = src_data[src_idx + 1]
                    dst_data[dst_idx + 2] = src_data[src_idx + 2]
                    dst_data[dst_idx + 3] = src_data[src_idx + 3]
            
            new_attr.data.foreach_set('color', dst_data)
            new_attr.data.update()
            mesh.color_attributes.remove(color_attr)
            new_attr.name = old_name
    if not bpy.context.scene.warframe_tools_props.LEVEL_IMPORT:
        me.flip_normals()
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.normal_update()
        bm.to_mesh(me)
        bm.free()
    me.shade_smooth()
class WARFRAME_OT_ImportModel(bpy.types.Operator):
    bl_idname = "wm.import_model"
    bl_label = "Import Model"
    bl_description = "Import and process Warframe model"
    
    def execute(self, context):
        props = context.scene.warframe_tools_props
        bpy.ops.import_scene.gltf(
            filepath=str(bpy.context.scene.warframe_tools_props.model_file_path), 
            guess_original_bind_pose=False, 
            bone_heuristic="TEMPERANCE")
        collections_dict = {}
        for obj in bpy.context.selected_objects:
            if obj.type != 'MESH':
                continue
            # Credit: KptWeedy
            if bpy.context.scene.warframe_tools_props.LEVEL_IMPORT:
                print(obj.data.validate(clean_customdata=True))
                if len(obj.material_slots) > 0 and obj.material_slots[0].material.name.lower().startswith("hidden"):
                    obj.hide_render = True
                    obj.hide_set(True)
                    continue
                material_name = ""
                if len(obj.material_slots) > 0 and obj.material_slots[0].material:
                    material_name = obj.material_slots[0].material.name
                    bpy.data.materials[material_name].use_fake_user = True
                    print(f"Processing material: {material_name}")
                    
                if material_name:
                    if material_name not in collections_dict:
                        new_collection = bpy.data.collections.new(material_name)
                        bpy.context.scene.collection.children.link(new_collection)
                        collections_dict[material_name] = new_collection
                    else:
                        new_collection = collections_dict[material_name]
                    
                    for collection in obj.users_collection:
                        collection.objects.unlink(obj)
                    new_collection.objects.link(obj)
            process_object(obj)
        collections_dict = {}
            
        self.report({'INFO'}, "Model imported successfully")
        return {'FINISHED'}
class WARFRAME_OT_SetupShader(bpy.types.Operator):
    bl_idname = "wm.setup_shader"
    bl_label = "Setup Shader"
    bl_description = "Configure material with textures and parameters"
    
    def execute(self, context):
        props = context.scene.warframe_tools_props
        mat = context.object.active_material
        if not mat:
            self.report({'ERROR'}, "No active material selected")
            return {'CANCELLED'}
            
        texture_locations = {}
        material_data, shader_data, hierarchy_data = parse_material_file(props.material_file_path)
        model_path = find_internal_path(props.material_file_path)
        
        set_material_properties(mat, material_data, props.pathToTextures, model_path, texture_locations, shader_data, hierarchy_data)
        self.report({'INFO'}, "Shader setup completed")
        return {'FINISHED'}    
class WM_OT_RunSetup(bpy.types.Operator):
    bl_idname = "wm.run_setup"
    bl_label = "Run Setup"

    def execute(self, context):
        props = context.scene.warframe_tools_props
            
        mode = props.mode
        if mode == 'IMPORT':
            return bpy.ops.wm.import_model('INVOKE_DEFAULT')
        elif mode == 'APPEND':
            return bpy.ops.shader.append_material('INVOKE_DEFAULT')
        elif mode == 'RIG':
            return bpy.ops.rig.append_rig('INVOKE_DEFAULT')
        elif mode == 'BAKE':
            # I hate azdfulla for making me do this
            sources = []
            if props.bake_base_color:
                sources.append('Base Color')
            if props.bake_emission:
                sources.append('Emission')
            if props.bake_metalness:
                sources.append('Metalness')
            if props.bake_roughness:
                sources.append('Roughness')
            if props.bake_specular:
                sources.append('Specular')
            if props.bake_normal:
                sources.append('Normal')
            if props.bake_alpha:
                sources.append('Alpha')
            return bpy.ops.object.bake_textures(source=",".join(sources))
        elif mode == 'SHADER':
            return bpy.ops.wm.setup_shader('INVOKE_DEFAULT')
        elif mode == 'EXPERIMENTAL':
            return bpy.ops.wm.experimental_mode('INVOKE_DEFAULT')
            
        self.report({'WARNING'}, "Unknown mode selected")
        return {'CANCELLED'}
class WM_OT_SetupPaths(bpy.types.Operator):
    bl_idname = "wm.setup_paths"
    bl_label = "Setup Required Paths"
    bl_description = "Select the path to file/folder"
    
    current_step: bpy.props.IntProperty(default=0)
    material_file_path: bpy.props.StringProperty(subtype='FILE_PATH')
    model_file_path: bpy.props.StringProperty(subtype='FILE_PATH')
    extractor_path: bpy.props.StringProperty(subtype='FILE_PATH')
    cache_path: bpy.props.StringProperty(subtype='DIR_PATH')
    shader_library_path: bpy.props.StringProperty(subtype='DIR_PATH')
    pathToShader: bpy.props.StringProperty(subtype='FILE_PATH')
    pathToRig: bpy.props.StringProperty(subtype='FILE_PATH')
    root: bpy.props.StringProperty(subtype='DIR_PATH')
    pathToTextures: bpy.props.StringProperty(subtype='DIR_PATH')
    normal_to_height_path: bpy.props.StringProperty(subtype='DIR_PATH')

    filter_glob: bpy.props.StringProperty(default="*")
    directory: bpy.props.StringProperty(subtype='DIR_PATH', default=str(Path.home()))
    filepath: bpy.props.StringProperty(subtype='FILE_PATH')

    def determine_steps(self):
        steps = []
        mode = bpy.context.scene.warframe_tools_props.mode
        if mode == 'IMPORT':
            steps.append(('model_file_path', 'Select Model File (.glb)', 'file', '*.glb'))
        elif mode == 'APPEND':
            steps.append(('pathToShader', 'Select Shader Blend File', 'file', '*.blend'))
        elif mode == 'RIG':
            self.root = bpy.context.scene.warframe_tools_props.rig_path
            if bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION and (self.pathToRig is None or self.pathToRig is ""):
                steps.append(('pathToRig', 'Select Rig Blend File', 'file', '*.blend'))
        elif mode == 'BAKE':
            return steps
        elif mode == '3DPRINT':
            steps.append(('normal_to_height_path', 'Select Normal Map File', 'file', '*'))
        elif mode == 'EXPERIMENTAL':
            steps.append(('model_file_path', 'Select Model File (.glb)', 'file', '*.glb'))
            steps.append(('shader_library_path', 'Select Shader Library Folder', 'directory', ''))
            self.root = bpy.context.scene.warframe_tools_props.root
            if bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION and (self.root is None or self.root is ""):
                steps.append(('root', 'Select Root Directory', 'directory', ''))
            if bpy.context.scene.warframe_tools_props.USE_EXTRACTOR:
                steps.append(('extractor_path', 'Select Extractor CLI', 'file', '*'))
                steps.append(('cache_path', 'Select Cache Folder', 'directory', ''))
        elif mode == 'SHADER':
            steps.append(('material_file_path', 'Select Material File (.txt)', 'file', '*.txt'))
            self.root = bpy.context.scene.warframe_tools_props.root
            if bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION and (self.root is None or self.root is ""):
                steps.append(('root', 'Select Root Directory', 'directory', ''))
            elif not bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION:
                steps.append(('pathToTextures', 'Select Textures Directory', 'directory', ''))
        return steps

    def invoke(self, context, event):
        self.steps = self.determine_steps()
        if not self.steps:
            self.report({'WARNING'}, "No paths required for current mode")
            return self.execute(context)
        self.current_step = 0
        self.filepath = ""
        self.directory = str(Path.home())
        self.material_file_path = ""
        self.model_file_path = ""
        self.extractor_path = ""
        self.cache_path = ""
        self.shader_library_path = ""
        self.pathToShader = ""
        self.pathToRig = ""
        self.root = ""
        self.pathToTextures = ""
        self.normal_to_height_path = ""
        return self.execute(context)
    
    def execute(self, context):
        if self.current_step >= len(self.steps):
            if self.material_file_path:
                bpy.context.scene.warframe_tools_props.material_file_path = self.material_file_path
            if self.model_file_path:
                bpy.context.scene.warframe_tools_props.model_file_path = self.model_file_path
            if self.extractor_path:
                bpy.context.scene.warframe_tools_props.extractor_path = self.extractor_path
            if self.cache_path:
                bpy.context.scene.warframe_tools_props.cache_path = self.cache_path
            if self.shader_library_path:
                bpy.context.scene.warframe_tools_props.shader_library_path = self.shader_library_path
            if self.pathToTextures:
                bpy.context.scene.warframe_tools_props.pathToTextures = self.pathToTextures
            if self.pathToRig:
                bpy.context.scene.warframe_tools_props.rig_path = self.pathToRig
            if self.pathToShader:
                bpy.context.scene.warframe_tools_props.pathToShader = self.pathToShader
            if self.normal_to_height_path:
                bpy.context.scene.warframe_tools_props.normal_to_height_path = self.normal_to_height_path
            if self.root:
                bpy.context.scene.warframe_tools_props.root = self.root
            if self.pathToTextures:
                bpy.context.scene.warframe_tools_props.pathToTextures = self.pathToTextures
            return bpy.ops.wm.run_setup('INVOKE_DEFAULT')
        
        step = self.steps[self.current_step]
        step_id, label, step_type, filter_glob = step
        current_value = getattr(self, step_id, "")
        props = context.scene.warframe_tools_props

        if not current_value:
            if step_type == 'file':
                if not self.filepath:
                    if hasattr(props, step_id):
                        scene_value = getattr(props, step_id)
                        if scene_value:
                            self.filepath = scene_value
                    self.filter_glob = filter_glob
                    context.window_manager.fileselect_add(self)
                    return {'RUNNING_MODAL'}
                else:
                    setattr(self, step_id, self.filepath)
                    self.filepath = ""
                    self.current_step += 1
            elif step_type == 'directory':
                if not self.filepath:
                    if hasattr(props, step_id):
                        scene_value = getattr(props, step_id)
                        if scene_value:
                            self.filepath = scene_value
                    context.window_manager.fileselect_add(self)
                    return {'RUNNING_MODAL'}
                else:
                    setattr(self, step_id, self.filepath)
                    self.filepath = ""
                    self.current_step += 1
        else:
            self.current_step += 1

        return self.execute(context)

    def modal(self, context, event):
        if event.type == 'FILE_SELECT':
            return self.execute(context)
        return {'PASS_THROUGH'}

    def draw(self, context):
        layout = self.layout
        for i, step in enumerate(self.steps):
            step_id, label, step_type, _ = step
            row = layout.row()
            if i == self.current_step:
                row.alert = True
                row.label(text=f"➤ {label}", icon='FILEBROWSER')
                current_value = getattr(self, step_id, "")
                if current_value:
                    name = os.path.basename(current_value)
                    row.label(text=name, icon='CHECKMARK')
            else:
                row.label(text=f"   {label}")
                current_value = getattr(self, step_id, "")
                if current_value:
                    name = os.path.basename(current_value)
                    row.label(text=name, icon='CHECKMARK')
                    
class WARFRAME_OT_ExperimentalMode(bpy.types.Operator):
    bl_idname = "wm.experimental_mode"
    bl_label = "Experimental Mode"
    bl_description = "Import model and auto-setup materials from MaterialPath"
    
    def execute(self, context):
        
        start_time = time.time()
        props = context.scene.warframe_tools_props
        set_up_mats = []
        bpy.ops.wm.import_model('EXEC_DEFAULT')
        
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
            if(obj.data.materials[0].name.split('.')[0] in set_up_mats):
                continue    
            material_path = obj.data.materials[0].get('FullPath')
            if not material_path:
                set_up_mats.append(obj.data.materials[0].name.split('.')[0])
                self.report({'WARNING'}, f"Object {obj.name} has no FullPath custom property")
                continue
            
            internal_path = find_internal_path(material_path) #возможно не надо
            material_file_path = os.path.join(props.root, internal_path) + ".txt"
            
            if not os.path.exists(material_file_path):
                if props.USE_EXTRACTOR:
                    success = extract_material_with_cli(
                        props.extractor_path,
                        props.cache_path,
                        internal_path,
                        props.root
                    )
                    if not success:
                        self.report({'ERROR'}, f"Failed to extract material: {internal_path}")
                        set_up_mats.append(obj.data.materials[0].name.split('.')[0])
                        continue
                else:
                    self.report({'WARNING'}, f"Material file not found: {material_file_path}")
                    set_up_mats.append(obj.data.materials[0].name.split('.')[0])
                    continue
            
            try:
                material_data, shader_data, hierarchy_data = parse_material_file(material_file_path)
            except Exception as e:
                self.report({'ERROR'}, f"Failed to parse material file: {str(e)}")
                set_up_mats.append(obj.data.materials[0].name.split('.')[0])
                continue
            
            shader_name = None
            for key in shader_data:
                if isinstance(key, str) and '_p.hlsl' in key:
                    shader_name = key.split('_p.hlsl')[0].split("/")[-2]
                    break
            
            if not shader_name:
                self.report({'WARNING'}, f"No shader found in material file: {material_file_path}")
                set_up_mats.append(obj.data.materials[0].name.split('.')[0])
                continue
            print(f"Found shader name: {shader_name}")
            shader_blend_path, error = find_shader_material(shader_name, props.shader_library_path)
            if error:
                self.report({'ERROR'}, error)
                set_up_mats.append(obj.data.materials[0].name.split('.')[0])
                continue
            
            print(f"Found shader: {shader_blend_path}")
            material_name = get_best_material_from_blend(shader_blend_path, material_data)
            if not material_name:
                self.report({'ERROR'}, f"No suitable material found in {shader_blend_path}")
                set_up_mats.append(obj.data.materials[0].name.split('.')[0])
                continue
            print(f"Chosen material: {material_name}")
            original_base_name = None
            if obj and obj.data and hasattr(obj.data, 'materials') and obj.data.materials:
                if obj.data.materials[0]:
                    original_base_name = obj.data.materials[0].name.split('.')[0]

            before = set(bpy.data.materials.keys())
            
            before_images = set(bpy.data.images.keys())
            bpy.ops.wm.append(
                directory=os.path.join(shader_blend_path, "Material") + os.sep,
                filename=material_name,
                do_reuse_local_id=False
            )
            after = set(bpy.data.materials.keys())
            new_material_names = after - before
            
            if not new_material_names:
                self.report({'ERROR'}, "Failed to append material")
                set_up_mats.append(obj.data.materials[0].name.split('.')[0])
                continue
                
            new_material = bpy.data.materials[list(new_material_names)[0]]
            self.report({'INFO'}, f"Appended material: {material_name}")

            after_images = set(bpy.data.images.keys())
            new_image_names = after_images - before_images
            
            self.cleanup_textures(new_material, new_image_names) #change
            gn_node_groups = []
            try:
                with bpy.data.libraries.load(context.scene.warframe_tools_props.pathToShader, link=False) as (data_from, data_to):
                    gn_node_groups = [name for name in data_from.node_groups if name.startswith("Gn") and name not in data_to.node_groups]
            except Exception as e:
                self.report({'WARNING'}, f"Could not read node groups: {str(e)}")
            
            for node_group_name in gn_node_groups:
                if node_group_name not in bpy.data.node_groups:
                    try:
                        bpy.ops.wm.append(
                            directory=os.path.join(context.scene.warframe_tools_props.pathToShader, "NodeTree") + os.sep,
                            filename=node_group_name,
                            do_reuse_local_id=True
                        )
                        self.report({'INFO'}, f"Appended node group: {node_group_name}")
                    except Exception as e:
                        self.report({'WARNING'}, f"Failed to append node group {node_group_name}: {str(e)}")

            if original_base_name:
                old_materials = [mat for mat in bpy.data.materials 
                                if mat.name.startswith(original_base_name + '.') or 
                                mat.name == original_base_name]
                
                for old_mat in old_materials:
                    old_mat.user_remap(new_material)
                    
                for old_mat in old_materials:
                    if old_mat.users == 0 and old_mat != new_material:
                        bpy.data.materials.remove(old_mat)
                
                new_material.name = original_base_name
            else:
                if obj and obj.data:
                    new_name = f"{obj.data.name}_Material"
                    new_material.name = new_name
                    
                    if not obj.data.materials:
                        obj.data.materials.append(new_material)
                    else:
                        obj.data.materials[0] = new_material
            
            texture_locations = {}
            
            model_path = find_internal_path(material_file_path)
            set_material_properties(new_material, material_data, props.pathToTextures, 
                                  model_path, texture_locations, shader_data, hierarchy_data)
                                  
            set_up_mats.append(obj.data.materials[0].name.split('.')[0])
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            minutes, seconds = divmod(elapsed_time, 60)
            
            self.report({'INFO'}, f"Setup completed in {int(minutes)}m {seconds:.2f}s")
            self.report({'INFO'}, f"Set up material for {obj.name}")
        
        return {'FINISHED'}
    def cleanup_textures(self, material, new_image_names):
        if not material.use_nodes:
            return
        unused_images = new_image_names
        
        for image_name in unused_images:
            image = bpy.data.images.get(image_name)
            if image:
                try:
                    bpy.data.images.remove(image)
                    self.report({'INFO'}, f"Removed unused image: {image_name}")
                except Exception as e:
                    self.report({'WARNING'}, f"Could not remove image {image_name}: {str(e)}")
    
class WarframeAutoPorter(bpy.types.AddonPreferences):
    # This must match the add-on name, use `__package__`
    # when defining this for add-on extensions or a sub-module of a python package.
    bl_idname = __name__

    root_preference: StringProperty(
        name="Extracted Root Folder Path",
        subtype='DIR_PATH'
    )
    rig_preference: StringProperty(
        name="Rig Blend Path",
        subtype='FILE_PATH'
    )
    texture_extension_preference: EnumProperty(
        name="Texture Extension",
        description="Choose the texture file extension",
        items=texture_extension_list,
        default='*.png'
    )
    def draw(self, context):
        layout = self.layout
        layout.label(text="Warning! Changing these in the panel will change the preferences!")
        layout.label(text="Path to the folder where Lotus, EE, DOS, SF and other folders are located.")
        layout.label(text=r"DO NOT CHOOSE LOTUS FOLDER (example, D:\tmp\Assets)")
        layout.prop(self, "root_preference")
        layout.label(text=r"Path to the rig blend file (example, D:\Downloads\WF_Rig.blend)")
        layout.prop(self, "rig_preference")
        layout.label(text="Default extracted texture extension.")
        layout.prop(self, "texture_extension_preference")
        
        
def get_root_value(self):
    return bpy.context.preferences.addons[__name__].preferences.root_preference
def set_root_value(self, value):
    bpy.context.preferences.addons[__name__].preferences.root_preference = value  
    
    
def get_rig_value(self):
    return bpy.context.preferences.addons[__name__].preferences.rig_preference
def set_rig_value(self, value):
    bpy.context.preferences.addons[__name__].preferences.rig_preference = value     
       
            
def set_uv_value(self, value):
    obj = bpy.context.selected_objects[0]
    if not obj or obj.type != 'MESH' or not obj.data.uv_layers:
        return
    val = obj.data.uv_layers[value].name
    if val in obj.data.uv_layers:
        for i, uv_layer in enumerate(obj.data.uv_layers):
            if uv_layer.name == val:
                uv_layer.active = True
def get_uv_items(self, context):
    obj = context.selected_objects[0]
    if not obj or obj.type != 'MESH' or not obj.data.uv_layers:
        return [("None", "Please select an object", "")]
    return [(uv.name, uv.name, uv.name) for uv in obj.data.uv_layers]
def get_uv_value(self):
    obj = bpy.context.selected_objects[0]
    if not obj or obj.type != 'MESH' or not obj.data.uv_layers:
        return 0
    return obj.data.uv_layers.active_index


def get_ext_value(self):
    val = bpy.context.preferences.addons[__name__].preferences.texture_extension_preference
    index = next((i for i, (first, *_) in enumerate(texture_extension_list) if first == val), None)
    return index
def set_ext_value(self, value):
    bpy.context.preferences.addons[__name__].preferences.texture_extension_preference = texture_extension_list[value][0]      

def get_image_items(self, context):
    items = [(img.name, img.name, "") for img in bpy.data.images]
    if not items:
        items.append(('NONE', 'No Images', ""))
    return items

class BakeSourceItem(bpy.types.PropertyGroup):
    name: StringProperty()
    value: BoolProperty(name="", default=False)
    identifier: StringProperty()
   
class WarframeAddonProperties(bpy.types.PropertyGroup):

    USE_ROOT_LOCATION: BoolProperty(
    name="Use Root Location",
    description="Determines paths from mat file using root location",
    default=True
)
    LEVEL_IMPORT: BoolProperty(
    name="Import Level",
    description="Due to differences, level import is slightly different. Choose it if you import levels",
    default=False
)    
    USE_PATHS: BoolProperty(
    name="Enable automatic paths",
    description="If deselected - new fields with required paths will appear",
    default=True
)
    EMPTY_IMAGES_BEFORE_SETUP: BoolProperty(
    name="Empty Images Before Setup",
    description="Empties all images from shader before set up",
    default=True
)
    REPLACE_IMAGES: BoolProperty(
    name="Replace Images",
    description="Replace images with ones from material file if the image was already set previously",
    default=True
)
    RESET_PARAMETERS: BoolProperty(
    name="Reset Parameters",
    description="Sets values that do not exist in the mat txt file to 0, gray, etc. Useful if there are parameters that a set to true but don't exist in your mat file",
    default=True
)
    invert_green: BoolProperty(
    name="Invert green",
    description="Inverts green or something, idk...",
    default=True
)
    texture_extension: EnumProperty(
    name="Texture Extension",
    description="Choose the texture file extension",
    items=texture_extension_list,
    get=get_ext_value,
    set=set_ext_value
)
    bake_base_color: BoolProperty(
        name="Base Color",
        default=True
    )
    bake_emission: BoolProperty(
        name="Emission",
        default=False
    )
    bake_metalness: BoolProperty(
        name="Metalness",
        default=False
    )
    bake_roughness: BoolProperty(
        name="Roughness",
        default=False
    )
    bake_specular: BoolProperty(
        name="Specular",
        default=False
    )
    bake_normal: BoolProperty(
        name="Normal",
        default=False
    )
    bake_alpha: BoolProperty(
        name="Alpha",
        default=False
    )
    uv_source: EnumProperty(
    name="UV Map Selection",
    description="Choose the uv map of the object",
    items=get_uv_items,
    get=get_uv_value,
    set=set_uv_value
)
    bake_height: IntProperty(
    name="Height",
    description="Height of the baked texture",
    default=2048
)
    bake_width: IntProperty(
    name="Width",
    description="Width of the baked texture",
    default=2048
)
    USE_EXTRACTOR: BoolProperty(
    name="Use Extractor",
    description="Use extractor to try and set everything up in one go.",
    default=False
)
    extractor_path: StringProperty(
    name="Extractor CLI Path",
    description=r"Path to the CLI Extractor to use.",
    default=r"D:\Extractor\Warframe-Extractor-CLI.exe",
    subtype='FILE_PATH'
)
    cache_path: StringProperty(
    name="Cache Folder Path",
    description=r"Path to the warframe cache folder (e.g., D:\Warframe\Cache.Windows)",
    default=r"",
    subtype='DIR_PATH'
)
    material_file_path: StringProperty(
    name="Material File Path",
    description=r"Material txt file path (e.g., D:\tmp\Assets\Lotus\Objects\Duviri\Props\DominitiusThraxThroneA.txt)",
    default=r"D:\tmp\Assets\Lotus\Objects\Duviri\Props\DominitiusThraxThroneA.txt",
    subtype='FILE_PATH'
)
    model_file_path: StringProperty(
    name="Model Path",
    description=r"Model file path (e.g., D:\tmp\Assets\Lotus\Objects\Duviri\Props\DUVxDominitiusThraxThrone.glb)",
    default=r"D:\tmp\Assets\Lotus\Objects\Duviri\Props\DUVxDominitiusThraxThrone.glb",
    subtype='FILE_PATH'
)
    pathToShader: StringProperty(
    name="Shader Path",
    description=r"Shader .blend path (e.g., D:\Download\PBRFillDeferred.blend)",
    default=r"E:\Download\PBRFillDeferred.blend",
    subtype='FILE_PATH'
)
    pathToTextures: StringProperty(
    name="Textures Path",
    description=r"Textures folder path (e.g., D:\UmbraArmorTextures)",
    default=r"E:\UmbraArmorTextures",
    subtype='FILE_PATH'
)    
    root: StringProperty(
    name="Extracted Root Folder Path",
    description=r"Path to the folder where Lotus, EE, DOS, SF and other folders are located. DO NOT CHOOSE LOTUS FOLDER (example, D:\tmp\Assets)",
    subtype='DIR_PATH',
    default=r"D:",
    get=get_root_value,
    set=set_root_value
)    
    rig_path: StringProperty(
    name="Rig Blend Path",
    description=r"Path to the .blend path (e.g., D:\Download\WFRig.blend",
    subtype='FILE_PATH',
    default=r"D:",
    get=get_rig_value,
    set=set_rig_value
)    
    normal_to_height_path: StringProperty(
    name="Normal Map Path",
    description=r"Path to the normal map to make height map out of",
    default=r"D:",
    subtype='FILE_PATH'
)
    subdiv_amount: IntProperty(
    name="Subdivision Amount",
    description="Subdivision Amount",
    default=4
)
    optimized_subdivision: BoolProperty(
        name="Use Simple + Catmull-Clark",
        default=False
)    
    ram_subdivision: BoolProperty(
        name="Use Ram Amount To Guess Amount Of Subdivisions",
        default=False
)    
    ram_amount: IntProperty(
        name="Ram Amount (GB)",
        default=8
)    
    separate_mode: BoolProperty(
        name="Separate Stages",
        default=False
)
    image_select: bpy.props.EnumProperty(
        name="Height Map",
        description="Select an image from the blend file",
        items=get_image_items
)
    shader_library_path: StringProperty(
        name="Shader Library Path",
        description="Path to the folder containing .blend files with shaders",
        subtype='DIR_PATH',
        default=""
)
    mode: EnumProperty(
    name="Mode",
    items=[
        ('IMPORT', "Import Model Mode", "Import the model from a file"),
        ('APPEND', "Shader Append Mode", "Append the shader from a blend file"),
        ('SHADER', "Shader Setup Mode", "Set up the shader parameters and textures"),
        ('RIG', "Rig Setup Mode", "Set up the rig for characters"),
        ('BAKE', "Baking Mode", "Bake the textures for the selected object"),
        ('3DPRINT', "3d Printing Mode", "Things for 3d printing and stuff"),
        ('EXPERIMENTAL', "Experimental Mode", "Import model and auto-setup materials from MaterialPath"),
    ],
    default='EXPERIMENTAL'
)
 
class WARFRAME_PT_SetupPanel(bpy.types.Panel):
    bl_label = "Warframe Model Setup"
    bl_idname = "WARFRAME_PT_SetupPanel"
    bl_description = "Panel for setting up warframe models"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        if not context:
            return
        layout = self.layout
        scene = context.scene
        props = scene.warframe_tools_props
        prefs = context.preferences.addons[__name__].preferences
        box = layout.box()
        box.label(text="Configuration")
        box.label(text="Select Mode:")
        box.prop(props, "mode")
        if props.mode == 'IMPORT':
            box.prop(props, "USE_PATHS")
            box.prop(props, "LEVEL_IMPORT")
            box.prop(props, "USE_EXTRACTOR")
            if not props.USE_PATHS: 
                box.prop(props, "model_file_path")
                box.prop(props, "extractor_path")
                box.prop(props, "cache_path")
            
            if props.USE_PATHS:
                layout.operator("wm.setup_paths", text="Import")
            else:
                layout.operator("wm.run_setup", text="Import")
            return
        if props.mode == 'APPEND':
            box.prop(props, "USE_PATHS")
            if not props.USE_PATHS: 
                box.prop(props, "pathToShader")
            
            if props.USE_PATHS:
                layout.operator("wm.setup_paths", text="Run Setup")
            else:
                layout.operator("wm.run_setup", text="Run Setup")
            return
        if props.mode == 'RIG':
            box.prop(props, "USE_PATHS")
            if not props.USE_PATHS: 
                box.prop(prefs, "rig_preference")
            if props.USE_PATHS:
                layout.operator("wm.setup_paths", text="Run Setup")
            else:
                layout.operator("wm.run_setup", text="Run Setup")
            return
        if props.mode == 'BAKE':
            box.prop(props, "USE_PATHS")
            box.label(text="Bake Sources:")
            grid = box.grid_flow(
                row_major=True,
                columns=3,
                even_columns=True,
                even_rows=True,
                align=True
            )
            grid.prop(props, "bake_base_color")
            grid.prop(props, "bake_emission")
            grid.prop(props, "bake_metalness")
            grid.prop(props, "bake_roughness")
            grid.prop(props, "bake_specular")
            grid.prop(props, "bake_normal")
            grid.prop(props, "bake_alpha")
            box.prop(props, "uv_source")
            row = box.row(align=True)
            row.prop(props, "bake_height")
            row.prop(props, "bake_width")
            if props.USE_PATHS:
                layout.operator("wm.setup_paths", text="Run Setup")
            else:
                layout.operator("wm.run_setup", text="Run Setup")
            return
        if props.mode == '3DPRINT':
            box.prop(props, "separate_mode")
            convert = box.box()
            convert.prop(props, "normal_to_height_path")
            convert.prop(props, "invert_green")
            
            if props.separate_mode:
                convert.operator("dprint.normal_to_height", text="Convert Normal Map to Height Map")
            box.separator()
            
            subd = box.box()
            subd.prop(props, "optimized_subdivision")
            subd.prop(props, "ram_subdivision")
            if not props.ram_subdivision:
                subd.prop(props, "subdiv_amount")
            if props.ram_subdivision: 
                subd.prop(props, "ram_amount")
            
            if props.separate_mode:
                subd.operator("dprint.subdivide", text="Add subdivision")
            box.separator()
            
            if props.separate_mode:
                heightm = box.box()
                heightm.prop(props, "image_select")
                heightm.operator("dprint.add_height", text="Add Deform Modifier With Selected Height Map")
            
            if not props.separate_mode:
                row = box.row()
                row.operator("dprint.run_all_operations", text="Run All Operations")
            return
        if props.mode == 'EXPERIMENTAL':
            box.prop(props, "USE_PATHS")
            box.prop(props, "USE_EXTRACTOR")
            box.prop(props, "LEVEL_IMPORT")
            box.prop(props, "RESET_PARAMETERS")
            if not props.USE_PATHS: 
                box.prop(props, "model_file_path")
                box.prop(props, "extractor_path")
                box.prop(props, "cache_path")
                box.prop(props, "shader_library_path")
            box.prop(props, "USE_ROOT_LOCATION")
            if not props.USE_PATHS and props.USE_ROOT_LOCATION: 
                box.prop(prefs, "root_preference")
            
            if props.USE_PATHS:
                layout.operator("wm.setup_paths", text="Run Experimental Setup")
            else:
                layout.operator("wm.run_setup", text="Run Experimental Setup")
            return
        if props.mode == 'SHADER':
            box.prop(props, "USE_PATHS")
            
            box.prop(props, "USE_EXTRACTOR")
            if not props.USE_PATHS: 
                box.prop(props, "material_file_path")
                box.prop(props, "extractor_path")
                box.prop(props, "cache_path")
            box.prop(props, "USE_ROOT_LOCATION")
            if not props.USE_PATHS and not props.USE_ROOT_LOCATION: box.prop(props, "pathToTextures")
            elif not props.USE_PATHS and props.USE_ROOT_LOCATION: box.prop(prefs, "root_preference") 
            box.prop(props, "EMPTY_IMAGES_BEFORE_SETUP")
            box.prop(props, "REPLACE_IMAGES")
            box.prop(props, "RESET_PARAMETERS")
            box.prop(props, "texture_extension")
        if props.USE_PATHS:
            layout.operator("wm.setup_paths", text="Run Setup")
        else:
            layout.operator("wm.run_setup", text="Run Setup")

classes = (
    WarframeAutoPorter,
    WARFRAME_PT_SetupPanel,
    WM_OT_RunSetup,
    WARFRAME_OT_SetupShader,
    WARFRAME_OT_ImportModel,
    WARFRAME_OT_ExperimentalMode,
    WM_OT_SetupPaths,
    SHADER_OT_append_material,
    NormalToHeightOperator,
    SubDivisionOperator,
    DeformOperator,
    RunAllOperationsOperator,
    RIG_OT_append_rig,
    WarframeAddonProperties,
    OBJECT_OT_BakeTextures
)
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.warframe_tools_props = PointerProperty(type=WarframeAddonProperties)
    bpy.context.preferences.use_preferences_save = True

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.warframe_tools_props
if __name__ == "__main__":
    register()
