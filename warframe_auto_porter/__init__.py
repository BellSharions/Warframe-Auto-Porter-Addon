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

from .constants import COLOR_SPACE_MAP, EMISSION_FLAGS_FOR_BAKING
from .utils import extract_texture_with_cli, extract_material_with_cli, find_shader_material, get_best_material_from_blend, strtobool, get_color_space, find_internal_path, find_internal_texture_path, contains, containstexture, set_default, reset_default, parse_material_file
from .material_processing import connect_textures_and_parameters, set_material_properties, get_shader_items, get_rig_items
from .operators import BakeState, setup_bake, cleanup_bake, CreateBakedMaterialOperator, BakeTexturesOperator, NormalToHeightOperator, SubDivisionOperator, DeformOperator, RunAllOperationsOperator, AppendMaterialOperator, AppendRigOperator, ImportModelOperator, SetupShaderOperator, RunSetupOperator, SetupPathsOperator, ExperimentalModeOperator
from .preferences import WarframeAutoPorter
from .properties import BakeSourceItem, WarframeAddonProperties
from .panel import SetupPanelOperator

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
    CreateBakedMaterialOperator
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
