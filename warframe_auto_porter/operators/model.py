import os
import time

import bpy

from ..materials.matcher import find_shader_material, get_best_material_from_blend
from ..materials.parser import parse_material_file
from ..materials.processor import set_material_properties
from ..utils.extraction import extract_material_with_cli
from ..utils.object_utils import process_object
from ..utils.path_utils import find_internal_path
from ..utils.texture_cleanup import cleanup_textures


class ImportModelOperator(bpy.types.Operator):
    bl_idname = "wm.import_model"
    bl_label = "Import Model"
    bl_description = "Import and process Warframe model"

    def execute(self, context):
        props = context.scene.warframe_tools_props
        bpy.ops.import_scene.gltf(
            filepath=str(bpy.context.scene.warframe_tools_props.model_file_path),
            guess_original_bind_pose=False,
            bone_heuristic="TEMPERANCE",
        )
        collections_dict = {}
        for obj in bpy.context.selected_objects:
            if obj.type != "MESH":
                continue
            # Credit: KptWeedy
            if bpy.context.scene.warframe_tools_props.LEVEL_IMPORT:
                print(obj.data.validate(clean_customdata=True))
                if len(obj.material_slots) > 0 and obj.material_slots[
                    0
                ].material.name.lower().startswith("hidden"):
                    obj.hide_render = True
                    obj.hide_viewport = True
                    continue
                material_name = ""
                if len(obj.material_slots) > 0 and obj.material_slots[0].material:
                    material_name = obj.material_slots[0].material.name
                    bpy.data.materials[material_name].use_fake_user = True
                    print(f"Processing material: {material_name}")

                if material_name:
                    if material_name not in collections_dict:
                        new_collection = bpy.data.collections.new(material_name)
                        bpy.context.scene.collection.children.link(new_collection)
                        collections_dict[material_name] = new_collection
                    else:
                        new_collection = collections_dict[material_name]

                    for collection in obj.users_collection:
                        collection.objects.unlink(obj)
                    new_collection.objects.link(obj)
            process_object(obj)
        collections_dict = {}

        self.report({"INFO"}, "Model imported successfully")
        return {"FINISHED"}


