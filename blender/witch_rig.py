import bpy
from mathutils import Vector

# Clear
for obj in bpy.data.objects:
    if obj.type == 'ARMATURE':
        bpy.data.objects.remove(obj, do_unlink=True)

bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
rig = bpy.context.active_object
rig.name = "Witch_Rig"
arm = rig.data
arm.name = "Witch_Armature"

bpy.ops.armature.select_all(action='SELECT')
bpy.ops.armature.delete()

def bone(name, head, tail, parent=None):
    b = arm.edit_bones.new(name)
    b.head = Vector(head)
    b.tail = Vector(tail)
    if parent and parent in arm.edit_bones:
        b.parent = arm.edit_bones[parent]
    return b

# ========== SPINE ==========

bone("Root", (0, 0, 0), (0, 0.08, 0.05))
bone("Hips", (0, 0, 0.88), (0, 0, 1.0), "Root")
bone("Spine", (0, 0, 1.0), (0, 0, 1.18), "Hips")
bone("Chest", (0, 0, 1.18), (0, 0, 1.36), "Spine")
bone("Neck", (0, 0, 1.40), (0, 0, 1.52), "Chest")
bone("Head", (0, 0, 1.52), (0, 0, 1.76), "Neck")

# ========== ARMS (T-POSE) ==========

# Right
bone("Shoulder_R", (-0.12, 0, 1.36), (-0.20, 0, 1.36), "Chest")
bone("UpperArm_R", (-0.20, 0, 1.36), (-0.44, 0, 1.36), "Shoulder_R")
bone("LowerArm_R", (-0.44, 0, 1.36), (-0.60, 0, 1.36), "UpperArm_R")
bone("Hand_R", (-0.60, 0, 1.36), (-0.72, 0, 1.36), "LowerArm_R")

# Left
bone("Shoulder_L", (0.12, 0, 1.36), (0.20, 0, 1.36), "Chest")
bone("UpperArm_L", (0.20, 0, 1.36), (0.44, 0, 1.36), "Shoulder_L")
bone("LowerArm_L", (0.44, 0, 1.36), (0.60, 0, 1.36), "UpperArm_L")
bone("Hand_L", (0.60, 0, 1.36), (0.72, 0, 1.36), "LowerArm_L")

# ========== LEGS ==========

# Right
bone("UpperLeg_R", (0.08, 0, 0.84), (0.08, 0, 0.50), "Hips")
bone("LowerLeg_R", (0.08, 0, 0.50), (0.08, 0, 0.10), "UpperLeg_R")
bone("Foot_R", (0.08, 0, 0.10), (0.08, -0.08, 0.0), "LowerLeg_R")
bone("Toe_R", (0.08, -0.08, 0.0), (0.08, -0.14, 0.0), "Foot_R")

# Left
bone("UpperLeg_L", (-0.08, 0, 0.84), (-0.08, 0, 0.50), "Hips")
bone("LowerLeg_L", (-0.08, 0, 0.50), (-0.08, 0, 0.10), "UpperLeg_L")
bone("Foot_L", (-0.08, 0, 0.10), (-0.08, -0.08, 0.0), "LowerLeg_L")
bone("Toe_L", (-0.08, -0.08, 0.0), (-0.08, -0.14, 0.0), "Foot_L")

# ========== HAIR ==========

bone("Hair_Base", (0, 0.08, 1.72), (0, 0.08, 1.55), "Head")
bone("Hair_Mid", (0, 0.09, 1.55), (0, 0.10, 1.35), "Hair_Base")
bone("Hair_Tip", (0, 0.10, 1.35), (0, 0.10, 1.15), "Hair_Mid")

# ========== STAFF ==========

bone("Staff_Bone", (-0.58, 0, 0.10), (-0.58, 0, 1.72), "Hand_R")

# ========== FINISH ==========

bpy.ops.object.mode_set(mode='OBJECT')
arm.display_type = 'STICK'

print("Armature ready! Parent mesh to armature with Automatic Weights.")
