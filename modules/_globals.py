import bpy


def register():
    bpy.types.Scene.preview_material = bpy.props.PointerProperty(
        type=bpy.types.Material)
    bpy.types.Scene.preview_texture = bpy.props.PointerProperty(
        type=bpy.types.Image)
    bpy.types.Scene.loc_mat_supported_img_extensions = '.png, .jpg, .jpeg, .tiff, .exr'
