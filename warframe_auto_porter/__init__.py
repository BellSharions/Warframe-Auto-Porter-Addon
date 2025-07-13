bl_info = {
    "name": "Warframe Auto Porter",
    "author": "Bell Sharions",
    "version": (0, 45),
    "blender": (4, 2, 0),
    "location": "3D View > Tool Shelf (Right Panel) > Tool",
    "description": "Imports and configures Warframe models/materials",
    "category": "Import",
}
# Script done by Bell Sharions for Warframe Model Resources
# This is not a "do it all" script, some assebly and tweaks might be required in some cases

# Check Info panel for script completion/error
# Double check the material TXT file and tweak the shader accordingly if the model still looks wrong
# If there are errors in the Info panel, something in the material file is not applied, something applied wrongly
# etc, double check the material file and the previous state of shader. 
# If the parameter was already set to true by default the script will not set it to false automatically unless
# RESET_PARAMETERS was set to True in configuration 
# If the error reoccurs and it not a user error - message the creator of the script
# Do you want to just launch the script without pasting anything? 
# Use USE_PATHS to launch UI version. Currently support is limited(I don't know if everything is implemented 
# for the base user to understand clearly, but should be good enough for the default setup)
# IMPORTANT: set model_path in this version to the internal path
# model_path - Set this to the internal model location. 
# Example: /Lotus/Characters/Tenno/Nyx/SWAures - Nyx Tennogen skin location
# Set it to the exact internal path. Yes, it begins with /.
# (Configuration) - Set these paths before running
# material_file_path - Set this to the path of material TXT file. Yes, including .txt extension.
# model_file_path - Set if you use IMPORT_MODEL_MODE
# pathToShader - Set this if you use SHADER_APPEND_MODE. 
# Assign it to .blend file of where the materials that need to be appended are. Example is for PBRFillDeferred
# Model Setup
# This section is about model setup. If you just want to setup shader itself - turn both options off
# IMPORT_MODEL_MODE - Set this if you only want to import the model with the correct settings 
# for later use like appending shader and using Shader Setup. If set to True THIS WILL NOT RUN THE SHADER SETUP
# SHADER_APPEND_MODE - Set this to append the shader and assign it to the selected object automatically.
# If set to True THIS WILL NOT RUN THE SHADER SETUP.
# Shader Setup
# Method 1 - Copy all the textures from the material TXT file txt in a separate folder and copy the path to pathToTextures
# pathToTextures - Set this to the path of where ALL the textures from material TXT file are if USE_ROOT_LOCATION is False
# Method 2 - Set the root folder that contains Lotus, EE, etc folders and model path.
# USE_ROOT_LOCATION - Set this to use root folder(folder where Lotus, EE, etc are located instead of pathToTextures. 
# root and model_path locations are required for this to work correctly.
# root - Set this to the Root file location. Set this to the path where Lotus, EE, etc folders are located
# DO NOT set it to Lotus folder itself, set it to where the root is.
# In the example path folder 1 has Lotus, EE, SF and other folders that have extracted folders/files.
# EMPTY_IMAGES_BEFORE_SETUP - Set this to flush images before setup. Might cause errors on first run.
# REPLACE_IMAGES - Set this to force replace images
# RESET_PARAMETERS - Set this to reset all parameters to 0. Does not affect Image Textures.
# Do not use unless you know what you're doing.
# texture_extension - Set to the texture extension you're using in *.format style. Examples - *.png, *.dds, *.tga
# shader_exceptions_parameters - These are the parameters that depend on the specific shader number. 
# Useful only on rare occasions, like "Swizzle Vertex Channels" in TerrainFill. 
# Add to this list if the option is not added yet(it likely already was added). 
# Does not differentiate between shaders
# COMPARING_MODE - set this to also check the shader group name when setting the exceptions.
# Otherwise will assume first shader in shader list is the correct one.
from pathlib import Path
import bpy
import os
import ast
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
    index = path.rfind("Lotus")
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

def contains(str1, str2):
    if not isinstance(str1, str) or not isinstance(str2, str):
        return True
    if '=' in str1.lower() or '=' in str2.lower():
        return str1.lower() == str2.lower()
    return str1.lower() in str2.lower()

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
def reset_default(input_socket):
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
                
def parse_material_file(filepath):
    material_data = {}
    shader_data = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line and ':' not in line:
                print(line)
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
            if "shader" in value.lower() and '.hlsl' in value.lower():
                key = value.split("/")[-2]
                value = value.split("/")[-1].split(".")[0]
                if value.endswith("p") and "_" in value:
                    shader_data[key] = value.split("_")[0]
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
                print(key)
                material_data[line.strip()] = 1
                if(line.strip().lower().endswith("= none")):
                    continue
                material_data[key] = 1
                material_data[value.strip()] = 1
    return (material_data, shader_data)

