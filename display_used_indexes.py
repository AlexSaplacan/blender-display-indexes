bl_info = {
    "name": "Used Indexes",
    "author": "Alex Saplacan",
    "version": (0, 4),
    "blender": (2, 90, 0),
    "location": "Properties",
    "description": "Displays the Material or object indexes already used.",
    "warning": "",
    "wiki_url": "",
    "category": "UI",
    }


import bpy


def draw_indexes(self, context, idx_list):

    draw_text = " ".join(str(i) for i in idx_list)

    layout = self.layout
    flow = layout.grid_flow(
        row_major=True,
        columns=0,
        even_columns=True,
        even_rows=False,
        align=False
    )
    col = flow.column()
    col.separator()
    col.label(text="Indexes already used:")
    col.label(text=draw_text)


def get_scene_obj_indexes(context):
    objects = context.scene.objects
    ob_used_idx = {obj.pass_index for obj in objects}
    return ob_used_idx


def get_mat_indexes():
    materials = bpy.data.materials
    mat_used_idx = {mat.pass_index for mat in materials}
    return mat_used_idx


def draw_obj_used_indexes(self, context):
    """
    Display the Object IDs already used
    """
    idxs = get_scene_obj_indexes(bpy.context)
    draw_indexes(self, context, idxs)


def draw_mat_used_indexes(self, context):
    """
    Display IDs already used by other materials.
    """
    mat_used_idx = get_mat_indexes()
    draw_indexes(self, context, mat_used_idx)


def test_get_scene_obj_idx_returns_expected():
    # GIVEN a object with object index 2
    cube = bpy.context.scene.objects['Cube']
    cube.pass_index = 2
    # WHEN get_scene_obj_indexes is ran
    result = get_scene_obj_indexes(bpy.context)
    # THEN it returns the exepected result
    assert result == {0, 2}


def test_get_mat_obj_idx_returns_expected():
    # GIVEN a material with an index 2
    mat = bpy.data.materials['Material']
    mat.pass_index = 5
    # WHEN get_mat_indexes is called
    result = get_mat_indexes()
    # THEN it returns the exepected result 
    assert result == {0, 5}


def register():
    bpy.types.OBJECT_PT_relations.append(draw_obj_used_indexes)
    bpy.types.EEVEE_MATERIAL_PT_settings.append(draw_mat_used_indexes)


def unregister():
    bpy.types.OBJECT_PT_relations.remove(draw_obj_used_indexes)
    bpy.types.EEVEE_MATERIAL_PT_settings.remove(draw_mat_used_indexes)


if __name__ == "__main__":
    register()
