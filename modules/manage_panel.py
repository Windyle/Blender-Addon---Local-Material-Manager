import bpy


class LOC_MAT_MANAGE_Panel(bpy.types.Panel):

    bl_idname = 'LOC_MAT_LOAD_PT_manage_panel'
    bl_label = 'Material Manager'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Material Manager'

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, 'preview_material', text='')
        layout.template_ID_preview(context.scene, 'preview_material')

        # preview_row = layout.row()
        layout.operator(
            'loc_mat_load.replace_slot_0', icon='SHADING_RENDERED')
        layout.operator(
            'loc_mat_load.assign_material', icon='MATERIAL')
        layout.operator(
            'loc_mat_load.assign_material_to_faces', icon='UV')

        layout.separator()

        layout.operator(
            'loc_mat_load.unlink_selected', icon='UNLINKED')
        layout.operator(
            'loc_mat_load.clean_unused', icon='BRUSH_DATA')

        layout.separator()

        row = layout.row()
        row.operator(
            'loc_mat_load.mark_asset', icon='ASSET_MANAGER')
        row.operator(
            'loc_mat_load.unmark_asset', icon='X')

        layout.separator()

        layout.operator(
            'loc_mat_load.dialog_delete', icon='TRASH')


def register():
    bpy.utils.register_class(LOC_MAT_MANAGE_Panel)


def unregister():
    bpy.utils.unregister_class(LOC_MAT_MANAGE_Panel)
