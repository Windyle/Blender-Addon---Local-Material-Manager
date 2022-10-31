import bpy


class LOC_MAT_LOAD_displace_modifier(bpy.types.Operator):
    bl_idname = 'loc_mat_load.displace_modifier'
    bl_label = 'Add Displace'

    def execute(self, context):
        mat = context.scene.preview_material

        if mat.use_nodes:
            ntree = mat.node_tree
            node = ntree.nodes.get("Bump", None)
            if node is not None:
                selection_names = [
                    obj.name for obj in bpy.context.selected_objects]

                for obj_name in selection_names:
                    obj = bpy.data.objects[obj_name]

                    if 'loc_manager_Displace' not in obj.modifiers:
                        height_tex_name = 'loc_manager_' + obj_name + '_disp_texture'

                        if height_tex_name not in bpy.data.textures:
                            height_tex = bpy.data.textures.new(
                                height_tex_name, type='IMAGE')
                        else:
                            height_tex = bpy.data.textures[height_tex_name]

                        socket = node.inputs[2]

                        link = next(
                            link for link in mat.node_tree.links if link.to_socket == socket)

                        image_node = link.from_node

                        height_tex.image = image_node.image

                        disp_mod = obj.modifiers.new(
                            "loc_manager_Displace", type='DISPLACE')
                        disp_mod.texture = height_tex
                        disp_mod.texture_coords = 'UV'
                        disp_mod.strength = 0.2

                self.report(
                    {'INFO'}, 'Displacement Modifiers successfully applied')
            else:
                self.report(
                    {'WARNING'}, 'Material does not have a displacement texture')

        return {'FINISHED'}


class LOC_MAT_LOAD_remove_displace_modifier(bpy.types.Operator):
    bl_idname = 'loc_mat_load.remove_displace_modifier'
    bl_label = 'Remove Displace'

    def execute(self, context):
        mat = context.scene.preview_material

        if mat.use_nodes:
            ntree = mat.node_tree
            node = ntree.nodes.get("Bump", None)
            if node is not None:
                selection_names = [
                    obj.name for obj in bpy.context.selected_objects]

                for obj_name in selection_names:
                    obj = bpy.data.objects[obj_name]

                    if 'loc_manager_Displace' in obj.modifiers:
                        obj.modifiers.remove(
                            obj.modifiers['loc_manager_Displace'])

                        self.report(
                            {'INFO'}, 'Displacement Modifiers successfully removed')
            else:
                self.report(
                    {'WARNING'}, 'Material does not have a displacement texture')

        return {'FINISHED'}


def register():
    bpy.utils.register_class(LOC_MAT_LOAD_displace_modifier)
    bpy.utils.register_class(LOC_MAT_LOAD_remove_displace_modifier)


def unregister():
    bpy.utils.unregister_class(LOC_MAT_LOAD_displace_modifier)
    bpy.utils.unregister_class(LOC_MAT_LOAD_remove_displace_modifier)
