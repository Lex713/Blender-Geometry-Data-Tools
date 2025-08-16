bl_info = {
    "name": "Geometry Data Tools",
    "author": "Lex713",
    "version": (1, 3),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Misc Tab",
    "description": "Automate clearing geometry data from meshes",
    "category": "3D View",
}

import bpy

# ------------------------------------------------------------
# Operators
# ------------------------------------------------------------

class OBJECT_OT_select_all_meshes(bpy.types.Operator):
    bl_idname = "object.select_all_meshes_custom"
    bl_label = "Select All Mesh Objects"
    bl_description = "Select all mesh objects in the scene"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in context.scene.objects:
            if obj.type == 'MESH':
                obj.select_set(True)
        return {'FINISHED'}


class OBJECT_OT_add_custom_normals(bpy.types.Operator):
    bl_idname = "object.add_custom_split_normals"
    bl_label = "Add Custom Split Normals Data"
    bl_description = "Add custom split normals data to selected mesh objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        original_mode = bpy.context.mode

        for obj in context.selected_objects:
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                try:
                    bpy.ops.mesh.customdata_custom_splitnormals_add()
                    self.report({'INFO'}, f"Added custom normals: {obj.name}")
                except Exception as e:
                    self.report({'WARNING'}, f"{obj.name}: Failed - {str(e)}")
                bpy.ops.object.mode_set(mode='OBJECT')

        if original_mode != 'OBJECT':
            try:
                bpy.ops.object.mode_set(mode=original_mode)
            except:
                pass

        return {'FINISHED'}


class OBJECT_OT_clear_custom_normals(bpy.types.Operator):
    bl_idname = "object.clear_custom_split_normals"
    bl_label = "Clear Custom Split Normals"
    bl_description = "Clear custom split normals from selected mesh objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        original_mode = bpy.context.mode

        for obj in context.selected_objects:
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                try:
                    bpy.ops.mesh.customdata_custom_splitnormals_clear()
                    self.report({'INFO'}, f"Cleared custom normals: {obj.name}")
                except Exception as e:
                    self.report({'WARNING'}, f"{obj.name}: Failed - {str(e)}")
                bpy.ops.object.mode_set(mode='OBJECT')

        if original_mode != 'OBJECT':
            try:
                bpy.ops.object.mode_set(mode=original_mode)
            except:
                pass

        return {'FINISHED'}


class OBJECT_OT_clear_sculpt_mask(bpy.types.Operator):
    bl_idname = "object.clear_sculpt_mask"
    bl_label = "Clear Sculpt Mask Data"
    bl_description = "Clear sculpt mask data from selected mesh objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                if obj.data.vertex_paint_mask is None:
                    self.report({'INFO'}, f"No sculpt mask data on: {obj.name}")
                    continue
                try:
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.customdata_mask_clear()
                    bpy.ops.object.mode_set(mode='OBJECT')
                    self.report({'INFO'}, f"Cleared sculpt mask: {obj.name}")
                except Exception as e:
                    self.report({'WARNING'}, f"{obj.name}: Failed - {str(e)}")
        return {'FINISHED'}


class OBJECT_OT_clear_skin_data(bpy.types.Operator):
    bl_idname = "object.clear_skin_data"
    bl_label = "Clear Skin Data"
    bl_description = "Clear skin modifier vertex data from selected mesh objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                if not obj.data.skin_vertices:
                    self.report({'INFO'}, f"No skin data on: {obj.name}")
                    continue
                try:
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.customdata_skin_clear()
                    bpy.ops.object.mode_set(mode='OBJECT')
                    self.report({'INFO'}, f"Cleared skin data: {obj.name}")
                except Exception as e:
                    self.report({'WARNING'}, f"{obj.name}: Failed - {str(e)}")
        return {'FINISHED'}


# ------------------------------------------------------------
# Panel
# ------------------------------------------------------------

class VIEW3D_PT_mesh_data_tools(bpy.types.Panel):
    bl_label = "Geometry Data Tools"
    bl_idname = "VIEW3D_PT_mesh_data_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Misc'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.select_all_meshes_custom", icon='MESH_DATA')

        layout.separator()

        layout.label(text="Custom Normals:")
        layout.operator("object.add_custom_split_normals", icon='ADD')
        layout.operator("object.clear_custom_split_normals", icon='X')

        layout.separator()

        layout.label(text="Other Data:")
        layout.operator("object.clear_sculpt_mask", icon='BRUSH_DATA')
        layout.operator("object.clear_skin_data", icon='MOD_SKIN')


# ------------------------------------------------------------
# Registration
# ------------------------------------------------------------

classes = (
    OBJECT_OT_select_all_meshes,
    OBJECT_OT_add_custom_normals,
    OBJECT_OT_clear_custom_normals,
    OBJECT_OT_clear_sculpt_mask,
    OBJECT_OT_clear_skin_data,
    VIEW3D_PT_mesh_data_tools,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()