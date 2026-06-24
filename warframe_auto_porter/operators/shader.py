import bpy
import os

from ..materials.matcher import get_shader_items
from ..materials.parser import parse_material_file
from ..materials.processor import set_material_properties
from ..utils.path_utils import find_internal_path
from ..utils.texture_cleanup import cleanup_textures


class AppendMaterialOperator(bpy.types.Operator):
    bl_idname = "shader.append_material"
    bl_label = "Append Shader"
    bl_description = "Append material from shader library"
    bl_property = "material_name"
    bl_options = {'REGISTER', 'UNDO'}

    material_name: bpy.props.EnumProperty(
        name="Materials",
        description="Available materials",
        items=get_shader_items,
    )

    def execute(self, context):
        if not self.material_name:
            return {'CANCELLED'}

        try:
            for obj in context.selected_objects:
                original_base_name = None
                if obj and obj.data and hasattr(obj.data, 'materials') and obj.data.materials:
                    if obj.data.materials[0]:
                        original_base_name = obj.data.materials[0].name.split('.')[0]

                before = set(bpy.data.materials.keys())

                before_images = set(bpy.data.images.keys())
                print(os.path.join(context.scene.warframe_tools_props.pathToShader, "Material") + os.sep)
                print(self.material_name)
                bpy.ops.wm.append(
                    directory=os.path.join(context.scene.warframe_tools_props.pathToShader, "Material") + os.sep,
                    filename=self.material_name,
                    do_reuse_local_id=False
                )
                after = set(bpy.data.materials.keys())
                new_material_names = after - before

                if not new_material_names:
                    self.report({'ERROR'}, "Failed to append material")
                    return {'CANCELLED'}

                new_material = bpy.data.materials[list(new_material_names)[0]]
                self.report({'INFO'}, f"Appended material: {self.material_name}")

                after_images = set(bpy.data.images.keys())
                new_image_names = after_images - before_images

                cleanup_textures(self, new_material, new_image_names)
                gn_node_groups = []
                try:
                    with bpy.data.libraries.load(context.scene.warframe_tools_props.pathToShader, link=False) as (data_from, data_to):
                        gn_node_groups = [name for name in data_from.node_groups if name.startswith("Gn")]
                except Exception as e:
                    self.report({'WARNING'}, f"Could not read node groups: {str(e)}")

                for node_group_name in gn_node_groups:
                    if node_group_name not in bpy.data.node_groups:
                        try:
                            bpy.ops.wm.append(
                                directory=os.path.join(context.scene.warframe_tools_props.pathToShader, "NodeTree") + os.sep,
                                filename=node_group_name,
                                do_reuse_local_id=True
                            )
                            self.report({'INFO'}, f"Appended node group: {node_group_name}")
                        except Exception as e:
                            self.report({'WARNING'}, f"Failed to append node group {node_group_name}: {str(e)}")

                if original_base_name:
                    old_materials = [mat for mat in bpy.data.materials
                                    if mat.name.startswith(original_base_name + '.') or
                                    mat.name == original_base_name]

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

        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select Material to Append")
        layout.prop(self, "material_name", text="")
        layout.separator()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)


class SetupShaderOperator(bpy.types.Operator):
    bl_idname = "wm.setup_shader"
    bl_label = "Setup Shader"
    bl_description = "Configure material with textures and parameters"

    def execute(self, context):
        props = context.scene.warframe_tools_props
        mat = context.object.active_material
        if not mat:
            self.report({'ERROR'}, "No active material selected")
            return {'CANCELLED'}

        texture_locations = {}
        material_data, shader_data, hierarchy_data = parse_material_file(props.material_file_path)
        model_path = find_internal_path(props.material_file_path)

        set_material_properties(mat, material_data, props.pathToTextures, model_path, texture_locations, shader_data, hierarchy_data)
        self.report({'INFO'}, "Shader setup completed")
        return {'FINISHED'}
