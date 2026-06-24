import bpy


def cleanup_textures(operator, material, new_image_names):
    if not material.use_nodes:
        return
    unused_images = new_image_names

    for image_name in unused_images:
        image = bpy.data.images.get(image_name)
        if image:
            try:
                bpy.data.images.remove(image)
                operator.report({'INFO'}, f"Removed unused image: {image_name}")
            except Exception as e:
                operator.report({'WARNING'}, f"Could not remove image {image_name}: {str(e)}")
