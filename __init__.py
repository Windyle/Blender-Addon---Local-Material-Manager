import bpy
import sys
import importlib

bl_info = {
    # required
    'name': 'Local Material Manager',
    'blender': (3, 3, 1),
    'category': '3D View',
    # optional
    'version': (1, 0, 0),
    'author': 'Alberto Denti',
    'description': 'Select a folder with texture images and it will generate a basic node tree automatically',
    'location': 'View3D > Sidebar > Local-Mat'
}


# Set Classes and Module and register them

MODULES = [
    'assign_material',
    'load_material',
    'user_preferences',
    'load_panel',
    'manage_panel',
    '_globals',
    'delete_material',
    'link_manager',
    'mark_asset',
    'clear_preview',
    'displace_modifier'
]

modulesFullNames = {}
for currentModuleName in MODULES:
    modulesFullNames[currentModuleName] = (
        '{}.{}.{}'.format(__name__, 'modules', currentModuleName))

for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(
            currentModuleFullName)
        setattr(globals()[currentModuleFullName],
                'modulesNames', modulesFullNames)


def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()


def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()


if __name__ == '__main__':
    register()
