import bpy

# Loader Material Assign Class


class LOC_MAT_LOAD_assign_material(bpy.types.Operator):
    bl_idname = 'loc_mat_load.assign_material'
    bl_label = 'Append to Selected Objects'

    def execute(self, context):
        if context.scene.preview_material != None:
            selection_names = [
                obj.name for obj in bpy.context.selected_objects]

            for obj_name in selection_names:
                obj = bpy.data.objects[obj_name]
                if context.scene.preview_material.name in obj.data.materials:
                    self.report(
                        {'WARNING'}, 'Material already assigned to a slot of the selected object.')
                else:
                    obj.data.materials.append(
                        context.scene.preview_material)
                    self.report(
                        {'INFO'}, 'Material successfully assigned to selected object')

            # Update viewport to see the changes
            for win in bpy.context.window_manager.windows:
                for area in win.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
        else:
            self.report({'WARNING'}, "Can't assign undefined material")
        return {'FINISHED'}


class LOC_MAT_LOAD_assign_material_to_faces(bpy.types.Operator):
    bl_idname = 'loc_mat_load.assign_material_to_faces'
    bl_label = 'Assign to Selected Faces'

    def execute(self, context):
        if context.scene.preview_material != None:
            selection_names = [
                obj.name for obj in bpy.context.selected_objects]

            for obj_name in selection_names:
                obj = bpy.data.objects[obj_name]
                if obj.mode == 'EDIT':
                    if context.scene.preview_material.name not in obj.data.materials:
                        obj.data.materials.append(
                            context.scene.preview_material)

                    obj.active_material_index = obj.data.materials.find(
                        context.scene.preview_material.name)
                    bpy.ops.object.material_slot_assign()

                    obj.active_material_index = 0

            # Update viewport to see the changes
            for win in bpy.context.window_manager.windows:
                for area in win.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
        else:
            self.report({'WARNING'}, "Can't assign undefined material")
        return {'FINISHED'}


class LOC_MAT_LOAD_replace_slot_0(bpy.types.Operator):
    bl_idname = 'loc_mat_load.replace_slot_0'
    bl_label = 'Set First Material Slot for Selected Objects'

    def execute(self, context):
        if context.scene.preview_material != None:
            selection_names = [
                obj.name for obj in bpy.context.selected_objects]

            for obj_name in selection_names:
                obj = bpy.data.objects[obj_name]
                if obj.data.materials:
                    if context.scene.preview_material.name in obj.data.materials:
                        self.report(
                            {'WARNING'}, 'Material already assigned to a slot of the selected object.')
                    else:
                        obj.data.materials[0] = context.scene.preview_material
                else:
                    obj.data.materials.append(
                        context.scene.preview_material)
                    self.report(
                        {'INFO'}, 'Material successfully assigned to the first material slot of selected object')

            # Update viewport to see the changes
            for win in bpy.context.window_manager.windows:
                for area in win.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
        else:
            self.report({'WARNING'}, "Can't assign undefined material")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(LOC_MAT_LOAD_assign_material)
    bpy.utils.register_class(LOC_MAT_LOAD_assign_material_to_faces)
    bpy.utils.register_class(LOC_MAT_LOAD_replace_slot_0)


def unregister():
    bpy.utils.unregister_class(LOC_MAT_LOAD_assign_material)
    bpy.utils.unregister_class(LOC_MAT_LOAD_assign_material_to_faces)
    bpy.utils.unregister_class(LOC_MAT_LOAD_replace_slot_0)
