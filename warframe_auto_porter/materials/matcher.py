import os
import re

import bpy


def find_shader_material(shader_name, shader_library_path):
    shader_files = {}
    for f in os.listdir(shader_library_path):
        if f.endswith(".blend"):
            shader_files[f.lower()] = f

    target_file = f"{shader_name}.blend"
    if target_file in shader_files:
        original_filename = shader_files[target_file.lower()]
        return os.path.join(shader_library_path, original_filename), None

    for original_filename in shader_files.values():
        if shader_name.lower() in original_filename.lower():
            return os.path.join(shader_library_path, original_filename), None

    return None, f"No shader file found for {shader_name}"


def _should_exclude_material(mat_name):
    mat_lower = mat_name.lower()
    if re.search(r"\bstroke\b", mat_lower):
        return True
    if re.search(r"\bdev\b", mat_lower):
        return True
    return False


def get_best_material_from_blend(blend_path, params):
    materials = []
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        for mat_name in data_from.materials:
            if not _should_exclude_material(mat_name):
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


def get_shader_items(self, context):
    items = []
    if not os.path.exists(bpy.context.scene.warframe_tools_props.pathToShader):
        return items
    with bpy.data.libraries.load(
        bpy.context.scene.warframe_tools_props.pathToShader, link=False
    ) as (data_from, data_to):
        for mat_name in data_from.materials:
            if "dots stroke" not in mat_name.lower():
                items.append((mat_name, mat_name, ""))
    return items


def get_rig_items(self, context):
    items = []
    if not os.path.exists(bpy.context.scene.warframe_tools_props.rig_path):
        return items
    with bpy.data.libraries.load(bpy.context.scene.warframe_tools_props.rig_path, link=False) as (
        data_from,
        data_to,
    ):
        for rig_name in data_from.collections:
            print(rig_name)
            if "meta" not in rig_name.lower() and "wgts" not in rig_name.lower():
                items.append((rig_name, rig_name, ""))
    return items
