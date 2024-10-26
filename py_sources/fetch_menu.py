#!/usr/bin/env python3
"""Module docstring."""

from pathlib import Path
from enum import Enum
import requests
from bs4 import BeautifulSoup

# Couleurs pour la sortie terminal
class Colors(Enum):
    """Colors class docstring."""
    RED = "\033[31m"
    RESET = "\033[0m"

def fetch_first_menu(url):
    """
    Récupère et affiche le premier menu d'un restaurant universitaire à partir de son URL.
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # On utilise BeautifulSoup pour parser l'html
            soup = BeautifulSoup(response.content, "html.parser")

            # Nom du restaurant
            restaurant_name_element = soup.find("h1", class_="post_title")
            if restaurant_name_element:
                restaurant_name = restaurant_name_element.get_text(strip=True)
            else:
                restaurant_name = "Nom non spécifié"

            # Récupérer la date du menu
            menu_date = soup.find("div", class_="menu_date")
            if menu_date:
                date_element = menu_date.find("time", class_="menu_date_title")
                if date_element:
                    date_text = date_element.get_text(strip=True)
                else:
                    date_text = "Date non spécifiée"
                print(f"\n{Colors.RED.value}{date_text} pour {restaurant_name}:{Colors.RESET.value}")

                # Récupérer les repas
                meal = menu_date.find_next("div", class_="meal")
                if meal:
                    meal_title = meal.find("div", class_="meal_title").get_text(strip=True)
                    print(f"  {meal_title}:")
                    meal_foodies = meal.find("ul", class_="meal_foodies")
                    for item in meal_foodies.find_all("li", recursive=False):
                        category = item.get_text(strip=True, separator=': ')
                        print(f"    - {category}")
                else:
                    print("  Aucun repas trouvé pour cette date.")
            else:
                print("Aucune date de menu trouvée.")
        else:
            print(f"Erreur {response.status_code} en accédant à {url}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête vers {url}: {e}")

def main():
    """Main function docstring."""
    # Les urls se trouve dans urls.txt, dans le dossier urls à la racine du projet
    current_directory = Path(__file__).parent
    urls_directory = current_directory.parent / "urls"
    file_path = urls_directory / "urls.txt"

    # Pour chaque url, appel de fetch_first_menu.py
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            urls = [line.strip() for line in file if line.strip()]

        for url in urls:
            fetch_first_menu(url)

    except FileNotFoundError:
        print(f"Fichier 'urls.txt' introuvable à l'emplacement {file_path}.")

if __name__ == "__main__":
    main()
