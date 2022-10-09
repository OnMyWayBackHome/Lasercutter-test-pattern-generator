# Program to create test files to import into Glowforge to test cut power and speed settings for new materials
# You can give it header text to score. Scoring is quicker than engraving.
# Specify the speeds and power settings that you want to test and this will create a matrix of squares 
# in individual colors so you can add the speed/power setting to each square. Create as many or as few items to test.
from HersheyFonts import HersheyFonts
import svgwrite

materials = [
    {"filename" : "test_cut_acrylic_estreet",
    "header" : ['Acrylic 1/8 Red', "estreet plastics", "thick: 0.115in"], # title plus two lines of text to print at the top. Make these short enough to fit. This program doesn't check length
    "powers" : [-1], # list the power settings to test separated by commas (-1 = Full power)
    "speeds" : [190, 210, 230, 250],},  # list the speeds to test. This will make a square matrix with powers across the top and speeds going down.
    {"filename" : "test_cut_acrylic_optyx",
    "header" : ['Acrylic 1/8"', "optyx", "thick: 0.105in"], 
    "powers" : [-1], 
    "speeds" : [170, 175, 180, 185],},
    {"filename" : "test_cut_plywood_woodpecker",
    "header" : ['Plywood 1/8"', "woodpecker birch", "thick: 0.125in"], 
    "powers" : [-1], 
    "speeds" : [200, 225, 250, 300],},
    {"filename" : "test_cut_mylar_4mil",
    "header" : ['Mylar 4mil', "Aooin", "thick: 0.01 w/card stock"], 
    "powers" : [5, 15, 25], 
    "speeds" : [200, 225, 250, 275],}, 
    {"filename" : "test_cut_mylar_6mil",
    "header" : ['Mylar 6mil', "Amazon", "thick: 0.01 w/card stock"], 
    "powers" : [5, 10, 15], 
    "speeds" : [250, 270, 250, 275],}, 
    {"filename" : "test_cut_foam_core",
    "header" : ['Foam Core', "Amazon", "thickness 0.25"], 
    "powers" : [60, 80, 100], 
    "speeds" : [200, 250, 300, 350],}, 
    {"filename" : "test_cut_cardboard",
    "header" : ['Cardboard', "--", "thickness 0.125"], 
    "powers" : [80, 85, 90], 
    "speeds" : [280, 300, 320],}, 
    {"filename" : "test_cut_felt",
    "header" : ['Felt', "VieFantaisie", "thickness 0.04"], 
    "powers" : [30, 20, 10], 
    "speeds" : [300, 400, 500],}, 
]

filename_version_number = "_v2"  #append this to the file name to distinguish versions. This can be blank "" if you don't need it.
units="in"  # enter the values below using these units. Valid SVG units are in, cm, mm, pt, px
size_of_test_cut = 0.5 # how big of a square to cut out for each power/speed combo (in "units" )
top_header = 1 # the space reserved for header text above the grid of test cut-outs. Make this bigger if you have more lines of header.
left_header = 0.75 # space reserved for text to the left of the grid of test cut-outs
gap_between_cuts = 0.25 # space between each square test cut-outs and margins
text_height = 0.125 # height of letters of large text
line_spacing = 0.05 # space between lines of text
ppu = 96 # pixels per unit. Used to make user coordinates in pixels. 96 Pixels per inch. 37.8 for pixels per centimeter, etc.

score_color = "green" # pick a color with a hex value less than 0xFF0000 so it appears at the top of the Glowforge app and scores first.
smaller_text_factor = 0.8 # scale down the second and third lines of the header by this factor
cut_color = 0xFF0000 #the first test cut-out will be red and the rest will add more and more blue and be cut later.

# convert to user coordinates to (approximate) pixels
left_header *= ppu
top_header *= ppu
gap_between_cuts *= ppu
line_spacing *= ppu
text_height *= ppu
size_of_test_cut *= ppu

