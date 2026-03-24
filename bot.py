import requests
import time
import os
import sys

# --- CONFIGURATION VIA ENVIRONNEMENT ---
# Dans Docker, on passera la clé via -e SL_API_KEY="ta_cle"
API_KEY = os.getenv("SL_API_KEY", "CLE_NON_DEFINIE")
API_URL = "https://app.simplelogin.io/api/alias/random/new"

# Paramètres (tu peux aussi les mettre en ENV si tu veux)
NOMBRE_D_ALIAS = 1000
SLEEP_INTERVAL = 60
PAUSE_429 = 1800  # 30 minutes en secondes
NAME_DESCRIPTION = "Généré par Bot Aléatoire"

if API_KEY == "CLE_NON_DEFINIE":
    print("❌ Erreur : La variable d'environnement SL_API_KEY n'est pas définie.")
    sys.exit(1)

headers = {
    "Authentication": API_KEY,
    "Content-Type": "application/json"
}

def create_random_alias():
    data = {"note": NAME_DESCRIPTION}
    try:
        response = requests.post(API_URL, json=data, headers=headers)
        
        if response.status_code in [200, 201]:
            full_alias = response.json().get("alias")
            print(f"✅ Succès : {full_alias}")
            with open("alias_aleatoires.txt", "a") as f:
                f.write(f"{full_alias}\n")
            return "OK"
            
        elif response.status_code == 429:
            print(f"⚠️ Erreur 429 (Rate Limit). Pause de 30 minutes demandée...")
            return "WAIT"
            
        else:
            print(f"❌ Erreur {response.status_code} : {response.text}")
            return "ERROR"
            
    except Exception as e:
        print(f"⚠️ Erreur de connexion : {e}")
        return "ERROR"

# --- BOUCLE PRINCIPALE ---
print(f"🚀 Bot démarré. Cible : {NOMBRE_D_ALIAS} alias.")

created_count = 0
while created_count < NOMBRE_D_ALIAS:
    status = create_random_alias()
    
    if status == "OK":
        created_count += 1
        if created_count < NOMBRE_D_ALIAS:
            print(f"⏳ [{created_count}/{NOMBRE_D_ALIAS}] Attente de {SLEEP_INTERVAL}s...")
            time.sleep(SLEEP_INTERVAL)
            
    elif status == "WAIT":
        # On attend 30 minutes
        for remaining in range(30, 0, -1):
            print(f"🕒 Rate Limit atteint. Reprise dans {remaining} minutes...", end="\r")
            time.sleep(60)
        print("\n🔄 Tentative de reprise...")
        
    else:
        print("⏳ Petite pause de 10s avant de réessayer suite à une erreur...")
        time.sleep(10)

print("🏁 Mission terminée !")