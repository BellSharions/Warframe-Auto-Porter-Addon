import bpy
import os
from pathlib import Path


class RunSetupOperator(bpy.types.Operator):
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


class SetupPathsOperator(bpy.types.Operator):
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
            self.pathToRig = bpy.context.scene.warframe_tools_props.rig_path
            if bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION and (self.pathToRig is None or self.pathToRig is ""):
                steps.append(('pathToRig', 'Select Rig Blend File', 'file', '*.blend'))
        elif mode == 'BAKE':
            return steps
        elif mode == '3DPRINT':
            steps.append(('normal_to_height_path', 'Select Normal Map File', 'file', '*'))
        elif mode == 'EXPERIMENTAL':
            steps.append(('model_file_path', 'Select Model File (.glb)', 'file', '*.glb'))
            self.shader_library_path = bpy.context.scene.warframe_tools_props.shader_library_path
            if not self.shader_library_path:
                steps.append(('shader_library_path', 'Select Shader Library Folder', 'directory', ''))
            self.root = bpy.context.scene.warframe_tools_props.root
            if bpy.context.scene.warframe_tools_props.USE_ROOT_LOCATION and (self.root is None or self.root is ""):
                steps.append(('root', 'Select Root Directory', 'directory', ''))
            if bpy.context.scene.warframe_tools_props.USE_EXTRACTOR:
                self.extractor_path = bpy.context.scene.warframe_tools_props.extractor_path
                self.cache_path = bpy.context.scene.warframe_tools_props.cache_path
                if not self.extractor_path:
                    steps.append(('extractor_path', 'Select Extractor CLI', 'file', '*'))
                if not self.cache_path:
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
