# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Exporting .obj for GMod",
    "author" : "Opti1337",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (1, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import (BoolProperty, FloatProperty, StringProperty)
import re

class ExportObjForGmod(bpy.types.Operator, ExportHelper):
    """НЮХАЙ БЕБРУ))))))))"""
    bl_idname = "export_scene.obj_for_gmod"
    bl_label = "Export .obj for GMod"

    filename_ext = ".obj"

    global_scale_setting: FloatProperty(name="Scale", min=0.01, max=1000.0, default=39.37)

    optimize_setting: bpy.props.BoolProperty(name="Optimize .obj", default=True)

    filepath: StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        bpy.ops.export_scene.obj(
            filepath=self.filepath,
            use_selection=True,
            axis_forward="-X", 
            axis_up="Z",
            use_mesh_modifiers=True,
            use_normals=True,
            use_uvs=True,
            use_triangles=True,
            use_materials=False,
            global_scale=self.global_scale_setting
        )

        if self.optimize_setting:
            file = open(self.filepath, 'r+')
            obj = file.read()

            # Remove comments
            obj = re.sub("^#.*$[\r\n]*", "", obj, flags=re.MULTILINE)

            # Remove "l" tags
            obj = re.sub("\nl\s\d+\s\d+", "", obj, flags=re.MULTILINE)

            # Optimize vertexes
            obj = re.sub("(v\s\-?\d+\.\d{3})\d*(\s\-?\d+\.\d{3})\d*(\s\-?\d+\.\d{3})\d*", r"\1\2\3", obj, flags=re.MULTILINE)

            # Optimize textures
            obj = re.sub("(vt\s\-?\d+\.\d{3})\d*(\s\-?\d+\.\d{3})\d*((\s\-?\d+\.\d{3})\d*)?", r"\1\2\3", obj, flags=re.MULTILINE)

            # Optimize normals
            obj = re.sub("(vn\s\-?\d+\.\d{3})\d*(\s\-?\d+\.\d{3})\d*(\s\-?\d+\.\d{3})\d*", r"\1\2\3", obj, flags=re.MULTILINE)

            # Optimize vertex parameters
            obj = re.sub("(vp\s\-?\d+\.\d{3})\d*((\s\-?\d+\.\d{3})\d*){0,2}", r"\1\2", obj, flags=re.MULTILINE)
    
            file.seek(0)
            file.write(obj)
            file.truncate()

        return {'FINISHED'}

def export_button(self, context):
    self.layout.operator_context = 'INVOKE_DEFAULT'
    self.layout.operator(ExportObjForGmod.bl_idname, text=ExportObjForGmod.bl_label)

def register():
    bpy.utils.register_class(ExportObjForGmod)
    bpy.types.TOPBAR_MT_file_export.append(export_button)

def unregister():
    bpy.utils.unregister_class(ExportObjForGmod)
    bpy.types.TOPBAR_MT_file_export.remove(export_button)

if __name__ == "__main__":
    register()