def connect_textures_and_parameters(material, node_group, parameters, textures, pathToTextures, texture_locations, labeled_reroutes, shader_data):
    group_tree = node_group.node_tree
    
    if node_group.name.lower() in parameters.keys():
        for nodegroup_to_link in bpy.data.node_groups:
            if parameters[node_group.name.lower()] in nodegroup_to_link.name:
                node_group.node_tree = nodegroup_to_link
            
    
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
                    name = filename.split('/')[-1]
                    if any(contains(tex_name, input_socket.name) for link in input_socket.links):
                        try:
                            img = None
                            for img_tex in bpy.data.images:
                                if(img_tex.name in name):
                                    img = img_tex
                            if(img is None):
                                img = bpy.data.images.load(filename)
                            img.colorspace_settings.name = 'Non-Color'
                            if((current.image is None) or (bpy.context.scene.warframe_tools_props.REPLACE_IMAGES and current.image.name not in img.name)):
                                current.image = img
                            print(f"Connected texture: {filename}")
                        except Exception as e:
                            print(f"Texture error: {str(e)}")
        # Dunno if needed
        if input_socket.name in parameters:
            value = parameters[input_socket.name]
            set_default(input_socket, value)
        elif(bpy.context.scene.warframe_tools_props.RESET_PARAMETERS):
            reset_default(input_socket)

        for name in parameters:
            if contains(name, input_socket.name) and (input_socket.type == 'BOOLEAN' or input_socket.type == 'COLOR' or input_socket.type == 'VECTOR' or input_socket.type == 'VALUE' or input_socket.type == 'RGBA'):
                value = None
                try:
                    if input_socket.name.endswith('XYZ'):
                        value = parameters[input_socket.name.split(" ")[0].lower()]
                    elif input_socket.name.endswith('X'):
                        value = parameters[input_socket.name.split(" ")[0].lower()] if isinstance(parameters[input_socket.name.split(" ")[0].lower()], int) else parameters[input_socket.name.split(" ")[0].lower()][0]
                    elif input_socket.name.endswith('Y'):
                        value = parameters[input_socket.name.split(" ")[0].lower()] if isinstance(parameters[input_socket.name.split(" ")[0].lower()], int) else parameters[input_socket.name.split(" ")[0].lower()][1]
                    elif input_socket.name.endswith('Z'):
                        value = parameters[input_socket.name.split(" ")[0].lower()] if isinstance(parameters[input_socket.name.split(" ")[0].lower()], int) else parameters[input_socket.name.split(" ")[0].lower()][2]
                    elif input_socket.name.endswith('W') or input_socket.name.endswith('Alpha'):
                        value = parameters[input_socket.name.split(" ")[0].lower()] if isinstance(parameters[input_socket.name.split(" ")[0].lower()], int) else parameters[input_socket.name.split(" ")[0].lower()][3]
                    else:
                        if input_socket.name.lower().endswith("= none"):
                            value = parameters[input_socket.name.lower()]
                        else:
                            value = parameters[input_socket.name.split(" ")[0].lower()]
                    print(f"Setting instance parameter: {input_socket.name} = {value}")
                    set_default(input_socket, value)
                    break
                except Exception as e:
                    if(input_socket.name.split(" ")[0].lower() in "UvScale01".lower()):
                        print(parameters[input_socket.name.split(" ")[0].lower()])
                    print(input_socket.type)
                    print(input_socket.name)
                    print(f"Parameter error: {str(e)}")
                    break
            elif(bpy.context.scene.warframe_tools_props.RESET_PARAMETERS):
                reset_default(input_socket)
        if input_socket.name in shader_exceptions_parameters:
            first_value = next(iter(shader_data.values()))
            for key in shader_data:
                if key in node_group.node_tree.name:
                    first_value = shader_data[key]
            for item in labeled_reroutes:
                if item == first_value:
                    set_default(input_socket, True)
                                      
