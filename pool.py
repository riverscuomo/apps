import asyncio
# import iaqualink
from iaqualink import AqualinkClient
from rich import print
from datetime import datetime
from gspreader import get_sheet
from convert import timestampToDateObject
from functools import wraps
from asyncio.proactor_events import _ProactorBasePipeTransport
from dotenv import load_dotenv
import os
load_dotenv()

"""
I think this depends on this old version: iaqualink==0.3.90
"""

username = os.environ.get("POOL_USER")
password = os.environ.get("POOL_PASSWORD")


def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != "Event loop is closed":
                raise

    return wrapper


_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(
    _ProactorBasePipeTransport.__del__
)

""" """


async def connectToIAqua(temp):
    print("connectToIAqua...")
    
    async with AqualinkClient(username, password) as c:
        s = await c.get_systems()
        print(s)
        d = await list(s.values())[0].get_devices()
        print(d["pool_set_point"].data["state"])

        device = d["pool_set_point"]
        await device.set_temperature(temp)
        # print("Success!")

        # d['pool_set_point'].data['state'] =  temp
        # print(d['pool_set_point'].data)


def getTemp():
    print("getTemp...")
    sheet = get_sheet("Calendar: weezer/rc", 0)
    data = sheet.get_all_records(head=2)
    today = datetime.today().date()


    for row in data:
        calDateString = row["date"] + " " + str(row["year"])
        calDateDto = timestampToDateObject(calDateString).date()
        if calDateDto == today:
            # print(today)
            # print(row['pool'])
            return int(row["pool"])


def main():

    print("pool.py main()...")

    temp = getTemp()
    print(temp)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(connectToIAqua(temp))

    loop.close()

    # local_encoding = "cp850"  # adapt for other encodings
    deg = "\xb0"

    m = f"Success! Pool set to {temp}{deg}."
    print(m)

    return m


if __name__ == "__main__":

    main()
