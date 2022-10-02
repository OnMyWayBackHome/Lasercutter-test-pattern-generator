from HersheyFonts import HersheyFonts
import svgwrite

material = 'Transparent Acrylic 1/8"'
notes = "Focus 0.21"
powers = [-1] # list the power settings to test (-1 = Full power)
speeds = [130, 150, 170, 190]  # list the speeds to test


units="in"
size_of_test_cut = 0.5 # how big of a square to cut out for each power/speed combo (in "units" )
top_margin = 1
left_margin = 0.75
gap_between_cuts = 0.25
text_height = 0.125
line_spacing = 0.05

svg_size = (left_margin + len(powers) * (size_of_test_cut + gap_between_cuts),
            top_margin +  len(speeds) * (size_of_test_cut + gap_between_cuts)) # (length, width) in the units specified above that will be used as the size attribute of the SVG file.
engrave_color = "blue"
score_color = "green"
cut_color = 0xFF0000
ppi = 96 # pixels per inch for user coordinates to be in (approximate) pixels
viewbox_x, viewbox_y = svg_size[0] * ppi, svg_size[1] * ppi #viewbox coordinates are in 100ths of an inch

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


dwg = svgwrite.drawing.Drawing("tmp.svg", 
    size=(f'{svg_size[0]}{units}', f'{svg_size[1]}{units}'),
    viewBox=f"0 0 {viewbox_x} {viewbox_y}", 
    profile='full')

left_margin *= ppi
top_margin *= ppi
gap_between_cuts *= ppi
line_spacing *= ppi
text_height *= ppi
size_of_test_cut *= ppi

y = text_height + line_spacing
for polyline in text_to_polylines(material, gap_between_cuts, y, text_height):
    dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))
y = y + text_height + line_spacing
for polyline in text_to_polylines(notes, gap_between_cuts, y, text_height * 0.8):
    dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))
y = y + text_height + line_spacing
for polyline in text_to_polylines("Power", left_margin, y, text_height):
    dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))    
y = y + text_height + line_spacing
for i, power in enumerate(powers):
    if power == -1:
        label = "Full" 
    else:
        label = str(power)
    for polyline in text_to_polylines(label, left_margin + i * (size_of_test_cut + gap_between_cuts), y, text_height):
      dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))

for polyline in text_to_polylines("Speed", gap_between_cuts, top_margin, text_height):
      dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))
for i, speed in enumerate(speeds):
    for polyline in text_to_polylines(str(speed), gap_between_cuts, top_margin + text_height + line_spacing + i * (size_of_test_cut + gap_between_cuts), text_height):
      dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))


for i in range(len(speeds)):
    for j in range(len(powers)):
        top_left = (left_margin + j*(size_of_test_cut + gap_between_cuts),
                    top_margin + i*(size_of_test_cut + gap_between_cuts))
        dwg.add(dwg.rect(top_left, (size_of_test_cut, size_of_test_cut), stroke=hex_color_code(cut_color), fill='none'))        
        cut_color += 2
dwg.add(dwg.rect((0,0), (viewbox_x, viewbox_y), stroke=hex_color_code(cut_color), fill='none'))
dwg.save()


