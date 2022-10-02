from HersheyFonts import HersheyFonts
import svgwrite

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


dwg = svgwrite.drawing.Drawing(
    "tmphershey.svg", 
    size=('500', '100'),
    profile='full')

for polyline in text_to_polylines('0.123', 40, 50, 10):
    dwg.add(dwg.polyline(polyline, stroke='blue', fill='none'))        

dwg.save()