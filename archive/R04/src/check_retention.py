import bpy,os,json
from mathutils.bvhtree import BVHTree
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=R+'/design/case_parts_mm.blend')
def tree(o):
 o.data.calc_loop_triangles();return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles],all_triangles=True,epsilon=0)
def check(a,b):return {'a':a.name,'b':b.name,'surface_triangle_pairs':len(tree(a).overlap(tree(b)))}
o=bpy.data.objects
res=[check(o['Camera shell + AirTag pod'],o['AirTag snap retaining ring']),check(o['PaperDIY shell + service tray'],o['PaperDIY snap window frame'])]
bpy.ops.mesh.primitive_cylinder_add(vertices=128,radius=15.95,depth=8,location=(0,-16,5.6));tag=bpy.context.object;tag.name='AirTag nominal whole-unit envelope'
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,5.25));kit=bpy.context.object;kit.name='K159 maximum envelope';kit.dimensions=(64.2,117.05,5.5);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
res += [check(o['Camera shell + AirTag pod'],tag),check(o['AirTag snap retaining ring'],tag),check(o['PaperDIY shell + service tray'],kit),check(o['PaperDIY snap window frame'],kit)]
json.dump({'units':'mm','scope':'Seated-state surface intersections only; positive-clearance contained parts are not diagnosed by surface test. No insertion or flex simulation.','checks':res,'nominal_clearances_mm':{'tag_radial':.55,'tag_floor':.4,'ring_bead_groove_radial':.25,'ring_bead_insertion_radial_deflection':.3,'paper_kit_to_tongue':.25,'paper_carrier_to_kit':.3,'phone_front_lip_to_AR_min':.19}},open(R+'/validation/retention_checks.json','w'),indent=2);print(json.dumps(res))
