import random
import string
import time
import threading
import concurrent.futures

# --- Configuration des poids pour les 2 premières lettres ---

# Voyelles : A très fréquent, Y très rare
# A=50, E=40, I=30, O=20, U=10, Y=5
WEIGHTED_VOWELS_CHARS = list("aeiouy")
WEIGHTED_VOWELS_PROBS = [50, 40, 30, 20, 10, 5]

# Consonnes : Q, W, X très rares
RARE_CONSONANTS = "qwx"
COMMON_CONSONANTS = "".join(sorted(list(set(string.ascii_lowercase) - set("aeiouy") - set(RARE_CONSONANTS))))

# On construit la liste complète des consonnes et leurs poids associés
WEIGHTED_CONSONANTS_CHARS = list(COMMON_CONSONANTS) + list(RARE_CONSONANTS)
# Poids : 15 pour les communes, 1 pour les rares (pour marquer vraiment la différence)
WEIGHTED_CONSONANTS_PROBS = [15] * len(COMMON_CONSONANTS) + [1] * len(RARE_CONSONANTS)

# --- Listes uniformes pour le reste du nom ---
ALL_VOWELS = "aeiouy"
ALL_CONSONANTS = "".join(set(string.ascii_lowercase) - set(ALL_VOWELS))

def get_weighted_letter(is_vowel):
    """Retourne une lettre en fonction des poids définis (pour le début du nom)."""
    if is_vowel:
        return random.choices(WEIGHTED_VOWELS_CHARS, weights=WEIGHTED_VOWELS_PROBS, k=1)[0]
    else:
        return random.choices(WEIGHTED_CONSONANTS_CHARS, weights=WEIGHTED_CONSONANTS_PROBS, k=1)[0]

def generate_random_name(max_length=6, fixed_length=None):
    """
    Génère un nom aléatoire.
    :param max_length: Longueur maximale si fixed_length n'est pas défini.
    :param fixed_length: Force la longueur du nom (utile pour le jeu).
    """
    if fixed_length:
        length = fixed_length
    else:
        length = random.randint(3, max_length)
    
    # 75% de chance de finir par une voyelle
    ends_with_vowel = random.random() < 0.75
    
    # Adaptation pour la consistance : si on force la longueur, on respecte quand même la logique de fin
    if ends_with_vowel:
        start_with_vowel = (length % 2 != 0)
    else:
        start_with_vowel = (length % 2 == 0)

    name = []
    is_vowel = start_with_vowel
    
    for i in range(length):
        letter = ""
        # Règle spéciale pour les 2 premières lettres uniquement
        if i < 2:
            letter = get_weighted_letter(is_vowel)
        else:
            # Aléatoire classique pour la fin du nom
            if is_vowel:
                letter = random.choice(ALL_VOWELS)
            else:
                letter = random.choice(ALL_CONSONANTS)
        
        name.append(letter)
        is_vowel = not is_vowel # Alternance
        
    return "".join(name).capitalize()

# --- Logique du Mini-Jeu Multi-thread ---

def search_worker(target_name, stop_event, thread_id, show_progress=False):
    """Fonction exécutée par chaque thread pour chercher le nom."""
    count = 0
    length = len(target_name)
    
    while not stop_event.is_set():
        generated = generate_random_name(fixed_length=length)
        count += 1
        
        # Si c'est le thread désigné pour l'affichage
        if show_progress and count % 10 == 0:
            # On affiche le nom sur la même ligne pour un effet "défilement"
            print(f"\r🔍 Recherche... Tentative : {generated} ", end="", flush=True)
            time.sleep(0.01) # Petit délai pour que l'œil puisse voir
            
        if generated == target_name:
            if not stop_event.is_set():
                stop_event.set()
                print(f"\n\n✅ TROUVÉ PAR LE THREAD #{thread_id} !")
                return (True, count, thread_id)
    
    return (False, count, thread_id)

def start_minigame():
    print("\n--- 🎲 MINI-JEU : CRACK THE NAME 🎲 ---")
    target = input("Entrez le nom cible à trouver : ").strip().capitalize()
    
    print(f"Lancement des moteurs de recherche pour '{target}'...")
    time.sleep(1)
    
    start_time = time.time()
    stop_event = threading.Event()
    
    num_threads = 4
    total_attempts = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i in range(num_threads):
            # Le thread 0 sera celui qui affiche ses progrès
            show = (i == 0)
            futures.append(executor.submit(search_worker, target, stop_event, i, show))
        
        try:
            for future in concurrent.futures.as_completed(futures):
                found, count, thread_id = future.result()
                total_attempts += count
                if found:
                    end_time = time.time()
                    duration = end_time - start_time
                    print(f"⏱️  Temps total : {duration:.4f} secondes")
                    print(f"🔄 Tentatives du thread gagnant : {count}")
                    break
        except KeyboardInterrupt:
            stop_event.set()
            print("\n🛑 Recherche arrêtée.")

if __name__ == "__main__":
    while True:
        print("\n=== GÉNÉRATEUR DE NOMS ===")
        print("1. Générer 5 noms aléatoires")
        print("2. Mini-Jeu : Trouver mon nom")
        print("3. Quitter")
        
        choice = input("Choix : ")
        
        if choice == "1":
            print("\n--- Noms Générés ---")
            for _ in range(5):
                print(generate_random_name())
        elif choice == "2":
            start_minigame()
        elif choice == "3":
            print("Bye !")
            break
        else:
            print("Choix invalide.")