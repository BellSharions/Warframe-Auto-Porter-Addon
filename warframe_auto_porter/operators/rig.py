import bpy
import os

from ..materials.matcher import get_rig_items


class AppendRigOperator(bpy.types.Operator):
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
