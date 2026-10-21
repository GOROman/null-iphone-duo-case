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
def shell(n,hinge,back=1.2):
 o=rounded(n,86.6,122.1,8.1,-6.2,back)
 boolean(o,rounded('cavity',83.4,118.9,6.5,-5.2,0))
 boolean(o,rounded('mouth',82,117.5,5.8,-8,-5.19))
 boolean(o,box('hinge clearance',(hinge*48,0,0),(24,150,30)))
 for v,l in [(-26,26),(16,28)]:boolean(o,box('controls',(-hinge*43,v,-2),(12,l,12)))
 for v in [-61,61]:boolean(o,box('ports',(0,v,-2),(28,12,6)))
 return o
# Official AR bump projected silhouette; construction profile for the case opening.
CAMERA_PROFILE = [[-23.93886, 43.67588], [-23.92274, 42.88381], [-23.8628, 42.09367], [-23.75992, 41.30957], [-23.61471, 40.53247], [-23.42775, 39.76407], [-23.20034, 39.00813], [-22.93341, 38.26657], [-22.62781, 37.54071], [-22.28471, 36.83263], [-21.90488, 36.14366], [-21.49, 35.47631], [-21.04129, 34.83224], [-20.55974, 34.21272], [-20.04408, 33.61636], [-19.49595, 33.04611], [-18.9218, 32.50838], [-18.32102, 32.0022], [-17.69161, 31.52668], [-17.03783, 31.08553], [-16.37029, 30.68475], [-15.67395, 30.31497], [-14.95934, 29.98265], [-14.22908, 29.6883], [-13.49531, 29.43562], [-12.7534, 29.21926], [-12.00801, 29.0389], [-11.24929, 28.89005], [-10.52644, 28.77774], [-9.80331, 28.69081], [-9.09187, 28.62696], [-8.39743, 28.58194], [-6.84682, 28.56628], [-5.88869, 28.56174], [20.46003, 28.51506], [21.67071, 28.51385], [22.86438, 28.52107], [23.78149, 28.53621], [24.71445, 28.56172], [25.36588, 28.58898], [26.16075, 28.62627], [26.87515, 28.67909], [27.59601, 28.75089], [28.33268, 28.84863], [29.08056, 28.97887], [29.83264, 29.14759], [30.59629, 29.36073], [31.345, 29.62508], [32.07873, 29.9398], [32.79987, 30.31003], [33.47487, 30.7195], [34.12085, 31.17337], [34.7328, 31.6665], [35.30644, 32.19256], [35.84345, 32.74995], [36.35813, 33.35336], [36.83232, 33.98354], [37.24802, 34.61289], [37.62897, 35.25312], [37.97572, 35.90778], [38.29182, 36.57833], [38.57521, 37.2542], [38.82959, 37.93803], [39.05956, 38.62957], [39.26441, 39.33015], [39.44529, 40.03952], [39.6041, 40.76666], [39.72502, 41.42224], [39.83692, 42.14396], [39.93973, 42.86917], [39.93938, 43.49574], [39.93747, 44.11908], [39.92961, 44.88164], [39.91119, 45.65982], [39.87651, 46.42521], [39.82073, 47.17367], [39.73375, 47.92896], [39.6109, 48.67864], [39.44726, 49.41839], [39.23878, 50.14549], [38.98298, 50.85583], [38.67817, 51.54687], [38.32479, 52.21266], [37.92346, 52.85062], [37.47562, 53.4572], [36.98389, 54.02822], [36.45051, 54.56101], [35.8792, 55.05201], [35.27251, 55.49932], [34.63348, 55.90081], [33.96731, 56.2539], [33.27592, 56.55842], [32.5651, 56.81381], [31.83721, 57.02216], [31.09727, 57.18567], [30.34752, 57.30843], [29.59118, 57.39527], [28.83007, 57.45217], [28.06522, 57.48622], [27.29728, 57.50415], [26.53403, 57.512], [25.91011, 57.51425], [25.28317, 57.51502], [24.65067, 57.51528], [23.92321, 57.51543], [23.32574, 57.5155], [-8.32724, 57.51538], [-9.3187, 57.49237], [-10.35943, 57.40316], [-11.04183, 57.31804], [-11.73629, 57.20961], [-12.43563, 57.07563], [-13.13678, 56.91378], [-13.85103, 56.7178], [-14.5302, 56.49955], [-15.21541, 56.24519], [-15.89496, 55.96067], [-16.57391, 55.63121], [-17.23244, 55.26911], [-17.86967, 54.87405], [-18.48698, 54.44414], [-19.08397, 53.97821], [-19.65686, 53.47801], [-20.20451, 52.9429], [-20.72359, 52.37384], [-21.21137, 51.77195], [-21.67522, 51.12397], [-22.09167, 50.46139], [-22.46858, 49.77407], [-22.8053, 49.06259], [-23.09984, 48.33066], [-23.35116, 47.58067], [-23.5582, 46.81685], [-23.7206, 46.04136], [-23.83821, 45.25688], [-23.91088, 44.46732]]
CAMERA_FOOT_PROFILE = [[-39.08039, 54.02341], [-25.60345, 32.92165], [-25.03011, 32.07203], [-24.41396, 31.25441], [-23.75915, 30.47026], [-23.06578, 29.72136], [-22.33732, 29.01026], [-21.57901, 28.34086], [-20.77901, 27.70475], [-19.9602, 27.13486], [-19.10975, 26.60595], [-18.23998, 26.1226], [-17.35501, 25.6887], [-16.45518, 25.29972], [-6.14355, 25.148], [-4.75089, 25.14169], [32.8832, 25.06564], [33.43716, 25.27197], [33.9911, 25.4937], [34.54477, 25.73081], [35.09793, 25.98341], [35.6501, 26.25131], [38.99833, 28.1024], [39.59517, 35.77961], [39.63987, 41.12125], [39.65898, 44.12674], [39.64793, 44.863], [39.61288, 45.60952], [39.55632, 46.35024], [39.47387, 47.08637], [39.36015, 47.81444], [39.21137, 48.53473], [39.02424, 49.24359], [38.79597, 49.93884], [38.52499, 50.61713], [38.21015, 51.27642], [37.85217, 51.91179], [37.45165, 52.52118], [37.0099, 53.1017], [36.52925, 53.64991], [36.01152, 54.16364], [35.4599, 54.63985], [34.87639, 55.07704], [34.26352, 55.47342], [33.62564, 55.82666], [32.96427, 56.13667], [32.28431, 56.40272], [31.58755, 56.62642], [30.8782, 56.80931], [30.15799, 56.95459], [29.42936, 57.06586], [28.69402, 57.14766], [27.95286, 57.20565], [27.20612, 57.24507], [26.46116, 57.27067], [25.79861, 57.28542], [25.13476, 57.29508], [24.15978, 57.30315], [23.18377, 57.30719], [21.79833, 57.30857], [-10.91798, 57.31812], [-11.60755, 57.31729], [-37.41786, 56.57122], [-37.66826, 56.56196], [-37.90165, 56.53981], [-38.06288, 56.51577], [-38.22233, 56.48272], [-38.37757, 56.43274], [-38.52566, 56.36473], [-38.65879, 56.2707], [-38.77399, 56.15538], [-38.86905, 56.02312], [-38.93761, 55.8753], [-38.98671, 55.71995], [-39.0206, 55.56081], [-39.04455, 55.39968], [-39.06639, 55.16532], [-39.07582, 54.91449], [-39.08022, 54.47024]]
CAMERA_FOOT_RELIEF_TOP_W_MM = 0.60
CAMERA_XY_CLEARANCE_MM = 0.55
CAMERA_RIM_WALL_MM = 1.40
CAMERA_PROTECTION_ABOVE_AR_LENS_MM = 0.60
CAMERA_AR_MAX_LENS_W_MM = 5.627655
CAMERA_TOP_CHAMFER_MM = 0.25
CAMERA_TOP_W_MM = CAMERA_AR_MAX_LENS_W_MM + CAMERA_PROTECTION_ABOVE_AR_LENS_MM

