import requests
import time

# --- CONFIGURATION ---
API_KEY = "KEy-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Remplacez par votre clé API SimpleLogin
# URL pour créer un alias totalement aléatoire
API_URL = "https://app.simplelogin.io/api/alias/random/new"
NOMBRE_D_ALIAS = 1000
SLEEP_INTERVAL = 30  # en secondes

headers = {
    "Authentication": API_KEY,
    "Content-Type": "application/json"
}

def create_random_alias():
    # On peut optionnellement envoyer une note
    data = {"note": "Généré par Bot Aléatoire"}
    
    try:
        response = requests.post(API_URL, json=data, headers=headers)
        
        if response.status_code == 201 or response.status_code == 200:
            alias_data = response.json()
            full_alias = alias_data.get("alias")
            print(f"✅ Alias créé avec succès : {full_alias}")
            
            # Sauvegarde dans le fichier
            with open("alias_aleatoires.txt", "a") as f:
                f.write(f"{full_alias}\n")
        else:
            print(f"❌ Erreur {response.status_code} : {response.text}")
            
    except Exception as e:
        print(f"⚠️ Erreur de connexion : {e}")

# --- BOUCLE ---
print(f"Démarrage du bot en mode ALÉATOIRE. Intervalle : 30s.")

for i in range(NOMBRE_D_ALIAS):
    print(f"[{i+1}/{NOMBRE_D_ALIAS}] Création en cours...")
    create_random_alias()
    
    if i < NOMBRE_D_ALIAS - 1:
        print("⏳ Pause de 30 secondes...")
        time.sleep(SLEEP_INTERVAL)

print("🏁 Opération terminée. Les alias sont dans 'alias_aleatoires.txt'.")