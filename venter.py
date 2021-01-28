import os, time, asyncio, aiohttp, re

W, H = os.get_terminal_size()

FILTER = True
PATTERN = r"^(\d+)$"

async def retrieve(to_print, printed):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.ventspace.life/api/v1/ventpost/recent') as response:
            recents = await response.json()
    
    for msg in [recent["messageText"] for recent in recents]:
        if msg not in printed and not re.match(r"^(\d+)$", msg):
            to_print.append(msg)

async def print_msg(to_print, printed):
    while to_print:
        msg = to_print.pop(0)
        printed.add(msg)
        print(msg.center(W))
        await asyncio.sleep(1)
    
async def venter(to_print, printed):
    await retrieve(to_print, printed)
    await print_msg(to_print, printed)

def main():
    to_print = []
    printed = set()
    
    while True:
        asyncio.run(venter(to_print, printed))
        
if __name__ == "__main__":
    main()
