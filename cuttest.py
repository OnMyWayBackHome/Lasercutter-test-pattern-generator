import svgwrite

units="in"
stroke_width = '0.01'
svg_size = (5,6) # (length, width) in the units specified above that will be used as the size attribute of the SVG file.

engrave_color = "blue"
score_color = "green"
cut_color = "red"

dwg = svgwrite.drawing.Drawing("tmp.svg", 
    size=(f'{svg_size[0]}{units}', f'{svg_size[1]}{units}'),
    viewBox=f"0 0 {svg_size[0]} {svg_size[1]}", 
    profile='full')

dwg.add(dwg.rect((0.5, 0.50), (2, 3), stroke=cut_color, fill='none'))
path = ['m',1, 1]+number_path['8'][1]
dwg.add(dwg.path(d=path, stroke=score_color, fill='none'))

dwg.save()


