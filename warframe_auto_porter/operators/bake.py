import os

import bpy

from ..constants import EMISSION_FLAGS_FOR_BAKING


class BakeState:
    """Storage for bake operation state"""

    def __init__(
        self, material, output_node, orig_socket, image_node, source_socket, renderer_state
    ):
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
    if source == "Specular":
        source = "Specular IOR Level"
    output_node = next((n for n in node_tree.nodes if n.type == "OUTPUT_MATERIAL"), None)
    if not output_node:
        raise Exception("Material Output node not found")
    orig_socket = None
    if output_node.inputs["Surface"].is_linked:
        orig_socket = output_node.inputs["Surface"].links[0].from_socket
    source_socket = None
    fallback_socket = None
    for node in node_tree.nodes:
        if node.type in {"GROUP", "GROUP_OUTPUT"}:
            for output in node.outputs:
                if source == output.name:
                    fallback_socket = output
                    if (
                        source == "Normal"
                        and "final" in getattr(node.node_tree, "name", "").lower()
                    ):
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

    if source == "Specular IOR Level":
        source = "Specular"
    image_name = f"{material.name}_{source.replace(' ', '')}.png"
    image = bpy.data.images.get(image_name)
    if image is None:
        image = bpy.data.images.new(
            image_name,
            *(
                bpy.context.scene.warframe_tools_props.bake_width,
                bpy.context.scene.warframe_tools_props.bake_height,
            ),
        )
        image.colorspace_settings.name = (
            "sRGB" if source in ["Base Color", "Emission"] else "Non-Color"
        )
    elif bake_all_users:
        pass

    image_node = None
    for node in node_tree.nodes:
        if node.type == "TEX_IMAGE" and node.image and node.image.name == image_name:
            image_node = node
            break

    if image_node is None:
        image_node = node_tree.nodes.new("ShaderNodeTexImage")
        image_node.location = (output_node.location.x - 300, output_node.location.y + 500)

    image_node.image = image

    if output_node.inputs["Surface"].is_linked:
        for link in output_node.inputs["Surface"].links:
            node_tree.links.remove(link)
    node_tree.links.new(source_socket, output_node.inputs["Surface"])

    renderer_state = {}
    renderer_state["margin"] = context.scene.render.bake.margin
    renderer_state["use_clear"] = context.scene.render.bake.use_clear
    renderer_state["target"] = context.scene.render.bake.target
    renderer_state["bake_type"] = context.scene.cycles.bake_type
    renderer_state["engine"] = context.scene.render.engine
    renderer_state["samples"] = context.scene.cycles.samples
    renderer_state["device"] = context.scene.cycles.device

    context.scene.render.bake.margin = 3
    context.scene.render.bake.target = "IMAGE_TEXTURES"
    context.scene.render.bake.use_clear = False
    context.scene.cycles.bake_type = "EMIT"
    context.scene.render.engine = "CYCLES"
    context.scene.cycles.samples = 3

    prefs = context.preferences
    if prefs.addons.get("cycles"):
        cprefs = prefs.addons["cycles"].preferences
        if hasattr(cprefs, "devices") and any(device.type == "CUDA" for device in cprefs.devices):
            context.scene.cycles.device = "GPU"

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

    output_surface = state.output_node.inputs["Surface"]

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


class CreateBakedMaterialOperator(bpy.types.Operator):
    bl_idname = "object.create_baked_material"
    bl_label = "Create Baked Material"
    bl_description = "Create a basic Principled BSDF material with baked textures"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"ERROR"}, "No active mesh object selected")
            return {"CANCELLED"}

        original_material = obj.active_material
        if not original_material:
            self.report({"ERROR"}, "Object has no active material")
            return {"CANCELLED"}

        orig_name = original_material.name
        new_mat_name = orig_name + "_Baked"

        new_material = bpy.data.materials.new(new_mat_name)
        new_material.use_nodes = True
        node_tree = new_material.node_tree

        for node in node_tree.nodes:
            node_tree.nodes.remove(node)

        principled = node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        principled.location = (0, 0)
        output = node_tree.nodes.new("ShaderNodeOutputMaterial")
        output.location = (300, 0)
        node_tree.links.new(principled.outputs["BSDF"], output.inputs["Surface"])

        texture_mappings = {
            "BaseColor": ("Base Color", "COLOR"),
            "Emission": ("Emission Color", "COLOR"),
            "Metalness": ("Metallic", "VALUE"),
            "Specular": ("Specular IOR Level", "VALUE"),
            "Roughness": ("Roughness", "VALUE"),
            "Normal": ("Normal", "VECTOR"),
            "Alpha": ("Alpha", "VALUE"),
        }

        for image in bpy.data.images:
            if not image.name.startswith(f"{orig_name}_"):
                continue

            suffix = image.name[len(f"{orig_name}_") :].split(".")[0]

            if suffix in texture_mappings:
                input_name, input_type = texture_mappings[suffix]
                tex_node = node_tree.nodes.new("ShaderNodeTexImage")
                print(
                    f"Before: {image.name}, source={image.source}, packed={image.packed_file is not None}, filepath={image.filepath}"
                )
                tex_node.image = image
                print(
                    f"After: {image.name}, source={image.source}, packed={image.packed_file is not None}"
                )
                image.update()
                tex_node.location = (-300, -200 * len(node_tree.nodes))

                if input_type == "COLOR" or input_type == "VALUE":
                    node_tree.links.new(tex_node.outputs["Color"], principled.inputs[input_name])
                elif input_type == "VECTOR":
                    normal_node = node_tree.nodes.new("ShaderNodeNormalMap")
                    normal_node.location = (-100, tex_node.location.y)
                    node_tree.links.new(tex_node.outputs["Color"], normal_node.inputs["Color"])
                    node_tree.links.new(normal_node.outputs["Normal"], principled.inputs["Normal"])

                if suffix in ["BaseColor", "Emission"]:
                    image.colorspace_settings.name = "sRGB"
                else:
                    image.colorspace_settings.name = "Non-Color"

                print(
                    f"After: {image.name}, source={image.source}, packed={image.packed_file is not None}"
                )

        principled.inputs["Emission Strength"].default_value = 1.0

        for ob in bpy.data.objects:
            if hasattr(ob, "material_slots"):
                for slot in ob.material_slots:
                    if slot.material == original_material:
                        slot.material = new_material

        self.report({"INFO"}, f"Created material '{new_material.name}'")
        return {"FINISHED"}


