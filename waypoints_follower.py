import rclpy


# Define locations


def main():
    rclpy.init()
    navigator = BasicNavigator()
    

    while True:
        print("\n" + "="*40)
        print(f"Locations: {list(WAYPOINTS.keys())}")
        print("Enter route (e.g., 'A B C') or 'q': ", end="")
        
        

        # Split input into a list (e.g., "A C" -> ["A", "C"])
        

        # Validate keys
        

        print(f"[INFO] Starting Route: {' -> '.join(valid_route)}")

        # Visit each waypoint in order
        for key in valid_route:
            
            print(f"\n>>> Going to {key}...")
            
            

            while not navigator.isTaskComplete():
                pass
            
            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                print(f"[SUCCESS] Arrived at {key}!")
            else:
                print(f"[FAIL] Failed to reach {key}. Stopping route.")
                break  # Stop the rest of the route if one fails

    exit(0)

if __name__ == '__main__':
    main()