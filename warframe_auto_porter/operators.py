import bpy
import os
import time
import math
import numpy as np
from pathlib import Path

from .utils import (
    extract_texture_with_cli, extract_material_with_cli, find_internal_path,
    find_internal_texture_path, parse_material_file,
    get_best_material_from_blend, find_shader_material, process_object
)
from .material_processing import set_material_properties, get_shader_items, get_rig_items, connect_textures_and_parameters
from .constants import EMISSION_FLAGS_FOR_BAKING


class BakeState:
    """Storage for bake operation state"""
    def __init__(self, material, output_node, orig_socket, image_node, source_socket, renderer_state):
        self.material = material
        self.output_node = output_node
        self.orig_socket = orig_socket
        self.image_node = image_node
        self.source_socket = source_socket
        self.renderer_state = renderer_state


def setup_bake(context, source):
    """Prepare baking for a specific source"""
    material = context.active_object.active_material
    node_tree = material.node_tree

    output_node = next((n for n in node_tree.nodes if n.type == 'OUTPUT_MATERIAL'), None)
    if not output_node:
        raise Exception("Material Output node not found")
    orig_socket = None
    if output_node.inputs['Surface'].is_linked:
        orig_socket = output_node.inputs['Surface'].links[0].from_socket
    source_socket = None
    fallback_socket = None
    for node in node_tree.nodes:
        if node.type in {'GROUP', 'GROUP_OUTPUT'}:
            for output in node.outputs:
                if source in output.name:
                    fallback_socket = output
                    if source == "Normal" and "final" in getattr(node.node_tree, 'name', '').lower():
                        continue
                    source_socket = output
                    break
            if source == "Emission":
                for input in node.inputs:
                    if input.name.lower() in EMISSION_FLAGS_FOR_BAKING:
                        input.default_value = False
                        break
        if source_socket:
            break

    if not source_socket and fallback_socket:
        source_socket = fallback_socket
    if not source_socket:
        raise Exception(f"Output socket '{source}' not found")
    bake_all_users = context.scene.warframe_tools_props.bake_all_material_users
    image_name = f"{material.name}_{source.replace(' ', '')}"
    image = bpy.data.images.get(image_name)
    if image is None:
        image = bpy.data.images.new(image_name, *(bpy.context.scene.warframe_tools_props.bake_width, bpy.context.scene.warframe_tools_props.bake_height))
        image.colorspace_settings.name = 'sRGB' if source in ['Base Color', 'Emission'] else 'Non-Color'
    elif bake_all_users:
        pass

    image_node = None
    for node in node_tree.nodes:
        if node.type == 'TEX_IMAGE' and node.image and node.image.name == image_name:
            image_node = node
            break

    if image_node is None:
        image_node = node_tree.nodes.new('ShaderNodeTexImage')
        image_node.location = (output_node.location.x - 300, output_node.location.y + 500)

    image_node.image = image

    if output_node.inputs['Surface'].is_linked:
        for link in output_node.inputs['Surface'].links:
            node_tree.links.remove(link)
    node_tree.links.new(source_socket, output_node.inputs['Surface'])

    renderer_state = {}
    renderer_state["margin"] = context.scene.render.bake.margin
    renderer_state["use_clear"] = context.scene.render.bake.use_clear
    renderer_state["target"] = context.scene.render.bake.target
    renderer_state["bake_type"] = context.scene.cycles.bake_type
    renderer_state["engine"] = context.scene.render.engine
    renderer_state["samples"] = context.scene.cycles.samples
    renderer_state["device"] = context.scene.cycles.device

    context.scene.render.bake.margin = 3
    context.scene.render.bake.target = 'IMAGE_TEXTURES'
    context.scene.render.bake.use_clear = False
    context.scene.cycles.bake_type = 'EMIT'
    context.scene.render.engine = 'CYCLES'
    context.scene.cycles.samples = 3

    prefs = context.preferences
    if prefs.addons.get('cycles'):
        cprefs = prefs.addons['cycles'].preferences
        if hasattr(cprefs, 'devices') and any(device.type == 'CUDA' for device in cprefs.devices):
            context.scene.cycles.device = 'GPU'

    node_tree.nodes.active = image_node
    return BakeState(material, output_node, orig_socket, image_node, source_socket, renderer_state)


