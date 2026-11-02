import csv
from pathlib import Path


def read_schedule(file_path):
    """필수 열과 중복 열을 확인하고 CSV의 데이터 행 목록을 반환한다."""
    required_columns = ["nurse_id", "date", "shift"]

    with open(file_path, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames

        if fieldnames is None:
            raise ValueError("입력 오류: CSV 파일에 헤더가 없습니다.")

        missing_columns = []

        for column in required_columns:
            if column not in fieldnames:
                missing_columns.append(column)

        if missing_columns:
            missing_text = ", ".join(missing_columns)
            raise ValueError(f"입력 오류: 필수 열이 없습니다: {missing_text}")

        seen_columns = set()
        duplicate_columns = []

        for column in fieldnames:
            if column in seen_columns:
                if column not in duplicate_columns:
                    duplicate_columns.append(column)
            else:
                seen_columns.add(column)

        if duplicate_columns:
            duplicate_text = ", ".join(duplicate_columns)
            raise ValueError(f"입력 오류: 중복된 열 이름이 있습니다: {duplicate_text}")

        rows = []

        for row in reader:
            if None in row:
                raise ValueError(
                    f"입력 오류: CSV {reader.line_num}번째 줄의 "
                    "값 개수가 헤더의 열 개수보다 많습니다."
                )

            if None in row.values():
                raise ValueError(
                    f"입력 오류: CSV {reader.line_num}번째 줄의 "
                    "값 개수가 헤더의 열 개수보다 적습니다."
                )

            for column in required_columns:
                value = row[column]

                if value.strip() == "":
                    raise ValueError(
                        f"입력 오류: CSV {reader.line_num}번째 줄의 "
                        f"필수값이 비어 있습니다: {column}"
                    )

            rows.append(row)

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
