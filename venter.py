import os, time, asyncio, aiohttp, re, random

W, H = os.get_terminal_size()

FILTER = True
PATTERN = r"^(\d+)$"
API_COOLDOWN = 1

async def retrieve(to_print, printed):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.ventspace.life/api/v1/ventpost/recent') as response:
            recents = await response.json()
            await asyncio.sleep(API_COOLDOWN)
    
    for msg in [recent["messageText"] for recent in recents]:
        if msg not in printed and not re.match(r"^(\d+)$", msg):
            to_print.append(msg)

async def print_msg(to_print, printed):
    while to_print:
        msg = to_print.pop(0)
        printed[msg] = "Ø"
        print(msg.center(W))
        await asyncio.sleep(1)
    
async def venter(to_print, printed):
    try:
        await retrieve(to_print, printed)
        await print_msg(to_print, printed)
    except Exception as e:
        pass

def main():
    to_print = []
    printed = {}
    
    while True:
        try:
            asyncio.run(venter(to_print, printed))
        except:
            with open(f"vent_session_{random.randint(0, 37543)}.txt", "w") as f:
                f.writelines(msg + '\n' for msg in printed)
            break
        
if __name__ == "__main__":
    main()
