import bpy


class WARFRAME_PT_SetupPanel(bpy.types.Panel):
    bl_label = "Warframe Model Setup"
    bl_idname = "WARFRAME_PT_SetupPanel"
    bl_description = "Panel for setting up warframe models"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        if not context:
            return
        layout = self.layout
        scene = context.scene
        props = scene.warframe_tools_props
        prefs = context.preferences.addons[__package__].preferences
        box = layout.box()
        box.label(text="Configuration")
        box.label(text="Select Mode:")
        box.prop(props, "mode")
        if props.mode == 'IMPORT':
            box.prop(props, "USE_PATHS")
            box.prop(props, "LEVEL_IMPORT")
            box.prop(props, "USE_EXTRACTOR")
            if not props.USE_PATHS:
                box.prop(props, "model_file_path")
                box.prop(props, "extractor_path")
                box.prop(props, "cache_path")

            if props.USE_PATHS:
                layout.operator("wm.setup_paths", text="Import")
            else:
                layout.operator("wm.run_setup", text="Import")
            return
        if props.mode == 'APPEND':
            box.prop(props, "USE_PATHS")
            if not props.USE_PATHS:
                box.prop(props, "pathToShader")

            if props.USE_PATHS:
                layout.operator("wm.setup_paths", text="Run Setup")
            else:
                layout.operator("wm.run_setup", text="Run Setup")
            return
        if props.mode == 'RIG':
            box.prop(props, "USE_PATHS")
            if not props.USE_PATHS:
                box.prop(prefs, "rig_preference")
            if props.USE_PATHS:
                layout.operator("wm.setup_paths", text="Run Setup")
            else:
                layout.operator("wm.run_setup", text="Run Setup")
            return
        if props.mode == 'BAKE':
            box.prop(props, "USE_PATHS")
            box.label(text="Bake Sources:")
            grid = box.grid_flow(
                row_major=True,
                columns=3,
                even_columns=True,
                even_rows=True,
                align=True
            )
            grid.prop(props, "bake_base_color")
            grid.prop(props, "bake_emission")
            grid.prop(props, "bake_metalness")
            grid.prop(props, "bake_roughness")
            grid.prop(props, "bake_specular")
            grid.prop(props, "bake_normal")
            grid.prop(props, "bake_alpha")
            box.prop(props, "bake_all_material_users")
            box.prop(props, "uv_source")
            row = box.row(align=True)
            row.prop(props, "bake_height")
            row.prop(props, "bake_width")
            box.separator()
            box.operator("object.create_baked_material", text="Create Material With Baked Textures")
            if props.USE_PATHS:
                layout.operator("wm.setup_paths", text="Run Setup")
            else:
                layout.operator("wm.run_setup", text="Run Setup")
            return
        if props.mode == '3DPRINT':
            box.prop(props, "separate_mode")
            convert = box.box()
            convert.prop(props, "normal_to_height_path")
            convert.prop(props, "invert_green")

            if props.separate_mode:
                convert.operator("dprint.normal_to_height", text="Convert Normal Map to Height Map")
            box.separator()

            subd = box.box()
            subd.prop(props, "optimized_subdivision")
            subd.prop(props, "ram_subdivision")
            if not props.ram_subdivision:
                subd.prop(props, "subdiv_amount")
            if props.ram_subdivision:
                subd.prop(props, "ram_amount")

            if props.separate_mode:
                subd.operator("dprint.subdivide", text="Add subdivision")
            box.separator()

            if props.separate_mode:
                heightm = box.box()
                heightm.prop(props, "image_select")
                heightm.operator("dprint.add_height", text="Add Deform Modifier With Selected Height Map")

            if not props.separate_mode:
                row = box.row()
                row.operator("dprint.run_all_operations", text="Run All Operations")
            return
        if props.mode == 'EXPERIMENTAL':
            box.prop(props, "USE_PATHS")
            box.prop(props, "USE_EXTRACTOR")
            box.prop(props, "LEVEL_IMPORT")
            box.prop(props, "RESET_PARAMETERS")
            if not props.USE_PATHS:
                box.prop(props, "model_file_path")
                box.prop(props, "extractor_path")
                box.prop(props, "cache_path")
                box.prop(props, "shader_library_path")
            box.prop(props, "USE_ROOT_LOCATION")
            if not props.USE_PATHS and props.USE_ROOT_LOCATION:
                box.prop(prefs, "root_preference")

            if props.USE_PATHS:
                layout.operator("wm.setup_paths", text="Run Experimental Setup")
            else:
                layout.operator("wm.run_setup", text="Run Experimental Setup")
            return
        if props.mode == 'SHADER':
            box.prop(props, "USE_PATHS")

            box.prop(props, "USE_EXTRACTOR")
            if not props.USE_PATHS:
                box.prop(props, "material_file_path")
                box.prop(props, "extractor_path")
                box.prop(props, "cache_path")
            box.prop(props, "USE_ROOT_LOCATION")
            if not props.USE_PATHS and not props.USE_ROOT_LOCATION: box.prop(props, "pathToTextures")
            elif not props.USE_PATHS and props.USE_ROOT_LOCATION: box.prop(prefs, "root_preference")
            box.prop(props, "EMPTY_IMAGES_BEFORE_SETUP")
            box.prop(props, "REPLACE_IMAGES")
            box.prop(props, "RESET_PARAMETERS")
            box.prop(props, "texture_extension")
        if props.USE_PATHS:
            layout.operator("wm.setup_paths", text="Run Setup")
        else:
            layout.operator("wm.run_setup", text="Run Setup")
