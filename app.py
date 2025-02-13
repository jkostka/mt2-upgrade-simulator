from flask import Flask, request, render_template
import random
import statistics

app = Flask(__name__)

# Inicjalizacja wartości poza funkcją index
start_level = 0
number_of_attempts = 0
item_type = "please_choice"
enchantment_type = "please_choice"
number_of_simulations = 100

def modyfikuj_szanse(basic_chance, enchantment_type):
    modyfikator = 0
    if enchantment_type == "rytualny kamień":
        modyfikator = 10
    elif enchantment_type == "pieczęć boga smoków":
        modyfikator = 15

    if isinstance(basic_chance, list):
        szanse_zmodyfikowane = [min(100, szansa + modyfikator) for szansa in basic_chance]
        return [int(szansa) for szansa in szanse_zmodyfikowane]
    elif isinstance(basic_chance, dict):
        szanse_zmodyfikowane = {k: min(100, v + modyfikator) for k, v in basic_chance.items()}
        return {k: int(v) for k, v in szanse_zmodyfikowane.items()}
    else:
        return basic_chance

def symuluj_ulepszanie(start_level, number_of_attempts, item_type, enchantment_type):
    if item_type == "talisman":
        basic_chance = [55, 50, 45, 40, 35, 30, 25, 20, 15, 10]
    elif item_type == "serpentEquipment":
        basic_chance = {
            1: 90, 2: 75, 3: 60, 4: 50, 5: 40, 6: 30,
            7: 25, 8: 15, 9: 8, 10: 5, 11: 5, 12: 5,
            13: 5, 14: 3, 15: 3
        }
    else:
        return None, None
    szanse = modyfikuj_szanse(basic_chance, enchantment_type)
    actual_level = start_level
    historia_ulepszen = [start_level]

    for _ in range(number_of_attempts):
        if (item_type == "serpentEquipment" and actual_level >= 15) or \
           (item_type == "talisman" and actual_level >= 200):
            historia_ulepszen.append(actual_level)
            continue
        indeks_szansy = (actual_level - 1) % 10 if item_type == "talisman" else actual_level
        if isinstance(szanse, dict):
            szansa = szanse.get(actual_level + 1, 0)
        else:
            szansa = szanse[indeks_szansy]
        if szansa == 0:
            historia_ulepszen.append(actual_level)
            continue

        losowa_liczba = random.randint(1, 100)
        if losowa_liczba <= szansa:
            actual_level += 1
            historia_ulepszen.append(actual_level)
        else:
            historia_ulepszen.append(actual_level)

    return actual_level, historia_ulepszen

@app.route("/", methods=["GET", "POST"])
def index():
    global start_level, number_of_attempts, item_type, enchantment_type, number_of_simulations

    wyniki = None
    error_message = None

    if request.method == "POST":
        try:
            item_type = request.form.get("item_type")
            start_level = int(request.form.get("start_level"))
            number_of_attempts = int(request.form.get("number_of_attempts"))
            enchantment_type = request.form.get("enchantment_type")
            number_of_simulations = int(request.form.get("number_of_simulations"))

            if item_type == "please_choice":
                error_message = "Proszę wybrać rodzaj przedmiotu."
            elif item_type == "serpentEquipment" and enchantment_type == "please_choice":
                error_message = "Proszę wybrać rodzaj zwoju dla ekwipinku wężowego."
            elif not 1 <= number_of_simulations <= 1000:
                error_message = "Ilość symulacji musi być w zakresie od 1 do 1000."
            elif start_level < 0:
                error_message = "Startowy poziom nie może być ujemny."
            elif number_of_attempts <= 0:
                error_message = "Ilość prób musi być większa od 0."
            elif item_type == "serpentEquipment" and start_level >= 15:
                error_message = "Maksymalny poziom ulepszenia wężowego ekwipunku to +15."
            elif item_type == "talisman" and start_level >= 200:
                error_message = "Maksymalny poziom ulepszenia talizmanu to +200."    

            if error_message:
                return render_template("index.html", wyniki=wyniki, start_level=start_level, number_of_attempts=number_of_attempts, item_type=item_type, enchantment_type=enchantment_type, number_of_simulations=number_of_simulations, error_message=error_message), 400

            koncowe_levele = []
            for _ in range(number_of_simulations):
                koncowy_level, _ = symuluj_ulepszanie(start_level, number_of_attempts, item_type, enchantment_type)
                if koncowy_level is None:
                    return "Niepoprawny rodzaj przedmiotu", 400
                koncowe_levele.append(koncowy_level)

            sredni = statistics.mean(koncowe_levele)
            mediana = statistics.median(koncowe_levele)
            try:
                domina = statistics.mode(koncowe_levele)
            except statistics.StatisticsError:
                domina = "Brak jednoznacznej dominanty"

            level_counters = {}
            for level in koncowe_levele:
                level_counters[level] = level_counters.get(level, 0) + 1

            wyniki = {
                "sredni": sredni,
                "mediana": mediana,
                "domina": domina,
                "start": start_level,
                "prob": number_of_attempts,
                "item_type": item_type,
                "enchantment_type": enchantment_type,
                "liczniki": level_counters,
                "iloscsymulacji": number_of_simulations
            }
        except ValueError:
            error_message = "Wprowadź poprawne dane liczbowe."
            return render_template("index.html", wyniki=wyniki, start_level=start_level, number_of_attempts=number_of_attempts, item_type=item_type, enchantment_type=enchantment_type, number_of_simulations=number_of_simulations, error_message=error_message), 400

    return render_template("index.html", wyniki=wyniki, start_level=start_level, number_of_attempts=number_of_attempts, item_type=item_type, enchantment_type=enchantment_type, number_of_simulations=number_of_simulations, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)