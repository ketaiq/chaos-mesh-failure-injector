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
