import bpy

# Set Custom User Preferences Settings


class LOC_MAT_LOAD_TextureIdentifiersPreferences(bpy.types.AddonPreferences):
    bl_idname = 'loc_material_manager'

    colorIdentifierProp: bpy.props.StringProperty(
        name="Color",
        default="_basecolor, _color, _color_a, _base color, _base_color, _col, _albedo, _diffuse, _diff"
    )

    normalIdentifierProp: bpy.props.StringProperty(
        name="Normal",
        default="_normal, _norm, _nrm, _normal_map, _normal map, _normalgl, _nor_gl"
    )

    roughnessIdentifierProp: bpy.props.StringProperty(
        name="Roughness",
        default="_roughness, _rough, _gloss, _spec, _refl"
    )

    metalnessIdentifierProp: bpy.props.StringProperty(
        name="Metalness",
        default="_metalness, _metal, _met, _metallic"
    )

    occlusionIdentifierProp: bpy.props.StringProperty(
        name="AO",
        default="_ao, _occlusion, _ambient_occlusion, _ambient occlusion, _ambientocclusion, _occ"
    )

    displacementIdentifierProp: bpy.props.StringProperty(
        name="Displacement/Height",
        default="_disp, _displacement, _height"
    )

    emissionIdentifierProp: bpy.props.StringProperty(
        name="Emission",
        default="_emission, _emissive"
    )

    transmissionIdentifierProp: bpy.props.StringProperty(
        name="Transmission",
        default="_transmission, _glass"
    )

    alphaIdentifierProp: bpy.props.StringProperty(
        name="Alpha/Opacity",
        default="_alpha, _opacity"
    )

    preloadPreviewIdentifierProp: bpy.props.StringProperty(
        name="Pre-Load Preview",
        default="_preview"
    )

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text='Texture Identifiers:')
        box.prop(self, 'colorIdentifierProp', expand=True)
        box.prop(self, 'normalIdentifierProp', expand=True)
        box.prop(self, 'roughnessIdentifierProp', expand=True)
        box.prop(self, 'metalnessIdentifierProp', expand=True)
        box.prop(self, 'occlusionIdentifierProp', expand=True)
        box.prop(self, 'displacementIdentifierProp', expand=True)
        box.prop(self, 'emissionIdentifierProp', expand=True)
        box.prop(self, 'transmissionIdentifierProp', expand=True)
        box.prop(self, 'alphaIdentifierProp', expand=True)

        preview_box = layout.box()
        preview_box.label(text='Preview Identifier:')
        preview_box.prop(self, 'preloadPreviewIdentifierProp', expand=True)


def register():
    bpy.utils.register_class(LOC_MAT_LOAD_TextureIdentifiersPreferences)


def unregister():
    bpy.utils.unregister_class(LOC_MAT_LOAD_TextureIdentifiersPreferences)