def text_to_polylines(text, x_offset, y_offset, height=10):
    """
    Function to create a list of coordinates to draw the given text in a Hershey Font. These lists are used to make SVG polylines.

    :param text: the text to create paths for
    :param x_offset: the x coordinate of the starting point in pixels
    :param y_offset: ditto for y coordinate
    :param height: the height of the  letters in pixels
    :return: a list of lists with each sublist a list of coordinates that describe a path that draws a letter or part of a letter
    """     
    
    thefont = HersheyFonts()
    thefont.load_default_font()
    scale_factor = float(height) / (thefont.render_options['bottom_line'] - thefont.render_options['cap_line'])
    thefont.render_options.scaley = scale_factor
    thefont.render_options.scalex = scale_factor
    thefont.render_options.xofs = x_offset
    thefont.render_options.yofs = y_offset 

    polylines = []
    first_point = True
    for (x1, y1), (x2, y2) in thefont.lines_for_text(text):
        if first_point:
            polyline = [(x1, y1), (x2, y2)]
            prev_x2, prev_y2 = (x2, y2)
            first_point = False
        elif (x1, y1) == (prev_x2, prev_y2):
            polyline.append((x2, y2))  #lines_for_text returns coordinates of beginning and end. This code ensures that you don't repeat a coordinate pair.
            prev_x2, prev_y2 = (x2, y2)
        else:
            polylines.append(polyline)
            polyline = [(x1, y1), (x2, y2)]  # start a new polyine
            prev_x2, prev_y2 = (x2, y2)
    polylines.append(polyline)  
    return polylines

def hex_color_code(n):
    return f'#{n:06X}' #return a hexadecimal number in the format #000000 through #FFFFFF


for material in materials:
    svg_size = (left_header + len(material["powers"]) * (size_of_test_cut + gap_between_cuts),
                top_header +  len(material["speeds"]) * (size_of_test_cut + gap_between_cuts) ) # (length, width) in pixels.
    viewbox_x, viewbox_y = svg_size[0], svg_size[1] #viewbox coordinates as (approximate) pixels
    dwg = svgwrite.drawing.Drawing(f'{material["filename"]}{filename_version_number}.svg', 
        size=(f'{svg_size[0] / ppu }{units}', f'{svg_size[1] / ppu}{units}'), # size is in real-world units
        viewBox=f"0 0 {viewbox_x} {viewbox_y}", 
        profile='full')

    # create header text, and power and speed labels to score. (Scoring is quicker than engraving.)
    y = text_height + line_spacing
    for polyline in text_to_polylines(material["header"][0], gap_between_cuts, y, text_height):
        dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))
    y += text_height + line_spacing
    for line in material['header'][1:]:
        for polyline in text_to_polylines(line, gap_between_cuts, y, text_height * smaller_text_factor):
            dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))
        y += text_height + line_spacing * smaller_text_factor
    for polyline in text_to_polylines("Power", left_header, y, text_height):
        dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))    
    y += text_height + line_spacing
    for i, power in enumerate(material["powers"]):
        if power == -1:
            label = "Full" 
        else:
            label = str(power)
        for polyline in text_to_polylines(label, left_header + i * (size_of_test_cut + gap_between_cuts), y, text_height):
            dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))

    for polyline in text_to_polylines("Speed", gap_between_cuts, top_header, text_height):
        dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))
    for i, speed in enumerate(material["speeds"]):
        for polyline in text_to_polylines(str(speed), gap_between_cuts, top_header + text_height + line_spacing + i * (size_of_test_cut + gap_between_cuts), text_height):
            dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))

    # create a grid of test cut-outs, each with their own color so you can set speed and power individually
    for i in range(len(material["speeds"])): 
        for j in range(len(material["powers"])):
            top_left = (left_header + j*(size_of_test_cut + gap_between_cuts),
                        top_header + i*(size_of_test_cut + gap_between_cuts))
            dwg.add(dwg.rect(top_left, (size_of_test_cut, size_of_test_cut), stroke=hex_color_code(cut_color), fill='none'))        
            cut_color += 16
    dwg.add(dwg.rect((0,0), (viewbox_x, viewbox_y), stroke=hex_color_code(cut_color), fill='none'))  # box around the entire SVG
    dwg.save()