def cleanup_bake(state):
    """Restore original node connections after baking"""
    if not state or not state.material:
        return
    bpy.context.scene.render.bake.margin = state.renderer_state["margin"]
    bpy.context.scene.render.bake.use_clear = state.renderer_state["use_clear"]
    bpy.context.scene.render.bake.target = state.renderer_state["target"]
    bpy.context.scene.cycles.bake_type = state.renderer_state["bake_type"]
    bpy.context.scene.render.engine = state.renderer_state["engine"]
    bpy.context.scene.cycles.samples = state.renderer_state["samples"]
    bpy.context.scene.cycles.device = state.renderer_state["device"]
    node_tree = state.material.node_tree
    if not node_tree:
        return

    output_surface = state.output_node.inputs['Surface']

    if output_surface.is_linked:
        for link in output_surface.links[:]:
            if link.from_socket == state.source_socket:
                node_tree.links.remove(link)
                break

    if state.orig_socket:
        try:
            if not output_surface.is_linked:
                node_tree.links.new(state.orig_socket, output_surface)
        except Exception as e:
            print(f"Error restoring connection: {e}")


class OBJECT_OT_CreateBakedMaterial(bpy.types.Operator):
    bl_idname = "object.create_baked_material"
    bl_label = "Create Baked Material"
    bl_description = "Create a basic Principled BSDF material with baked textures"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No active mesh object selected")
            return {'CANCELLED'}

        material = obj.active_material
        if not material:
            self.report({'ERROR'}, "Object has no active material")
            return {'CANCELLED'}

        node_tree = material.node_tree

        for node in node_tree.nodes:
            node_tree.nodes.remove(node)

        principled = node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        principled.location = (0, 0)
        output = node_tree.nodes.new('ShaderNodeOutputMaterial')
        output.location = (300, 0)
        node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])

        texture_mappings = {
            'BaseColor': ('Base Color', 'COLOR'),
            'Emission': ('Emission Color', 'COLOR'),
            'Metalness': ('Metallic', 'VALUE'),
            'Specular': ('Specular IOR Level', 'VALUE'),
            'Roughness': ('Roughness', 'VALUE'),
            'Normal': ('Normal', 'VECTOR'),
            'Alpha': ('Alpha', 'VALUE')
        }

        material_name = material.name
        for image in bpy.data.images:
            if not image.name.startswith(f"{material_name}_"):
                continue

            suffix = image.name[len(f"{material_name}_"):]

            if suffix in texture_mappings:
                input_name, input_type = texture_mappings[suffix]
                tex_node = node_tree.nodes.new('ShaderNodeTexImage')
                tex_node.image = image
                tex_node.location = (-300, 200 * len(node_tree.nodes))
                if input_type == 'COLOR':
                    node_tree.links.new(tex_node.outputs['Color'], principled.inputs[input_name])
                elif input_type == 'VALUE':
                    node_tree.links.new(tex_node.outputs['Color'], principled.inputs[input_name])
                elif input_type == 'VECTOR':
                    normal_node = node_tree.nodes.new('ShaderNodeNormalMap')
                    normal_node.location = (-100, tex_node.location.y)
                    node_tree.links.new(tex_node.outputs['Color'], normal_node.inputs['Color'])
                    node_tree.links.new(normal_node.outputs['Normal'], principled.inputs['Normal'])

                if suffix in ['BaseColor', 'Emission']:
                    image.colorspace_settings.name = 'sRGB'
                else:
                    image.colorspace_settings.name = 'Non-Color'

        principled.inputs["Emission Strength"].default_value = int(1)
        self.report({'INFO'}, f"Created material '{material.name}' with baked textures")
        return {'FINISHED'}


class OBJECT_OT_BakeTextures(bpy.types.Operator):
    bl_idname = "object.bake_textures"
    bl_label = "Bake Textures"
    bl_options = {'REGISTER', 'UNDO'}

    source: bpy.props.StringProperty(name="Source", default="Base Color")

    def execute(self, context):

        self.sources = [s.strip() for s in self.source.split(',') if s.strip()]
        self.current_index = -1
        self.bake_state = None
        self.baking = False

        self.objects_to_bake = []
        active_obj = context.active_object
        active_material = active_obj.active_material if active_obj else None

        if context.scene.warframe_tools_props.bake_all_material_users and active_material:
            for obj in bpy.data.objects:
                if obj.type == 'MESH':
                    for slot in obj.material_slots:
                        if slot.material == active_material:
                            self.objects_to_bake.append(obj)
                            break
            if active_obj in self.objects_to_bake:
                self.objects_to_bake.remove(active_obj)
                self.objects_to_bake.insert(0, active_obj)
        else:
            self.objects_to_bake = [active_obj] if active_obj else []

        if not self.objects_to_bake:
            self.report({'ERROR'}, "No objects to bake")
            return {'CANCELLED'}

        self.current_object_index = 0

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if not self.sources or not self.objects_to_bake:
            return {'FINISHED'}

        if self.current_index < 0:
            self.current_index = 0
            self.start_next_bake(context)
            return {'RUNNING_MODAL'}

        if self.baking:
            if bpy.app.is_job_running('OBJECT_BAKE'):
                return {'PASS_THROUGH'}

            cleanup_bake(self.bake_state)
            print(f"Baked {self.sources[self.current_index]} for {self.objects_to_bake[self.current_object_index].name} complete!")
            self.current_index += 1
            self.baking = False

        if self.current_index >= len(self.sources):
            self.current_index = 0
            self.current_object_index += 1

        if self.current_object_index >= len(self.objects_to_bake):
            return {'FINISHED'}

        if self.current_index < len(self.sources):
            self.start_next_bake(context)
            return {'RUNNING_MODAL'}

        return {'FINISHED'}

    def start_next_bake(self, context):
        source = self.sources[self.current_index]
        current_obj = self.objects_to_bake[self.current_object_index]

        bpy.context.view_layer.objects.active = current_obj
        print(f"Starting bake: {source} for {current_obj.name}")

        try:
            self.bake_state = setup_bake(context, source)
            print(context.active_object.name)
            bpy.ops.object.bake('INVOKE_DEFAULT', type='EMIT')
            self.baking = True
        except Exception as e:
            self.report({'ERROR'}, f"Bake failed: {str(e)}")
            self.current_index = len(self.sources)


