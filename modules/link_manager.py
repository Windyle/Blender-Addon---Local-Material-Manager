import bpy


class LOC_MAT_LOAD_unlink_selected(bpy.types.Operator):
    bl_idname = 'loc_mat_load.unlink_selected'
    bl_label = 'Unlink from Selected Objects'

    def execute(self, context):
        if context.scene.preview_material != None:
            selection_names = [
                obj.name for obj in bpy.context.selected_objects]

            for obj_name in selection_names:
                obj = bpy.data.objects[obj_name]
                if context.scene.preview_material.name not in obj.data.materials:
                    self.report(
                        {'WARNING'}, 'The material is not linked to the selected object')
                    return {'FINISHED'}

                obj.data.materials[obj.data.materials.find(
                    context.scene.preview_material.name)] = None

                bpy.ops.object.material_slot_remove_unused({
                    'object': obj
                })

            # Update viewport to see the changes
            for win in bpy.context.window_manager.windows:
                for area in win.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
        else:
            self.report({'WARNING'}, "Can't unlink undefined material")
        return {'FINISHED'}


class LOC_MAT_LOAD_clean_unused(bpy.types.Operator):
    bl_idname = 'loc_mat_load.clean_unused'
    bl_label = 'Clean Unused from Selected Objects'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        vl_objs = bpy.context.view_layer.objects
        for obj in vl_objs.selected:
            if obj.type == 'MESH':
                vl_objs.active = obj
                bpy.ops.object.material_slot_remove_unused()

        # Update viewport to see the changes
        for win in bpy.context.window_manager.windows:
            for area in win.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


def register():
    bpy.utils.register_class(LOC_MAT_LOAD_clean_unused)
    bpy.utils.register_class(LOC_MAT_LOAD_unlink_selected)


def unregister():
    bpy.utils.unregister_class(LOC_MAT_LOAD_clean_unused)
    bpy.utils.unregister_class(LOC_MAT_LOAD_unlink_selected)
