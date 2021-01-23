$fn = 100;
stand_height = 8;

// tolerance for fitting parts together
gap = 0.25;

// who would have though an m5 screw would be 5mm
// adjust this so the screw threads hold
m5_diameter = 5;

// for camera holder
mount_screw_radius = 5.25 / 2;
mount_screw_length = 6;
height = 25;

thickness = 3;

union() {
    difference() {
        linear_extrude(height) square([
            stand_height + thickness * 2,
            stand_height + thickness * 2
        ], center=true);
        
        translate([0, 0, thickness])
            linear_extrude(height)
                square([
                    stand_height + gap,
                    stand_height + gap
                ], center=true);
        
        // Screw hole
        translate([
            0,
            0,
            height / 2
        ]) rotate([0, 90, 0]) cylinder(100, r=m5_diameter/2);
    }
    
    translate([
        
        -(stand_height + gap)/2 - thickness / 2,
        0,
        height / 2
    ]) rotate([
        0, -90, 0
    ]) cylinder(mount_screw_length - (thickness/2), r=m5_diameter/2);
}