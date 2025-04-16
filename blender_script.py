# just copy the script below in to the blender scripting tab.

import bpy

# Set the frame step (e.g., 2 for every second frame, 3 for every third frame)
frame_step = 7  # Change to 3 if you want to remove every third frame

# Get the active object
obj = bpy.context.object

# Ensure the object has animation data
if obj and obj.animation_data and obj.animation_data.action:
    action = obj.animation_data.action
    for fcurve in action.fcurves:
        # Get all keyframe points
        keyframe_points = fcurve.keyframe_points
        
        # Collect indices of keyframes to remove
        indices_to_remove = []
        for i, keyframe in enumerate(keyframe_points):
            if i % frame_step == 0:  # Keep every nth frame
                continue
            indices_to_remove.append(i)
        
        # Remove keyframes in reverse order to avoid index shifting
        for index in reversed(indices_to_remove):
            keyframe_points.remove(keyframe_points[index])
    
    print("Keyframes decimated successfully.")
else:
    print("No animation data found on the active object.")