class NormalToHeightOperator(bpy.types.Operator):
    bl_idname = "dprint.normal_to_height"
    bl_label = "Convert Normal to Height"

    def execute(self, context):
        normal_img = bpy.data.images.load(bpy.context.scene.warframe_tools_props.normal_to_height_path, check_existing=False)
        normal_img.colorspace_settings.name = 'Non-Color'
        height_data = self.normal_to_height(normal_img, iterations=2000)

        w, h = normal_img.size
        height_img = bpy.data.images.new(
            name=f"{normal_img.name}_Height",
            width=w,
            height=h,
            alpha=False,
            float_buffer=True
        )

        height_rgba = np.zeros((h, w, 4), dtype=np.float32)
        height_rgba[..., 0] = height_data
        height_rgba[..., 1] = height_data
        height_rgba[..., 2] = height_data
        height_rgba[..., 3] = 1.0

        height_img.pixels = height_rgba.ravel()

        height_img.pack()
        bpy.context.scene.warframe_tools_props.image_select = height_img.name
        return {'FINISHED'}

    def normal_to_height(self, normal_img, iterations=5000, damping=0.1):
        """
        Convert normal map to height map using iterative Poisson solver.
        Args:
            normal_img: Blender image object (normal map)
            iterations: Number of solver iterations (higher = more accurate)
            damping: Relaxation factor (0.1-0.5 recommended)
        Returns:
            Height map as 2D numpy array (normalized to 0-1)
        """
        normal_px = np.array(normal_img.pixels).reshape(
            normal_img.size[1], normal_img.size[0], -1
        )

        normal_data = normal_px[..., :3].astype(np.float32)
        normal_data = normal_data * 2.0 - 1.0

        normal_data[..., 1] *= -1 if bpy.context.scene.warframe_tools_props.invert_green else 1

        n_x, n_y, n_z = (
            normal_data[..., 0],
            normal_data[..., 1],
            np.clip(normal_data[..., 2], 1.0, 1.0)
        )
        n_z = 1
        dx = -n_x / n_z
        dy = -n_y / n_z

        h, w = dx.shape
        f = np.zeros((h, w), dtype=np.float32)

        f[1:-1, 1:-1] = 0.5 * (dx[1:-1, 2:] - dx[1:-1, :-2]) + \
                         0.5 * (dy[2:, 1:-1] - dy[:-2, 1:-1])

        f[0, :] = dy[0, :]
        f[-1, :] = -dy[-2, :]
        f[:, 0] = dx[:, 0]
        f[:, -1] = -dx[:, -2]

        height = np.zeros((h, w), dtype=np.float32)
        for _ in range(iterations):
            new_height = height.copy()
            new_height[1:-1, 1:-1] = (1 - damping) * height[1:-1, 1:-1] + \
                damping * 0.25 * (
                    height[1:-1, :-2] +
                    height[1:-1, 2:] +
                    height[:-2, 1:-1] +
                    height[2:, 1:-1] -
                    f[1:-1, 1:-1]
                )

            new_height[0, :] = new_height[1, :]
            new_height[-1, :] = new_height[-2, :]
            new_height[:, 0] = new_height[:, 1]
            new_height[:, -1] = new_height[:, -2]
            height = new_height

        return (height - height.min()) / (height.max() - height.min())


