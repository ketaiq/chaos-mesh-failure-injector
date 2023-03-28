from app.utils.string import add_time
from datetime import timedelta


def test_compute_failure_begin():
    iso_format_time = add_time(
        "26/03/2023, 12:14:38",
        timedelta(hours=9, minutes=10),
    )
    assert iso_format_time == "2023-03-26T21:24:38+01:00"


def main():
    test_compute_failure_begin()


if __name__ == "__main__":
    main()