class ExperimentalModeOperator(bpy.types.Operator):
    bl_idname = "wm.experimental_mode"
    bl_label = "Auto Setup Mode"
    bl_description = "Import model and auto-setup materials from MaterialPath"

    def execute(self, context):

        start_time = time.time()
        props = context.scene.warframe_tools_props
        set_up_mats = []
        bpy.ops.wm.import_model("EXEC_DEFAULT")

        for obj in context.selected_objects:
            if obj.type != "MESH":
                continue
            if obj.data.materials[0].name.split(".")[0] in set_up_mats:
                continue
            material_path = obj.data.materials[0].get("FullPath")
            if not material_path:
                set_up_mats.append(obj.data.materials[0].name.split(".")[0])
                self.report({"WARNING"}, f"Object {obj.name} has no FullPath custom property")
                continue

            internal_path = find_internal_path(material_path)  # возможно не надо
            material_file_path = os.path.join(props.root, internal_path) + ".txt"

            if not os.path.exists(material_file_path):
                if props.USE_EXTRACTOR:
                    success = extract_material_with_cli(
                        props.extractor_path, props.cache_path, internal_path, props.root
                    )
                    if not success:
                        self.report({"ERROR"}, f"Failed to extract material: {internal_path}")
                        set_up_mats.append(obj.data.materials[0].name.split(".")[0])
                        continue
                else:
                    self.report({"WARNING"}, f"Material file not found: {material_file_path}")
                    set_up_mats.append(obj.data.materials[0].name.split(".")[0])
                    continue

            try:
                material_data, shader_data, hierarchy_data = parse_material_file(material_file_path)
            except Exception as e:
                self.report({"ERROR"}, f"Failed to parse material file: {e!s}")
                set_up_mats.append(obj.data.materials[0].name.split(".")[0])
                continue

            shader_name = None
            for key in shader_data:
                if isinstance(key, str) and "_p.hlsl" in key:
                    shader_name = key.split("_p.hlsl")[0].split("/")[-2]
                    break

            if not shader_name:
                self.report({"WARNING"}, f"No shader found in material file: {material_file_path}")
                set_up_mats.append(obj.data.materials[0].name.split(".")[0])
                continue
            print(f"Found shader name: {shader_name}")
            shader_blend_path, error = find_shader_material(shader_name, props.shader_library_path)
            if error:
                self.report({"WARNING"}, error)
                set_up_mats.append(obj.data.materials[0].name.split(".")[0])
                continue

            print(f"Found shader: {shader_blend_path}")
            material_name = get_best_material_from_blend(shader_blend_path, material_data, shader_name)
            if not material_name:
                self.report({"ERROR"}, f"No suitable material found in {shader_blend_path}")
                set_up_mats.append(obj.data.materials[0].name.split(".")[0])
                continue
            print(f"Chosen material: {material_name}")
            original_base_name = None
            if obj and obj.data and hasattr(obj.data, "materials") and obj.data.materials:
                if obj.data.materials[0]:
                    original_base_name = obj.data.materials[0].name.split(".")[0]

            before = set(bpy.data.materials.keys())

            before_images = set(bpy.data.images.keys())
            bpy.ops.wm.append(
                directory=os.path.join(shader_blend_path, "Material") + os.sep,
                filename=material_name,
                do_reuse_local_id=False,
            )
            after = set(bpy.data.materials.keys())
            new_material_names = after - before

            if not new_material_names:
                self.report({"ERROR"}, "Failed to append material")
                set_up_mats.append(obj.data.materials[0].name.split(".")[0])
                continue

            new_material = bpy.data.materials[list(new_material_names)[0]]
            self.report({"INFO"}, f"Appended material: {material_name}")

            after_images = set(bpy.data.images.keys())
            new_image_names = after_images - before_images

            cleanup_textures(self, new_material, new_image_names)  # change
            gn_node_groups = []
            try:
                with bpy.data.libraries.load(
                    context.scene.warframe_tools_props.pathToShader, link=False
                ) as (data_from, data_to):
                    gn_node_groups = [
                        name
                        for name in data_from.node_groups
                        if name.startswith("Gn") and name not in data_to.node_groups
                    ]
            except Exception as e:
                self.report({"WARNING"}, f"Could not read node groups: {e!s}")

            for node_group_name in gn_node_groups:
                if node_group_name not in bpy.data.node_groups:
                    try:
                        bpy.ops.wm.append(
                            directory=os.path.join(
                                context.scene.warframe_tools_props.pathToShader, "NodeTree"
                            )
                            + os.sep,
                            filename=node_group_name,
                            do_reuse_local_id=True,
                        )
                        self.report({"INFO"}, f"Appended node group: {node_group_name}")
                    except Exception as e:
                        self.report(
                            {"WARNING"}, f"Failed to append node group {node_group_name}: {e!s}"
                        )

            if original_base_name:
                old_materials = [
                    mat
                    for mat in bpy.data.materials
                    if mat.name.startswith(original_base_name + ".")
                    or mat.name == original_base_name
                ]

                for old_mat in old_materials:
                    old_mat.user_remap(new_material)

                for old_mat in old_materials:
                    if old_mat.users == 0 and old_mat != new_material:
                        bpy.data.materials.remove(old_mat)

                new_material.name = original_base_name
            else:
                if obj and obj.data:
                    new_name = f"{obj.data.name}_Material"
                    new_material.name = new_name

                    if not obj.data.materials:
                        obj.data.materials.append(new_material)
                    else:
                        obj.data.materials[0] = new_material

            texture_locations = {}

            model_path = find_internal_path(material_file_path)
            set_material_properties(
                new_material,
                material_data,
                props.pathToTextures,
                model_path,
                texture_locations,
                shader_data,
                hierarchy_data,
            )

            set_up_mats.append(obj.data.materials[0].name.split(".")[0])

            end_time = time.time()
            elapsed_time = end_time - start_time
            minutes, seconds = divmod(elapsed_time, 60)

            self.report({"INFO"}, f"Setup completed in {int(minutes)}m {seconds:.2f}s")
            self.report({"INFO"}, f"Set up material for {obj.name}")

        return {"FINISHED"}
