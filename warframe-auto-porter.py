bl_info = {
    "name": "Warframe Auto Porter",
    "author": "Bell Sharions",
    "version": (0, 40),
    "blender": (4, 2, 0),
    "location": "3D View > Tool Shelf (Right Panel)",
    "description": "Imports and configures Warframe models/materials",
    "category": "Import",
}
# Script done by Bell Sharions for Warframe Model Resources
# This is not a "do it all" script, some assebly and tweaks might be required in some cases

# To use the script:
# 1. Open it in blender scripting tab of the blend file
# 2. Set up (Configuration)
# 3. Select the object you want the script to work on
# 4. Press "Run script"
# 5. Check Info panel for script completion/error
# 6. Double check the material TXT file and tweak the shader accordingly if the model still looks wrong
# If there are errors in the Info panel, something in the material file is not applied, something applied wrongly
# etc, double check the material file and the previous state of shader. 
# If the parameter was already set to true by default the script will not set it to false automatically unless
# RESET_PARAMETERS was set to True in configuration 
# If the error reoccurs and it not a user error - message the creator of the script

from pathlib import Path
# Do you want to just launch the script without pasting anything? 
# Use USE_PATHS to launch UI version. Currently support is limited(I don't know if everything is implemented 
# for the base user to understand clearly, but should be good enough for the default setup)
# IMPORTANT: set model_path in this version to the internal path before starting the script
USE_PATHS = True
# model_path - Set this to the internal model location. 
# Example: /Lotus/Characters/Tenno/Nyx/SWAures - Nyx Tennogen skin location
# Set it to the exact internal path. Yes, it begins with /.
model_path = "/Lotus/Objects/Duviri/Props"
# !!!!!!!!
# SET TO FALSE IF USING AS A SCRIPT. THIS IS ONLY FOR ADDON STUFF.
IS_ADDON = True
# (Configuration) - Set these paths before running
# material_file_path - Set this to the path of material TXT file. Yes, including .txt extension.
material_file_path = Path(r"D:\tmp\Assets\Lotus\Objects\Duviri\Props\DominitiusThraxThroneA.txt")
# model_file_path - Set if you use IMPORT_MODEL_MODE
model_file_path = Path(r"D:\tmp\Assets\Lotus\Objects\Duviri\Props\DUVxDominitiusThraxThrone.glb")
# pathToShader - Set this if you use SHADER_APPEND_MODE. 
# Assign it to .blend file of where the materials that need to be appended are. Example is for PBRFillDeferred
pathToShader = r"E:\Download\PBRFillDeferred(5).blend"

# Model Setup
# This section is about model setup. If you just want to setup shader itself - turn both options off
# IMPORT_MODEL_MODE - Set this if you only want to import the model with the correct settings 
# for later use like appending shader and using Shader Setup. If set to True THIS WILL NOT RUN THE SHADER SETUP
IMPORT_MODEL_MODE = False
# SHADER_APPEND_MODE - Set this to append the shader and assign it to the selected object automatically.
# If set to True THIS WILL NOT RUN THE SHADER SETUP.
SHADER_APPEND_MODE = False

# Shader Setup
# Method 1 - Copy all the textures from the material TXT file txt in a separate folder and copy the path to pathToTextures
# pathToTextures - Set this to the path of where ALL the textures from material TXT file are if USE_ROOT_LOCATION is False
pathToTextures = Path(r"E:\UmbraArmorTextures")

# Method 2 - Set the root folder that contains Lotus, EE, etc folders and model path.
# USE_ROOT_LOCATION - Set this to use root folder(folder where Lotus, EE, etc are located instead of pathToTextures. 
# root and model_path locations are required for this to work correctly.
USE_ROOT_LOCATION = True
# root - Set this to the Root file location. Set this to the path where Lotus, EE, etc folders are located
# DO NOT set it to Lotus folder itself, set it to where the root is.
# In the example path folder 1 has Lotus, EE, SF and other folders that have extracted folders/files.
root = Path(r"D:\tmp\Assets") 

