import bpy

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 120
scene.render.fps = 24

rig = bpy.data.objects.get("Witch_Rig")
if not rig:
    print("ERROR: Run body + rig scripts first.")
    exit()

bpy.context.view_layer.objects.active = rig

def pose(name, rot=(0,0,0), loc=(0,0,0), scale=(1,1,1), frame=1):
    b = rig.pose.bones.get(name)
    if not b: return
    b.rotation_euler = rot
    b.location = loc
    b.scale = scale
    b.keyframe_insert("rotation_euler", frame=frame)
    b.keyframe_insert("location", frame=frame)
    b.keyframe_insert("scale", frame=frame)

def clear(frame=1):
    for b in rig.pose.bones:
        b.rotation_euler = (0,0,0)
        b.location = (0,0,0)
        b.scale = (1,1,1)
        b.keyframe_insert("rotation_euler", frame=frame)
        b.keyframe_insert("location", frame=frame)
        b.keyframe_insert("scale", frame=frame)

# ===== IDLE (1-60) =====
clear(1)
pose("Chest", scale=(1,1,1.015), frame=15)
pose("Chest", scale=(1,1,0.985), frame=45)
pose("Chest", scale=(1,1,1), frame=60)

pose("Hair_Base", rot=(0,0,0.05), frame=20)
pose("Hair_Base", rot=(0,0,-0.05), frame=50)
pose("Hair_Base", rot=(0,0,0), frame=60)

pose("Hair_Mid", rot=(0,0,0.08), frame=20)
pose("Hair_Mid", rot=(0,0,-0.08), frame=50)
pose("Hair_Mid", rot=(0,0,0), frame=60)

# ===== RELAXED (61-120) =====
pose("UpperArm_L", rot=(0,0,0), frame=61)
pose("LowerArm_L", rot=(0,0,0), frame=61)
pose("UpperArm_R", rot=(0,0,0), frame=61)
pose("LowerArm_R", rot=(0,0,0), frame=61)

pose("UpperArm_L", rot=(0.1,0,-1.4), frame=90)
pose("LowerArm_L", rot=(0,0.3,-0.1), frame=90)
pose("UpperArm_R", rot=(0.1,0,1.4), frame=90)
pose("LowerArm_R", rot=(0,-0.3,0.1), frame=90)
pose("Head", rot=(0.05,0.1,0.05), frame=85)

pose("UpperArm_L", rot=(0.05,0,-1.35), frame=120)
pose("LowerArm_L", rot=(0,0.25,-0.05), frame=120)
pose("UpperArm_R", rot=(0.05,0,1.35), frame=120)
pose("LowerArm_R", rot=(0,-0.25,0.05), frame=120)
pose("Head", rot=(0.02,0.05,0.02), frame=120)

# Smooth interpolation
for action in bpy.data.actions:
    for fc in action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = 'BEZIER'
            kp.handle_left_type = 'AUTO_CLAMPED'
            kp.handle_right_type = 'AUTO_CLAMPED'

bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='OBJECT')

print("Animations: Idle (1-60), Relaxed (61-120)")