class SubDivisionOperator(bpy.types.Operator):
    bl_idname = "dprint.subdivide"
    bl_label = "Add Subdivision Surface Modifier"
    bl_description = "Adds a Catmull-Clark subdivision surface modifier"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None and
            context.active_object.type == 'MESH'
        )

    def execute(self, context):
        props = bpy.context.scene.warframe_tools_props
        obj = context.active_object
        subdiv_levels = props.subdiv_amount
        ram_subdivision = props.ram_subdivision
        ram_amount = props.ram_amount * 1000000
        optimized = props.optimized_subdivision
        if ram_subdivision:
            subdiv_levels = int(max(0, math.floor(math.log(ram_amount / len(obj.data.vertices), 4) - 1) if len(obj.data.vertices) <= ram_amount else 0))
        for mod in obj.modifiers:
            if mod.name.startswith("AutoSubdivision"):
                obj.modifiers.remove(mod)

        if optimized and subdiv_levels > 1:
            base_mod = obj.modifiers.new(name="AutoSubdivision_Base", type='SUBSURF')
            base_mod.subdivision_type = 'SIMPLE'
            base_mod.levels = 1
            base_mod.render_levels = 1
            base_mod.show_expanded = False

            detail_mod = obj.modifiers.new(name="AutoSubdivision_Detail", type='SUBSURF')
            detail_mod.subdivision_type = 'CATMULL_CLARK'
            detail_levels = max(0, subdiv_levels - 1)
            detail_mod.levels = detail_levels
            detail_mod.render_levels = detail_levels
            detail_mod.show_expanded = False

            self.report({'INFO'}, f"Added optimized subdivision: Simple(1) + Catmull-Clark({detail_levels})")

        else:
            mod = obj.modifiers.new(name="AutoSubdivision", type='SUBSURF')
            mod.subdivision_type = 'CATMULL_CLARK'
            mod.levels = subdiv_levels
            mod.render_levels = subdiv_levels
            mod.show_expanded = False

            self.report({'INFO'}, f"Added Catmull-Clark subdivision with {subdiv_levels} levels")

        return {'FINISHED'}


class DeformOperator(bpy.types.Operator):
    bl_idname = "dprint.add_height"
    bl_label = "Add Height Map as Deform Modifier"
    bl_description = "Adds displace modifier with selected height map image"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None and
            context.active_object.type == 'MESH'
        )

    def execute(self, context):
        props = bpy.context.scene.warframe_tools_props
        selected_image_name = props.image_select

        if selected_image_name == 'NONE' or not selected_image_name:
            self.report({'ERROR'}, "No image selected")
            return {'CANCELLED'}

        img = bpy.data.images.get(selected_image_name)
        if not img:
            self.report({'ERROR'}, f"Image '{selected_image_name}' not found")
            return {'CANCELLED'}

        obj = context.active_object

        texture_name = f"{obj.name}_{img.name}_displace"
        tex = bpy.data.textures.get(texture_name) or bpy.data.textures.new(name=texture_name, type='IMAGE')
        tex.image = img
        tex.use_preview_alpha = True

        modifier_name = f"Displace_{img.name}"
        mod = obj.modifiers.get(modifier_name) or obj.modifiers.new(name=modifier_name, type='DISPLACE')
        mod.texture = tex
        mod.strength = 0.01
        mod.texture_coords = 'UV'
        mod.mid_level = 0.5

        self.report({'INFO'}, f"Added displace modifier with {img.name}")
        return {'FINISHED'}


class RunAllOperationsOperator(bpy.types.Operator):
    bl_idname = "dprint.run_all_operations"
    bl_label = "Run All Operations"
    bl_description = "Execute normal map conversion, subdivision, and height deformation"

    def execute(self, context):
        props = bpy.context.scene.warframe_tools_props

        try:
            bpy.ops.dprint.normal_to_height()

            bpy.ops.dprint.subdivide()

            bpy.ops.dprint.add_height()

            self.report({'INFO'}, "All operations completed successfully!")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Operation failed: {str(e)}")
            return {'CANCELLED'}


class SHADER_OT_append_material(bpy.types.Operator):
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

                self.cleanup_textures(new_material, new_image_names)
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
    def cleanup_textures(self, material, new_image_names):
        if not material.use_nodes:
            return
        unused_images = new_image_names

        for image_name in unused_images:
            image = bpy.data.images.get(image_name)
            if image:
                try:
                    bpy.data.images.remove(image)
                    self.report({'INFO'}, f"Removed unused image: {image_name}")
                except Exception as e:
                    self.report({'WARNING'}, f"Could not remove image {image_name}: {str(e)}")
    def draw(self, context):
        layout = self.layout
        layout.label(text="Select Material to Append")
        layout.prop(self, "material_name", text="")
        layout.separator()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)


