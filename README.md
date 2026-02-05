# Random Name Generator

A Python-based random name generator that uses weighted probabilities for realistic phonetic results and includes a multi-threaded mini-game.

## Features

- **Weighted Generation**: The first two letters of each name are generated based on language frequency weights (e.g., 'a' is more frequent than 'y').
- **Phonetic Logic**: Automatically alternates between vowels and consonants to create readable names.
- **Multi-threaded Mini-Game**: Includes a "Crack the Name" game where multiple threads compete to brute-force a target name.
- **Interactive CLI**: Simple menu-driven interface.

## Requirements

- Python 3.x

## Usage

Run the generator directly from your terminal:

```bash
python generator.py
```

### Menu Options

1. **Générer 5 noms aléatoires**: Instantly generates 5 names following the phonetic rules.
2. **Mini-Jeu : Trouver mon nom**: Enter a name, and the script will launch 4 parallel threads to try and generate that exact name, showing real-time attempts.
3. **Quitter**: Exit the application.

## How it Works

### Name Generation logic
The script uses a weighted system for the start of the name to avoid awkward combinations. It then alternates vowels and consonants. There is a 75% chance that a name ends with a vowel, and the starting letter (vowel or consonant) is calculated to respect this preference based on the desired name length.

### Multi-threading
The mini-game uses `concurrent.futures.ThreadPoolExecutor` to run 4 workers. Each worker generates names as fast as possible until one of them hits the target.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
