from background_task import background
from datetime import datetime, timedelta, timezone
from getnotice import save_notices

@background(schedule=60)
def call_notices():
    save_notices()
    print("saved!")