import subprocess
import os
import re
import ast
from pathlib import Path
from collections import OrderedDict
import bpy

from .constants import (
    extractor_commands, COLOR_SPACE_MAP, special_reset_rules,
    special_aliases, texture_ignores
)


def extract_texture_with_cli(extractor_path, cache_path, texture_format, internal_path, output_dir):
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


def strtobool(val):
    if not isinstance(val, str):
        return val
    if val.lower() in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif ('none') in val.lower() or val.lower() in ('none', '', 'no', 'false'):
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
