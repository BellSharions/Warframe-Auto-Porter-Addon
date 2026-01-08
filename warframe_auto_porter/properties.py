import bpy
from bpy.props import StringProperty, BoolProperty, PointerProperty, EnumProperty, IntProperty, CollectionProperty

from .constants import texture_extension_list


def get_root_value(self):
    return bpy.context.preferences.addons[__package__].preferences.root_preference


def set_root_value(self, value):
    bpy.context.preferences.addons[__package__].preferences.root_preference = value


def get_rig_value(self):
    return bpy.context.preferences.addons[__package__].preferences.rig_preference


def set_rig_value(self, value):
    bpy.context.preferences.addons[__package__].preferences.rig_preference = value


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
    val = bpy.context.preferences.addons[__package__].preferences.texture_extension_preference
    index = next((i for i, (first, *_) in enumerate(texture_extension_list) if first == val), None)
    return index


def set_ext_value(self, value):
    bpy.context.preferences.addons[__package__].preferences.texture_extension_preference = texture_extension_list[value][0]


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
    bake_all_material_users: BoolProperty(
        name="Bake All Material Users",
        description="When enabled, bake textures for all objects using the same material instead of just the active object",
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
        description="Choose what to do",
        items=[
            ('IMPORT', 'Import Model', 'Import model from file'),
            ('APPEND', 'Append Shader', 'Append shader from file'),
            ('SHADER', 'Setup Shader', 'Setup shader with material file'),
            ('EXPERIMENTAL', 'Experimental', 'Experimental mode'),
            ('RIG', 'Append Rig', 'Append rig from file'),
            ('BAKE', 'Bake Textures', 'Bake textures from active material'),
            ('3DPRINT', '3D Print', '3D Print operations'),
        ],
        default='IMPORT'
    )
