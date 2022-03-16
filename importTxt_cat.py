# Let's create a Connection class; a joint contains several connections

# Let's create a Bone class

class Bone:
  # A point where two bones get united, which belongs to a joint
    def __init__(self, a: int):
        self._a = a # referring to the name of the bone
    def draw_bone(self):
        return 0
    
    def get_bone(self):
        return (self._a)


class Connection:
  # A point where two bones get united, which belongs to a joint
    def __init__(self, a: Bone, b: Bone, x: float, y: float, z: float):
        self._a = a
        self._b = b
        self._x = x
        self._y = y
        self._z = z

    def draw_joint(self):
        return 0
    
    def get_join(self):
        return (self._a, self._b, self._x, self._y, self._z)
    
    def get_bones(self):
        return (self._a.get_bone(), self._b.get_bone())
    
    def get_first_bone(self):
        return (self._a.get_bone())
    def get_x(self):
        return self._x
    def get_y(self):
        return self._y
    def get_z(self):
        return self._z
    
class Frame:
    def __init__(self, f: int, bones, transform):
        self._f = f #name of the frame itself
        self._bones = bones
        self._transforms = transforms
        
    def get_bones_vertex(self):
        return self._bones
    
    def get_weights(self):
        return self._transforms
    
class Vert:
    def __init__(self, v: int, bones, weights):
        self._v = v #name of the vertex itself
        self._weights = weights
        self._bones = bones
        
    def get_bones_vertex(self):
        return self._bones
    
    def get_weights(self):
        return self._weights     
        
    


import bpy, bmesh
from pathlib import Path
import math
import statistics


#path = some_object.filepath # as declared by props
path = "//Desktop/SkeRig_v1.0/cat-poses.rig.txt"  # a blender relative path
f = Path(bpy.path.abspath(path)) # make a path object of abs path

#--------------------------------------- PARSE THE FILE INTO 3 COLLECTIONS ---------------------------------------------#
connections = []    # Assume this is 0 mapping
frames = []         # Assume this is 1 mapping
vertices = []       # Assume this is 2 mapping

with open(f) as f:
    lines = f.readlines()

count = 0
collect = 0
for line in lines:
    count += 1
    if "#" in line:
          collect+=1
    else:
        collection = math.floor(collect/3)-1
        if collection==0:
            connections.append(line)
        if collection==1:
            frames.append(line)
        if collection==2:
            vertices.append(line)

#--------------------------------------- GET NUMBER OF BONES & CONNECTIONS ---------------------------------------------#
connect_iterator = connections[0].split(' ')
bone_qty = int(connect_iterator[0])
connect_qty = int(connect_iterator[1].replace('\n', ''))

connections.pop(0)

#--------------------------------------------- GET NUMBER OF FRAMES ----------------------------------------------------#
frame_iterator = frames[0].split(' ')
frame_qty = int(frame_iterator[0])

frames.pop(0)
#-------------------------------------------- GET NUMBER OF VERTICES ---------------------------------------------------#
vert_iterator = vertices[0].split(' ')
vert_qty = int(vert_iterator[0])

vertices.pop(0)

#-------------------------------------------- CREATE BONES IN PYTHON ---------------------------------------------------#
bones_arr = []
for i in range(bone_qty):
    bones_arr.append(Bone(i))

#------------------------------------------ CREATE CONNECTIONS TO BONES ------------------------------------------------#
connect_arr = []
for item in connections:
    connect_iterator = item.split(' ') 
    connect_iterator=list(filter(None, connect_iterator))
    connect_arr.append(Connection(bones_arr[int(connect_iterator[0])],bones_arr[int(connect_iterator[1])], float(connect_iterator[2]), float(connect_iterator[3]), float(connect_iterator[4].replace('\n', ''))))

#tuples = []
#for item in connect_arr:
#    tuples.append(item.get_bones())

#print(set(tuples))

#------------------------------------------ CREATE FRAMES FROM BONES --------------------------------------------------#
frame_arr = []
dic_frame = {}

for item in frames:
    frame_iterator = item.split(' ')
    frame_iterator = list(filter(None, frame_iterator))
    if len(frame_iterator) == 1:
        frame_i = int(frame_iterator.pop(0))
        dic_frame.update({frame_i:{}})
    else:
        bone_i = frame_iterator.pop(0)
        dic_frame[frame_i].update({bone_i:frame_iterator})
          

#------------------------------------ CREATE VERTICES WITH BONES & WEIGHTS --------------------------------------------# 
vertex_arr = []
bone_v = []
w_v = []
for item in vertices:
    vert_iterator = item.split(' ')
    vert_iterator = list(filter(None, vert_iterator))
    vert_i = int(vert_iterator.pop(0))
    for info in vert_iterator:
        if (vert_iterator.index(info)%2)==0:
            bone_v.append(bones_arr[int(info)])
        else:
            w_v.append(float(info))
    
    vert = Vert(vert_i, bone_v, w_v)
    vertex_arr.append(vert)
  
