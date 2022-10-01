from HersheyFonts import HersheyFonts
import svgwrite

material = "Acrylic"
powers = [-1] # list the power settings to test (-1 = Full power)
speeds = [130, 150, 170]  # list the speeds to test


units="in"
size_of_test_cut = 0.5 # how big of a square to cut out for each power/speed combo (in "units" )
top_margin = 1
left_margin = 1
gap_between_cuts = 0.25
svg_size = (left_margin + len(powers) * (size_of_test_cut + gap_between_cuts),
            top_margin +  len(speeds) * (size_of_test_cut + gap_between_cuts)) # (length, width) in the units specified above that will be used as the size attribute of the SVG file.
engrave_color = "blue"
score_color = "green"
cut_color = 0xFF0000

viewbox_x, viewbox_y = svg_size[0] * 100, svg_size[1] * 100 #viewbox coordinates are in 100ths of an inch

def text_to_polylines(text, x_offset, y_offset, height=10):
    thefont = HersheyFonts()
    thefont.load_default_font()
    scale_factor = float(height) / (thefont.render_options['bottom_line'] - thefont.render_options['cap_line'])
    thefont.render_options.scaley = scale_factor
    thefont.render_options.scalex = scale_factor
    thefont.render_options.yofs = x_offset #thefont.render_options['bottom_line'] * scale_factor
    thefont.render_options.xofs = y_offset

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


for polyline in text_to_polylines('0.123', 60, 55, 10):
    dwg.add(dwg.polyline(polyline, stroke=score_color, fill='none'))
dwg.add(dwg.rect((50, 50), (200, 300), stroke=hex_color_code(cut_color), fill='none'))
cut_color += 1
dwg.add(dwg.rect((0,0), (viewbox_x, viewbox_y), stroke=hex_color_code(cut_color), fill='none'))
dwg.save()


