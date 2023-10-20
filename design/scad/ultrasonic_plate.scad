// Ultrasonic Sensor - Plate 

length = 45.5; // mm 
width = 20.70; // mm 
depth = 5; // mm - arbitrary thickness 

sensor_diameter = 16;//mm
sensor_separation = 10.5;//mm (10.42) 
crystal_length = 10.35;//mm  (10.32)
crystal_width = 3.5;//mm
crystal_height = 3.5; //mm (3.0)



difference() {
    translate([-length/2, -width/2,0]) cube([length, width, depth]);
    
    translate([-sensor_separation/2 - sensor_diameter/2, 0,0]) cylinder(depth, d=sensor_diameter,$fn=64);
    
    translate([sensor_separation/2 + sensor_diameter/2, 0,0]) cylinder(depth, d=sensor_diameter,$fn=64);
    
    translate([-crystal_length/2, width/2 - crystal_width, 0])cube([crystal_length, crystal_width, crystal_height]);
    
    translate([-crystal_length/2, - width/2 , 0])cube([crystal_length, crystal_width, crystal_height]);
}