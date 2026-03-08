COLOR_SPACE_MAP = {
    'Base Color': 'sRGB',
    'Emission': 'sRGB',
    'Metalness': 'Non-Color',
    'Roughness': 'Non-Color',
    'Specular': 'Non-Color',
    'Normal': 'Non-Color',
    'Alpha': 'Non-Color'
}

EMISSION_FLAGS_FOR_BAKING = ["emission_mask", "multi_tint_and_mask", "emissive_mask"]
shader_exceptions_parameters = [ "Swizzle Vertex Channels" ]

texture_extension_list = [
    ('*.png', 'PNG', 'Use PNG textures'),
    ('*.tga', 'TGA', 'Use TGA textures'),
]

special_reset_rules = {
    'EffectsIntensityStrength': 1,
    'EffectsIntensity X': 1,
    'EffectsIntensity Y': 1,
    'EffectsIntensity Z': 1,
    'EffectsIntensity W': 1,
    'EffectsIntensity2 X': 1,
    'EffectsIntensity2 Y': 1,
    'PanGlobalScale': 1,
    'FPS Value': 30,
    'AOTintColor': tuple([0, 0, 0, 1]),
    'DetailMapDiffuseRange': 100,
    'DetailMapNormalRange': 100,
    'EmissiveTintColor': tuple([1, 1, 1, 1]),
    'EmissiveTintColor Alpha': 1,
    'TimeScalar': 1,
    'UvScale X': 1,
    'UvScale Y': 1,
    'UvScale Z': 1,
    'UvScale W': 1,
    'UVScale01 X': 1,
    'UVScale01 Y': 1,
    'UVScale01 Z': 1,
    'UVScale01 W': 1,
    'UVScale23 X': 1,
    'UVScale23 Y': 1,
    'UVScale23 Z': 1,
    'UVScale23 W': 1,
    'HeightPanScale X': 0,
    'HeightPanScale Y': 0,
    'HeightPanScale Z': 1,
    'HeightPanScale W': 1,
    'AlphaTestValue': 0.5,
    'FacingRoughness': 1,
    'GlancingRoughness': 1,
    'EmissiveFresnelPow': 1,
    'emissiveFade Y': 1,
    'FlickerParam X': 1,
    'GlassColor': tuple([1, 1, 1, 0]),
    'WetBias': -1,
    'Roughness': 0.5,
    'Radius': tuple([1, 0.2, 0.1]),
    'X Scale': 1,
    'Y Scale': 1,
    'HairCapMask X': 1,
    'HairCapMask Y': 1,
    'HairCapMask Z': 1,
    'HairCapMask W': 1,
    'MakeUpMask X': 1,
    'MakeUpMask Y': 1,
    'MakeUpMask Z': 1,
    'MakeUpMask W': 1,
    'RoughnessAtten': 1,
    'ViewExtents W': -1,
    'ViewExtents Z': 0,
    'SSSFactor': 1,
    'BoostMetallic': 0,
    'IOR Boost': 0.5,
    'ExposureVerctor': 0.660,
    'ClearCoat IOR': 1.5,
    'ClearCoat Power': 3.0,
    'LightingBuffer': tuple([1, 1, 1, 1]),
}

special_aliases = {
    "TINT_MASK_PACK_MAP_BLEND": "TINT_MASK_PACK_MAP",
}

special_ignores = {
    "CLOAK": "CLOAK",
    # "EMISSIVE_COMPRESSION = EC_COMPONENT": "EmissiveTintColor",
}

special_skips = {
    "cb0": "cb0",
    "windnoisemap": "windnoisemap",
    "windparams": "windparams",
}

texture_ignores = [
    "BaseMaterialMetal"
]

extractor_commands = {
    "Texture": '{0} --extract-textures --texture-format {2} --cache-dir "{1}" --internal-path "{3}" --output-path "{4}"',
    "Material": '{0} --extract-materials --cache-dir "{1}" --internal-path "{2}" --output-path "{3}"'
}
