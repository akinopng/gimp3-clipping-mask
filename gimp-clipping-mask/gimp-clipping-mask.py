#!/usr/bin/env python3
import gi
gi.require_version("Gimp", "3.0")
from gi.repository import Gimp
from gi.repository import GLib
import sys


def clipping_mask_run(procedure, run_mode, image, drawables, config, data):
    Gimp.context_push()
    image.undo_group_start()
    try:
        top = drawables[0]
        parent = top.get_parent()
        if parent is None:
            siblings = [l for l in image.get_layers()]
        elif isinstance(parent, Gimp.GroupLayer):
            siblings = [c for c in parent.get_children()]
        else:
            return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, GLib.Error())
        try:
            pos = siblings.index(top)
        except ValueError:
            return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, GLib.Error())
        if pos == len(siblings) - 1:
            return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, GLib.Error())
        bottom = siblings[pos + 1]
        if isinstance(bottom, Gimp.GroupLayer):
            return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, GLib.Error())
        group = Gimp.GroupLayer.new(image)
        group.set_name("Clipping Group")
        if parent is None:
            image.insert_layer(group, None, image.get_item_position(bottom))
        else:
            image.insert_layer(group, parent, parent.get_item_position(bottom))
        image.reorder_item(top, group, 0)
        image.reorder_item(bottom, group, 1)
        Gimp.Image.select_item(image, Gimp.ChannelOps.REPLACE, bottom)
        mask = group.create_mask(Gimp.AddMaskType.SELECTION)
        group.add_mask(mask)
        group.set_visible(True)
        Gimp.displays_flush()
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())
    except Exception as e:
        err = GLib.Error()
        err.message = repr(e)
        return procedure.new_return_values(Gimp.PDBStatusType.EXECUTION_ERROR, err)
    finally:
        image.undo_group_end()
        Gimp.context_pop()


class ClippingMaskPlugIn(Gimp.PlugIn):
    def do_set_i18n(self, procname):
        return False, None, None

    def do_query_procedures(self):
        return ["python-fu-clipping-mask"]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(
            self, name, Gimp.PDBProcType.PLUGIN,
            clipping_mask_run, None
        )
        procedure.set_image_types("RGB*, GRAY*")
        procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.DRAWABLE)
        procedure.set_documentation(
            "Create Clipping Mask (Group Method)",
            "Creates a clipping mask by grouping the active layer with the layer below it.",
            "python-fu-clipping-mask"
        )
        procedure.set_menu_label("_Clipping Mask")
        procedure.set_attribution("akino", "akino", "2026")
        procedure.add_menu_path("<Image>/Filters/Generic")
        return procedure


Gimp.main(ClippingMaskPlugIn.__gtype__, sys.argv)
