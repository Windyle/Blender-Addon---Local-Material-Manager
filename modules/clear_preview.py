import bpy


class LOC_MAT_LOAD_clear_preview(bpy.types.Operator):
    bl_idname = 'loc_mat_load.clear_preview'
    bl_label = 'Clear'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        context.scene.conf_path = ''

        if 'PRELOAD PREVIEW' in bpy.data.images:
            bpy.data.images.remove(bpy.data.images['PRELOAD PREVIEW'])

        return {'FINISHED'}


def register():
    bpy.utils.register_class(LOC_MAT_LOAD_clear_preview)


def unregister():
    bpy.utils.unregister_class(LOC_MAT_LOAD_clear_preview)
