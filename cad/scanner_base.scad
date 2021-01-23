$fn = 100;
card_width = 65;
card_height = 90;
card_diagonal = sqrt(pow(card_width, 2) + pow(card_height, 2));
base_height = 8;

// Camera Settings (For Logitech StreamCam)
d_fov = 78; // degrees
camera_height = 60;

focal_length = card_diagonal / (2 * tan(d_fov / 2));

stand_height = camera_height + focal_length;



union() {
    // Base
    difference() {
        translate([0, 0, base_height/2]) cube([
            card_width + base_height,
            card_height + base_height * 2,
            base_height
        ], center=true);

        translate([
            -card_width/2 + base_height/2,
            -card_height/2,
            base_height - 1
        ]) cube([card_width, card_height, 1.5]);
    }
    
    // Stand
    translate([
        -(card_width + base_height)/2,
        -base_height / 2,
        0
    ]) {
        cube([base_height, base_height, base_height + stand_height]);
    }

    // stand support
    fillet_radius = (card_height - base_height )/ 2;
    
    difference() {
        translate([
            -(card_width + base_height)/2,
            -card_height / 2,
            0
        ]) cube([
            base_height,
            card_height,
            base_height + fillet_radius
        ]);
        
        translate([
            -(card_width + base_height),
            -fillet_radius - base_height / 2,
            base_height + fillet_radius
        ]) rotate([0, 90, 0]) cylinder(card_width + base_height, r=fillet_radius);
        
        translate([
            -(card_width + base_height),
            fillet_radius + base_height / 2,
            base_height + fillet_radius
        ]) rotate([0, 90, 0]) cylinder(card_width + base_height, r=fillet_radius);
    }
}
