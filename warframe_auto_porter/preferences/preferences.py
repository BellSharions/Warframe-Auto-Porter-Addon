import bpy
from bpy.props import StringProperty, EnumProperty

from ..constants import texture_extension_list


class WarframeAutoPorter(bpy.types.AddonPreferences):
    bl_idname = __package__.rpartition('.')[0]

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
    extractor_path_preference: StringProperty(
        name="Extractor CLI Path",
        description=r"Path to the CLI Extractor to use.",
        subtype='FILE_PATH',
        default=""
    )
    cache_path_preference: StringProperty(
        name="Cache Folder Path",
        description=r"Path to the warframe cache folder (e.g., D:\Warframe\Cache.Windows)",
        subtype='DIR_PATH',
        default=""
    )
    shader_library_path_preference: StringProperty(
        name="Shader Library Path",
        description="Path to the folder containing .blend files with shaders",
        subtype='DIR_PATH',
        default=""
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
        layout.separator()
        layout.label(text="Extractor CLI path (for auto-extraction of textures/materials)")
        layout.prop(self, "extractor_path_preference")
        layout.label(text="Warframe cache folder (e.g., D:\\Warframe\\Cache.Windows)")
        layout.prop(self, "cache_path_preference")
        layout.label(text="Folder containing .blend shader files")
        layout.prop(self, "shader_library_path_preference")
