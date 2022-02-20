import bpy, os
from bpy import context
import bmesh

# get current selection 
selection=bpy.context.selected_objects
scene=bpy.context.scene
startFrame = scene.frame_start
endFrame = scene.frame_end
currentFrame = scene.frame_current

# Get object data
me = bpy.context.object.data
bm=bmesh.new()
bm.from_mesh(me)

#get path to render output
temp_folder = os.path.abspath(bpy.context.scene.render.filepath)
filename=os.path.join(temp_folder, "air-poses.txt")
file=open(filename, "w")

if hasattr(bm.verts, "ensure_lookup_table"):
    bm.verts.ensure_lookup_table()
    
file.write("%d %d \n" % (len(range(endFrame-startFrame+1)), len(bm.verts)))

for sel in selection:
    for i in range(endFrame-startFrame+1):
        frame=i+startFrame
        scene.frame_set(frame)
        j=0
        while j < len(bm.verts):
            vertex_co=bm.verts[j].co
            file.write("%f %f %f " % (vertex_co[0], vertex_co[1], vertex_co[2]))
            j+=1
            
        file.write("\n")
        
file.close()

scene.frame_set(currentFrame)

print(os.path.abspath(filename))



# Now let's export.obj
mesh = bpy.context
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
bpy.ops.object.mode_set(mode='OBJECT')

me=mesh.object.data

filepath = "/tmp/air-poses.obj"
with open(filepath, 'w') as f:
    for v in me.vertices:
        f.write("v %.4f %.4f %.4f\n" % v.co[:])
    for p in me.polygons:
        f.write("f")
        for k in p.vertices:
            f.write(" %d" % (k + 1))
        f.write("\n")

file.close()
        
print("DONE WITH OBJ")
