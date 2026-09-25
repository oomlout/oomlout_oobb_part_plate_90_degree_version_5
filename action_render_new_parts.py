import os

import opsc


def main():
    folders = sorted(
        folder
        for folder in os.listdir("parts")
        if "degree_max" in folder
    )
    print(f"rendering {len(folders)} parts")
    for folder in folders:
        scad = os.path.join("parts", folder, "3dpr.scad")
        if not os.path.isfile(scad):
            print(f"missing scad: {scad}")
            continue
        print(f"rendering {folder}")
        opsc.saveToAll(scad)
        # The published parts only ship the png and stl exports.
        for extension in (".dxf", ".svg"):
            path = scad.replace(".scad", extension)
            if os.path.exists(path):
                os.remove(path)
    print("render complete")


if __name__ == "__main__":
    main()
