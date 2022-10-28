import bpy
import os


def UpdateTexturePreview(self, context):
    dir = context.scene.conf_path.replace('\\', '/')[:-1]

    if dir == '/' or dir == '' or dir == '[Directory not containing supported files':
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
        context.scene.conf_path = '[Directory not containing supported files]'
        return

    imgPath = dir + '/' + preview_image
    img = bpy.data.images.load(filepath=imgPath)

    if 'PRELOAD PREVIEW' in bpy.data.images:
        bpy.data.images.remove(bpy.data.images['PRELOAD PREVIEW'])

    img.name = 'PRELOAD PREVIEW'

    context.scene.preview_texture = img
# Panel


class LOC_MAT_LOAD_Panel(bpy.types.Panel):

    bl_idname = 'LOC_MAT_LOAD_PT_main_panel'
    bl_label = 'Local Material Manager'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Material Manager'

    def draw(self, context):
        layout = self.layout

        load_box = layout.box()
        load_box.label(text='Load New Material')
        load_box.prop(context.scene, 'conf_path')

        load_box.template_ID_preview(context.scene, 'preview_texture')
        load_box.operator('loc_mat_load.load_material', icon='ADD')

        preview_box = layout.box()
        preview_box.label(text='Material Preview')

        preview_box.prop(context.scene, 'preview_material', text='')
        preview_box.template_ID_preview(context.scene, 'preview_material')

        # preview_row = preview_box.row()
        preview_box.operator(
            'loc_mat_load.assign_material', icon='SHADING_RENDERED')
        preview_box.operator(
            'loc_mat_load.assign_material_to_faces', icon='MATERIAL')
        preview_box.operator(
            'loc_mat_load.replace_slot_0', icon='SELECT_SET')


def register():
    bpy.types.Scene.conf_path = bpy.props.StringProperty(
        name="",
        default="",
        description="Choose the path of the material you want to load",
        subtype='DIR_PATH',
        update=UpdateTexturePreview
    )

    bpy.utils.register_class(LOC_MAT_LOAD_Panel)


def unregister():
    bpy.utils.unregister_class(LOC_MAT_LOAD_Panel)
