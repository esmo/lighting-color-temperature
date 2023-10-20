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

# Function to update RGB values based on color temperature
def update_color_temperature(self, context):
    light = context.light
    temp = light.color_temperature

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

# Adding custom property for color temperature
bpy.types.Light.color_temperature = FloatProperty(
    name="Color Temperature",
    description="Set the color temperature of the light",
    default=6500.0,
    min=1000.0,
    max=10000.0,
    update=update_color_temperature
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
        layout.prop(light, "color_temperature")
def register():
    bpy.utils.register_class(LIGHT_PT_color_temperature)

def unregister():
    bpy.utils.unregister_class(LIGHT_PT_color_temperature)

if __name__ == "__main__":
    register()