class RIG_OT_append_rig(bpy.types.Operator):
    bl_idname = "rig.append_rig"
    bl_label = "Append Rig"
    bl_description = "Append rig and do automatic setup"
    bl_property = "rig_name"
    bl_options = {'REGISTER', 'UNDO'}

    rig_name: bpy.props.EnumProperty(
        name="Rigs",
        description="Available rigs",
        items=get_rig_items,
    )

    def execute(self, context):
        if not self.rig_name:
            return {'CANCELLED'}
        original_selection = context.selected_objects
        original_active = context.active_object
        selected = context.selected_objects
        bpy.ops.wm.append(
            directory=os.path.join(bpy.context.scene.warframe_tools_props.rig_path, "Collection") + os.sep,
            filename=self.rig_name
        )
        bpy.ops.wm.append(
            directory=os.path.join(bpy.context.scene.warframe_tools_props.rig_path, "Text") + os.sep,
            filename="Bones Snap"
        )
        self.report({'INFO'}, f"Appended rig: {self.rig_name}")
        obj = bpy.context.object
        new_rig_collection  = bpy.data.collections.get(self.rig_name)
        if new_rig_collection.name not in context.scene.collection.children:
            bpy.context.scene.collection.children.link(new_rig_collection)
        else:
            print("Failed to append rig")
        target_armature = None
        for obj in new_rig_collection.objects:
            print(obj.name)
            if obj.type == 'ARMATURE' and obj.name.lower() in self.rig_name.lower():
                target_armature = obj
                break

        if not target_armature:
            self.report({'ERROR'}, f"Armature '{self.rig_name}' not found in collection")
            return {'CANCELLED'}
        updated_count = 0
        old_armatures = set()
        for obj in selected:
            print(obj)
            for mod in obj.modifiers:
                if mod.type == 'ARMATURE':
                    if mod.object != target_armature:
                        old_armatures.add(mod.object)
                        mod.object = target_armature
                        updated_count += 1
        special_rigs = {"face rig": ["Face Metarig", "MetaRig"], "long arm rig": ["Long Arm Metarig", "Long Arm Metarig"]}
        for sprig in special_rigs:
            if sprig in self.rig_name.lower() and old_armatures:
                face_meta_rig = None
                face_meta_rig = bpy.data.objects.get(special_rigs[sprig][0])

                if not face_meta_rig:
                    self.report({'WARNING'}, "Face MetaRig not found in appended collection")
                else:
                    snap_script = bpy.data.texts.get("Bones Snap")
                    if snap_script:
                        print(special_rigs[sprig][1])
                        metacol = bpy.data.collections.get(special_rigs[sprig][1])
                        print(metacol)
                        metacol.hide_viewport = False
                        bpy.ops.object.select_all(action='DESELECT')
                        face_meta_rig.hide_set(False)
                        face_meta_rig.hide_viewport = False
                        face_meta_rig.hide_select = False
                        face_meta_rig.select_set(True)
                        context.view_layer.objects.active = face_meta_rig
                        for old_arm in old_armatures:
                            old_arm.select_set(True)
                            context.view_layer.objects.active = old_arm
                            break
                        try:
                            ctx = {
                                'bpy': bpy,
                                'context': context,
                                'selected_objects': context.selected_objects,
                                'active_object': context.active_object
                            }
                            exec(snap_script.as_string(), ctx)
                        except Exception as e:
                            metacol.hide_viewport = True
                            self.report({'ERROR'}, f"Bone Snap failed: {str(e)}")
                        bpy.ops.object.select_all(action='DESELECT')
                        face_meta_rig.select_set(True)
                        context.view_layer.objects.active = face_meta_rig
                        try:
                            bpy.ops.pose.rigify_generate()
                        except Exception as e:
                            metacol.hide_viewport = True
                            self.report({'ERROR'}, f"Rigify generation failed: {str(e)}")
                            return {'CANCELLED'}
                        metacol.hide_viewport = True
                    else:
                        self.report({'WARNING'}, "Bones Snap script not found")
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select Rig to Append")
        layout.prop(self, "rig_name", text="")
        layout.separator()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)


class WARFRAME_OT_ImportModel(bpy.types.Operator):
    bl_idname = "wm.import_model"
    bl_label = "Import Model"
    bl_description = "Import and process Warframe model"

    def execute(self, context):
        props = context.scene.warframe_tools_props
        bpy.ops.import_scene.gltf(
            filepath=str(bpy.context.scene.warframe_tools_props.model_file_path),
            guess_original_bind_pose=False,
            bone_heuristic="TEMPERANCE")
        collections_dict = {}
        for obj in bpy.context.selected_objects:
            if obj.type != 'MESH':
                continue
            # Credit: KptWeedy
            if bpy.context.scene.warframe_tools_props.LEVEL_IMPORT:
                print(obj.data.validate(clean_customdata=True))
                if len(obj.material_slots) > 0 and obj.material_slots[0].material.name.lower().startswith("hidden"):
                    obj.hide_render = True
                    obj.hide_set(True)
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

        self.report({'INFO'}, "Model imported successfully")
        return {'FINISHED'}


