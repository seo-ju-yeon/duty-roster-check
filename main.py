import csv
from pathlib import Path


def read_schedule(file_path):
    """CSV 파일을 읽어 각 행을 딕셔너리로 담은 리스트를 반환한다."""
    with open(file_path, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    return rows


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parent
    schedule_path = project_dir / "data" / "fixtures" / "small" / "base" / "schedule.csv"

    schedule = read_schedule(schedule_path)

    print(f"읽은 행 수: {len(schedule)}")
    if schedule:
        print(f"첫 번째 행: {schedule[0]}")
    else:
        print("읽은 데이터 행이 없습니다.")
