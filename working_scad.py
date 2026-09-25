import copy
import math
import oobb
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    typ = scad_help.get_typ(**kwargs)
    oomp_mode = "project"
    #oomp_mode = "oobb"
    filt = ""
    build_variables = scad_help.get_build_variables(typ, filter=filt)
    if True:
        kwargs["filter"] = build_variables["filter"]
        kwargs["save_type"] = build_variables["save_type"]
        kwargs["navigation"] = build_variables["navigation"]
        kwargs["overwrite"] = build_variables["overwrite"]
        kwargs["modes"] = build_variables["modes"]
        kwargs["oomp_mode"] = oomp_mode
        kwargs["oomp_run"] = build_variables["oomp_run"]
    parts = get_parts(kwargs, oomp_mode)

    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    if kwargs["navigation"]:
        oobb_style = False
        sort = scad_help.get_navigation_sort(oobb_style=oobb_style)
        scad_help.generate_navigation(sort=sort)

def get_parts(kwargs, oomp_mode):
    parts = []

    #load parts from parts/folder/working.yaml
    parts_directory = os.path.join(os.path.dirname(__file__), "parts")
    if not os.path.isdir(parts_directory):
        return parts

    for folder in os.listdir(parts_directory):
        folder_path = os.path.join(parts_directory, folder)
        if not os.path.isdir(folder_path):
            continue

        working_yaml_path = os.path.join(folder_path, "working.yaml")
        if not os.path.isfile(working_yaml_path):
            continue

        with open(working_yaml_path, "r", encoding="utf-8") as infile:
            loaded_part = yaml.safe_load(infile)

        if not isinstance(loaded_part, dict):
            continue

        oobb_details = loaded_part.get("oobb_details")
        if not isinstance(oobb_details, dict):
            continue

        part = loaded_part

        part_kwargs = copy.deepcopy(kwargs)
        part_kwargs.update(copy.deepcopy(loaded_part.get("kwargs", {})))
        part_kwargs.update(copy.deepcopy(oobb_details))
        part["kwargs"] = part_kwargs
        part["oobb_name"] = part.get("oobb_name", oobb_details.get("oobb_name", "default"))

        if oomp_mode == "oobb":
            part["kwargs"]["oomp_size"] = part["oobb_name"]

        parts.append(part)


    return parts

