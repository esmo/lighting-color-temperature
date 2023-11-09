import math
import bpy
from bpy.props import FloatProperty, EnumProperty
from bpy.types import Light, Panel

from .cieValues import cie_1931_values, cie_1964_values
from .presets import preset_items

temperature_calculation_options = [
    ('CIE1931', 'CIE 1931', 'Use values based on CIE 1931 color space'),
    ('CIE1964', 'CIE 1964', 'Use values based on CIE 1964 color space'),
    ('TannerHelland', 'Tanner Helland',
     'Compute values based on algorithm by Tanner Helland')
]

skip_update = False;

def update_color_temperature_from_slider(self, context):
    global skip_update
    light = context.light
    set_color_temperature(light)
    used_preset = '0'
    for preset_item in preset_items:
        if int(preset_item[0]) == light.color_temperature:
            used_preset = preset_item[0]
            break
    skip_update = True;
    light.temperature_presets = used_preset
    skip_update = False;

def update_color_temperature_from_preset(self, context):
    global skip_update;
    if(not skip_update):
        light = context.light
        light.color_temperature = int(self.temperature_presets)
        set_color_temperature(light)


def set_color_temperature_calculation_method(self, context):
    light = context.light
    light.temperature_calculation_method = self.temperature_calculation_method
    set_color_temperature(light)

# Callback to update RGB values based on color temperature


def set_color_temperature(light):
    if (light.temperature_calculation_method == "TannerHelland"):
        red, green, blue = compute_color_temperature_tanner_helland(
            light)
        light.color = (red, green, blue)
    else:
        red, green, blue = compute_color_temperature_cie(
            light)
        light.color = (red, green, blue)

# Based on a color table computed by Mitchell Charity
# using the CIE 1931 or CIE 1964 color space
# http://www.vendian.org/mncharity/dir3/blackbody/UnstableURLs/bbr_color.html


def compute_color_temperature_cie(light):
    temp = light.color_temperature
    precomputed_values = cie_1931_values if light.temperature_calculation_method == "CIE1931" else cie_1964_values

    sorted_keys = sorted(precomputed_values.keys())
    lower_key = max(k for k in sorted_keys if float(k) <= temp)
    upper_key = min(k for k in sorted_keys if float(k) >= temp)

    if lower_key == upper_key:
        red, green, blue = precomputed_values[lower_key]
        return float(red), float(green), float(blue)

    # linear interpolation of the 2 values

    lower_rgb = precomputed_values[lower_key]
    upper_rgb = precomputed_values[upper_key]

    ratio = (temp - float(lower_key)) / (float(upper_key) - float(lower_key))

    lower_red = float(lower_rgb[0])
    lower_green = float(lower_rgb[1])
    lower_blue = float(lower_rgb[2])

    upper_red = float(upper_rgb[0])
    upper_green = float(upper_rgb[1])
    upper_blue = float(upper_rgb[2])

    red = (lower_red + (upper_red - lower_red) * ratio) / 255
    green = (lower_green + (upper_green - lower_green) * ratio) / 255
    blue = (lower_blue + (upper_blue - lower_blue) * ratio) / 255
    return red, green, blue

# Based on an algorithm by Tanner Helland
# https://tannerhelland.com/2012/09/18/convert-temperature-rgb-algorithm-code.html


def compute_color_temperature_tanner_helland(light):
    kelvin = light.color_temperature / 100.0
    red, green, blue = 0.0, 0.0, 0.0

    if kelvin <= 66:
        red = 255
        green = kelvin
        green = 99.4708025861 * math.log(green) - 161.1195681661
        if kelvin <= 19:
            blue = 0
        else:
            blue = kelvin - 10
            blue = 138.5177312231 * math.log(blue) - 305.0447927307
    else:
        red = kelvin - 60
        red = 329.698727446 * (red ** -0.1332047592)
        green = kelvin - 60
        green = 288.1221695283 * (green ** -0.0755148492)
        blue = 255

    red = max(0, min(255, red)) / 255.0
    green = max(0, min(255, green)) / 255.0
    blue = max(0, min(255, blue)) / 255.0

    return red, green, blue


# Create EnumProperty
Light.temperature_presets = EnumProperty(
    items=preset_items,
    name="Temperature Presets",
    description="Color temperature preset",
    default="6500",
    update=update_color_temperature_from_preset
)


# Adding custom property for color temperature
Light.color_temperature = FloatProperty(
    name="Color Temperature",
    description="Set the color temperature of the light",
    default=6500.0,
    min=1000.0,
    max=40000.0,
    update=update_color_temperature_from_slider
)

# Adding custom property for color temperature
Light.temperature_calculation_method = EnumProperty(
    items=temperature_calculation_options,
    name="Calculation Method",
    description="Choose the method by which the color temperature is calculated",
    default='CIE1931',
    update=set_color_temperature_calculation_method
)

# Creating custom panel


class LIGHT_PT_color_temperature(Panel):
    bl_label = "Color Temperature"
    bl_idname = "LIGHT_PT_color_temperature"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}
    bl_category = "Light"

    @ classmethod
    def poll(cls, context):
        return context.light is not None

    def draw(self, context):
        layout = self.layout
        light = context.light
        # Add preset dropdown
        layout.prop(light, 'temperature_presets', text="Preset")
        # Add manual color temperature slider
        layout.prop(light, "color_temperature")
        # Add calculation method dropdown
        layout.prop(light, "temperature_calculation_method",
                    text="Calculation Method")


def register():
    bpy.utils.register_class(LIGHT_PT_color_temperature)
    Light.color_temperature = FloatProperty(
        name="Color Temperature",
        default=6500,
        update=update_color_temperature_from_slider
    )


def unregister():
    bpy.utils.unregister_class(LIGHT_PT_color_temperature)
    del Light.color_temperature
    # del Light.temperature_presets
    # del Light.temperature_calculation_method
