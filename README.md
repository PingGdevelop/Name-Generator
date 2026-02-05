# Générateur de Noms Aléatoires

Un générateur de noms aléatoires basé sur Python qui utilise des probabilités pondérées pour des résultats phonétiques réalistes et inclut un mini-jeu multi-thread.

## Fonctionnalités

- **Génération Pondérée** : Les deux premières lettres de chaque nom sont générées en fonction de poids de fréquence linguistique (par exemple, 'a' est plus fréquent que 'y').
- **Logique Phonétique** : Alterne automatiquement entre voyelles et consonnes pour créer des noms lisibles.
- **Mini-Jeu Multi-thread** : Comprend un jeu "Trouver le nom" où plusieurs threads s'affrontent pour trouver un nom cible par force brute.
- **CLI Interactive** : Interface simple pilotée par menu.

## Prérequis

- Python 3.x

## Utilisation

Lancez le générateur directement depuis votre terminal :

```bash
python generator.py
```

### Options du Menu

1. **Générer 5 noms aléatoires** : Génère instantanément 5 noms en suivant les règles phonétiques.
2. **Mini-Jeu : Trouver mon nom** : Entrez un nom, et le script lancera 4 threads en parallèle pour tenter de générer ce nom exact, en affichant les tentatives en temps réel.
3. **Quitter** : Quitte l'application.

## Fonctionnement

### Logique de génération de noms
Le script utilise un système de pondération pour le début du nom afin d'éviter les combinaisons étranges. Il alterne ensuite voyelles et consonnes. Il y a 75 % de chances qu'un nom se termine par une voyelle, et la lettre de départ (voyelle ou consonne) est calculée pour respecter cette préférence en fonction de la longueur de nom souhaitée.

### Multi-threading
Le mini-jeu utilise `concurrent.futures.ThreadPoolExecutor` pour exécuter 4 workers. Chaque worker génère des noms aussi vite que possible jusqu'à ce que l'un d'entre eux atteigne la cible.

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.
