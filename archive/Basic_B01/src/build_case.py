import bpy, math, json, os, struct
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def rounded(name,w,h,r,z0,z1):
 p=[]
 for cx,cy,a in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)]:
  for k in range(17):
   t=math.radians(a+k*90/16); p.append((cx+r*math.cos(t),cy+r*math.sin(t)))
 n=len(p); verts=[(x,y,z) for z in [z0,z1] for x,y in p]
 faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update(); ob=bpy.data.objects.new(name,me); bpy.context.collection.objects.link(ob); return ob
def box(n,loc,dim):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object;o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return o
def cyl(n,r,z0,z1,x=0,y=0):
 bpy.ops.mesh.primitive_cylinder_add(vertices=128,radius=r,depth=z1-z0,location=(x,y,(z0+z1)/2));o=bpy.context.object;o.name=n;return o
def boolean(o,c,op='DIFFERENCE'):
 bpy.context.view_layer.objects.active=o;m=o.modifiers.new(op,'BOOLEAN');m.operation=op;m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(c,do_unlink=True)
def shell(n,hinge):
 o=rounded(n,86.6,122.1,8.1,-6.2,1.2)
 boolean(o,rounded('cavity',83.4,118.9,6.5,-5.2,0))
 boolean(o,rounded('mouth',82,117.5,5.8,-8,-5.19))
 boolean(o,box('hinge clearance',(hinge*48,0,0),(24,150,30)))
 for v,l in [(-26,26),(16,28)]:boolean(o,box('controls',(-hinge*43,v,-2),(12,l,12)))
 for v in [-61,61]:boolean(o,box('ports',(0,v,-2),(28,12,6)))
 return o
camera=shell('Basic camera-side shell',-1)
boolean(camera,box('camera top open',(10,47,0),(78,46,30)))
other=shell('Basic opposite-side shell',1)
parts=[camera,other]
report=[]
import bmesh
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bm.normal_update()
 seen=set(); cc=0
 for v in bm.verts:
  if v in seen:continue
  cc+=1; todo=[v];seen.add(v)
  while todo:
   for e in todo.pop().link_edges:
    q=e.other_vert(e.verts[0]) if False else None
    for q in e.verts:
     if q not in seen:seen.add(q);todo.append(q)
 report.append({'part':o.name,'vertices':len(bm.verts),'faces':len(bm.faces),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'components':cc,'volume_mm3':bm.calc_volume(),'bbox_mm':list(o.dimensions),'retention':'Front lip geometry only; insertion, force and real fit unverified'})
 bm.free()
 o.data.calc_loop_triangles(); path=os.path.join(ROOT,'design/stl',o.name.replace(' ','_').replace('+','and')+'.stl')
 with open(path,'wb') as f:
  f.write(b'Basic B01 mm draft - unvalidated fit'.ljust(80,b' '));f.write(struct.pack('<I',len(o.data.loop_triangles)))
  for t in o.data.loop_triangles:
   vs=[o.matrix_world@o.data.vertices[i].co for i in t.vertices]; no=(vs[1]-vs[0]).cross(vs[2]-vs[0]).normalized();f.write(struct.pack('<12fH',*no,*vs[0],*vs[1],*vs[2],0))
mat=bpy.data.materials.new('Illustrative translucent TPU - not measured optical response');mat.diffuse_color=(.65,.8,.83,1);mat.use_nodes=True;p=mat.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.65,.8,.83,1);p.inputs['Roughness'].default_value=.38;p.inputs['Transmission Weight'].default_value=.45
for o in parts:o.data.materials.append(mat)
bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=.001
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'design/case_parts_mm.blend'))
json.dump(report,open(os.path.join(ROOT,'validation/topology.json'),'w'),indent=2)
print(json.dumps(report))