class WARFRAME_OT_SetupShader(bpy.types.Operator):
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


class WM_OT_RunSetup(bpy.types.Operator):
    bl_idname = "wm.run_setup"
    bl_label = "Run Setup"

    def execute(self, context):
        props = context.scene.warframe_tools_props

        mode = props.mode
        if mode == 'IMPORT':
            return bpy.ops.wm.import_model('INVOKE_DEFAULT')
        elif mode == 'APPEND':
            return bpy.ops.shader.append_material('INVOKE_DEFAULT')
        elif mode == 'RIG':
            return bpy.ops.rig.append_rig('INVOKE_DEFAULT')
        elif mode == 'BAKE':
            # I hate azdfulla for making me do this
            sources = []
            if props.bake_base_color:
                sources.append('Base Color')
            if props.bake_emission:
                sources.append('Emission')
            if props.bake_metalness:
                sources.append('Metalness')
            if props.bake_roughness:
                sources.append('Roughness')
            if props.bake_specular:
                sources.append('Specular')
            if props.bake_normal:
                sources.append('Normal')
            if props.bake_alpha:
                sources.append('Alpha')
            return bpy.ops.object.bake_textures(source=",".join(sources))
        elif mode == 'SHADER':
            return bpy.ops.wm.setup_shader('INVOKE_DEFAULT')
        elif mode == 'EXPERIMENTAL':
            return bpy.ops.wm.experimental_mode('INVOKE_DEFAULT')

        self.report({'WARNING'}, "Unknown mode selected")
        return {'CANCELLED'}


