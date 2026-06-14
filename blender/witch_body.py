import bpy
import bmesh
import math

# Clear
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj, do_unlink=True)

# ========== MATERIALS ==========

def mat(name, color, rough=0.6, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m

m_skin = mat("Skin", (0.82, 0.62, 0.52, 1), 0.7)
m_hair = mat("Hair", (0.04, 0.02, 0.06, 1), 0.4)
m_dress = mat("Dress", (0.10, 0.01, 0.13, 1), 0.5)
m_corset = mat("Corset", (0.13, 0.02, 0.04, 1), 0.4, 0.1)
m_boots = mat("Boots", (0.06, 0.03, 0.05, 1), 0.3, 0.1)
m_hat = mat("Hat", (0.08, 0.01, 0.10, 1), 0.5)
m_belt = mat("Belt", (0.22, 0.12, 0.06, 1), 0.3, 0.3)
m_eyes = mat("Eyes", (0.75, 0.08, 0.75, 1), 0.2)
m_lips = mat("Lips", (0.55, 0.08, 0.12, 1), 0.4)
m_staff = mat("Staff", (0.12, 0.08, 0.04, 1), 0.6)
m_gem = mat("Gem", (0.3, 0.0, 0.5, 1), 0.1, 0.3)

# ========== MESH BUILDER ==========

class Mesh:
    def __init__(self, name):
        self.mesh = bpy.data.meshes.new(name)
        self.obj = bpy.data.objects.new(name, self.mesh)
        bpy.context.collection.objects.link(self.obj)
        self.bm = bmesh.new()
        self.verts = []
    
    def v(self, x, y, z):
        v = self.bm.verts.new((x, y, z))
        self.verts.append(v)
        return len(self.verts) - 1
    
    def quad(self, *indices):
        self.bm.faces.new([self.verts[i] for i in indices])
    
    def done(self, smooth=True):
        self.bm.to_mesh(self.mesh)
        self.bm.free()
        if smooth:
            for p in self.mesh.polygons:
                p.use_smooth = True
        return self.obj

def add_mirror(obj, axis='X'):
    mod = obj.modifiers.new("Mirror", 'MIRROR')
    mod.use_clip = True

def add_subsurf(obj, levels=1):
    mod = obj.modifiers.new("Subsurf", 'SUBSURF')
    mod.levels = levels
    mod.render_levels = 2

# ========== TORSO ==========

torso = Mesh("Torso")

# Profile rings: (z, front_x, side_x, back_x, front_y, back_y)
# Each ring defines the cross-section at that height
# We use 6 points per ring for smoother shape
# Points: center-front, front-side, side, back-side, back, center-back

torso_profiles = [
    # z,     fx,   sx,   bx,   fy,   by     (half-widths and depths)
    (0.88,   0.12, 0.13, 0.11, 0.08, -0.08),  # hips
    (0.92,   0.11, 0.12, 0.10, 0.075,-0.075), # lower hip
    (0.96,   0.10, 0.11, 0.10, 0.07, -0.07),  # waist start
    (1.00,   0.095,0.10, 0.095,0.065,-0.065), # waist (narrowest)
    (1.04,   0.10, 0.11, 0.10, 0.07, -0.07),  # waist end
    (1.08,   0.12, 0.13, 0.11, 0.075,-0.075), # lower rib
    (1.12,   0.14, 0.15, 0.13, 0.08, -0.08),  # rib
    (1.16,   0.16, 0.17, 0.14, 0.08, -0.08),  # chest start
    (1.20,   0.17, 0.18, 0.14, 0.08, -0.075), # chest (widest)
    (1.24,   0.16, 0.17, 0.14, 0.075,-0.07),  # upper chest
    (1.28,   0.15, 0.16, 0.13, 0.07, -0.065), # collarbone
    (1.32,   0.14, 0.15, 0.12, 0.065,-0.06),  # shoulder area
    (1.36,   0.13, 0.14, 0.11, 0.06, -0.055), # shoulder top
    (1.40,   0.06, 0.07, 0.05, 0.05, -0.05),  # neck base
]

# Generate vertices for each profile
for z, fx, sx, bx, fy, by in torso_profiles:
    torso.v(0, fy, z)       # center front
    torso.v(fx*0.7, fy*0.9, z)  # front-side
    torso.v(fx, fy*0.3, z)      # side-front
    torso.v(sx, 0, z)           # side
    torso.v(bx, by*0.3, z)      # side-back
    torso.v(bx*0.7, by*0.9, z)  # back-side
    torso.v(0, by, z)           # center back

# Connect rings
num_rings = len(torso_profiles)
pts_per_ring = 7

for r in range(num_rings - 1):
    for p in range(pts_per_ring):
        p_next = (p + 1) % pts_per_ring
        i0 = r * pts_per_ring + p
        i1 = r * pts_per_ring + p_next
        i2 = (r + 1) * pts_per_ring + p_next
        i3 = (r + 1) * pts_per_ring + p
        torso.quad(i0, i1, i2, i3)

# Top and bottom caps
torso.quad(*range(pts_per_ring))
torso.quad(*range((num_rings-1)*pts_per_ring, num_rings*pts_per_ring))

torso_obj = torso.done()
add_mirror(torso_obj)
add_subsurf(torso_obj, 1)
torso_obj.data.materials.append(m_corset)

# ========== HEAD ==========

head = Mesh("Head")

# Head as layered rings with facial features
head_rings = [
    # z,       radius,  front_indent,  notes
    (1.48,     0.04,    0.0),    # neck top
    (1.52,     0.06,    0.0),    # chin start
    (1.55,     0.08,    0.01),   # jaw
    (1.58,     0.10,    0.02),   # lower cheek
    (1.61,     0.11,    0.03),   # cheek (widest)
    (1.64,     0.105,   0.02),   # eye level
    (1.67,     0.10,    0.01),   # forehead
    (1.70,     0.095,   0.0),    # upper forehead
    (1.73,     0.085,   0.0),    # top
    (1.76,     0.06,    0.0),    # crown
]

for z, r, fi in head_rings:
    segs = 12
    for i in range(segs):
        angle = (i / segs) * math.pi * 2
        x = math.cos(angle) * r
        y = math.sin(angle) * r
        # Add facial indent on front
        if -0.3 < angle < 0.3 or angle > math.pi * 1.7 or angle < math.pi * 0.3:
            y -= fi * math.cos(angle)
        head.v(abs(x), y, z)

# Connect head rings
head_pts = 12
for r in range(len(head_rings) - 1):
    for p in range(head_pts):
        p_next = (p + 1) % head_pts
        i0 = r * head_pts + p
        i1 = r * head_pts + p_next
        i2 = (r + 1) * head_pts + p_next
        i3 = (r + 1) * head_pts + p
        head.quad(i0, i1, i2, i3)

# Top cap
head.quad(*range((len(head_rings)-1)*head_pts, len(head_rings)*head_pts))

head_obj = head.done()
add_mirror(head_obj)
add_subsurf(head_obj, 1)
head_obj.data.materials.append(m_skin)

# ========== NECK ==========

neck = Mesh("Neck")
# Neck as cylinder connecting body to head
neck_segs = 8
neck_r = 0.045

for z in [1.40, 1.44, 1.48]:
    for i in range(neck_segs):
        angle = (i / neck_segs) * math.pi * 2
        neck.v(math.cos(angle) * neck_r, math.sin(angle) * neck_r, z)

for r in range(2):
    for p in range(neck_segs):
        p_next = (p + 1) % neck_segs
        neck.quad(r*neck_segs+p, r*neck_segs+p_next, 
                  (r+1)*neck_segs+p_next, (r+1)*neck_segs+p)

neck.quad(*range(neck_segs))
neck.quad(*range(neck_segs*2, neck_segs*3))

neck_obj = neck.done()
add_mirror(neck_obj)
add_subsurf(neck_obj, 1)
neck_obj.data.materials.append(m_skin)

# ========== SHOULDERS & ARMS (T-POSE) ==========

# Each arm segment: proper anatomical shape
# Shoulder -> Upper arm (with deltoid bulge) -> Elbow -> Lower arm -> Wrist -> Hand

def make_arm(side, name):
    arm = Mesh(f"Arm_{name}")
    x_sign = 1 if name == "R" else -1
    
    # Shoulder socket position
    shoulder_x = 0.14 * x_sign
    
    # Arm segments with anatomical profiles
    # Format: (x, z, radius_front, radius_side, radius_back)
    segments = [
        # Shoulder joint
        (0.16*x_sign, 1.36, 0.045, 0.05, 0.04),
        # Deltoid (bulge)
        (0.20*x_sign, 1.36, 0.05, 0.055, 0.045),
        # Upper arm
        (0.28*x_sign, 1.36, 0.042, 0.045, 0.04),
        (0.36*x_sign, 1.36, 0.04, 0.042, 0.038),
        # Elbow (slightly wider)
        (0.44*x_sign, 1.36, 0.042, 0.045, 0.04),
        # Forearm (tapers)
        (0.50*x_sign, 1.36, 0.038, 0.04, 0.035),
        (0.56*x_sign, 1.36, 0.035, 0.038, 0.032),
        # Wrist (narrow)
        (0.60*x_sign, 1.36, 0.028, 0.03, 0.026),
        # Hand base
        (0.64*x_sign, 1.36, 0.032, 0.035, 0.028),
        # Hand
        (0.68*x_sign, 1.36, 0.025, 0.03, 0.022),
        # Fingertips
        (0.72*x_sign, 1.36, 0.015, 0.018, 0.012),
    ]
    
    segs_per_ring = 8
    
    for x, z, rf, rs, rb in segments:
        for i in range(segs_per_ring):
            angle = (i / segs_per_ring) * math.pi * 2
            # Elliptical cross-section
            r = rf if abs(math.cos(angle)) > abs(math.sin(angle)) else rs
            r = max(r, rb) * 0.8 + r * 0.2
            vy = math.cos(angle) * r * 0.8
            vz = math.sin(angle) * r * 0.6
            arm.v(x, vy, z + vz)
    
    # Connect rings
    for r in range(len(segments) - 1):
        for p in range(segs_per_ring):
            p_next = (p + 1) % segs_per_ring
            i0 = r * segs_per_ring + p
            i1 = r * segs_per_ring + p_next
            i2 = (r+1) * segs_per_ring + p_next
            i3 = (r+1) * segs_per_ring + p
            arm.quad(i0, i1, i2, i3)
    
    # Cap end
    arm.quad(*range((len(segments)-1)*segs_per_ring, len(segments)*segs_per_ring))
    
    arm_obj = arm.done()
    add_mirror(arm_obj)
    add_subsurf(arm_obj, 1)
    arm_obj.data.materials.append(m_skin)
    return arm_obj

make_arm(1, "R")
make_arm(-1, "L")

# ========== LEGS ==========

def make_leg(side, name):
    leg = Mesh(f"Leg_{name}")
    x_sign = 1 if name == "R" else -1
    x = 0.08 * x_sign
    
    # Leg segments
    segments = [
        # Hip joint
        (x, 0.84, 0.06, 0.055),
        # Upper thigh (widest)
        (x, 0.75, 0.058, 0.052),
        (x, 0.65, 0.052, 0.048),
        # Knee (slightly wider)
        (x, 0.52, 0.048, 0.046),
        (x, 0.48, 0.05, 0.048),
        # Calf (calf muscle bulge)
        (x, 0.40, 0.045, 0.048),
        (x, 0.32, 0.04, 0.042),
        # Shin (tapers)
        (x, 0.22, 0.038, 0.038),
        (x, 0.14, 0.035, 0.035),
        # Ankle (narrow)
        (x, 0.08, 0.03, 0.028),
        # Foot top
        (x, 0.04, 0.035, 0.032),
        # Foot
        (x, 0.0, 0.04, 0.035),
    ]
    
    segs_per_ring = 8
    
    for px, z, rf, rb in segments:
        for i in range(segs_per_ring):
            angle = (i / segs_per_ring) * math.pi * 2
            r = rf if abs(math.cos(angle)) > 0.5 else rb
            vy = math.cos(angle) * r * 0.7
            vz = math.sin(angle) * r
            leg.v(px, vy, z + vz)
    
    for r in range(len(segments) - 1):
        for p in range(segs_per_ring):
            p_next = (p + 1) % segs_per_ring
            i0 = r * segs_per_ring + p
            i1 = r * segs_per_ring + p_next
            i2 = (r+1) * segs_per_ring + p_next
            i3 = (r+1) * segs_per_ring + p
            leg.quad(i0, i1, i2, i3)
    
    leg.quad(*range((len(segments)-1)*segs_per_ring, len(segments)*segs_per_ring))
    
    leg_obj = leg.done()
    add_mirror(leg_obj)
    add_subsurf(leg_obj, 1)
    leg_obj.data.materials.append(m_skin)
    return leg_obj

make_leg(1, "R")
make_leg(-1, "L")

# ========== BOOTS ==========

def make_boot(side, name):
    boot = Mesh(f"Boot_{name}")
    x_sign = 1 if name == "R" else -1
    x = 0.08 * x_sign
    
    # Boot shaft
    for z in [0.10, 0.14, 0.18, 0.22]:
        r = 0.042
        for i in range(8):
            angle = (i / 8) * math.pi * 2
            boot.v(x, math.cos(angle) * r * 0.7, z + math.sin(angle) * r)
    
    # Foot part
    boot.v(x-0.04, 0.04, 0.08)   # heel back
    boot.v(x+0.05, 0.04, 0.08)   # toe back
    boot.v(x+0.05, -0.04, 0.08)  # toe front
    boot.v(x-0.04, -0.04, 0.08)  # heel front
    
    boot.v(x-0.04, 0.05, 0.0)    # heel bottom
    boot.v(x+0.06, 0.05, 0.0)    # toe bottom
    boot.v(x+0.06, -0.04, 0.0)
    boot.v(x-0.04, -0.04, 0.0)
    
    # Connect shaft rings
    for r in range(3):
        for p in range(8):
            p_next = (p + 1) % 8
            boot.quad(r*8+p, r*8+p_next, (r+1)*8+p_next, (r+1)*8+p)
    
    # Foot faces
    boot.quad(32, 33, 34, 35)  # top
    boot.quad(36, 37, 38, 39)  # bottom
    boot.quad(32, 33, 37, 36)  # back
    boot.quad(33, 34, 38, 37)  # right
    boot.quad(34, 35, 39, 38)  # front
    boot.quad(35, 32, 36, 39)  # left
    
    boot_obj = boot.done()
    add_mirror(boot_obj)
    add_subsurf(boot_obj, 1)
    boot_obj.data.materials.append(m_boots)
    return boot_obj

make_boot(1, "R")
make_boot(-1, "L")

# ========== DRESS ==========

dress = Mesh("Dress")

# A-line skirt
dress_rings = [
    (0.88,  0.13),  # waist
    (0.80,  0.15),
    (0.70,  0.17),
    (0.60,  0.19),
    (0.50,  0.21),
    (0.40,  0.23),
    (0.30,  0.25),  # hem
]

for z, r in dress_rings:
    for i in range(12):
        angle = (i / 12) * math.pi * 2
        dress.v(math.cos(angle) * r, math.sin(angle) * r, z)

for r in range(len(dress_rings) - 1):
    for p in range(12):
        p_next = (p + 1) % 12
        dress.quad(r*12+p, r*12+p_next, (r+1)*12+p_next, (r+1)*12+p)

dress.quad(*range(12))

dress_obj = dress.done()
add_subsurf(dress_obj, 1)
dress_obj.data.materials.append(m_dress)

# ========== CORSET BELT ==========

corset = Mesh("Corset")
for z in [0.96, 1.00, 1.04]:
    r = 0.10
    for i in range(12):
        angle = (i / 12) * math.pi * 2
        corset.v(math.cos(angle) * r, math.sin(angle) * r, z)

for r in range(2):
    for p in range(12):
        p_next = (p + 1) % 12
        corset.quad(r*12+p, r*12+p_next, (r+1)*12+p_next, (r+1)*12+p)

corset.quad(*range(12))
corset.quad(*range(24, 36))

corset_obj = corset.done()
add_mirror(corset_obj)
add_subsurf(corset_obj, 1)
corset_obj.data.materials.append(m_corset)

# ========== HAIR ==========

hair = Mesh("Hair")

# Main hair volume
hair_rings = [
    (1.76,  0.07),
    (1.72,  0.10),
    (1.68,  0.11),
    (1.62,  0.10),
    (1.56,  0.09),
    (1.50,  0.08),
    (1.44,  0.07),
]

for z, r in hair_rings:
    for i in range(8):
        angle = (i / 8) * math.pi * 2
        # Hair is mostly on top and back
        x = math.cos(angle) * r * 0.9
        y = math.sin(angle) * r * 0.7 + 0.04  # shift back
        hair.v(abs(x), y, z)

for r in range(len(hair_rings) - 1):
    for p in range(8):
        p_next = (p + 1) % 8
        hair.quad(r*8+p, r*8+p_next, (r+1)*8+p_next, (r+1)*8+p)

hair.quad(*range(8))

# Hair strands hanging down
for offset in [0.06, 0.0, -0.06]:
    base = len(hair.verts)
    hair.v(offset-0.02, 0.08, 1.50)
    hair.v(offset+0.02, 0.08, 1.50)
    hair.v(offset+0.02, 0.10, 1.15)
    hair.v(offset-0.02, 0.10, 1.15)
    hair.quad(base, base+1, base+2, base+3)

hair_obj = hair.done()
add_mirror(hair_obj)
add_subsurf(hair_obj, 1)
hair_obj.data.materials.append(m_hair)

# ========== WITCH HAT ==========

# Brim
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.16, depth=0.012, location=(0, 0, 1.78))
hat_brim = bpy.context.active_object
hat_brim.name = "Hat_Brim"
hat_brim.data.materials.append(m_hat)
bpy.ops.object.shade_smooth()

