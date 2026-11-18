# Tidewind grass patch: a 1.9 m square of single-triangle blades, made to tile with its neighbours.
# Each blade is one triangle (two root corners and a tip); colour runs from dark at the root to light at the tip,
# so the patch melts into the ground under it. The game bends each blade in the wind in its vertex shader.
import bpy, bmesh, random, math, sys
random.seed(7)
bpy.ops.wm.read_factory_settings(use_empty=True)
N, HALF = int(sys.argv[-1]) if sys.argv[-1].isdigit() else 150, 0.95
me = bpy.data.meshes.new('grass_patch'); bm = bmesh.new()
col = bm.loops.layers.color.new('Col')
pts = []
# blue-noise-ish scatter: best of a few candidates, so blades don't clump and leave holes
for i in range(N):
    best = None
    for _ in range(8):
        c = (random.uniform(-HALF, HALF), random.uniform(-HALF, HALF))
        d = min([math.hypot(c[0]-p[0], c[1]-p[1]) for p in pts] or [9])
        if best is None or d > best[0]: best = (d, c)
    pts.append(best[1])
for (x, y) in pts:
    a = random.uniform(0, math.pi)                      # which way the blade faces
    w = random.uniform(0.07, 0.115) / 2
    h = random.uniform(0.42, 0.78)
    lean = random.uniform(0, 0.12); la = random.uniform(0, 2 * math.pi)
    ca, sa = math.cos(a), math.sin(a)
    v1 = bm.verts.new((x - ca * w, y - sa * w, 0.0))
    v2 = bm.verts.new((x + ca * w, y + sa * w, 0.0))
    v3 = bm.verts.new((x + math.cos(la) * lean, y + math.sin(la) * lean, h))
    f = bm.faces.new((v1, v2, v3))
    shade = random.uniform(0.9, 1.08)
    for l in f.loops:
        t = l.vert.co.z / h
        base, tip = (0.7, 0.7, 0.7), (0.95, 0.95, 0.8)
        c = [(base[k] + (tip[k] - base[k]) * t) * shade for k in range(3)]
        l[col] = (min(c[0], 1), min(c[1], 1), min(c[2], 1), 1.0)
bm.to_mesh(me); bm.free()
for p in me.polygons: p.use_smooth = False
ob = bpy.data.objects.new('grass_patch', me); bpy.context.collection.objects.link(ob)
mat = bpy.data.materials.new('TW_grass_blade'); mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']; bsdf.inputs['Roughness'].default_value = 0.85
vc = mat.node_tree.nodes.new('ShaderNodeVertexColor'); vc.layer_name = 'Col'
mat.node_tree.links.new(vc.outputs['Color'], bsdf.inputs['Base Color'])
me.materials.append(mat)
# custom up-facing normals: the game lights grass as if it were the ground it covers
me.normals_split_custom_set_from_vertices([(0, 0, 1)] * len(me.vertices)) if hasattr(me, 'normals_split_custom_set_from_vertices') else None
bpy.ops.export_scene.gltf(filepath='/home/claude/grass/grass_patch.glb', export_format='GLB', use_selection=False, export_normals=True, export_vertex_color='ACTIVE' if bpy.app.version >= (4, 2, 0) else None, export_all_vertex_colors=True) if False else \
bpy.ops.export_scene.gltf(filepath='/home/claude/grass/grass_patch.glb', export_format='GLB', export_normals=True)
print('blades', N, 'tris', len(me.polygons))