# EMPTY_IMAGES_BEFORE_SETUP - Set this to flush images before setup. Might cause errors on first run.
EMPTY_IMAGES_BEFORE_SETUP = True
# REPLACE_IMAGES - Set this to force replace images
REPLACE_IMAGES = True
# RESET_PARAMETERS - Set this to reset all parameters to 0. Does not affect Image Textures.
# Do not use unless you know what you're doing.
RESET_PARAMETERS = False
# texture_extension - Set to the texture extension you're using in *.format style. Examples - *.png, *.dds, *.tga
texture_extension = "*.png"

# shader_exceptions_parameters - These are the parameters that depend on the specific shader number. 
# Useful only on rare occasions, like "Swizzle Vertex Channels" in TerrainFill. 
# Add to this list if the option is not added yet(it likely already was added). 
# Does not differentiate between shaders
shader_exceptions_parameters = [ "Swizzle Vertex Channels" ]
# COMPARING_MODE - set this to also check the shader group name when setting the exceptions.
# Otherwise will assume first shader in shader list is the correct one.
COMPARING_MODE = True



import bpy
import os
import ast
import bmesh
from fnmatch import fnmatch
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, BoolProperty, PointerProperty, EnumProperty
labeled_reroutes = []
texture_locations =[]

def strtobool (val):
    if not isinstance(val, str):
        return val
    if val.lower() in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif ('none') in val.lower() or   val.lower() in ('none', '', 'no', 'false'):
        return False
    else:
        return False


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
        print(input_socket.name)
        print(value)
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
        input_socket.default_value = tuple([0, 0, 0])
    elif input_socket.type == 'RGBA':
        input_socket.default_value = tuple([0, 0, 0, 0])
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
            if "shader" in value.lower():
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

def connect_textures_and_parameters(material, node_group, parameters, textures, pathToTextures, texture_locations):
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
                if(EMPTY_IMAGES_BEFORE_SETUP):
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
                            if((current.image is None) or (REPLACE_IMAGES and current.image.name not in img.name)):
                                current.image = img
                            print(f"Connected texture: {filename}")
                        except Exception as e:
                            print(f"Texture error: {str(e)}")
        # Dunno if needed
        if input_socket.name in parameters:
            value = parameters[input_socket.name]
            set_default(input_socket, value)
        elif(RESET_PARAMETERS):
            reset_default(input_socket)

        for name in parameters:
            if contains(name, input_socket.name) and (input_socket.type == 'BOOLEAN' or input_socket.type == 'COLOR' or input_socket.type == 'VECTOR' or input_socket.type == 'VALUE' or input_socket.type == 'RGBA'):
                value = None
                try:
                    if input_socket.name.endswith('XYZ'):
                        value = parameters[input_socket.name.split(" ")[0].lower()]
                    elif input_socket.name.endswith('X'):
                        value = parameters[input_socket.name.split(" ")[0].lower()][0]
                    elif input_socket.name.endswith('Y'):
                        value = parameters[input_socket.name.split(" ")[0].lower()][1]
                    elif input_socket.name.endswith('Z'):
                        value = parameters[input_socket.name.split(" ")[0].lower()][2]
                    elif input_socket.name.endswith('W') or input_socket.name.endswith('Alpha'):
                        value = parameters[input_socket.name.split(" ")[0].lower()][3]
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
            elif(RESET_PARAMETERS):
                reset_default(input_socket)
        if input_socket.name in shader_exceptions_parameters:
            first_value = next(iter(shader_data.values()))
            if COMPARING_MODE:
                for key in shader_data:
                    if key in node_group.node_tree.name:
                        first_value = shader_data[key]
            for item in labeled_reroutes:
                if item == first_value:
                    set_default(input_socket, True)
                                      
