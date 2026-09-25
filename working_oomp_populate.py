
import copy

from oomp_populate_helper import build_oomp_id, write_extras


def apply_plate_details(option):
    """Add the shared OOMP and OOBB metadata for a 90 degree plate beam."""
    width = option["width"]
    height = option["height"]
    thickness = option["thickness"]
    part_name = option.get("part_name", "plate_90_degree")

    description_main = f"{width}_width_{height}_height_{thickness}_mm_depth"

    option["classification"] = "oobb"
    option["type"] = "part"
    option["size"] = part_name
    option["name"] = part_name
    option["color"] = ""
    option["description_main"] = description_main
    option["description_extra"] = ""
    option["manufacturer"] = ""
    option["part_number"] = ""
    option["taxonomy_1"] = "oobb"
    option["taxonomy_2"] = "part"
    option["taxonomy_3"] = part_name
    option["taxonomy_4"] = f"{width}_width"
    option["taxonomy_5"] = f"{height}_height"
    option["taxonomy_6"] = f"{thickness}_mm_depth"
    option["oobb_details"] = {
        "oobb_name": part_name,
        "width": width,
        "height": height,
        "depth": thickness,
        "thickness": thickness,
    }


def main(**kwargs):
    options = []

    # 90 degree plate beams: a one-unit wide (14 mm) square-profile beam,
    # 14 mm deep, running three to fifteen OOBB units long.  Hole pairs
    # alternate down the beam -- vertical m6 + vertical m3, then
    # horizontal m6 + horizontal m3 -- so half the holes pass through the
    # top face and half through the side faces, letting standard OOBB
    # plates bolt on at 90 degrees to each other.
    for length in range(3, 16):
        options.append(
            {
                "width": 1,
                "height": length,
                "thickness": 14,
                "part_name": "plate_90_degree",
            }
        )

    for option in options:
        apply_plate_details(option)

    extras = [copy.deepcopy(option) for option in options]

    import working_oomp_populate_extra_detail

    working_oomp_populate_extra_detail.main(extras=extras)
    write_extras(extras)


if __name__ == "__main__":
    main()
