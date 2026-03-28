"""
BOB Discord Bot Configurator
Developed by BOB
"""

import requests
import time
import sys

# ==========================================
# CONFIGURATION
# ==========================================
# WARNING: NEVER SHARE YOUR USER TOKEN PUBLICLY
USER_TOKEN = 'YOUR_USER_TOKEN_HERE' 
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
GUILD_ID = 'YOUR_GUILD_ID_HERE'

API = 'https://discord.com/api/v10'

BH = {'Authorization': f'Bot {BOT_TOKEN}', 'Content-Type': 'application/json'}
UH = {'Authorization': USER_TOKEN, 'Content-Type': 'application/json'}

def bapi(m, e, d=None):
    r = getattr(requests, m)(f"{API}{e}", headers=BH, json=d)
    if r.status_code in [200, 201, 204]:
        try: return r.json()
        except: return True
    return None

def usend(cid, txt):
    r = requests.post(f"{API}/channels/{cid}/messages", headers=UH, json={"content": txt})
    if r.status_code in [200, 201]:
        print(f"  >> {txt[:60]}")
        return True
    return False

def configure_bots():
    print("=" * 55)
    print("  BOB DISCORD AUTOMATOR - BOT CONFIGURATOR")
    print("=" * 55)

    channels = bapi('get', f'/guilds/{GUILD_ID}/channels')
    ch = {c['name']: c['id'] for c in channels} if channels else {}

    # Define your channels here
    bot_ch = ch.get('\u0627\u0648\u0627\u0645\u0631-\u0627\u0644\u0628\u0648\u062a\u0627\u062a') # bot-commands
    music_ch = ch.get('\u0628\u0648\u062a-\u0627\u0644\u0645\u0648\u0633\u064a\u0642\u0649') # music-bot

    D = 4

    if bot_ch:
        print("\nConfiguring Carl-bot...")
        usend(bot_ch, "!autorole add Member")
        time.sleep(D)
        for am in ["spam", "links", "invites", "caps", "massmention"]:
            usend(bot_ch, f"!automod {am} on")
            time.sleep(D)

        print("\nConfiguring ProBot...")
        usend(bot_ch, "#autorole Member")
        time.sleep(D)
        usend(bot_ch, "#anti raid on")
        time.sleep(D)

    if music_ch:
        print("\nConfiguring Jockie Music...")
        usend(music_ch, "m!setup")
        time.sleep(D)

    print("\n" + "=" * 55)
    print("  DONE! All bots configured!")
    print("=" * 55)

if __name__ == "__main__":
    configure_bots()
