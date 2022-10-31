import bpy
import os

# Manage Texture by Type


def GetTexture(currentDir, material, files, type):
    def switch(type):
        if type == 'COLOR':
            return {'filters': bpy.context.preferences.addons['loc_material_manager'].preferences.colorIdentifierProp, 'colorspace': 'sRGB'}
        elif type == 'NORMAL':
            return {'filters': bpy.context.preferences.addons['loc_material_manager'].preferences.normalIdentifierProp, 'colorspace': 'Non-Color'}
        elif type == 'ROUGHNESS':
            return {'filters': bpy.context.preferences.addons['loc_material_manager'].preferences.roughnessIdentifierProp, 'colorspace': 'Non-Color'}
        elif type == 'METAL':
            return {'filters': bpy.context.preferences.addons['loc_material_manager'].preferences.metalnessIdentifierProp, 'colorspace': 'Non-Color'}
        elif type == 'OCCLUSION':
            return {'filters': bpy.context.preferences.addons['loc_material_manager'].preferences.occlusionIdentifierProp, 'colorspace': 'Non-Color'}
        elif type == 'DISPLACEMENT':
            return {'filters': bpy.context.preferences.addons['loc_material_manager'].preferences.displacementIdentifierProp, 'colorspace': 'Non-Color'}
        elif type == 'EMISSION':
            return {'filters': bpy.context.preferences.addons['loc_material_manager'].preferences.emissionIdentifierProp, 'colorspace': 'sRGB'}
        elif type == 'TRANSMISSION':
            return {'filters': bpy.context.preferences.addons['loc_material_manager'].preferences.transmissionIdentifierProp, 'colorspace': 'Non-Color'}
        elif type == 'ALPHA':
            return {'filters': bpy.context.preferences.addons['loc_material_manager'].preferences.alphaIdentifierProp, 'colorspace': 'Non-Color'}

    type_obj = switch(type)
    filters = type_obj['filters'].split(', ')
    supported_extensions = bpy.types.Scene.loc_mat_supported_img_extensions.split(
        ', ')

    imgFile = ""
    for file in files:
        if imgFile == "":
            for filter in filters:
                if filter in file.lower() and imgFile == "":
                    for ext in supported_extensions:
                        if file.lower().endswith(ext) and imgFile == "":
                            imgFile = file

    if imgFile == "":
        return None

    imgPath = currentDir + '/' + imgFile

    img = bpy.data.images.load(filepath=imgPath, check_existing=True)
    tex_node = material.node_tree.nodes.new('ShaderNodeTexImage')
    tex_node.image = img
    tex_node.extension = 'REPEAT'
    tex_node.image.colorspace_settings.name = type_obj['colorspace']

    return tex_node

# Generate Material Function