def set_material_properties(material, material_data, pathToTextures, model_path, texture_locations, shader_data):
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
            if(not result.endswith(bpy.context.scene.warframe_tools_props.texture_extension.split("*")[1]) and "." in result):
                result = result.split(".")[0] + bpy.context.scene.warframe_tools_props.texture_extension.split("*")[1]
            if(not "/" in result and bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION):
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
                print(result)
                onlyfiles = [f for f in os.listdir(str(Path(root_loc + value))) if os.path.isfile(os.path.join(str(Path(root_loc + value)), f))]
                for idx, file in enumerate(onlyfiles):
                    print(root_loc)
                    texture_locations[key + " " + str(idx)] = str(Path(root_loc + value + file))
                continue
            elif (not str(Path(root_loc + value)).endswith(bpy.context.scene.warframe_tools_props.texture_extension.split("*")[1])):
                texture_locations[key] = str(Path(root_loc + value + bpy.context.scene.warframe_tools_props.texture_extension.split("*")[1]))
                continue
            texture_locations[key] = str(Path(root_loc + value))
    elif(not bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION):
        for key, value in textures.items():
            if (not str(Path(str(pathToTextures) + value.split("/")[-1])).endswith(bpy.context.scene.warframe_tools_props.texture_extension.split("*")[1])):
                texture_locations[key] = str(Path(os.path.join(pathToTextures, value.split("/")[-1]) + bpy.context.scene.warframe_tools_props.texture_extension.split("*")[1]))
                continue
            texture_locations[key] = os.path.join(pathToTextures, value.split("/")[-1])
    node_groups = []
    for node in material.node_tree.nodes:
        if node.type == 'REROUTE' and node.label.strip():
            input_unlinked = not node.inputs[0].is_linked
            output_unlinked = not node.outputs[0].is_linked
            
            if input_unlinked or output_unlinked:
                labeled_reroutes.append(node.label)
        if node.type == 'GROUP' and node.node_tree:
            node_groups.append(node)
    print(texture_locations)
    node_groups_for_gn = [ng for ng in bpy.data.node_groups if ng.type == 'GEOMETRY' and ng.name.startswith("Gn. ")]
    
    node_group_map = {}
    print(parameters)
    for ng in node_groups_for_gn:
        base_name = ng.name[4:].split(maxsplit=1)[0]
        node_group_map[base_name.lower()] = ng
    
    for param_name, param_value in (parameters | shader_data).items():
        if param_name.lower() in node_group_map:
            ng = node_group_map[param_name]
            
            mod = bpy.context.active_object.modifiers.new(name=ng.name, type='NODES')
            mod.node_group = ng
            
            for item in ng.interface.items_tree:
                print(item)
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
    for node in node_groups:  
        print(node.type)
        if node.type is not 'GEOMETRY':
            connect_textures_and_parameters(material, node, parameters, textures, pathToTextures, texture_locations, labeled_reroutes, shader_data)

def get_shader_items(self, context):
    items = []
    if not os.path.exists(bpy.context.scene.warframe_tools_props.pathToShader):
        return items
    with bpy.data.libraries.load(bpy.context.scene.warframe_tools_props.pathToShader, link=False) as (data_from, data_to):
        for mat_name in data_from.materials:
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
    renderer_state["bake_type"] = context.scene.cycles.bake_type
    renderer_state["engine"] = context.scene.render.engine
    renderer_state["samples"] = context.scene.cycles.samples
    renderer_state["device"] = context.scene.cycles.device
    
    context.scene.render.bake.margin = 3
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
def bake():
    # I hate azdfulla for making me do this
    props = bpy.context.scene.warframe_tools_props
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
    bpy.ops.object.bake_textures(source=",".join(sources))
    
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
            obj = context.object
            original_base_name = None
            if obj and obj.data and hasattr(obj.data, 'materials') and obj.data.materials:
                if obj.data.materials[0]:
                    original_base_name = obj.data.materials[0].name.split('.')[0]

            before = set(bpy.data.materials.keys())
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


def menu_func(self, context):
    self.layout.operator(SHADER_OT_append_material.bl_idname)

def register_shader():
    bpy.ops.shader.append_material('INVOKE_DEFAULT')

def unregister_shader():
    bpy.utils.unregister_class(SHADER_OT_append_material)
def register_rig():
    bpy.ops.rig.append_rig('INVOKE_DEFAULT')

def unregister_rig():
    bpy.utils.unregister_class(RIG_OT_append_rig)


def process_object(obj):
    if obj.type != 'MESH':
        return
    me = obj.data
    if not bpy.context.scene.warframe_tools_props.LEVEL_IMPORT:
        me.flip_normals()
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.normal_update()
        bm.to_mesh(me)
        bm.free()
    me.shade_smooth()

def run_setup():
    mode = bpy.context.scene.warframe_tools_props.mode
    if mode == 'IMPORT':
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
            obj.select_set(False)
            print(obj.data.validate(clean_customdata=True))
        collections_dict = {}
            
    elif mode == 'APPEND':
        register_shader()
    elif mode == 'RIG':
        register_rig()
    elif mode == 'BAKE':
        bake()
    elif mode == 'SHADER':
        mat = bpy.context.object.active_material
        if not mat:
            raise Exception("No active material selected")
        texture_locations = {}
        (material_data, shader_data) = parse_material_file(bpy.context.scene.warframe_tools_props.material_file_path)
        model_path = find_internal_path(bpy.context.scene.warframe_tools_props.material_file_path)
        print(model_path)
        print("!!!!")
        set_material_properties(mat, material_data, bpy.context.scene.warframe_tools_props.pathToTextures, model_path, texture_locations, shader_data)
        
        
