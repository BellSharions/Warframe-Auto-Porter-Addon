import re
import ast
from collections import OrderedDict

from ..constants import special_aliases, texture_ignores


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