#----------------------------------------- CREATE BONES IN 3D BLENDER ------------------------------------------------# 
me = bpy.data.meshes.new('meshName')
ob = bpy.data.objects.new('obName', me)


amt = bpy.data.armatures.new('amtname')
ob = bpy.data.objects.new('obname', amt)

scn = bpy.context.scene
bpy.context.collection.objects.link(ob)
bpy.context.view_layer.objects.active=ob
bpy.context.active_object.select_set(state=True)

bpy.ops.object.mode_set(mode='EDIT')

# Insert bones 
#for bone in bones_arr:
    #bone_eb = amt.edit_bones.new(str(bone.get_bone()))
#    #print(bone)
#    bone_cords = []
#    for connection in connect_arr:
#        if connection.get_bones()[0] == bone.get_bone():
#            bone_cords += [connection.get_join()[2:]]
#    x = []
#    y = []
#    z = []
#    for cord in bone_cords:
#        x.append(cord[0])
#    for cord in bone_cords:
#        y.append(cord[1])
#    for cord in bone_cords:
#        z.append(cord[2])
#    
#    x = statistics.median(x)
#    y = statistics.median(y)
#    z = statistics.median(z)
#    
#    bone_eb.head = (0,2,0)
#    bone_eb.tail = (x,y,z)
# Edit bones and their head and tail
#for bone in bones_arr:

#0 1    0.0989986 0.551856 -0.223275
#0 2    -0.00291732 0.625009 -0.208812 -> esta coordenada para el proximo estremo
#0 3    -0.104319 0.545009 -0.226535 
#0 24    -0.00603603 0.66892 -0.437428 ->THIS ONE
  
bone_eb = amt.edit_bones.new(str(bones_arr[0].get_bone()))
bone_eb.head = (-0.00603603, 0.66892, -0.437428) #24 is the head 
bone_eb.tail = (-0.00291732, 0.625009, -0.208812) 
  
bone_eb = amt.edit_bones.new(str(bones_arr[1].get_bone()))
bone_eb.head = (-0.00291732, 0.625009, -0.208812) #--> changed to 0 2 
bone_eb.tail = (0.139713, 0.385744, -0.199375) 

bone_eb = amt.edit_bones.new(str(bones_arr[2].get_bone()))
bone_eb.head = (-0.00291732, 0.625009, -0.208812)
bone_eb.tail = (-0.00297453, 0.623664, 0.0355155)

bone_eb = amt.edit_bones.new(str(bones_arr[3].get_bone()))   
bone_eb.head = (-0.00291732, 0.625009, -0.208812) #--> changed to 0 2 
bone_eb.tail = (-0.143733, 0.388083, -0.196876) 

bone_eb = amt.edit_bones.new(str(bones_arr[4].get_bone()))  
bone_eb.head = (-0.00297453, 0.623664, 0.0355155)
bone_eb.tail = ( -0.00153086, 0.627919, 0.254107) 


#5 4    -0.00153086 0.627919 0.254107
#5 6    0.108947 0.565086 0.400366
#5 7    0.00423991 0.694824 0.520566
#5 8    -0.107163 0.564258 0.39875
# CALCULATED COORDINATES FOR 6,7,8 -> (0.000892, 0.565086, 0.399558)
bone_eb = amt.edit_bones.new(str(bones_arr[5].get_bone()))   
bone_eb.head = (-0.00153086, 0.627919, 0.254107)
bone_eb.tail = (0.000892, 0.565086, 0.399558) # CHANGED TO (0.000892, 0.565086, 0.399558)  

bone_eb = amt.edit_bones.new(str(bones_arr[6].get_bone()))   
bone_eb.head = (0.000892, 0.565086, 0.399558)# CHANGED TO (0.000892, 0.565086, 0.399558) 
bone_eb.tail = (0.105991, 0.391849, 0.396647) 

bone_eb = amt.edit_bones.new(str(bones_arr[7].get_bone()))   
bone_eb.head = (0.000892, 0.565086, 0.399558)# CHANGED TO (0.000892, 0.565086, 0.399558) 
bone_eb.tail = (0.00529898, 0.737161, 0.650565) 

bone_eb = amt.edit_bones.new(str(bones_arr[8].get_bone()))   
bone_eb.head = (0.000892, 0.565086, 0.399558)# CHANGED TO (0.000892, 0.565086, 0.399558) 
bone_eb.tail = (-0.105521, 0.392747, 0.396101) 
 
bone_eb = amt.edit_bones.new(str(bones_arr[9].get_bone()))   
bone_eb.head = (0.105991, 0.391849, 0.396647)
bone_eb.tail = (0.115866, 0.159611, 0.398529) 
  
bone_eb = amt.edit_bones.new(str(bones_arr[10].get_bone()))   
bone_eb.head = (0.115866, 0.159611, 0.398529)
bone_eb.tail = (0.106794, 0.0623831, 0.404181)  