def get_base(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("depth", 3)
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")



    #add plate
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "positive"
        p3["shape"] = f"oobb_plate"
        p3["depth"] = depth
        #p3["holes"] = True         uncomment to include default holes
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        p3["pos"] = pos1
        oobb.append_full(thing,**p3)

    #add holes seperate
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "p"
        p3["shape"] = f"oobb_holes"
        p3["both_holes"] = True
        p3["depth"] = depth
        p3["holes"] = "perimeter"
        #p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        p3["pos"] = pos1
        oobb.append_full(thing,**p3)

    #add a test screw_countersunk
    if True:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "p"
        p3["shape"] = f"screw_countersunk"
        p3["depth"] = depth
        p3["radius_name"] = "m3"
        pos1 = copy.deepcopy(pos)
        pos1[2] += depth
        p3["pos"] = pos1
        p3["m"] = "#"
        oobb.append_full(thing,**p3)

    if prepare_print:
        scad_help.prepare_base_for_print(thing, pos, **kwargs)


# 90 degree plate beam: a one-unit wide square-profile beam whose hole
# pairs alternate vertical (through the top face) and horizontal (through
# the side faces) so standard OOBB plates bolt on at 90 degrees to each
# other.
PLATE_90_DEGREE_CORNER_RADIUS = 2.0
PLATE_90_DEGREE_HOLE_PITCH = 7.5
PLATE_90_DEGREE_HOLE_OVERHANG = 2.0


def _get_plate_90_degree_holes(length, width_mm, depth_mm):
    """Return the alternating hole definitions for one beam.

    The holes march down the beam on the regular OOBB half pitch: an m6 on
    every 15 mm grid point with an m3 between each pair.  They are grouped
    in pairs that start on each m6, and the pairs alternate orientation --
    vertical m6 + vertical m3, then horizontal m6 + horizontal m3, and so
    on -- so half the holes pass through the top face and half through the
    side faces.  Vertical holes are drilled down from above; horizontal
    holes start outside one side, at the beam's mid height, and cut clean
    through both sides thanks to the overhang.
    """
    holes = []
    for index in range(length * 2 - 1):
        along = (index - (length - 1)) * PLATE_90_DEGREE_HOLE_PITCH
        vertical = (index // 2) % 2 == 0
        overhang = PLATE_90_DEGREE_HOLE_OVERHANG
        if vertical:
            pos = [along, 0, -overhang]
            rot = [0, 0, 0]
            depth = depth_mm + 2 * overhang
        else:
            pos = [along, width_mm / 2 + overhang, depth_mm / 2]
            rot = [90, 0, 0]
            depth = width_mm + 2 * overhang
        holes.append(
            {
                "pos": pos,
                "rot": rot,
                "depth": depth,
                "radius_name": "m6" if index % 2 == 0 else "m3",
                "orientation": "vertical" if vertical else "horizontal",
            }
        )
    return holes


def get_plate_90_degree(thing, **kwargs):
    """Build a 90 degree plate beam.

    A one-unit wide square-profile beam, 14 mm across and 14 mm deep,
    running three to fifteen OOBB units long with 2 mm rounded corners.
    Hole pairs alternate orientation down its length: vertical m6 +
    vertical m3, then horizontal m6 + horizontal m3.  The vertical holes
    pass through the top face so a plate bolts flat against the beam; the
    horizontal holes pass through the sides so a second plate bolts on at
    90 degrees to the first.
    """
    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    length = kwargs.get("height", 3)
    depth = kwargs.get("depth", kwargs.get("thickness", 14))
    pos = kwargs.get("pos", [0, 0, 0])

    length_mm = length * 15 - 1
    width_mm = width * 15 - 1

    # Solid beam with 2 mm rounded corners, sitting on z = 0.  The
    # rounded rectangle's pos anchors its bottom face.
    beam_pos = copy.deepcopy(pos)
    oobb.append_full(
        thing,
        type="positive",
        shape="rounded_rectangle",
        size=[length_mm, width_mm, depth],
        pos=beam_pos,
        radius=PLATE_90_DEGREE_CORNER_RADIUS,
    )

    # The alternating vertical and horizontal hole pairs.
    for hole in _get_plate_90_degree_holes(length, width_mm, depth):
        hole_pos = [
            pos[0] + hole["pos"][0],
            pos[1] + hole["pos"][1],
            pos[2] + hole["pos"][2],
        ]
        oobb.append_full(
            thing,
            type="negative",
            shape="oobb_hole",
            pos=hole_pos,
            rot=hole["rot"],
            depth=hole["depth"],
            radius_name=hole["radius_name"],
        )

    if prepare_print:
        scad_help.prepare_base_for_print(thing, pos, **kwargs)


def get_hole_cover(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("depth", 3)
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")

    diameter = kwargs.get("diameter", 10)
    clearance = kwargs.get("clearance", 0.5)
    thickness_wall = 2
    depth_taper = 3
    depth_top = 2
    diameter_top_extra = 10
    radius_gap=6
    diameter_top_taper = 5

    #add cylinder
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_cylinder"
    dep = depth - depth_taper
    p3["depth"] = dep
    p3["radius"] = (diameter-clearance)/2
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth_taper + dep/2
    p3["pos"] = pos1
    oobb.append_full(thing,**p3)

    #add cylinder taper using radius_1 and radius_2
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_cylinder"
    p3["depth"] = depth_taper
    p3["radius_2"] = (diameter-clearance)/2
    p3["radius_1"] = (diameter+clearance-thickness_wall)/2
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth_taper/2
    p3["pos"] = pos1
    oobb.append_full(thing,**p3)

    #add top cylinder
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_cylinder"
    p3["depth"] = depth_top
    dia = diameter+diameter_top_extra
    p3["radius_2"] = (dia-diameter_top_taper)/2
    p3["radius_1"] = (dia)/2
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth-depth_top/2
    p3["pos"] = pos1
    oobb.append_full(thing,**p3)


    #add hole
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"oobb_cylinder"
    p3["depth"] = depth - depth_top/2
    p3["radius"] = (diameter+clearance-thickness_wall)/2

    pos1 = copy.deepcopy(pos)
    pos1[2] += depth/2 - depth_top/2
    p3["pos"] = pos1
    #p3["m"] = "#"
    oobb.append_full(thing,**p3)


    #diameter_top 30
    #add hole_top
    diameter_top_hole = 30
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"oobb_cylinder"
    p3["depth"] = depth_top
    p3["radius"] = (diameter_top_hole)/2
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth - depth_top/2

    p3["pos"] = pos1
    p3["m"] = "#"
    oobb.append_full(thing,**p3)

    pos1 = copy.deepcopy(pos)
    pos1[1] += 100



    if prepare_print:
        scad_help.prepare_base_for_print(thing, pos, **kwargs)


if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)
