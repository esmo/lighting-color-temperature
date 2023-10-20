bl_info = {
    "name": "Color Temperature Add-on",
    "blender": (2, 80, 0),
    "category": "Lighting",
    "description": "Allows you to set color temperature for lights",
    "author": "Your Name",
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
            ('2700', 'Incandescent Bulbs', '2700K'),
            ('3000', 'Warm White LED', '3000K'),
            ('3500', 'Halogen Lamp', '3500K'),
            ('4000', 'Cool White Fluorescent', '4000K'),
            ('4100', 'Moonlight', '4100K'),
            ('4500', 'Overcast Sky', '4500K'),
            ('5000', 'Daylight', '5000K'),
            ('5500', 'Noon Sunlight', '5500K'),
            ('6000', 'Bright Midday Sun', '6000K'),
            ('6500', 'Lightly Overcast Sky', '6500K'),
            ('7000', 'Shade', '7000K'),
            ('8000', 'Blue Sky', '8000K'),
            ('9000', 'Open Shade on Clear Day', '9000K'),
            ('10000', 'Heavy Overcast Sky or Sunset', '10000K'),
            ('11000', 'Deep Blue Sky', '11000K'),
            ('12000', 'Arctic Light', '12000K')]


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

def set_color_temperature(light, temp):
    temp = temp / 100
    if temp <= 66:
        red = 255
        green = temp
        green = 99.4708025861 * math.log(green) - 161.1195681661
    else:
        red = temp - 60
        red = 329.698727446 * (red ** -0.1332047592)
        green = temp - 60
        green = 288.1221695283 * (green ** -0.0755148492)

    if temp >= 66:
        blue = 255
    elif temp <= 19:
        blue = 0
    else:
        blue = temp - 10
        blue = 138.5177312231 * math.log(blue) - 305.0447927307

    red = min(max(red, 0), 255)/255
    green = min(max(green, 0), 255)/255
    blue = min(max(blue, 0), 255)/255

    light.color = (red, green, blue)

# Create EnumProperty
bpy.types.Light.temperature_presets = bpy.props.EnumProperty(
    items=temperature_presets_callback,
    name="Temperature Presets",
    description="Select a color temperature preset",
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
    bl_parent_id = "DATA_PT_context_light"

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
    bpy.types.Light.color_temperature = FloatProperty(name="Color Temperature", default=5500, update=update_color_temperature_from_slider)

def unregister():
    bpy.utils.unregister_class(LIGHT_PT_color_temperature)
    del bpy.types.Light.color_temperature
    del bpy.types.Light.temperature_presets

if __name__ == "__main__":
    register()
