import bpy,os,sys,math
from mathutils import Vector
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=R+'/design/case_parts_mm.blend')
for o in bpy.context.scene.objects:
 if 'opposite' in o.name:o.location.x-=48
 else:o.location.x+=48
 if 'snap retaining' in o.name:o.location.z+=20
 if 'snap window' in o.name:o.location.z+=20
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=True
s.world.use_nodes=True;n=s.world.node_tree;n.nodes.clear();e=n.nodes.new('ShaderNodeTexEnvironment');e.image=bpy.data.images.load(sys.argv[sys.argv.index('--')+1]);b=n.nodes.new('ShaderNodeBackground');b.inputs['Strength'].default_value=.7;out=n.nodes.new('ShaderNodeOutputWorld');n.links.new(e.outputs[0],b.inputs[0]);n.links.new(b.outputs[0],out.inputs[0])
bpy.ops.object.camera_add(location=(180,-230,235));s.camera=bpy.context.object;s.camera.rotation_euler=(Vector((0,0,4))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.type='ORTHO';s.camera.data.ortho_scale=220;s.camera.data.clip_end=1000
s.render.resolution_x=1800;s.render.resolution_y=1350;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_depth='8';s.render.filepath=R+'/previews/Basic_B01_case_only.png';bpy.ops.render.render(write_still=True)
