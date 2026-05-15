import rclpy


# ==========================================
# CONFIGURATION
# ==========================================
  # 배터리 소모 속도 (Loop당 차감)
  # 복귀 기준 (20% 미만이면 복귀)
  # 충전 소요 시간 (초)

# 순찰 경로


# 충전소 위치 (보통 시작점)

# ==========================================

def main():
    rclpy.init()
    navigator = BasicNavigator()
    
    print("[INFO] Connecting to Nav2...")
    
    print("[INFO] Nav2 is Ready!")

    current_battery = 100.0

    while True: # 무한 순찰 루프
        print(f"\n[START] Starting Patrol Loop. Current Battery: {current_battery:.1f}%")
        
        # 경로상의 각 지점 방문
        for i, waypoint in enumerate(PATROL_ROUTE):
            
            # 1. 배터리 체크 (이동 전)
            if :
                print(f"[WARN] Battery Low ({current_battery:.1f}%)! Returning to charger...")
                break # 순찰 중단, 충전하러 가기

            # 2. 목표 설정 및 이동 명령
            print(f"[MOVE] Heading to Waypoint {i+1}...")
            

            

            # 3. 이동 중 상태 모니터링 (가장 중요한 부분)
            while not navigator.isTaskComplete():
                # 배터리 소모
                
                
                # 시뮬레이션 효과를 위한 출력
                print(f"   >>> Moving... Battery: {current_battery:.1f}%", end='\r')
                time.sleep(0.1)

                # [핵심] 이동 중에도 배터리가 떨어지면 즉시 취소!
                if current_battery < BATTERY_THRESHOLD:
                    print(f"\n[EMERGENCY] Battery Critical! Canceling current path!")
                     # 현재 이동 명령 취소
                    break
            
            # 4. 이동 결과 확인 (도착했는지, 취소됐는지)
            if navigator.getResult() == TaskResult.CANCELED:
                # 배터리 부족으로 취소된 경우이므로 for문을 탈출하여 충전 로직으로 이동
                break 
            
            print(f"\n[INFO] Waypoint {i+1} Reached.")
            time.sleep(1) # 잠시 대기

        # ==========================================
        # 충전 로직 (순찰 for문이 끝나거나 break로 탈출했을 때 실행)
        # ==========================================
        if current_battery < BATTERY_THRESHOLD:
            print("\n[DOCKING] Moving to Charging Station...")
            
            
            
            while not navigator.isTaskComplete():
                pass # 복귀 중에는 배터리 감소 로직을 적용하지 않음 (최후의 비상 전력)

            print(f"[CHARGE] Charging for {CHARGING_TIME} seconds...")
            
            
            print("[INFO] Battery Full! Resuming Patrol.")

    exit(0)

if __name__ == '__main__':
    main()