$fn = 50;

difference() {
	union() {
		hull() {
			translate(v = [-57.5, 5.0, 0]) {
				cylinder(h = 14, r = 2.0);
			}
			translate(v = [57.5, 5.0, 0]) {
				cylinder(h = 14, r = 2.0);
			}
			translate(v = [-57.5, -5.0, 0]) {
				cylinder(h = 14, r = 2.0);
			}
			translate(v = [57.5, -5.0, 0]) {
				cylinder(h = 14, r = 2.0);
			}
		}
	}
	union() {
		translate(v = [-52.5, 0, -2.0]) {
			cylinder(h = 18.0, r = 3.25);
		}
		translate(v = [-45.0, 0, -2.0]) {
			cylinder(h = 18.0, r = 1.8);
		}
		translate(v = [-37.5, 9.0, 7.0]) {
			rotate(a = [90, 0, 0]) {
				cylinder(h = 18.0, r = 3.25);
			}
		}
		translate(v = [-30.0, 9.0, 7.0]) {
			rotate(a = [90, 0, 0]) {
				cylinder(h = 18.0, r = 1.8);
			}
		}
		translate(v = [-22.5, 0, -2.0]) {
			cylinder(h = 18.0, r = 3.25);
		}
		translate(v = [-15.0, 0, -2.0]) {
			cylinder(h = 18.0, r = 1.8);
		}
		translate(v = [-7.5, 9.0, 7.0]) {
			rotate(a = [90, 0, 0]) {
				cylinder(h = 18.0, r = 3.25);
			}
		}
		translate(v = [0.0, 9.0, 7.0]) {
			rotate(a = [90, 0, 0]) {
				cylinder(h = 18.0, r = 1.8);
			}
		}
		translate(v = [7.5, 0, -2.0]) {
			cylinder(h = 18.0, r = 3.25);
		}
		translate(v = [15.0, 0, -2.0]) {
			cylinder(h = 18.0, r = 1.8);
		}
		translate(v = [22.5, 9.0, 7.0]) {
			rotate(a = [90, 0, 0]) {
				cylinder(h = 18.0, r = 3.25);
			}
		}
		translate(v = [30.0, 9.0, 7.0]) {
			rotate(a = [90, 0, 0]) {
				cylinder(h = 18.0, r = 1.8);
			}
		}
		translate(v = [37.5, 0, -2.0]) {
			cylinder(h = 18.0, r = 3.25);
		}
		translate(v = [45.0, 0, -2.0]) {
			cylinder(h = 18.0, r = 1.8);
		}
		translate(v = [52.5, 9.0, 7.0]) {
			rotate(a = [90, 0, 0]) {
				cylinder(h = 18.0, r = 3.25);
			}
		}
	}
}