class BakeTexturesOperator(bpy.types.Operator):
    bl_idname = "object.bake_textures"
    bl_label = "Bake Textures"
    bl_options = {"REGISTER", "UNDO"}

    source: bpy.props.StringProperty(name="Source", default="Base Color")

    def execute(self, context):

        self.sources = [s.strip() for s in self.source.split(",") if s.strip()]
        self.current_index = -1
        self.bake_state = None
        self.baking = False

        self.objects_to_bake = []
        active_obj = context.active_object
        active_material = active_obj.active_material if active_obj else None

        if context.scene.warframe_tools_props.bake_all_material_users and active_material:
            for obj in bpy.data.objects:
                if obj.type == "MESH":
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
            self.report({"ERROR"}, "No objects to bake")
            return {"CANCELLED"}

        self.current_object_index = 0

        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if not self.sources or not self.objects_to_bake:
            return {"FINISHED"}

        if self.current_index < 0:
            self.current_index = 0
            self.start_next_bake(context)
            return {"RUNNING_MODAL"}

        if self.baking:
            if bpy.app.is_job_running("OBJECT_BAKE"):
                return {"PASS_THROUGH"}

            cleanup_bake(self.bake_state)
            print(
                f"Baked {self.sources[self.current_index]} for {self.objects_to_bake[self.current_object_index].name} complete!"
            )
            if self.bake_state and self.bake_state.image_node and self.bake_state.image_node.image:
                image = self.bake_state.image_node.image
                source = self.sources[self.current_index]
                material_name = self.bake_state.material.name
                self.save_baked_image(context, image, source, material_name)
            self.current_index += 1
            self.baking = False

        if self.current_index >= len(self.sources):
            self.current_index = 0
            self.current_object_index += 1

        if self.current_object_index >= len(self.objects_to_bake):
            return {"FINISHED"}

        if self.current_index < len(self.sources):
            self.start_next_bake(context)
            return {"RUNNING_MODAL"}

        return {"FINISHED"}

    def start_next_bake(self, context):
        source = self.sources[self.current_index]
        current_obj = self.objects_to_bake[self.current_object_index]

        bpy.context.view_layer.objects.active = current_obj
        print(f"Starting bake: {source} for {current_obj.name}")

        try:
            self.bake_state = setup_bake(context, source)
            print(context.active_object.name)
            bpy.ops.object.bake("INVOKE_DEFAULT", type="EMIT")
            self.baking = True
        except Exception as e:
            self.report({"ERROR"}, f"Bake failed: {e!s}")
            self.current_index = len(self.sources)

    def save_baked_image(self, context, image, source, material_name):
        props = context.scene.warframe_tools_props
        output_dir = getattr(props, "bake_output_path", "")

        if not output_dir:
            blend_path = bpy.data.filepath
            if blend_path:
                output_dir = os.path.join(os.path.dirname(blend_path), "BakedTextures")
            else:
                self.report({"WARNING"}, "No output directory and unsaved blend – image not saved")
                return

        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            self.report({"ERROR"}, f"Cannot create output directory: {e}")
            return

        safe_source = source.replace(" ", "_")
        filename = f"{material_name}_{safe_source}.png"
        filepath = os.path.join(output_dir, filename)

        try:
            image.filepath_raw = filepath
            image.file_format = "PNG"
            image.save()
            self.report({"INFO"}, f"Saved: {filepath}")
        except Exception as e:
            self.report({"ERROR"}, f"Save failed: {e}")
