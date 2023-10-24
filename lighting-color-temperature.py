bl_info = {
    "name": "Color Temperature",
    "blender": (2, 80, 0),
    "category": "Lighting",
    "description": "Allows you to set color temperature for lights",
    "author": "Edouard J. Simon",
    "version": (1, 0)
}

import bpy
from bpy.types import Panel
from bpy.props import FloatProperty
import math

# Define preset values
def temperature_presets_callback(scene, context):
     return [('1000', 'Candlelight', '1000K'),
             ('2000', 'Antique Filament Bulbs', '2000K'),
             ('2700', 'Soft White Incandescent Bulbs', '2700K'),
             ('3000', 'Evening Sunlight', '3000K'),
             ('3500', 'Neutral White LED', '3500K'),
             ('4000', 'Cool White Fluorescent', '4000K'),
             ('4100', 'Moonlight', '4100K'),
             ('4500', 'Overcast Morning/Evening', '4500K'),
             ('5000', 'Morning Sunlight', '5000K'),
             ('5500', 'Midday Sunlight', '5500K'),
             ('6000', 'Direct Midday Sunlight', '6000K'),
             ('6500', 'Standard Daylight', '6500K'),
             ('7000', 'Cloudy Sky', '7000K'),
             ('8000', 'Partly Cloudy Sky', '8000K'),
             ('9000', 'Shade in Clear Sky', '9000K'),
             ('10000', 'Overcast Sky', '10000K'),
             ('11000', 'Deep Blue Sky', '11000K'),
             ('12000', 'Arctic Sky', '12000K')]


# Function to update RGB values based on color temperature
def update_color_temperature_from_slider(self, context):
    light = context.light
    temp = light.color_temperature
    set_color_temperature(light, temp)

# Function to update RGB values based on color temperature
def update_color_temperature_from_preset(self, context):
    light = context.light
    temp = int(self.temperature_presets)
    light.color_temperature = temp
    set_color_temperature(light, temp)

def set_color_temperature(light, kelvin):
    kelvin = kelvin / 100.0
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
        green = 288.1221695283 * (green ** -0.0755148492 )
        blue = 255

    red = max(0, min(255, red)) / 255.0
    green = max(0, min(255, green)) / 255.0
    blue = max(0, min(255, blue)) / 255.0

    #print("RGB for {}K: {}".format(kelvin, (red, green, blue)))

    light.color = (red, green, blue)

preset_items = [('1000', 'Candlelight', '1000K'),
        ('2000', 'Antique Filament Bulbs', '2000K'),
        ('2700', 'Soft White Incandescent Bulbs', '2700K'),
        ('3000', 'Evening Sunlight', '3000K'),
        ('3500', 'Neutral White LED', '3500K'),
        ('4000', 'Cool White Fluorescent', '4000K'),
        ('4100', 'Moonlight', '4100K'),
        ('4500', 'Overcast Morning/Evening', '4500K'),
        ('5000', 'Morning Sunlight', '5000K'),
        ('5500', 'Midday Sunlight', '5500K'),
        ('6000', 'Direct Midday Sunlight', '6000K'),
        ('6500', 'Standard Daylight', '6500K'),
        ('7000', 'Cloudy Sky', '7000K'),
        ('8000', 'Partly Cloudy Sky', '8000K'),
        ('9000', 'Shade in Clear Sky', '9000K'),
        ('10000', 'Overcast Sky', '10000K'),
        ('11000', 'Deep Blue Sky', '11000K'),
        ('12000', 'Arctic Sky', '12000K')]

# Create EnumProperty
bpy.types.Light.temperature_presets = bpy.props.EnumProperty(
    items=preset_items,
    name="Temperature Presets",
    description="Color temperature preset",
    default="6500",
    update=update_color_temperature_from_preset
)


# Adding custom property for color temperature
bpy.types.Light.color_temperature = FloatProperty(
    name="Color Temperature",
    description="Set the color temperature of the light",
    default=6500.0,
    min=1000.0,
    max=12000.0,
    update=update_color_temperature_from_slider
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

    @classmethod
    def poll(cls, context):
        return context.light is not None

    def draw(self, context):
        layout = self.layout
        light = context.light
        # Add preset dropdown
        layout.prop(light, 'temperature_presets', text="Presets")
        # Add manual color temperature slider
        layout.prop(light, "color_temperature")

def register():
    bpy.utils.register_class(LIGHT_PT_color_temperature)
    bpy.types.Light.color_temperature = FloatProperty(name="Color Temperature", default=6500, update=update_color_temperature_from_slider)

def unregister():
    bpy.utils.unregister_class(LIGHT_PT_color_temperature)
    del bpy.types.Light.color_temperature
    del bpy.types.Light.temperature_presets

if __name__ == "__main__":
    register()
