bl_info = {
    "name": "Warframe Auto Porter",
    "author": "Bell Sharions",
    "version": (0, 50, 21),
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


import ast
import math
import os
import re
import time
import traceback
from collections import OrderedDict
from fnmatch import fnmatch
from pathlib import Path

import bmesh
import bpy
import numpy as np
from bpy.app.handlers import persistent
from bpy.props import (
    BoolProperty,
    CollectionProperty,
    EnumProperty,
    IntProperty,
    PointerProperty,
    StringProperty,
)
from bpy.types import AddonPreferences, Macro, Operator, PropertyGroup

from .constants import COLOR_SPACE_MAP, EMISSION_FLAGS_FOR_BAKING
from .materials import (
    connect_geometry_node_parameters,
    connect_textures_and_parameters,
    find_shader_material,
    get_best_material_from_blend,
    get_rig_items,
    get_shader_items,
    parse_material_file,
    set_material_properties,
)
from .operators import (
    AppendMaterialOperator,
    AppendRigOperator,
    BakeState,
    BakeTexturesOperator,
    CreateBakedMaterialOperator,
    DeformOperator,
    ExperimentalModeOperator,
    ImportModelOperator,
    NormalToHeightOperator,
    RunAllOperationsOperator,
    RunSetupOperator,
    SetupPathsOperator,
    SetupShaderOperator,
    SubDivisionOperator,
    cleanup_bake,
    setup_bake,
)
from .preferences import WarframeAutoPorter
from .properties import BakeSourceItem, WarframeAddonProperties
from .ui import SetupPanelOperator
from .utils import (
    cleanup_textures,
    contains,
    containstexture,
    extract_material_with_cli,
    extract_texture_with_cli,
    find_internal_path,
    find_internal_texture_path,
    get_color_space,
    process_object,
    reset_default,
    set_default,
    strtobool,
)

classes = (
    WarframeAutoPorter,
    SetupPanelOperator,
    RunSetupOperator,
    SetupShaderOperator,
    ImportModelOperator,
    ExperimentalModeOperator,
    SetupPathsOperator,
    AppendMaterialOperator,
    NormalToHeightOperator,
    SubDivisionOperator,
    DeformOperator,
    RunAllOperationsOperator,
    AppendRigOperator,
    WarframeAddonProperties,
    BakeTexturesOperator,
    CreateBakedMaterialOperator,
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
