import rclpy

import time

def main():
    rclpy.init()


    # 순찰할 경로 리스트 (순서대로 방문)
    

    print("[INFO] Start Patrolling... (Press Ctrl+C to stop)")

    while True:  # 무한 루프
        for i, waypoint in enumerate(patrol_route):
            print(f"\n[INFO] Heading to Waypoint {i+1}...")
            
           

            

            while not navigator.isTaskComplete():
                pass # 이동 중...

            
            if result == TaskResult.SUCCEEDED:
                print(f"[INFO] Waypoint {i+1} Reached! Scanning area for 3 seconds...")
                time.sleep(3) # 3초간 경비(대기) 후 다음 장소로
            else:
                print(f"[ERROR] Failed to reach Waypoint {i+1}. Skipping...")

if __name__ == '__main__':
    main()