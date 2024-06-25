"""
Importing molecular dynamics trajectories and associated files.
"""

__name__ = "MolecularNodes.trajectory"
__author__ = "Brady Johnston"

import bpy
import MDAnalysis as mda

from ...blender import path_resolve
from .universe import MNUniverse
from bpy.props import StringProperty

bpy.types.Scene.MN_import_md_topology = StringProperty(
    name="Topology",
    description="File path for the toplogy file for the trajectory",
    subtype="FILE_PATH",
    maxlen=0,
)
bpy.types.Scene.MN_import_md_trajectory = StringProperty(
    name="Trajectory",
    description="File path for the trajectory file for the trajectory",
    subtype="FILE_PATH",
    maxlen=0,
)
bpy.types.Scene.MN_import_md_name = StringProperty(
    name="Name",
    description="Name of the molecule on import",
    default="NewTrajectory",
    maxlen=0,
)


def load(
    top,
    traj,
    name="NewTrajectory",
    style="spheres",
    subframes: int = 0,
):
    top = path_resolve(top)
    traj = path_resolve(traj)

    universe = mda.Universe(top, traj)

    mn_universe = MNUniverse(universe=universe)

    mn_universe.create_model(name=name, style=style, subframes=subframes)

    return mn_universe


class MN_OT_Import_Protein_MD(bpy.types.Operator):
    bl_idname = "mn.import_protein_md"
    bl_label = "Import Protein MD"
    bl_description = "Load molecular dynamics trajectory"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        top = scene.MN_import_md_topology
        traj = scene.MN_import_md_trajectory
        name = scene.MN_import_md_name

        mu = load(
            top=top,
            traj=traj,
            name=name,
            style=scene.MN_import_style,
        )

        context.view_layer.objects.active = mu.object
        context.scene.frame_start = 0
        context.scene.frame_end = mu.universe.trajectory.n_frames

        self.report(
            {"INFO"},
            message=f"Imported '{top}' as {name} "
            f"with {str(mu.universe.trajectory.n_frames)} "
            f"frames from '{traj}'.",
        )

        return {"FINISHED"}


# UI


def panel(layout, scene):
    layout.label(text="Load MD Trajectories", icon="FILE_TICK")
    layout.separator()
    col = layout.column(align=True)
    row_import = col.row()
    row_import.prop(scene, "MN_import_md_name")
    row_import.operator("mn.import_protein_md", text="Load")
    col.separator()
    col.prop(scene, "MN_import_md_topology")
    col.prop(scene, "MN_import_md_trajectory")

    layout.separator()
    layout.label(text="Options", icon="MODIFIER")
    row = layout.row()
    row.prop(scene, "MN_import_node_setup", text="")
    col = row.column()
    col.prop(scene, "MN_import_style")
    col.enabled = scene.MN_import_node_setup


CLASSES = [
    MN_OT_Import_Protein_MD,
]
