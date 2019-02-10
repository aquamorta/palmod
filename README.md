## A simply tool to modify Canvans/Palette2 mcf.gcode files

Palette 2 is a hardware to enable a 3D printer to print multi colored objects or objects
of different materials.

This a a small python script to modify the extrusion speed while doing side transitions.
Side transitions offers the possibility to save filament compared to a transition tower.

Unfortunately the files produced by the web based Mosaic Canvas slicer software contains very fast flow rates
while doing site transitions to change materials.

The script empowers you to change this extrusion speed. To use it download the generated file from your account on canvas3d.io,
save it to your harddisk, transform it by palmod and upload the modified file to your Canvas Hub or Octoprint installation.

You can get a small help by entering:

    ./palmod.py -h

    usage: palmod [-h] [-o OUTPUT] [-v] [-t TRANSITION_SPEED] input
    
    Program for modifying palette mcf.gcode files. Copyright (C) 2019 Bernd Breitenbach
    This program comes with ABSOLUTELY NO WARRANTY. This is free software,
    and you are welcome to redistribute it under certain conditions; See COPYING for details.

    positional arguments:
      input                 input file
    
    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            output file
      -v, --verbosity       increase verbosity level
      -t TRANSITION_SPEED, --transition-speed TRANSITION_SPEED
                            sets the extrusion speed for side transitions


Here is an example for setting the side transition extrusion speed to 200 with increased verbosity and writing the result to out.mcf.gcode:

    ./palmod -v -t 200 -o out.mcf.gcode in.mcf.gcode
    
    line [1701] layer:1 extruder:0  Y:0.0 X:0.0 Z:0.65 E:182.62326 F:2400.0 changing "G1 E182.62326 F2400" --> "G1 E182.62326 F200.0"
    line [2316] layer:2 extruder:1  Y:0.0 X:0.0 Z:0.8 E:355.17416 F:2400.0 changing "G1 E178.5509 F2400" --> "G1 E178.5509 F200.0"
    line [30480] layer:34 extruder:0  Y:0.0 X:0.0 Z:5.6 E:1940.2408 F:2400.0 changing "G1 E151.27121 F2400" --> "G1 E151.27121 F200.0"
    line [30482] layer:34 extruder:0  Y:0.0 X:0.0 Z:5.6 E:1991.66219 F:2400.0 changing "G1 E202.6926 F2400" --> "G1 E202.6926 F200.0"
    line [39130] layer:46 extruder:1  Y:0.0 X:0.0 Z:7.4 E:2878.75204 F:2400.0 changing "G1 E181.29405 F2400" --> "G1 E181.29405 F200.0"

    summary:
    ====================================
    lines processed :44863
    layers          :51
    extruder changes:4


## Disclaimer

This software comes without any warranty. It currently works for me but in the future it could be possible that Mosaic Manufactoring
changes the format of their generated mcf.gcode files
so it could be that this script stops working. Don't blame Mosaic Manufactoring (or me) for this.



