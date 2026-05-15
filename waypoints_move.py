import rclpy


# Define your locations here [x, y, z, w]


def main():
    # 1. Initialize ROS 2
    

    # 2. Verify Nav2 is Active
    # (Assuming initial_pose_setter.py was already run)
    
    print("[INFO] Nav2 is Ready!")

    # 3. Continuous Loop
    while True:
        print("\n" + "="*40)
        print(f"Available Locations: {list(WAYPOINTS.keys())}")
        print("Enter location key (or 'q' to quit): ", end="")
        
        

        if user_input in WAYPOINTS:
            

            # 4. Create Goal Pose
            

            # 5. Send Goal
            print(f"[INFO] Moving to '{user_input}' (x={target_x}, y={target_y})...")
            

            # 6. Wait for task to complete
            while not navigator.isTaskComplete():
                pass

            # 7. Check Result
            
            if result == TaskResult.SUCCEEDED:
                print("[INFO] Goal reached!")
            else:
                print("[ERROR] Goal failed or canceled!")
        else:
            print("[WARN] Unknown location! Please try again.")

    # Shutdown
    # navigator.lifecycleShutdown()
    exit(0)

if __name__ == '__main__':
    main()