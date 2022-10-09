# Laser cutter test pattern generator
Creates an SVG files to use to test speed and power settings to cut different materials on a Glowforge laser cutter. This is probably only useful for a Glowforge which does not have built-in test pattern as of this writing and also makes you enter cut speed/power manually for each test cut-out shape.
# Features: 
* Specify the speeds and power settings to test and this program creates a matrix of squares.
* Enter three lines of text to score (instead of engrave) as a header. Scoring vector text is significantly faster than engraving raster. A test SVG with 9 different combinations of speed and power typically takes less than 2 minutes to cut.
* Batch up many materials and it will create SVG files for all of them at once.
