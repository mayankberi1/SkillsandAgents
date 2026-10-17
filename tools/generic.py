from datetime import date, datetime

from langchain_core.tools import tool


@tool
def get_todays_date() -> str:
    """
    get today's date
    :return: date in string format %Y-%m-%d
    """
    today = date.today()
    return today.strftime("%Y-%m-%d")

@tool
def get_time() -> str:
    """
    get  time right now
    :return: time in string format %H:%M:%S
    """
    now = datetime.now()
    return now.strftime("%H:%M:%S")
