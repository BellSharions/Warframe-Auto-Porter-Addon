import bpy
from bpy.props import StringProperty, EnumProperty

from .constants import texture_extension_list


class WarframeAutoPorter(bpy.types.AddonPreferences):
    # This must match the add-on name, use `__package__`
    # when defining this for add-on extensions or a sub-module of a python package.
    bl_idname = __package__

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
