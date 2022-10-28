import bpy


class delete_popup(bpy.types.Operator):
    bl_idname = 'loc_mat_load.dialog_delete'
    bl_label = 'Delete'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        if context.scene.preview_material != None:
            bpy.data.materials.remove(context.scene.preview_material)

            self.report({'INFO'}, 'Material Succesfully Deleted')
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


def register():
    bpy.utils.register_class(delete_popup)


def unregister():
    bpy.utils.unregister_class(delete_popup)