class WM_OT_SetupPaths(bpy.types.Operator):
    bl_idname = "wm.setup_paths"
    bl_label = "Setup Required Paths"
    bl_description = "Select the path to file/folder"

    current_step: bpy.props.IntProperty(default=0)
    material_file_path: bpy.props.StringProperty(subtype='FILE_PATH')
    model_file_path: bpy.props.StringProperty(subtype='FILE_PATH')
    extractor_path: bpy.props.StringProperty(subtype='FILE_PATH')
    cache_path: bpy.props.StringProperty(subtype='DIR_PATH')
    shader_library_path: bpy.props.StringProperty(subtype='DIR_PATH')
    pathToShader: bpy.props.StringProperty(subtype='FILE_PATH')
    pathToRig: bpy.props.StringProperty(subtype='FILE_PATH')
    root: bpy.props.StringProperty(subtype='DIR_PATH')
    pathToTextures: bpy.props.StringProperty(subtype='DIR_PATH')
    normal_to_height_path: bpy.props.StringProperty(subtype='DIR_PATH')

    filter_glob: bpy.props.StringProperty(default="*")
    directory: bpy.props.StringProperty(subtype='DIR_PATH', default=str(Path.home()))
    filepath: bpy.props.StringProperty(subtype='FILE_PATH')

    def determine_steps(self):
        steps = []
        mode = bpy.context.scene.warframe_tools_props.mode
        if mode == 'IMPORT':
            steps.append(('model_file_path', 'Select Model File (.glb)', 'file', '*.glb'))
        elif mode == 'APPEND':
            steps.append(('pathToShader', 'Select Shader Blend File', 'file', '*.blend'))
        elif mode == 'RIG':
            self.root = bpy.context.scene.warframe_tools_props.rig_path
            if bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION and (self.pathToRig is None or self.pathToRig is ""):
                steps.append(('pathToRig', 'Select Rig Blend File', 'file', '*.blend'))
        elif mode == 'BAKE':
            return steps
        elif mode == '3DPRINT':
            steps.append(('normal_to_height_path', 'Select Normal Map File', 'file', '*'))
        elif mode == 'EXPERIMENTAL':
            steps.append(('model_file_path', 'Select Model File (.glb)', 'file', '*.glb'))
            steps.append(('shader_library_path', 'Select Shader Library Folder', 'directory', ''))
            self.root = bpy.context.scene.warframe_tools_props.root
            if bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION and (self.root is None or self.root is ""):
                steps.append(('root', 'Select Root Directory', 'directory', ''))
            if bpy.context.scene.warframe_tools_props.USE_EXTRACTOR:
                steps.append(('extractor_path', 'Select Extractor CLI', 'file', '*'))
                steps.append(('cache_path', 'Select Cache Folder', 'directory', ''))
        elif mode == 'SHADER':
            steps.append(('material_file_path', 'Select Material File (.txt)', 'file', '*.txt'))
            self.root = bpy.context.scene.warframe_tools_props.root
            if bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION and (self.root is None or self.root is ""):
                steps.append(('root', 'Select Root Directory', 'directory', ''))
            elif not bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION:
                steps.append(('pathToTextures', 'Select Textures Directory', 'directory', ''))
        return steps

    def invoke(self, context, event):
        self.steps = self.determine_steps()
        if not self.steps:
            self.report({'WARNING'}, "No paths required for current mode")
            return self.execute(context)
        self.current_step = 0
        self.filepath = ""
        self.directory = str(Path.home())
        self.material_file_path = ""
        self.model_file_path = ""
        self.extractor_path = ""
        self.cache_path = ""
        self.shader_library_path = ""
        self.pathToShader = ""
        self.pathToRig = ""
        self.root = ""
        self.pathToTextures = ""
        self.normal_to_height_path = ""
        return self.execute(context)

    def execute(self, context):
        if self.current_step >= len(self.steps):
            if self.material_file_path:
                bpy.context.scene.warframe_tools_props.material_file_path = self.material_file_path
            if self.model_file_path:
                bpy.context.scene.warframe_tools_props.model_file_path = self.model_file_path
            if self.extractor_path:
                bpy.context.scene.warframe_tools_props.extractor_path = self.extractor_path
            if self.cache_path:
                bpy.context.scene.warframe_tools_props.cache_path = self.cache_path
            if self.shader_library_path:
                bpy.context.scene.warframe_tools_props.shader_library_path = self.shader_library_path
            if self.pathToTextures:
                bpy.context.scene.warframe_tools_props.pathToTextures = self.pathToTextures
            if self.pathToRig:
                bpy.context.scene.warframe_tools_props.rig_path = self.pathToRig
            if self.pathToShader:
                bpy.context.scene.warframe_tools_props.pathToShader = self.pathToShader
            if self.normal_to_height_path:
                bpy.context.scene.warframe_tools_props.normal_to_height_path = self.normal_to_height_path
            if self.root:
                bpy.context.scene.warframe_tools_props.root = self.root
            if self.pathToTextures:
                bpy.context.scene.warframe_tools_props.pathToTextures = self.pathToTextures
            return bpy.ops.wm.run_setup('INVOKE_DEFAULT')

        step = self.steps[self.current_step]
        step_id, label, step_type, filter_glob = step
        current_value = getattr(self, step_id, "")
        props = context.scene.warframe_tools_props

        if not current_value:
            if step_type == 'file':
                if not self.filepath:
                    if hasattr(props, step_id):
                        scene_value = getattr(props, step_id)
                        if scene_value:
                            self.filepath = scene_value
                    self.filter_glob = filter_glob
                    context.window_manager.fileselect_add(self)
                    return {'RUNNING_MODAL'}
                else:
                    setattr(self, step_id, self.filepath)
                    self.filepath = ""
                    self.current_step += 1
            elif step_type == 'directory':
                if not self.filepath:
                    if hasattr(props, step_id):
                        scene_value = getattr(props, step_id)
                        if scene_value:
                            self.filepath = scene_value
                    context.window_manager.fileselect_add(self)
                    return {'RUNNING_MODAL'}
                else:
                    setattr(self, step_id, self.filepath)
                    self.filepath = ""
                    self.current_step += 1
        else:
            self.current_step += 1

        return self.execute(context)

    def modal(self, context, event):
        if event.type == 'FILE_SELECT':
            return self.execute(context)
        return {'PASS_THROUGH'}

    def draw(self, context):
        layout = self.layout
        for i, step in enumerate(self.steps):
            step_id, label, step_type, _ = step
            row = layout.row()
            if i == self.current_step:
                row.alert = True
                row.label(text=f"➤ {label}", icon='FILEBROWSER')
                current_value = getattr(self, step_id, "")
                if current_value:
                    name = os.path.basename(current_value)
                    row.label(text=name, icon='CHECKMARK')
            else:
                row.label(text=f"   {label}")
                current_value = getattr(self, step_id, "")
                if current_value:
                    name = os.path.basename(current_value)
                    row.label(text=name, icon='CHECKMARK')