class WM_OT_SetupPaths(bpy.types.Operator):
    bl_idname = "wm.setup_paths"
    bl_label = "Setup Required Paths"
    bl_description = "Select the path to file/folder"
    
    current_step: bpy.props.IntProperty(default=0)
    material_file_path: bpy.props.StringProperty(subtype='FILE_PATH')
    model_file_path: bpy.props.StringProperty(subtype='FILE_PATH')
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
        elif mode == 'EXPERIMENTAL':
            steps.append(('normal_to_height_path', 'Select Normal Map File', 'file', '*'))
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
        return self.execute(context)
    
    def execute(self, context):
        if self.current_step >= len(self.steps):
            if self.material_file_path:
                bpy.context.scene.warframe_tools_props.material_file_path = self.material_file_path
            if self.model_file_path:
                bpy.context.scene.warframe_tools_props.model_file_path = self.model_file_path
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
            run_setup()
            self.report({'INFO'}, "Setup Completed Successfully!")
            return {'FINISHED'}
        
        step = self.steps[self.current_step]
        step_id, label, step_type, filter_glob = step
        current_value = getattr(self, step_id, "")

        if not current_value:
            if step_type == 'file':
                if not self.filepath:
                    self.filter_glob = filter_glob
                    context.window_manager.fileselect_add(self)
                    return {'RUNNING_MODAL'}
                else:
                    setattr(self, step_id, self.filepath)
                    self.filepath = ""
                    self.current_step += 1
            elif step_type == 'directory':
                if not self.filepath:
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

class OBJECT_OT_addon_prefs_example(bpy.types.Operator):
    """Display example preferences"""
    bl_idname = "object.addon_prefs_example"
    bl_label = "Add-on Preferences Example"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences

        return {'FINISHED'}
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
    default=False
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
    default=r"E:\Download\PBRFillDeferred(5).blend",
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
    mode: EnumProperty(
    name="Mode",
    items=[
        ('IMPORT', "Import Model Mode", "Import the model from a file"),
        ('APPEND', "Shader Append Mode", "Append the shader from a blend file"),
        ('SHADER', "Shader Setup Mode", "Set up the shader parameters and textures"),
        ('RIG', "Rig Setup Mode", "Set up the rig for characters"),
        ('BAKE', "Baking Mode", "Bake the textures for the selected object"),
        ('EXPERIMENTAL', "Experimental Mode", "Things for 3d printing and stuff"),
    ],
    default='SHADER'
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
            if not props.USE_PATHS: 
                box.prop(props, "model_file_path")
            layout.operator("wm.run_setup", text="Import")
            return
        if props.mode == 'APPEND':
            box.prop(props, "USE_PATHS")
            if not props.USE_PATHS: 
                box.prop(props, "pathToShader")
            layout.operator("wm.run_setup", text="Append Shader")
            return
        if props.mode == 'RIG':
            box.prop(props, "USE_PATHS")
            if not props.USE_PATHS: 
                box.prop(prefs, "rig_preference")
            layout.operator("wm.run_setup", text="Setup Rig")
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
            layout.operator("wm.run_setup", text="Bake")
            return
        if props.mode == 'EXPERIMENTAL':
            box.label(text="3d print stuff")
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
        if props.mode == 'SHADER':
            box.prop(props, "USE_PATHS")
            if not props.USE_PATHS: 
                box.prop(props, "material_file_path")
            box.prop(props, "USE_ROOT_LOCATION")
            if not props.USE_PATHS and not props.USE_ROOT_LOCATION: box.prop(props, "pathToTextures")
            elif not props.USE_PATHS and props.USE_ROOT_LOCATION: box.prop(prefs, "root_preference") 
            box.prop(props, "EMPTY_IMAGES_BEFORE_SETUP")
            box.prop(props, "REPLACE_IMAGES")
            box.prop(props, "RESET_PARAMETERS")
            box.prop(props, "texture_extension")
        layout.operator("wm.run_setup", text="Run Setup")

class WM_OT_RunSetup(bpy.types.Operator):
    bl_idname = "wm.run_setup"
    bl_label = "Run Setup"

    def execute(self, context):
        if bpy.context.scene.warframe_tools_props.USE_PATHS:
            bpy.ops.wm.setup_paths('INVOKE_DEFAULT')
        else:
            run_setup()
            self.report({'INFO'}, "Setup Completed Successfully!")
        return {'FINISHED'}

classes = (
    WarframeAutoPorter,
    WARFRAME_PT_SetupPanel,
    WM_OT_RunSetup,
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