def set_material_properties(material, material_data, pathToTextures, model_path, texture_locations):
    parameters = {}
    textures = {}
    path = model_path if USE_ROOT_LOCATION else str(pathToTextures)
    if(not path.endswith("/")):
        path += "/"
    for key, value in material_data.items():
        if key.startswith('TX:'):
            result = value
            if(not result.endswith(texture_extension.split("*")[1]) and "." in result):
                result = result.split(".")[0] + texture_extension.split("*")[1]
            if(not "/" in result and USE_ROOT_LOCATION):
                result = path + result
            if(not USE_ROOT_LOCATION):
                result = path + result
            textures[key[3:]] = result
        elif ':' in key:
            prefix, param_name = key.split(':', 1)
            parameters[param_name.lower()] = value
        else:
            parameters[key.lower()] = value
    if(USE_ROOT_LOCATION):
        root_loc = str(root)
        if(not str(root).endswith("/")):
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
            elif (not str(Path(root_loc + value)).endswith(texture_extension.split("*")[1])):
                texture_locations[key] = str(Path(root_loc + value + texture_extension.split("*")[1]))
                continue
            texture_locations[key] = str(Path(root_loc + value))
    elif(not USE_ROOT_LOCATION):
        for key, value in textures.items():
            if (not str(Path(str(pathToTextures) + value.split("/")[-1])).endswith(texture_extension.split("*")[1])):
                texture_locations[key] = str(Path(os.path.join(pathToTextures, value.split("/")[-1]) + texture_extension.split("*")[1]))
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
    for node in node_groups:  
        connect_textures_and_parameters(material, node, parameters, textures, pathToTextures, texture_locations)
    
    print(labeled_reroutes)

def get_shader_items(self, context):
    items = []
    if not os.path.exists(pathToShader):
        return items
    with bpy.data.libraries.load(pathToShader, link=False) as (data_from, data_to):
        for mat_name in data_from.materials:
            items.append((mat_name, mat_name, ""))
    return items

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
            bpy.ops.wm.append(
                directory=os.path.join(pathToShader, "Material") + os.sep,
                filename=self.material_name
            )
            self.report({'INFO'}, f"Appended material: {self.material_name}")
            obj = bpy.context.object

            if obj:
                new_material = bpy.data.materials.get(self.material_name)
                
                if new_material:
                    if obj.data.materials and obj.data.materials[0] is not None:
                            original_name = obj.data.materials[0].name
                            new_material.name = original_name 
                            obj.data.materials[0] = new_material
                    else:
                        new_name = f"{obj.data.name}_Material"
                        new_material.name = new_name
                        obj.data.materials.append(new_material)
                        obj.data.materials[0] = new_material
                else:
                    print("Failed to append material")
            else:
                print("No object selected")
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

def menu_func(self, context):
    self.layout.operator(SHADER_OT_append_material.bl_idname)

def register_shader():
    bpy.ops.shader.append_material('INVOKE_DEFAULT')

def unregister_shader():
    bpy.utils.unregister_class(SHADER_OT_append_material)


def process_object(obj):
    if obj.type != 'MESH':
        return
    me = obj.data
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
    if IS_ADDON:
        global model_path, USE_ROOT_LOCATION, EMPTY_IMAGES_BEFORE_SETUP, REPLACE_IMAGES, RESET_PARAMETERS, texture_extension, USE_PATHS, material_file_path, model_file_path, pathToShader, pathToTextures, root
        model_path = bpy.context.scene.warframe_tools_props.model_path
        USE_ROOT_LOCATION = bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION
        EMPTY_IMAGES_BEFORE_SETUP = bpy.context.scene.warframe_tools_props.EMPTY_IMAGES_BEFORE_SETUP
        REPLACE_IMAGES = bpy.context.scene.warframe_tools_props.REPLACE_IMAGES
        RESET_PARAMETERS = bpy.context.scene.warframe_tools_props.RESET_PARAMETERS
        texture_extension = bpy.context.scene.warframe_tools_props.texture_extension
        USE_PATHS = bpy.context.scene.warframe_tools_props.USE_PATHS
        if not USE_PATHS:
            material_file_path = bpy.context.scene.warframe_tools_props.material_file_path
            model_file_path = bpy.context.scene.warframe_tools_props.model_file_path
            pathToShader = bpy.context.scene.warframe_tools_props.pathToShader
        if not USE_ROOT_LOCATION and not USE_PATHS:
            pathToTextures = bpy.context.scene.warframe_tools_props.pathToTextures
        if USE_ROOT_LOCATION and not USE_PATHS:
            root = bpy.context.scene.warframe_tools_props.root
    if IMPORT_MODEL_MODE:
        bpy.ops.import_scene.gltf(
            filepath=str(model_file_path), 
            guess_original_bind_pose=False, 
            bone_heuristic="TEMPERANCE")

        for obj in bpy.context.selected_objects:
            if obj.type != 'MESH':
                continue
            print(obj.data.validate(clean_customdata=True))
            process_object(obj)
            obj.select_set(False)
            print(obj.data.validate(clean_customdata=True))
    elif SHADER_APPEND_MODE:
        register_shader()
    else:
        mat = bpy.context.object.active_material
        if not mat:
            raise Exception("No active material selected")
        labeled_reroutes = []
        texture_locations = {}
        (material_data, shader_data) = parse_material_file(material_file_path)
        set_material_properties(mat, material_data, pathToTextures, model_path, texture_locations)
        
