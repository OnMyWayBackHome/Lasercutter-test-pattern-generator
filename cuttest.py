from HersheyFonts import HersheyFonts
import svgwrite

materials = [
    {"filename" : "test_cut_acrylic_estreet",
    "header" : ['Acrylic 1/8"', "estreet plastics", "thick: 0.115in"], # title and two additional lines. Make these short enough to fit. This program doesn't check length
    "powers" : [-1], # list the power settings to test separated by commas (-1 = Full power)
    "speeds" : [130, 150, 170, 190],},  # list the speeds to test
    {"filename" : "test_cut_acrylic_optyx",
    "header" : ['Acrylic 1/8"', "optyx", "thick: 0.105in"], 
    "powers" : [-1], 
    "speeds" : [150, 170, 190, 200],},
    {"filename" : "test_cut_plywood_woodpecker",
    "header" : ['Plywood 1/8"', "woodpecker", "thick: 0.125in"], 
    "powers" : [-1], 
    "speeds" : [130, 150, 170, 190],},
    {"filename" : "test_cut_mylar_aooin",
    "header" : ['Mylar 4mil', "Aooin", "0.01 w/card stock"], 
    "powers" : [5, 15, 25], 
    "speeds" : [200, 225, 250, 275],}, 
    {"filename" : "test_cut_foam_core",
    "header" : ['Foam Core', "--", "thickness 0.25"], 
    "powers" : [60, 80, 100], 
    "speeds" : [200, 250, 300, 350],}, 
    {"filename" : "test_cut_cardboard",
    "header" : ['Cardboard', "--", "thickness 0.125"], 
    "powers" : [80, 100, -1], 
    "speeds" : [200, 250, 300],}, 
    {"filename" : "test_cut_felt",
    "header" : ['Felt', "VieFantaisie", "thickness 0.04"], 
    "powers" : [30, 45, 60], 
    "speeds" : [200, 250, 300],}, 
]


units="in"  # enter the values below using these units. Valid SVG units are in, cm, mm, pt, px
size_of_test_cut = 0.5 # how big of a square to cut out for each power/speed combo (in "units" )
top_margin = 1
left_margin = 0.75
gap_between_cuts = 0.25
text_height = 0.125
line_spacing = 0.05
ppu = 96 # pixels per unit. Used to make user coordinates in pixels. 96 Pixels per inch. 37.8 for pixels per centimeters, etc.

score_color = "green"
smaller_text_factor = 0.8 # scale down the smaller text by this factor.
cut_color = 0xFF0000 #the first test cut will be red and the rest will add more and more blue.

# convert to user coordinates of (approximate) pixels by 
left_margin *= ppu
top_margin *= ppu
gap_between_cuts *= ppu
line_spacing *= ppu
text_height *= ppu
size_of_test_cut *= ppu

def text_to_polylines(text, x_offset, y_offset, height=10):
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
            polyline.append((x2, y2))
            prev_x2, prev_y2 = (x2, y2)
        else:
            polylines.append(polyline)
            polyline = [(x1, y1), (x2, y2)]  # start a new polyine
            prev_x2, prev_y2 = (x2, y2)
    polylines.append(polyline)  
    return polylines

def hex_color_code(n):
    return f'#{n:06X}'


for material in materials:
    svg_size = (left_margin + len(material["powers"]) * (size_of_test_cut + gap_between_cuts),
                top_margin +  len(material["speeds"]) * (size_of_test_cut + gap_between_cuts) ) # (length, width) in pixels.

    viewbox_x, viewbox_y = svg_size[0], svg_size[1] #viewbox coordinates as (approximate) pixels

    
    dwg = svgwrite.drawing.Drawing(f'{material["filename"]}.svg', 
        size=(f'{svg_size[0] / ppu }{units}', f'{svg_size[1] / ppu}{units}'), # size is in real-world units
        viewBox=f"0 0 {viewbox_x} {viewbox_y}", 
        profile='full')



    y = text_height + line_spacing
    for polyline in text_to_polylines(material["header"][0], gap_between_cuts, y, text_height):
        dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))
    y += text_height + line_spacing
    for line in material['header'][1:]:
        for polyline in text_to_polylines(line, gap_between_cuts, y, text_height * smaller_text_factor):
            dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))
        y += text_height + line_spacing * smaller_text_factor
    for polyline in text_to_polylines("Power", left_margin, y, text_height):
        dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))    
    y += text_height + line_spacing
    for i, power in enumerate(material["powers"]):
        if power == -1:
            label = "Full" 
        else:
            label = str(power)
        for polyline in text_to_polylines(label, left_margin + i * (size_of_test_cut + gap_between_cuts), y, text_height):
            dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))

    for polyline in text_to_polylines("Speed", gap_between_cuts, top_margin, text_height):
        dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))
    for i, speed in enumerate(material["speeds"]):
        for polyline in text_to_polylines(str(speed), gap_between_cuts, top_margin + text_height + line_spacing + i * (size_of_test_cut + gap_between_cuts), text_height):
            dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))


    for i in range(len(material["speeds"])):
        for j in range(len(material["powers"])):
            top_left = (left_margin + j*(size_of_test_cut + gap_between_cuts),
                        top_margin + i*(size_of_test_cut + gap_between_cuts))
            dwg.add(dwg.rect(top_left, (size_of_test_cut, size_of_test_cut), stroke=hex_color_code(cut_color), fill='none'))        
            cut_color += 16
    dwg.add(dwg.rect((0,0), (viewbox_x, viewbox_y), stroke=hex_color_code(cut_color), fill='none'))
    dwg.save()


