import bpy
import os


class invalid_dir_popup(bpy.types.Operator):
    bl_idname = 'dialog.invalid_dir'
    bl_label = 'The selected directory does not contain any supported file'

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def UpdateTexturePreview(self, context):
    dir = context.scene.conf_path.replace('\\', '/')[:-1]

    if dir == '/' or dir == '':
        return

    # Get Current Folder Files
    preview_image = ''

    preview_identifiers = bpy.context.preferences.addons[
        'loc_material_manager'].preferences.preloadPreviewIdentifierProp.split(', ')
    color_identifiers = bpy.context.preferences.addons[
        'loc_material_manager'].preferences.colorIdentifierProp.split(', ')
    supported_extensions = bpy.types.Scene.loc_mat_supported_img_extensions.split(
        ', ')

    for file in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, file)):
            if preview_image == '':
                for filter in preview_identifiers:
                    if filter in file.lower() and preview_image == '':
                        for ext in supported_extensions:
                            if file.lower().endswith(ext) and preview_image == '':
                                preview_image = file
    for file in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, file)):
            if preview_image == '':
                for filter in color_identifiers:
                    if filter in file.lower() and preview_image == '':
                        for ext in supported_extensions:
                            if file.lower().endswith(ext) and preview_image == '':
                                preview_image = file

    for file in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, file)):
            if preview_image == '':
                for ext in supported_extensions:
                    if file.lower().endswith(ext) and preview_image == '':
                        preview_image = file

    if preview_image == '':
        bpy.ops.dialog.invalid_dir('INVOKE_DEFAULT')
        context.scene.conf_path = ''
        return

    imgPath = dir + '/' + preview_image
    img = bpy.data.images.load(filepath=imgPath)

    if 'PRELOAD PREVIEW' in bpy.data.images:
        bpy.data.images.remove(bpy.data.images['PRELOAD PREVIEW'])

    img.name = 'PRELOAD PREVIEW'

    context.scene.preview_texture = img
# Panel


class LOC_MAT_LOAD_Panel(bpy.types.Panel):

    bl_idname = 'LOC_MAT_LOAD_PT_load_panel'
    bl_label = 'Import Tool'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Material Manager'

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, 'conf_path')

        layout.template_ID_preview(context.scene, 'preview_texture')

        row = layout.row()
        row.operator('loc_mat_load.load_material', icon='ADD')
        row.operator('loc_mat_load.clear_preview', icon='BRUSH_DATA')


def register():
    bpy.types.Scene.conf_path = bpy.props.StringProperty(
        name="",
        default="",
        description="Choose the path of the material you want to load",
        subtype='DIR_PATH',
        update=UpdateTexturePreview
    )

    bpy.utils.register_class(LOC_MAT_LOAD_Panel)
    bpy.utils.register_class(invalid_dir_popup)


def unregister():
    bpy.utils.unregister_class(LOC_MAT_LOAD_Panel)
    bpy.utils.unregister_class(invalid_dir_popup)
