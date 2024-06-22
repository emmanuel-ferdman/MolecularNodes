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

import bpy

from . import ui
from . import session
from .io import ops_io
from .io.md import TrajectorySelectionItem
from .io.parse.mda import update_universes
from .props import MolecularNodesObjectProperties
from .ui import pref
from .ui.node_menu import MN_add_node_menu
from .ui.panel import MN_PT_panel, change_style_menu, change_style_node_menu
from bpy.app.handlers import load_post, save_post, frame_change_post

all_classes = (
    ui.CLASSES
    + ops_io
    + [
        MolecularNodesObjectProperties,
        MN_PT_panel,
    ]
    + pref.CLASSES
)


def register():
    # register all of the import operators
    for op in all_classes:
        try:
            bpy.utils.register_class(op)
        except Exception as e:
            print(e)
            pass
    bpy.types.Scene.MNSession = session.MNSession()

    bpy.types.NODE_MT_add.append(MN_add_node_menu)
    bpy.types.Object.mn = bpy.props.PointerProperty(type=MolecularNodesObjectProperties)
    bpy.types.Object.mn_universe_selections = bpy.props.CollectionProperty(
        type=TrajectorySelectionItem
    )

    bpy.types.VIEW3D_MT_object_context_menu.prepend(change_style_menu)
    bpy.types.NODE_MT_context_menu.prepend(change_style_node_menu)
    save_post.append(session._pickle)
    load_post.append(session._load)
    frame_change_post.append(update_universes)


def unregister():
    for op in all_classes:
        try:
            bpy.utils.unregister_class(op)
        except Exception as e:
            print(e)
            pass

    bpy.types.NODE_MT_add.remove(MN_add_node_menu)
    bpy.types.VIEW3D_MT_object_context_menu.remove(change_style_menu)
    bpy.types.NODE_MT_context_menu.remove(change_style_node_menu)
    try:
        save_post.remove(session._pickle)
        load_post.remove(session._load)
        frame_change_post.remove(update_universes)
    except Exception as e:
        print(e)
        pass

    try:
        del bpy.types.Object.mn
        del bpy.types.Object.mn_selection_list
    except AttributeError:
        print("bpy.types.Object.mn not registered, unable to delete")