class WARFRAME_OT_ExperimentalMode(bpy.types.Operator):
    bl_idname = "wm.experimental_mode"
    bl_label = "Experimental Mode"
    bl_description = "Import model and auto-setup materials from MaterialPath"

    def execute(self, context):

        start_time = time.time()
        props = context.scene.warframe_tools_props
        set_up_mats = []
        bpy.ops.wm.import_model('EXEC_DEFAULT')

        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
            if(obj.data.materials[0].name.split('.')[0] in set_up_mats):
                continue
            material_path = obj.data.materials[0].get('FullPath')
            if not material_path:
                set_up_mats.append(obj.data.materials[0].name.split('.')[0])
                self.report({'WARNING'}, f"Object {obj.name} has no FullPath custom property")
                continue

            internal_path = find_internal_path(material_path) #возможно не надо
            material_file_path = os.path.join(props.root, internal_path) + ".txt"

            if not os.path.exists(material_file_path):
                if props.USE_EXTRACTOR:
                    success = extract_material_with_cli(
                        props.extractor_path,
                        props.cache_path,
                        internal_path,
                        props.root
                    )
                    if not success:
                        self.report({'ERROR'}, f"Failed to extract material: {internal_path}")
                        set_up_mats.append(obj.data.materials[0].name.split('.')[0])
                        continue
                else:
                    self.report({'WARNING'}, f"Material file not found: {material_file_path}")
                    set_up_mats.append(obj.data.materials[0].name.split('.')[0])
                    continue

            try:
                material_data, shader_data, hierarchy_data = parse_material_file(material_file_path)
            except Exception as e:
                self.report({'ERROR'}, f"Failed to parse material file: {str(e)}")
                set_up_mats.append(obj.data.materials[0].name.split('.')[0])
                continue

            shader_name = None
            for key in shader_data:
                if isinstance(key, str) and '_p.hlsl' in key:
                    shader_name = key.split('_p.hlsl')[0].split("/")[-2]
                    break

            if not shader_name:
                self.report({'WARNING'}, f"No shader found in material file: {material_file_path}")
                set_up_mats.append(obj.data.materials[0].name.split('.')[0])
                continue
            print(f"Found shader name: {shader_name}")
            shader_blend_path, error = find_shader_material(shader_name, props.shader_library_path)
            if error:
                self.report({'ERROR'}, error)
                set_up_mats.append(obj.data.materials[0].name.split('.')[0])
                continue

            print(f"Found shader: {shader_blend_path}")
            material_name = get_best_material_from_blend(shader_blend_path, material_data)
            if not material_name:
                self.report({'ERROR'}, f"No suitable material found in {shader_blend_path}")
                set_up_mats.append(obj.data.materials[0].name.split('.')[0])
                continue
            print(f"Chosen material: {material_name}")
            original_base_name = None
            if obj and obj.data and hasattr(obj.data, 'materials') and obj.data.materials:
                if obj.data.materials[0]:
                    original_base_name = obj.data.materials[0].name.split('.')[0]

            before = set(bpy.data.materials.keys())

            before_images = set(bpy.data.images.keys())
            bpy.ops.wm.append(
                directory=os.path.join(shader_blend_path, "Material") + os.sep,
                filename=material_name,
                do_reuse_local_id=False
            )
            after = set(bpy.data.materials.keys())
            new_material_names = after - before

            if not new_material_names:
                self.report({'ERROR'}, "Failed to append material")
                set_up_mats.append(obj.data.materials[0].name.split('.')[0])
                continue

            new_material = bpy.data.materials[list(new_material_names)[0]]
            self.report({'INFO'}, f"Appended material: {material_name}")

            after_images = set(bpy.data.images.keys())
            new_image_names = after_images - before_images

            self.cleanup_textures(new_material, new_image_names) #change
            gn_node_groups = []
            try:
                with bpy.data.libraries.load(context.scene.warframe_tools_props.pathToShader, link=False) as (data_from, data_to):
                    gn_node_groups = [name for name in data_from.node_groups if name.startswith("Gn") and name not in data_to.node_groups]
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

            texture_locations = {}

            model_path = find_internal_path(material_file_path)
            set_material_properties(new_material, material_data, props.pathToTextures,
                                  model_path, texture_locations, shader_data, hierarchy_data)

            set_up_mats.append(obj.data.materials[0].name.split('.')[0])

            end_time = time.time()
            elapsed_time = end_time - start_time
            minutes, seconds = divmod(elapsed_time, 60)

            self.report({'INFO'}, f"Setup completed in {int(minutes)}m {seconds:.2f}s")
            self.report({'INFO'}, f"Set up material for {obj.name}")

        return {'FINISHED'}
    def cleanup_textures(self, material, new_image_names):
        if not material.use_nodes:
            return
        unused_images = new_image_names

        for image_name in unused_images:
            image = bpy.data.images.get(image_name)
            if image:
                try:
                    bpy.data.images.remove(image)
                    self.report({'INFO'}, f"Removed unused image: {image_name}")
                except Exception as e:
                    self.report({'WARNING'}, f"Could not remove image {image_name}: {str(e)}")