# Cone (tapered)
bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.09, radius2=0.003, depth=0.38, location=(0, 0, 1.97))
hat_cone = bpy.context.active_object
hat_cone.name = "Hat_Cone"
hat_cone.data.materials.append(m_hat)
bpy.ops.object.shade_smooth()

# Band
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.10, depth=0.03, location=(0, 0, 1.81))
hat_band = bpy.context.active_object
hat_band.name = "Hat_Band"
hat_band.data.materials.append(m_corset)
bpy.ops.object.shade_smooth()

# ========== EYES ==========

for side, name in [(0.038, "L"), (-0.038, "R")]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, radius=0.016, 
                                          location=(side, -0.10, 1.63))
    eye = bpy.context.active_object
    eye.name = f"Eye_{name}"
    eye.scale = (1.1, 0.6, 1)
    bpy.ops.object.transform_apply(scale=True)
    eye.data.materials.append(m_eyes)
    bpy.ops.object.shade_smooth()

# ========== STAFF ==========

bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.012, depth=1.6, location=(-0.58, 0, 0.90))
staff = bpy.context.active_object
staff.name = "Staff"
staff.data.materials.append(m_staff)
bpy.ops.object.shade_smooth()

bpy.ops.mesh.primitive_uv_sphere_add(segments=10, ring_count=6, radius=0.035, location=(-0.58, 0, 1.72))
orb = bpy.context.active_object
orb.name = "Staff_Orb"
orb.data.materials.append(m_gem)
bpy.ops.object.shade_smooth()

# ========== FINAL ==========

for obj in bpy.data.objects:
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.shade_smooth()
        obj.select_set(False)

print("Anatomically detailed Goth Mommy Witch with proper body parts!")
