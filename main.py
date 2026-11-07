import csv
import tomllib
from pathlib import Path
from datetime import date


# 간호사 목록을 읽음
def read_nurses(file_path):
    """간호사 CSV를 읽어 각 행을 딕셔너리로 담은 리스트를 반환한다."""
    with open(file_path, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames

        if fieldnames is None:
            raise ValueError("입력 오류: 간호사 CSV 파일에 헤더가 없습니다.")

        if "nurse_id" not in fieldnames:
            raise ValueError("입력 오류: 간호사 CSV에 필수 열이 없습니다: nurse_id")

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
            raise ValueError(
                f"입력 오류: 간호사 CSV에 중복된 열 이름이 있습니다: {duplicate_text}"
            )

        nurses = list(reader)

    return nurses


# file_path: 읽을 근무표 파일의 경로
# allowed_shifts: 허용된 근무 상태 목록
def read_schedule(file_path, allowed_shifts, start_date, end_date):
    """CSV의 입력 구조, 필수값, 근무 상태를 확인하고 행 목록을 반환한다."""
    required_columns = ["nurse_id", "date", "shift"]

    if start_date > end_date:
        raise ValueError("설정 오류: 검사 시작일이 종료일보다 늦습니다.")

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

            shift = row["shift"]

            if shift not in allowed_shifts:
                allowed_text = ", ".join(allowed_shifts)
                raise ValueError(
                    f"입력 오류: CSV {reader.line_num}번째 줄의 "
                    f"허용되지 않은 근무 상태입니다: {shift!r} "
                    f"(허용값: {allowed_text})"
                )

            date_text = row["date"]

            try:
                schedule_date = date.fromisoformat(date_text)
            except ValueError:
                raise ValueError(
                    f"입력 오류: CSV {reader.line_num}번째 줄의 "
                    f"날짜가 올바르지 않습니다: {date_text!r} "
                    "(YYYY-MM-DD 형식의 실제 날짜가 필요합니다.)"
                )

            if schedule_date.isoformat() != date_text:
                raise ValueError(
                    f"입력 오류: CSV {reader.line_num}번째 줄의 "
                    f"날짜 형식이 YYYY-MM-DD가 아닙니다: {date_text!r}"
                )

            if not start_date <= schedule_date <= end_date:
                raise ValueError(
                    f"입력 오류: CSV {reader.line_num}번째 줄의 "
                    f"날짜가 검사 기간 밖입니다: {date_text!r} "
                    f"(검사 기간: {start_date} ~ {end_date})"
                )

            rows.append(row)

    return rows


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parent

    config_path = project_dir / "config.toml"
    with open(config_path, mode="rb") as file:
        config = tomllib.load(file)

    allowed_shifts = config["rules"]["allowed_shifts"]
    # 작은 테스트용 설정 묶음을 가져옴
    dataset_config = config["datasets"]["small"]

    start_date = date.fromisoformat(dataset_config["start_date"])
    end_date = date.fromisoformat(dataset_config["end_date"])

    # 간호사 목록 읽기
    nurses_path = project_dir / "data" / "fixtures" / "small" / "nurses.csv"
    # nurses_path = project_dir / "sample_invalid_nurses.csv"
    nurses = read_nurses(nurses_path)

    print(f"읽은 간호사 행 수: {len(nurses)}")
    if nurses:
        print(f"첫 번째 간호사 행: {nurses[0]}")
    else:
        print("읽은 간호사 데이터 행이 없습니다.")

    # 근무표 읽기
    schedule_path = project_dir / "data" / "fixtures" / "small" / "base" / "schedule.csv"
    # schedule_path = project_dir / "sample_invalid_date.csv"
    # schedule_path = project_dir / "sample_required_value.csv"
    schedule = read_schedule(
        schedule_path,
        allowed_shifts,
        start_date,
        end_date,
    )

    print(f"읽은 행 수: {len(schedule)}")
    if schedule:
        print(f"첫 번째 행: {schedule[0]}")
    else:
        print("읽은 데이터 행이 없습니다.")
