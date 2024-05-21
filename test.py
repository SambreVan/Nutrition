import os
import json
import csv

def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Erreur de décodage JSON : vérifiez le format du fichier.")
    except FileNotFoundError:
        print("Fichier non trouvé : vérifiez le chemin du fichier.")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
    return None

def save_to_csv(product_name, nutrition_info, file_path='output.csv'):
    fieldnames = ['Nom du produit', 'Énergie (kcal pour 100g)', 'Protéines (g pour 100g)',
                  'Glucides (g pour 100g)', 'Sucres (g pour 100g)', 'Lipides (g pour 100g)',
                  'Acides gras saturés (g pour 100g)', 'Sel (g pour 100g)']
    row = {**{'Nom du produit': product_name}, **nutrition_info}

    if 'Non disponible' not in row.values():
        try:
            with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if csvfile.tell() == 0:  
                    writer.writeheader()
                writer.writerow(row)
            print("Données enregistrées avec succès dans:", file_path)
        except Exception as e:
            print(f"Erreur lors de l'écriture dans le fichier CSV : {e}")

def process_directory(directory_path, output_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                data = load_json_data(file_path)
                product_name, nutrition_info = get_essential_information(data)
                if product_name and nutrition_info:
                    save_to_csv(product_name, nutrition_info, output_path)

def get_essential_information(data):
    if data is None:
        return None, {}

    product_name = data.get('product_name', 'Nom non disponible')
    nutrients = data.get('nutriments', {})
    nutrition_info = {
        'Énergie (kcal pour 100g)': nutrients.get('energy-kcal_100g', 'Non disponible'),
        'Protéines (g pour 100g)': nutrients.get('proteins_100g', 'Non disponible'),
        'Glucides (g pour 100g)': nutrients.get('carbohydrates_100g', 'Non disponible'),
        'Sucres (g pour 100g)': nutrients.get('sugars_100g', 'Non disponible'),
        'Lipides (g pour 100g)': nutrients.get('fat_100g', 'Non disponible'),
        'Acides gras saturés (g pour 100g)': nutrients.get('saturated-fat_100g', 'Non disponible'),
        'Sel (g pour 100g)': nutrients.get('salt_100g', 'Non disponible')
    }
    
    return product_name, nutrition_info


main_directory_path = 'C:/Users/Pinta/Desktop/ProjetFinDAnnee/Folders'
output_csv_path = os.path.join(main_directory_path, '../output.csv')
process_directory(main_directory_path, output_csv_path)
