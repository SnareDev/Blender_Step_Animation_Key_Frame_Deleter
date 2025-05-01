# just copy the script below in to the blender scripting tab.

import bpy

# Step rate — keep every nth keyframe
frame_step = 4

# Root bone name
root_bone_name = "root"

# Get active object
obj = bpy.context.object

if obj and obj.animation_data and obj.animation_data.action:
    action = obj.animation_data.action

    for fcurve in action.fcurves:
        data_path = fcurve.data_path

        preserve = False

        # Case 1: Object-level transforms (root motion applied here)
        if data_path in {"location", "rotation_euler", "rotation_quaternion", "scale"}:
            preserve = True

        # Case 2: Pose bone fcurves — preserve only the "root" bone
        elif data_path.startswith('pose.bones["'):
            start = data_path.find('["') + 2
            end = data_path.find('"]')
            bone_name = data_path[start:end]

            if bone_name == root_bone_name:
                preserve = True

        # Skip keyframe removal for preserved F-curves
        if preserve:
            continue

        # Decimate keyframes
        keyframe_points = fcurve.keyframe_points
        indices_to_remove = [i for i in range(len(keyframe_points)) if i % frame_step != 0]

        for index in reversed(indices_to_remove):
            keyframe_points.remove(keyframe_points[index])

    print(f"Keyframes decimated. Object transforms and '{root_bone_name}' bone preserved.")
else:
    print("No animation data found on the active object.")
