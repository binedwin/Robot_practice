import rclpy
##
##

def main():
    # 1. Initialize ROS 2
    rclpy.init()
    
    # 2. Create Navigator
    

    # 3. Create Initial Pose
    # [IMPORTANT] Ensure these coordinates match the robot's spawn location in Gazebo
    
    
    # Position (x, y) and Orientation (z, w)
    # Usually (0,0) if you didn't change the spawn point
    

    # 4. Set Initial Pose
    print(f"Setting initial pose to (x={initial_pose.pose.position.x}, y={initial_pose.pose.position.y})...")
    

    # 5. Wait for Nav2 to activate
    # This checks if AMCL accepted the pose and became active.
    print("Waiting for Nav2 to activate...")
   

    print("Nav2 is now ACTIVE and ready for commands.")
    
    # Exit
    # navigator.lifecycleShutdown()
    exit(0)

if __name__ == '__main__':
    main()