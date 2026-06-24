import bpy
import math
import numpy as np


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
