bl_info = {
    "name": "Color Temperature",
    "blender": (2, 80, 0),
    "category": "Lighting",
    "description": "Allows you to set color temperature for lights",
    "author": "Edouard J. Simon",
    "version": (1, 0)
}

import bpy
from . import main_script

def register():
    main_script.register()

def unregister():
    main_script.unregister()

if __name__ == "__main__":
    register()