class WM_OT_SetupPaths(bpy.types.Operator):
    bl_idname = "wm.setup_paths"
    bl_label = "Setup Required Paths"
    bl_description = "Select the path to file/folder"
    
    current_step: bpy.props.IntProperty(default=0)
    material_file_path: bpy.props.StringProperty(subtype='FILE_PATH')
    model_file_path: bpy.props.StringProperty(subtype='FILE_PATH')
    pathToShader: bpy.props.StringProperty(subtype='FILE_PATH')
    root: bpy.props.StringProperty(subtype='DIR_PATH')
    pathToTextures: bpy.props.StringProperty(subtype='DIR_PATH')
    
    filter_glob: bpy.props.StringProperty(default="*")
    directory: bpy.props.StringProperty(subtype='DIR_PATH', default=str(Path.home()))
    filepath: bpy.props.StringProperty(subtype='FILE_PATH')

    def determine_steps(self):
        steps = []
        if IS_ADDON:
            global USE_ROOT_LOCATION, EMPTY_IMAGES_BEFORE_SETUP, REPLACE_IMAGES, RESET_PARAMETERS, USE_PATHS
            USE_ROOT_LOCATION = bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION
            EMPTY_IMAGES_BEFORE_SETUP = bpy.context.scene.warframe_tools_props.EMPTY_IMAGES_BEFORE_SETUP
            REPLACE_IMAGES = bpy.context.scene.warframe_tools_props.REPLACE_IMAGES
            RESET_PARAMETERS = bpy.context.scene.warframe_tools_props.RESET_PARAMETERS
            USE_PATHS = bpy.context.scene.warframe_tools_props.USE_PATHS
        if IMPORT_MODEL_MODE:
            steps.append(('model_file_path', 'Select Model File (.glb)', 'file', '*.glb'))
        elif SHADER_APPEND_MODE:
            steps.append(('pathToShader', 'Select Shader Blend File', 'file', '*.blend'))
        else:
            steps.append(('material_file_path', 'Select Material File (.txt)', 'file', '*.txt'))
            if USE_ROOT_LOCATION:
                steps.append(('root', 'Select Root Directory', 'directory', ''))
            else:
                steps.append(('pathToTextures', 'Select Textures Directory', 'directory', ''))
        return steps

    def invoke(self, context, event):
        self.steps = self.determine_steps()
        if not self.steps:
            self.report({'ERROR'}, "No paths required for current mode")
            return {'CANCELLED'}
        self.current_step = 0
        self.filepath = ""
        return self.execute(context)

    def execute(self, context):
        if self.current_step >= len(self.steps):
            global material_file_path, model_file_path, pathToShader, root, pathToTextures
            if self.material_file_path:
                material_file_path = Path(self.material_file_path)
            if self.model_file_path:
                model_file_path = Path(self.model_file_path)
            if self.pathToShader:
                pathToShader = self.pathToShader
            if self.root:
                root = Path(self.root)
            if self.pathToTextures:
                pathToTextures = Path(self.pathToTextures)
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
if IS_ADDON:
    class WarframeAutoPorter(bpy.types.AddonPreferences):
        # This must match the add-on name, use `__package__`
        # when defining this for add-on extensions or a sub-module of a python package.
        bl_idname = __name__

        root_preference: StringProperty(
            name="Extracted Root Folder Path",
            subtype='FILE_PATH'
        )
        texture_extension_preference: EnumProperty(
            name="Texture Extension",
            description="Choose the texture file extension",
            items=[
            ('*.png', 'PNG', 'Use PNG textures'),
            ('*.tga', 'TGA', 'Use TGA textures'),
            ('*.dds', 'DDS', 'Use DDS textures'),
            ],
            default='*.png'
        )
        def draw(self, context):
            layout = self.layout
            layout.label(text="Warning! Changing these in the panel will change the preferences!")
            layout.label(text="Path to the folder where Lotus, EE, DOS, SF and other folders are located.")
            layout.label(text=r"DO NOT CHOOSE LOTUS FOLDER (example, D:\tmp\Assets)")
            layout.prop(self, "root_preference")
            layout.label(text="Default extracted texture extension.")
            layout.prop(self, "texture_extension_preference")
    def get_root_value(self):
        return bpy.context.preferences.addons[__name__].preferences.root_preference

    def set_root_value(self, value):
        bpy.context.preferences.addons[__name__].preferences.root_preference = value  
            
    def get_ext_value(self):
        val = bpy.context.preferences.addons[__name__].preferences.texture_extension_preference
        data = [
            ('*.png', 'PNG', 'Use PNG textures'),
            ('*.tga', 'TGA', 'Use TGA textures'),
            ('*.dds', 'DDS', 'Use DDS textures'),
            ]
        index = next((i for i, (first, *_) in enumerate(data) if first == val), None)
        return index

    def set_ext_value(self, value):
        available = [
            ('*.png', 'PNG', 'Use PNG textures'),
            ('*.tga', 'TGA', 'Use TGA textures'),
            ('*.dds', 'DDS', 'Use DDS textures'),
            ]
        bpy.context.preferences.addons[__name__].preferences.texture_extension_preference = available[value][0]      
    class OBJECT_OT_addon_prefs_example(bpy.types.Operator):
        """Display example preferences"""
        bl_idname = "object.addon_prefs_example"
        bl_label = "Add-on Preferences Example"
        bl_options = {'REGISTER', 'UNDO'}

        def execute(self, context):
            preferences = context.preferences
            addon_prefs = preferences.addons[__name__].preferences

            return {'FINISHED'}
    
    class WarframeAddonProperties(bpy.types.PropertyGroup):
        def update_ui(self, context):
            if context and not context.area.as_pointer() == context.window_manager.filebrowser.as_pointer():
                for area in context.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()

        model_path: StringProperty(
        name="Internal Path",
        description="Internal model path (e.g., /Lotus/Objects/Duviri/Props)",
        default="/Lotus/Objects/Duviri/Props"
    )
        USE_ROOT_LOCATION: BoolProperty(
        name="Use Root Location",
        description="Determines paths from mat file using root location",
        default=True,
        update=update_ui
    )
        USE_PATHS: BoolProperty(
        name="Enable automatic paths",
        description="If deselected - new fields with required paths will appear",
        default=True,
        update=update_ui
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
        description="Sets values that do not exist in the mat txt file to 0, black, etc. DO NOT USE UNLESS YOU KNOW WHAT YOU'RE DOING",
        default=False
    )
        texture_extension: EnumProperty(
        name="Texture Extension",
        description="Choose the texture file extension",
        items=[
        ('*.png', 'PNG', 'Use PNG textures'),
        ('*.tga', 'TGA', 'Use TGA textures'),
        ('*.dds', 'DDS', 'Use DDS textures'),
        ],
        get=get_ext_value,
        set=set_ext_value
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
        subtype='FILE_PATH',
        get=get_root_value,
        set=set_root_value
    )
        mode: EnumProperty(
        name="Mode",
        items=[
            ('IMPORT', "Import Model Mode", "Import the model from a file"),
            ('APPEND', "Shader Append Mode", "Append the shader from a blend file"),
            ('SHADER', "Shader Setup Mode", "Set up the shader parameters and textures"),
        ],
        default='SHADER',
        update=update_ui
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
            global IMPORT_MODEL_MODE, SHADER_APPEND_MODE, USE_PATHS
            if IS_ADDON:
                USE_PATHS = props.USE_PATHS
            if props.mode == 'IMPORT':
                IMPORT_MODEL_MODE = True
                SHADER_APPEND_MODE = False
            elif props.mode == 'APPEND':
                IMPORT_MODEL_MODE = False
                SHADER_APPEND_MODE = True
            else:
                IMPORT_MODEL_MODE = False
                SHADER_APPEND_MODE = False
            box = layout.box()
            box.label(text="Configuration")
            box.label(text="Select Mode:")
            box.prop(props, "mode")
            box.prop(props, "USE_PATHS")
            if IMPORT_MODEL_MODE:
                if not props.USE_PATHS: 
                    box.prop(props, "model_file_path")
                layout.operator("wm.run_setup", text="Import Model")
                return
            if SHADER_APPEND_MODE:
                if not props.USE_PATHS: 
                    box.prop(props, "pathToShader")
                layout.operator("wm.run_setup", text="Append Shader")
                return
            if not (IMPORT_MODEL_MODE or SHADER_APPEND_MODE):
                box.prop(props, "model_path")
                if not props.USE_PATHS: 
                    box.prop(props, "material_file_path")
                box.prop(props, "USE_ROOT_LOCATION")
                if not props.USE_PATHS and not props.USE_ROOT_LOCATION: box.prop(props, "pathToTextures")
                elif not props.USE_PATHS and props.USE_ROOT_LOCATION: box.prop(props, "root") 
                box.prop(props, "EMPTY_IMAGES_BEFORE_SETUP")
                box.prop(props, "REPLACE_IMAGES")
                box.prop(props, "RESET_PARAMETERS")
                box.prop(props, "texture_extension")
            layout.operator("wm.run_setup", text="Run Setup")

    class WM_OT_RunSetup(bpy.types.Operator):
        bl_idname = "wm.run_setup"
        bl_label = "Run Setup"

        def execute(self, context):
            global IMPORT_MODEL_MODE, SHADER_APPEND_MODE, USE_PATHS
            if IS_ADDON:
                USE_PATHS = bpy.context.scene.warframe_tools_props.USE_PATHS
            mode = context.scene.warframe_tools_props.mode
            if mode == 'IMPORT':
                IMPORT_MODEL_MODE = True
                SHADER_APPEND_MODE = False
            elif mode == 'APPEND':
                IMPORT_MODEL_MODE = False
                SHADER_APPEND_MODE = True
            else:
                IMPORT_MODEL_MODE = False
                SHADER_APPEND_MODE = False

            if USE_PATHS:
                bpy.ops.wm.setup_paths('INVOKE_DEFAULT')
            else:
                run_setup()
                self.report({'INFO'}, "Setup Completed Successfully!")
            return {'FINISHED'}
def register():
    bpy.utils.register_class(WarframeAutoPorter)
    bpy.utils.register_class(WARFRAME_PT_SetupPanel)
    bpy.utils.register_class(WM_OT_RunSetup)
    bpy.utils.register_class(WM_OT_SetupPaths)
    bpy.utils.register_class(SHADER_OT_append_material)
    bpy.utils.register_class(WarframeAddonProperties)
    bpy.types.Scene.warframe_tools_props = PointerProperty(type=WarframeAddonProperties)
    bpy.context.preferences.use_preferences_save = True

def unregister():
    bpy.utils.unregister_class(WARFRAME_PT_SetupPanel)
    bpy.utils.unregister_class(WM_OT_RunSetup)
    bpy.utils.unregister_class(WM_OT_SetupPaths)
    bpy.utils.unregister_class(SHADER_OT_append_material)
    bpy.utils.unregister_class(WarframeAddonProperties) 
    bpy.utils.unregister_class(WarframeAutoPorter)  
    del bpy.types.Scene.warframe_tools_props
if __name__ == "__main__":
    if IS_ADDON:
        register()
    else:
        bpy.utils.register_class(SHADER_OT_append_material)
        bpy.utils.register_class(WM_OT_SelectMode)
        bpy.utils.register_class(WM_OT_SetupPaths)
        bpy.ops.wm.select_mode('INVOKE_DEFAULT')