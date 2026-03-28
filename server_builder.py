"""
BOB Discord Server Automator
Developed by BOB
"""

import requests
import time
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ==========================================
# CONFIGURATION
# ==========================================
# REPLACE WITH YOUR BOT TOKEN
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE' 
# REPLACE WITH YOUR SERVER ID
GUILD_ID = 'YOUR_GUILD_ID_HERE'

API = 'https://discord.com/api/v10'
HEADERS = {'Authorization': f'Bot {BOT_TOKEN}', 'Content-Type': 'application/json'}

def api(method, endpoint, data=None):
    r = getattr(requests, method)(f"{API}{endpoint}", headers=HEADERS, json=data)
    if r.status_code == 429:
        w = r.json().get('retry_after', 2)
        print(f"  [Rate limited {w}s...]")
        time.sleep(w + 0.5)
        r = getattr(requests, method)(f"{API}{endpoint}", headers=HEADERS, json=data)
    if r.status_code in [200, 201, 204]:
        try: return r.json()
        except: return True
    else:
        print(f"  ERR {r.status_code}: {r.text[:100]}")
        return None

def build_server():
    print("=" * 55)
    print("  BOB DISCORD AUTOMATOR - SERVER BUILDER")
    print("=" * 55)

    print("\n[1] Deleting old channels...")
    channels = api('get', f'/guilds/{GUILD_ID}/channels')
    if channels:
        for ch in channels:
            api('delete', f'/channels/{ch["id"]}')
            time.sleep(0.3)
    print("  Done!")

    roles_list = api('get', f'/guilds/{GUILD_ID}/roles')
    roles = {r['name']: r['id'] for r in roles_list} if roles_list else {}

    everyone = GUILD_ID

    # Setup permissions
    def readonly():
        return [{"id": everyone, "type": 0, "allow": "1024", "deny": "2048"}]
    def public():
        return []

    # Customize your channel structure here
    structure = [
        {
            "name": "\u0627\u0644\u062a\u0631\u062d\u064a\u0628", # Welcome
            "channels": [
                {"name": "\u0627\u0647\u0644\u0627-\u0648\u0633\u0647\u0644\u0627", "type": 0, "topic": "Welcome!", "perm": readonly()},
                {"name": "\u0627\u0644\u0642\u0648\u0627\u0646\u064a\u0646", "type": 0, "topic": "Rules", "perm": readonly()},
            ]
        },
        {
            "name": "\u0627\u0644\u062f\u0631\u062f\u0634\u0629", # Chat
            "channels": [
                {"name": "\u0627\u0644\u0639\u0627\u0645", "type": 0, "topic": "General chat", "perm": public()},
            ]
        }
    ]

    print("\n[2] Creating Arabic channels...")
    total = 0
    for cat in structure:
        category = api('post', f'/guilds/{GUILD_ID}/channels', {"name": cat['name'], "type": 4})
        if not category:
            continue
        cat_id = category['id']
        print(f"\n  [{cat['name']}]")
        time.sleep(0.3)

        for c in cat['channels']:
            data = {"name": c['name'], "type": c['type'], "parent_id": cat_id, "permission_overwrites": c.get('perm', [])}
            if 'topic' in c:
                data['topic'] = c['topic']
            result = api('post', f'/guilds/{GUILD_ID}/channels', data)
            if result:
                total += 1
                p = '#' if c['type'] == 0 else 'VC:'
                print(f"    {p} {c['name']}")
            time.sleep(0.3)

    print(f"\n  Total: {total} channels created!")
    print("\n" + "=" * 55)
    print("  DONE! All channels are now ready!")
    print("=" * 55)

if __name__ == "__main__":
    build_server()
