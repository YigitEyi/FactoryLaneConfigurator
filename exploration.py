import ezdxf

doc = ezdxf.readfile("/Users/yigiteyi/Desktop/ARZDA07/F6_AGV Rotalari2.dxf")
msp = doc.modelspace()

# Find layers that have LINE or LWPOLYLINE entities
print("=== Layers with LINE/POLYLINE entities ===")
line_layers = {}
for entity in msp.query("LINE LWPOLYLINE"):
    layer = entity.dxf.layer
    line_layers[layer] = line_layers.get(layer, 0) + 1

# Sort by count
for layer, count in sorted(line_layers.items(), key=lambda x: -x[1])[:15]:
    print(f"  {layer}: {count} lines/polylines")
print()

# Check UH6 layer (seems AGV related based on name)
print("=== UH6 layer (potential AGV routes) ===")
uh6_entities = {}
for entity in msp.query("*[layer=='UH6']"):
    t = entity.dxftype()
    uh6_entities[t] = uh6_entities.get(t, 0) + 1
print(f"Entity types: {uh6_entities}")
print()

# Sample some lines from UH6
print("Sample LINEs from UH6:")
for i, line in enumerate(msp.query("LINE[layer=='UH6']")):
    if i >= 5:
        print("  ...")
        break
    print(f"  ({line.dxf.start.x:.1f}, {line.dxf.start.y:.1f}) -> ({line.dxf.end.x:.1f}, {line.dxf.end.y:.1f})")
print()

# Sample polylines from UH6
print("Sample LWPOLYLINEs from UH6:")
for i, pline in enumerate(msp.query("LWPOLYLINE[layer=='UH6']")):
    if i >= 5:
        print("  ...")
        break
    points = list(pline.get_points())
    print(f"  Polyline with {len(points)} points: {points[0][:2]} -> ... -> {points[-1][:2]}")
print()

# Also check layers with "AGV" or "YOL" (road) in name
print("=== Checking other potential route layers ===")
for layer in line_layers:
    if 'AGV' in layer.upper() or 'YOL' in layer.upper() or 'ROTA' in layer.upper():
        print(f"  {layer}: {line_layers[layer]} entities")