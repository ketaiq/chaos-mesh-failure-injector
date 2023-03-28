from datetime import datetime, timedelta, timezone


def convert_duration(duration: int) -> str:
    """
    Converts duration in minutes to compact string format.

    Parameters
    ----------
    duration : int
        duration of the workflow in minutes
    """
    duration_hour = int(duration / 60)
    duration_minute = duration - duration_hour * 60
    duration_str = ""
    if duration_hour > 0:
        duration_str += f"{duration_hour}h"
    if duration_minute > 0:
        duration_str += f"{duration_minute}m"
    return duration_str


def add_time(
    start: str,
    suspend: timedelta,
):
    """
    Computes the new time with addition of suspending time and returns the result in ISO 8601 format.

    Parameters
    ----------
    start : str
        starting time of the experiment in locust report format like 26/03/2023, 12:14:38
    suspend : timedelta
        suspending time after starting time
    """
    start_dt_utc = datetime.strptime(start, "%d/%m/%Y, %H:%M:%S")
    start_dt = datetime(
        start_dt_utc.year,
        start_dt_utc.month,
        start_dt_utc.day,
        start_dt_utc.hour,
        start_dt_utc.minute,
        start_dt_utc.second,
        tzinfo=timezone(timedelta(hours=1)),
    )
    start_timestamp = (start_dt + suspend).timestamp()
    # use time zone CET(UTC+1) by default
    end_dt = datetime.fromtimestamp(start_timestamp, timezone(timedelta(hours=1)))
    return end_dt.isoformat()


def print_failure_period(start: str, suspend: timedelta, failure_duration: timedelta):
    failure_start = add_time(start, suspend)
    print(failure_start)
    failure_end = (datetime.fromisoformat(failure_start) + failure_duration).isoformat()
    print(failure_end)
