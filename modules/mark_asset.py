import bpy


class LOC_MAT_LOAD_mark_asset(bpy.types.Operator):
    bl_idname = 'loc_mat_load.mark_asset'
    bl_label = 'Mark as Asset'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        if context.scene.preview_material != None:
            bpy.data.materials[context.scene.preview_material.name].asset_mark()

            self.report({'INFO'}, 'Material succesfully marked as Asset')
        return {'FINISHED'}


class LOC_MAT_LOAD_unmark_asset(bpy.types.Operator):
    bl_idname = 'loc_mat_load.unmark_asset'
    bl_label = 'Unmark Asset'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        if context.scene.preview_material != None:
            bpy.data.materials[context.scene.preview_material.name].asset_clear()

            self.report({'INFO'}, 'Material succesfully unmarked from Assets')
        return {'FINISHED'}


def register():
    bpy.utils.register_class(LOC_MAT_LOAD_mark_asset)
    bpy.utils.register_class(LOC_MAT_LOAD_unmark_asset)


def unregister():
    bpy.utils.unregister_class(LOC_MAT_LOAD_mark_asset)
    bpy.utils.unregister_class(LOC_MAT_LOAD_unmark_asset)
