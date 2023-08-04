from background_task import background
from datetime import datetime, timedelta, timezone
from getnotice import save_notices

@background(schedule=datetime(year=2023, month=8, day=4, hour=23, minute=15, tzinfo=timezone(timedelta(hours=9))))
def call_notices():
    save_notices()
    print("saved!")