def GenerateMaterial(directory):
    currentDir = directory[:-1].replace('\\', '/')
    strMaterialName = currentDir.split('/')[-1]

    currentDir = bpy.path.abspath(currentDir)

    if strMaterialName in bpy.data.materials:
        return bpy.data.materials[strMaterialName]

    material = bpy.data.materials.new(name=strMaterialName)
    material.use_nodes = True

    # Create a reference to the material output
    material_output = material.node_tree.nodes.get('Material Output')
    Principled_BSDF = material.node_tree.nodes.get('Principled BSDF')

    # Get Current Folder Files
    files = []
    for file in os.listdir(currentDir):
        if os.path.isfile(os.path.join(currentDir, file)):
            files.append(file)

    # Manage Color
    texImage_node = GetTexture(currentDir, material, files, 'COLOR')

    # Manage Ambient Occlusion
    texOcc_node = GetTexture(currentDir, material, files, 'OCCLUSION')

    # Manage Roughness
    texRoughness_node = GetTexture(currentDir, material, files, 'ROUGHNESS')

    # Manage Metalness
    texMetalness_node = GetTexture(currentDir, material, files, 'METAL')

    # Manage Normal
    texNormal_node = GetTexture(currentDir, material, files, 'NORMAL')

    # Manage Displacement
    texDisplacement_node = GetTexture(
        currentDir, material, files, 'DISPLACEMENT')

    # Manage Emission
    texEmission_node = GetTexture(currentDir, material, files, 'EMISSION')

    # Manage Opacity
    texOpacity_node = GetTexture(currentDir, material, files, 'ALPHA')

    # Manage Transmission
    texTransmission_node = GetTexture(
        currentDir, material, files, 'TRANSMISSION')

    # set location of node
    material_output.location = (400, 20)
    Principled_BSDF.location = (0, 0)

    # Handle Ambient Occlusion Presence
    if texOcc_node != None and texImage_node != None:
        overlay_node = material.node_tree.nodes.new('ShaderNodeMixRGB')
        overlay_node.blend_type = 'OVERLAY'
        overlay_node.location = (-200, 300)
        texImage_node.location = (-600, 600)
        texOcc_node.location = (-600, 300)
        material.node_tree.links.new(
            texOcc_node.outputs[1], overlay_node.inputs[0])
        material.node_tree.links.new(
            texImage_node.outputs[0], overlay_node.inputs[1])
        material.node_tree.links.new(
            texOcc_node.outputs[0], overlay_node.inputs[2])
        material.node_tree.links.new(
            overlay_node.outputs[0], Principled_BSDF.inputs[0])
    elif texImage_node != None:
        texImage_node.location = (-600, 300)
        material.node_tree.links.new(
            texImage_node.outputs[0], Principled_BSDF.inputs[0])
    elif texOcc_node != None:
        overlay_node = material.node_tree.nodes.new('ShaderNodeMixRGB')
        overlay_node.blend_type = 'OVERLAY'
        overlay_node.location = (-200, 300)
        texOcc_node.location = (-600, 300)
        material.node_tree.links.new(
            texOcc_node.outputs[1], overlay_node.inputs[0])
        material.node_tree.links.new(
            texOcc_node.outputs[0], overlay_node.inputs[2])
        material.node_tree.links.new(
            overlay_node.outputs[0], Principled_BSDF.inputs[0])

    # Handle Roughness Presence
    if texRoughness_node != None:
        rough_color_ramp_node = material.node_tree.nodes.new(
            'ShaderNodeValToRGB')
        rough_color_ramp_node.location = (-300, -350)
        texRoughness_node.location = (-600, -350)
        material.node_tree.links.new(
            rough_color_ramp_node.outputs[0], Principled_BSDF.inputs[9])
        material.node_tree.links.new(
            texRoughness_node.outputs[0], rough_color_ramp_node.inputs[0])

    # Handle Metalness Presence
    if texMetalness_node != None:
        texMetalness_node.location = (-600, -50)
        material.node_tree.links.new(
            texMetalness_node.outputs[0], Principled_BSDF.inputs[6])

    # Handle Normal & Displacement Presence
    if texNormal_node != None and texDisplacement_node != None:
        bump_node = material.node_tree.nodes.new('ShaderNodeBump')
        bump_node.inputs[0].default_value = 0.1
        bump_node.inputs[1].default_value = 0.5
        bump_node.location = (-300, -650)
        texDisplacement_node.location = (-600, -650)
        normal_map_node = material.node_tree.nodes.new('ShaderNodeNormalMap')
        normal_map_node.location = (-300, -950)
        texNormal_node.location = (-600, -950)
        material.node_tree.links.new(
            texNormal_node.outputs[0], normal_map_node.inputs[1])
        material.node_tree.links.new(
            texDisplacement_node.outputs[0], bump_node.inputs[2])
        material.node_tree.links.new(
            normal_map_node.outputs[0], bump_node.inputs[3])
        material.node_tree.links.new(
            bump_node.outputs[0], Principled_BSDF.inputs[22])
        material.node_tree.links.new(
            bump_node.outputs[0], Principled_BSDF.inputs[23])
    elif texNormal_node != None:  # Handle Normal Presence
        normal_map_node = material.node_tree.nodes.new('ShaderNodeNormalMap')
        normal_map_node.location = (-300, -650)
        texNormal_node.location = (-600, -650)
        material.node_tree.links.new(
            texNormal_node.outputs[0], normal_map_node.inputs[1])
        material.node_tree.links.new(
            normal_map_node.outputs[0], Principled_BSDF.inputs[22])
        material.node_tree.links.new(
            normal_map_node.outputs[0], Principled_BSDF.inputs[23])
    elif texDisplacement_node != None:  # Handle Displacement Presence
        bump_node = material.node_tree.nodes.new('ShaderNodeBump')
        bump_node.location = (-300, -650)
        texDisplacement_node.location = (-600, -650)
        bump_node.inputs[0].default_value = 0.1
        bump_node.inputs[1].default_value = 0.5
        material.node_tree.links.new(
            texDisplacement_node.outputs[0], bump_node.inputs[2])
        material.node_tree.links.new(
            bump_node.outputs[0], Principled_BSDF.inputs[22])
        material.node_tree.links.new(
            bump_node.outputs[0], Principled_BSDF.inputs[23])

    # Handle Emission Presence
    if texEmission_node != None:
        texEmission_node.location = (-900, -350)
        material.node_tree.links.new(
            texEmission_node.outputs[0], Principled_BSDF.inputs[20])

    # Handle Opacity Presence
    if texOpacity_node != None:
        material.blend_method = 'CLIP'
        texTransparent_node = material.node_tree.nodes.new(
            'ShaderNodeBsdfTransparent')
        mix_shader_node = material.node_tree.nodes.new('ShaderNodeMixShader')
        texOpacity_node.location = (0, 300)
        texTransparent_node.location = (300, 300)
        mix_shader_node.location = (300, 0)
        material_output.location = (600, 0)
        material.node_tree.links.new(
            Principled_BSDF.outputs[0], mix_shader_node.inputs[2])
        material.node_tree.links.new(
            texTransparent_node.outputs[0], mix_shader_node.inputs[1])
        material.node_tree.links.new(
            texOpacity_node.outputs[0], mix_shader_node.inputs[0])
        material.node_tree.links.new(
            mix_shader_node.outputs[0], material_output.inputs[0])
    else:
        material.blend_method = 'OPAQUE'

    # Handle Transmission Presence
    if texTransmission_node != None:
        texTransmission_node.location = (-900, -650)
        material.node_tree.links.new(
            texTransmission_node.outputs[0], Principled_BSDF.inputs[17])

    return material

# Load Material Class


class LOC_MAT_LOAD_load_material(bpy.types.Operator):
    bl_idname = 'loc_mat_load.load_material'
    bl_label = 'Load Material'

    def execute(self, context):
        mat_directory = bpy.context.scene.conf_path

        # If the path is empty return
        if mat_directory.strip() == '':
            return {'FINISHED'}

        res = GenerateMaterial(mat_directory)

        context.scene.preview_material = res

        # Reset conf_path property
        bpy.context.scene.conf_path = ''

        if 'PRELOAD PREVIEW' in bpy.data.images:
            bpy.data.images.remove(bpy.data.images['PRELOAD PREVIEW'])

        return {'FINISHED'}


def register():
    bpy.utils.register_class(LOC_MAT_LOAD_load_material)


def unregister():
    bpy.utils.unregister_class(LOC_MAT_LOAD_load_material)
