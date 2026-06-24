import bmesh
import bpy


def process_object(obj):
    if obj.type != 'MESH':
        return
    me = obj.data
    if me.color_attributes:

        mesh = obj.data
        loops = mesh.loops
        polygons = mesh.polygons

        color_attr_names = []
        for att in mesh.color_attributes:
            if att.domain == 'POINT':
                color_attr_names.append(att.name)

        if not color_attr_names:
            return

        for attr_name in color_attr_names:
            if attr_name not in mesh.color_attributes:
                continue

            color_attr = mesh.color_attributes[attr_name]
            if color_attr.is_internal or color_attr.is_required:
                continue

            old_name = color_attr.name
            new_attr = mesh.color_attributes.new(
                name=old_name,
                type=color_attr.data_type,
                domain='CORNER'
            )
            src_data = [0.0] * (len(mesh.vertices) * 4)
            color_attr.data.foreach_get('color', src_data)
            dst_data = [0.0] * (len(loops) * 4)
            for poly in polygons:
                for loop_idx in poly.loop_indices:
                    vert_idx = loops[loop_idx].vertex_index
                    src_idx = vert_idx * 4
                    dst_idx = loop_idx * 4
                    dst_data[dst_idx] = src_data[src_idx]
                    dst_data[dst_idx + 1] = src_data[src_idx + 1]
                    dst_data[dst_idx + 2] = src_data[src_idx + 2]
                    dst_data[dst_idx + 3] = src_data[src_idx + 3]

            new_attr.data.foreach_set('color', dst_data)
            new_attr.data.update()
            mesh.color_attributes.remove(color_attr)
            new_attr.name = old_name
    if not bpy.context.scene.warframe_tools_props.LEVEL_IMPORT:
        me.flip_normals()
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.normal_update()
        bm.to_mesh(me)
        bm.free()
    me.shade_smooth()