# EDITED ONLY HAD HEAD
bone_eb = amt.edit_bones.new(str(bones_arr[11].get_bone()))   
bone_eb.head = (0.106794, 0.0623831, 0.404181)
bone_eb.tail = (0.106794, 0.0623831, 0.504181) #-->PATITA #1

bone_eb = amt.edit_bones.new(str(bones_arr[12].get_bone()))   
bone_eb.head = (-0.105521, 0.392747, 0.396101)
bone_eb.tail = (-0.115743, 0.15802, 0.399619) 

bone_eb = amt.edit_bones.new(str(bones_arr[13].get_bone()))   
bone_eb.head = (-0.115743, 0.15802, 0.399619)
bone_eb.tail = (-0.109156, 0.0636548, 0.404566) 

# EDITED ONLY HAD HEAD
bone_eb = amt.edit_bones.new(str(bones_arr[14].get_bone()))   
bone_eb.head = (-0.109156, 0.0636548, 0.404566)
bone_eb.tail = (-0.109156, 0.0636548, 0.504566) #--> PATITA #2

# EDITED ONLY HAD HEAD
bone_eb = amt.edit_bones.new(str(bones_arr[15].get_bone()))   
bone_eb.head = (-0.14483025, 0.713324, 0.76466)# CHANGED TO MIDPOINT 15-17 (-0.14483025, 0.713324, 0.76466)
bone_eb.tail = (-0.0301095, 0.758683, 0.855536)# SOMEHWERE IN THE HEAD

#16 7    0.00529898 0.737161 0.650565
#16 15    -0.0301095 0.758683 0.755536
#16 17    0.0114345 0.667965 0.773784
bone_eb = amt.edit_bones.new(str(bones_arr[16].get_bone()))   
bone_eb.head = (0.00529898, 0.737161, 0.650565) # starting in 7
bone_eb.tail = (-0.14483025, 0.713324, 0.76466) # CHANGED TO MIDPOINT 15-17 (-0.14483025, 0.713324, 0.76466)

# EDITED ONLY HAD HEAD
bone_eb = amt.edit_bones.new(str(bones_arr[17].get_bone()))   
bone_eb.head = (-0.14483025, 0.713324, 0.76466)# CHANGED TO MIDPOINT 15-17 (-0.14483025, 0.713324, 0.76466)
bone_eb.tail = (0.0114345, 0.667965, 0.873784)

bone_eb = amt.edit_bones.new(str(bones_arr[18].get_bone()))   
bone_eb.head = (0.139713, 0.385744, -0.199375)
bone_eb.tail = (0.120373, 0.248054, -0.276594)
  
bone_eb = amt.edit_bones.new(str(bones_arr[19].get_bone()))   
bone_eb.head = (0.120373, 0.248054, -0.276594)
bone_eb.tail = (0.107236, 0.0732609, -0.274245)

# EDITED ONLY HAD HEAD
bone_eb = amt.edit_bones.new(str(bones_arr[20].get_bone()))   
bone_eb.head = (0.107236, 0.0732609, -0.274245)
bone_eb.tail = (0.107236, 0.0732609, -0.174245) #--> PATITA DE ATRAS

bone_eb = amt.edit_bones.new(str(bones_arr[21].get_bone()))   
bone_eb.head = (-0.143733, 0.388083, -0.196876)
bone_eb.tail = (-0.123686, 0.24993, -0.271171)

bone_eb = amt.edit_bones.new(str(bones_arr[22].get_bone()))   
bone_eb.head = (-0.123686, 0.24993, -0.271171)
bone_eb.tail = (-0.117198, 0.0755979, -0.273044)

# EDITED ONLY HAD HEAD
bone_eb = amt.edit_bones.new(str(bones_arr[23].get_bone()))   
bone_eb.head = (-0.117198, 0.0755979, -0.273044)
bone_eb.tail = (-0.117198, 0.0755979, -0.173044) #--> PATITA DE ATRAS

bone_eb = amt.edit_bones.new(str(bones_arr[24].get_bone()))   
bone_eb.head = (-0.00603603, 0.66892, -0.437428)
bone_eb.tail = ( 0.0151284, 0.662006, -0.527779)

bone_eb = amt.edit_bones.new(str(bones_arr[25].get_bone()))   
bone_eb.head = (0.0151284, 0.662006, -0.527779)
bone_eb.tail = (0.00422263, 0.654022, -0.756715)

bone_eb = amt.edit_bones.new(str(bones_arr[26].get_bone()))   
bone_eb.head = (0.00422263, 0.654022, -0.756715)
bone_eb.tail = (0.0115577, 0.655873, -0.967474)

# EDITED ONLY HAD HEAD
bone_eb = amt.edit_bones.new(str(bones_arr[27].get_bone()))   
bone_eb.head = (0.0115577, 0.655873, -0.967474)
bone_eb.tail = (0.0115577, 0.655873, -1.067474) #---> END OF TAIL EDITED BY LSR


me.update()
