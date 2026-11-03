# 작업실 수정 테스트
# 교육 자료대로 실습 중
import os

FILENAME = "attendance.txt"

def add_attendance():
    """출석 정보를 입력받아 파일에 저장합니다."""
    date = input("날짜를 입력하세요 (예: 2023-10-27): ").strip()
    name = input("이름을 입력하세요: ").strip()
    
    if not date or not name:
        print("날짜와 이름을 모두 입력해야 합니다.")
        return

    # 'a' 모드는 파일 끝에 내용을 추가(append)합니다.
    with open(FILENAME, "a", encoding="utf-8") as f:
        f.write(f("{date}, {name}\n"))
    print(f"{name}님의 출석이 기록되었습니다!")

def view_attendance():
    """저장된 출석 목록을 불러와서 화면에 출력합니다."""
    if not os.path.exists(FILENAME):
        print("아직 출석 기록이 없습니다.")
        return

    print("\n--- 출석 목록 ---")
    print(f"{'날짜':<15} | {'이름'}")
    print("-" * 25)
    
    with open(FILENAME, "r", encoding="utf-8") as f:
        for line in f:
            # strip()으로 줄바꿈 제거 후, 쉼표를 기준으로 나눕니다.
            data = line.strip().split(", ")
            if len(data) == 2:
                date, name = data
                print(f"{date:<15} | {name}")
    print("-" * 25)

def main():
    """프로그램의 메인 메뉴를 구성합니다."""
    while True:
        print("\n[스터디 출석 관리 시스템]")
        print("1. 출석 체크")
        print("2. 출석 목록 보기")
        print("3. 종료")
        
        choice = input("원하는 메뉴 번호를 선택하세요: ")
        
        if choice == "1":
            add_attendance()
        elif choice == "2":
            view_attendance()
        elif choice == "3":
            print("프로그램을 종료합니다. 열공하세요!")
            break
        else:
            print("잘못된 선택입니다. 다시 입력해주세요.")

if __name__ == "__main__":
    main()
    
    
    