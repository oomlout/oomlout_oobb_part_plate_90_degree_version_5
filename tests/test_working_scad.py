import unittest

import working_scad


# The 3dpr clearance radii the hole library resolves for the named sizes.
HOLE_RADII = {"m3": 1.8, "m6": 3.25}


class Plate90DegreeHoleTests(unittest.TestCase):
    def test_pattern_starts_vertical_m6_vertical_m3_then_horizontal(self):
        holes = working_scad._get_plate_90_degree_holes(3, 14, 14)

        pattern = [(hole["orientation"], hole["radius_name"]) for hole in holes]
        self.assertEqual(
            [
                ("vertical", "m6"),
                ("vertical", "m3"),
                ("horizontal", "m6"),
                ("horizontal", "m3"),
                ("vertical", "m6"),
            ],
            pattern,
        )

    def test_orientation_pairs_alternate_for_every_length(self):
        for length in range(3, 16):
            holes = working_scad._get_plate_90_degree_holes(length, 14, 14)

            expected = []
            for pair in range(length):
                orientation = "vertical" if pair % 2 == 0 else "horizontal"
                expected.append(orientation)
                if pair < length - 1:
                    expected.append(orientation)

            self.assertEqual(
                expected, [hole["orientation"] for hole in holes]
            )

    def test_every_beam_has_one_m6_per_unit_and_one_fewer_m3(self):
        for length in range(3, 16):
            radii = [
                hole["radius_name"]
                for hole in working_scad._get_plate_90_degree_holes(length, 14, 14)
            ]

            self.assertEqual(length, radii.count("m6"))
            self.assertEqual(length - 1, radii.count("m3"))

    def test_holes_march_the_beam_on_the_half_pitch(self):
        for length in range(3, 16):
            holes = working_scad._get_plate_90_degree_holes(length, 14, 14)

            self.assertEqual(-7.5 * (length - 1), holes[0]["pos"][0])
            self.assertEqual(7.5 * (length - 1), holes[-1]["pos"][0])
            gaps = [b["pos"][0] - a["pos"][0] for a, b in zip(holes, holes[1:])]
            self.assertTrue(all(gap == 7.5 for gap in gaps))

    def test_end_holes_keep_a_three_mm_wall_to_the_beam_ends(self):
        for length in range(3, 16):
            beam_half_length = length * 15 / 2 - 0.5
            holes = working_scad._get_plate_90_degree_holes(length, 14, 14)

            for hole in (holes[0], holes[-1]):
                radius = HOLE_RADII[hole["radius_name"]]
                wall = beam_half_length - abs(hole["pos"][0]) - radius
                self.assertGreaterEqual(wall, 3)

    def test_vertical_holes_drill_through_the_top_face(self):
        for length in range(3, 16):
            holes = working_scad._get_plate_90_degree_holes(length, 14, 14)

            for hole in holes:
                if hole["orientation"] != "vertical":
                    continue
                self.assertEqual([0, 0, 0], hole["rot"])
                self.assertEqual(0, hole["pos"][1])
                self.assertLess(hole["pos"][2], 0)
                self.assertGreater(hole["pos"][2] + hole["depth"], 14)

    def test_horizontal_holes_drill_through_the_sides_at_mid_height(self):
        for length in range(3, 16):
            holes = working_scad._get_plate_90_degree_holes(length, 14, 14)

            for hole in holes:
                if hole["orientation"] != "horizontal":
                    continue
                self.assertEqual([90, 0, 0], hole["rot"])
                self.assertEqual(7, hole["pos"][2])
                self.assertGreater(hole["pos"][1], 7)
                self.assertLess(hole["pos"][1] - hole["depth"], -7)
                # The bore keeps a wall to the beam's top and bottom faces.
                radius = HOLE_RADII[hole["radius_name"]]
                self.assertGreaterEqual(7 - radius, 3)


if __name__ == "__main__":
    unittest.main()
