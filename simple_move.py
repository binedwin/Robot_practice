import rclpy
##
##
##

def main():
    # 1. Initialize ROS 2
    rclpy.init()
    
    # 2. Create Navigator
    

    # 3. Check Nav2 Status
    print("[DEBUG] Checking Nav2 active status...")
    # If this hangs here, it means Nav2 is not fully launched or crashed.
    
    print("[DEBUG] Nav2 is ACTIVE.")

    # 4. Set Goal
    

    # [TEST COORDINATES]
    # Ensure these coordinates are VALID (empty space) in your map.
    

    print(f"[DEBUG] Sending Goal: (x={goal_pose.pose.position.x}, y={goal_pose.pose.position.y})")
    
    # 5. Send Goal
    

    # 6. Monitor Loop with Timeout
    
    while not navigator.isTaskComplete():
        
        
        if feedback and i % 5 == 0:
            print(f"[INFO] Distance remaining: {feedback.distance_remaining:.2f} meters")
            
            # If distance is not changing for a long time, the robot might be stuck.
            if feedback.distance_remaining < 0.1:
                print("[INFO] Very close to target...")

    # 7. Detailed Result Analysis
    
    if result == TaskResult.SUCCEEDED:
        print("[SUCCESS] Goal reached!")
    elif result == TaskResult.CANCELED:
        print("[CANCELED] Goal was canceled. Check if another node canceled it.")
    elif result == TaskResult.FAILED:
        print("[FAILED] Goal failed!")
        print("  - Possible Reason 1: Goal is inside a wall/obstacle (Check Costmap).")
        print("  - Possible Reason 2: Robot is stuck.")
        print("  - Possible Reason 3: Path planning failed (No valid path found).")

    # navigator.lifecycleShutdown()
    exit(0)

if __name__ == '__main__':
    main()