def offset_profile(d, profile=None):
 profile = CAMERA_PROFILE if profile is None else profile
 out=[]
 for i,p in enumerate(profile):
  a=Vector(profile[i-1]);b=Vector(p);c=Vector(profile[(i+1)%len(profile)])
  u=(b-a).normalized();v=(c-b).normalized();n=Vector((u.y,-u.x));m=Vector((v.y,-v.x));q=b+(n+m)*(d/(1+n.dot(m)));out.append(tuple(q))
 return out
def contour_prism(name,profile,z0,z1):
 n=len(profile);vv=[(x,y,z) for z in [z0,z1] for x,y in profile];ff=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new(name);me.from_pydata(vv,[],ff);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);return o
def camera_rim():
 d=CAMERA_XY_CLEARANCE_MM;t=CAMERA_RIM_WALL_MM;h=CAMERA_TOP_W_MM;c=CAMERA_TOP_CHAMFER_MM
 loops=[(d+t,1.7),(d+t,h-c),(d+t-c,h),(d+c,h),(d,h-c),(d,1.7)]
 vv=[]
 for off,z in loops:vv.extend((x,y,z) for x,y in offset_profile(off))
 n=len(CAMERA_PROFILE);ff=[]
 for j in range(len(loops)):
  for i in range(n):ff.append((j*n+i,j*n+(i+1)%n,((j+1)%len(loops))*n+(i+1)%n,((j+1)%len(loops))*n+i))
 me=bpy.data.meshes.new('Continuous fitted camera rim');me.from_pydata(vv,[],ff);me.update();o=bpy.data.objects.new('Continuous fitted camera rim',me);bpy.context.collection.objects.link(o)
 import bmesh
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(me);bm.free();return o
camera=shell('Basic camera-side shell',-1,back=1.8)
boolean(camera,camera_rim(),'UNION')
boolean(camera,contour_prism('Camera contour clearance',offset_profile(CAMERA_XY_CLEARANCE_MM),-9,12))
boolean(camera,contour_prism('Hidden shoulder underside relief',offset_profile(CAMERA_XY_CLEARANCE_MM,CAMERA_FOOT_PROFILE),-1,CAMERA_FOOT_RELIEF_TOP_W_MM))
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
  f.write(b'Basic B02 mm draft - unvalidated fit'.ljust(80,b' '));f.write(struct.pack('<I',len(o.data.loop_triangles)))
  for t in o.data.loop_triangles:
   vs=[o.matrix_world@o.data.vertices[i].co for i in t.vertices]; no=(vs[1]-vs[0]).cross(vs[2]-vs[0]).normalized();f.write(struct.pack('<12fH',*no,*vs[0],*vs[1],*vs[2],0))
mat=bpy.data.materials.new('Illustrative translucent TPU - not measured optical response');mat.diffuse_color=(.65,.8,.83,1);mat.use_nodes=True;p=mat.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.65,.8,.83,1);p.inputs['Roughness'].default_value=.38;p.inputs['Transmission Weight'].default_value=.45
for o in parts:o.data.materials.append(mat)
bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=.001
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'design/case_parts_mm.blend'))
json.dump(report,open(os.path.join(ROOT,'validation/topology.json'),'w'),indent=2)
print(json.dumps(report))
