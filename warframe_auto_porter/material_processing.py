import bpy
import os
from pathlib import Path

from .utils import set_default, reset_default, containstexture, find_internal_texture_path, extract_texture_with_cli
from .constants import special_ignores, special_skips


def connect_geometry_node_parameters(node_group_map, parameters, shader_data_filtered):
    for param_name, param_value in (parameters | shader_data_filtered).items():
        print(param_name)
        if param_name.lower() in node_group_map:
            ng = node_group_map[param_name.lower()]

            existing_mod = None
            for mod in bpy.context.active_object.modifiers:
                if mod.type == 'NODES' and mod.node_group == ng:
                    existing_mod = mod
                    break

            if existing_mod is None:
                mod = bpy.context.active_object.modifiers.new(name=ng.name, type='NODES')
                mod.node_group = ng
            else:
                mod = existing_mod
                print(f"Using existing geometry node modifier: {ng.name}")

            should_reset = bpy.context.scene.warframe_tools_props.RESET_PARAMETERS
            for item in ng.interface.items_tree:
                if item.item_type == 'SOCKET' and item.in_out == 'INPUT':
                    socket_name = item.name
                    socket_name_lower = socket_name.lower()
                    socket_type = item.bl_socket_idname

                    try:
                        value = None
                        found_match = False

                        lookup_name = socket_name_lower
                        print(lookup_name)
                        print(special_skips)
                        if any(value in lookup_name for value in special_skips):
                            continue

                        if '/' in socket_name:
                            base_name, second_part = socket_name.split("/", 1)
                            base_name_lower = base_name.lower()
                            second_part_lower = second_part.lower()

                            for part in [base_name_lower, second_part_lower]:
                                if part in parameters:
                                    value = parameters[part]
                                    found_match = True
                                    break

                        if not found_match and any(socket_name.endswith(x) for x in ('XYZ', 'X', 'Y', 'Z', 'W', 'Alpha')):
                            base_name = socket_name.split(" ")[0].lower()
                            if base_name in parameters:
                                param_val = parameters[base_name]

                                if socket_name.endswith('XYZ'):
                                    value = param_val
                                elif socket_name.endswith('X'):
                                    value = param_val if isinstance(param_val, (int, float)) else param_val[0]
                                elif socket_name.endswith('Y'):
                                    value = param_val if isinstance(param_val, (int, float)) else param_val[1]
                                elif socket_name.endswith('Z'):
                                    value = param_val if isinstance(param_val, (int, float)) else param_val[2]
                                elif socket_name.endswith(('W', 'Alpha')):
                                    value = param_val if isinstance(param_val, (int, float)) else param_val[3]
                                found_match = True

                        if not found_match:
                            if lookup_name in parameters:
                                value = parameters[lookup_name]
                                found_match = True

                        if not found_match:
                            if socket_name_lower.endswith("= none"):
                                lookup_name = socket_name_lower
                            elif '=' in socket_name_lower:
                                lookup_name = socket_name_lower
                            else:
                                lookup_name = socket_name.split(" ")[0].lower()

                            if lookup_name in parameters:
                                value = parameters[lookup_name]
                                found_match = True

                        if found_match:
                            if socket_type == 'NodeSocketBool':
                                value = bool(value)
                            elif socket_type == 'NodeSocketInt':
                                value = int(value) if isinstance(value, (int, float)) else value
                            elif socket_type == 'NodeSocketFloat':
                                value = float(value) if isinstance(value, (int, float)) else value
                            elif socket_type == 'NodeSocketVector':
                                if isinstance(value, (list, tuple)) and len(value) >= 3:
                                    value = tuple(float(v) for v in value[:3])
                                else:
                                    value = (float(value), float(value), float(value))

                            mod[item.identifier] = value
                            print(f"Setting geometry node parameter: {socket_name} = {value}")
                        elif should_reset:
                            if socket_type == 'NodeSocketBool':
                                mod[item.identifier] = False
                            elif socket_type in ('NodeSocketInt', 'NodeSocketFloat'):
                                mod[item.identifier] = 0
                            elif socket_type == 'NodeSocketVector':
                                mod[item.identifier] = (0.0, 0.0, 0.0)

                    except Exception as e:
                        print(f"Exception processing geometry node {socket_name}: {str(e)}")


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
                                if(img_tex.name == name):
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
                    print(lookup_name)
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
                    print(lookup_name)
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

    print(node_groups_for_gn)
    node_group_map = {}
    for ng in node_groups_for_gn:
        base_name = ng.name[4:].split(maxsplit=1)[0]
        node_group_map[base_name.lower()] = ng
    print(node_group_map)
    print(shader_data)
    shader_data_filtered = {}
    for shader_path in shader_data:
        path_parts = shader_path.split('/')
        if len(path_parts) >= 2:
            main_shader_name = path_parts[-2]
            shader_data_filtered[main_shader_name] = shader_data[shader_path]

    connect_geometry_node_parameters(node_group_map, parameters, shader_data_filtered)
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
