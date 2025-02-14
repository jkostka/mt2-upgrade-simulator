from flask import Flask, request, render_template
import random
import statistics

app = Flask(__name__)

# Inicjalizacja wartości poza funkcją index
start_level = 0
number_of_attemps = 0
item_type = "please_choice"
scroll_type = "please_choice"
number_of_simulations = 100

def increase_chance(basic_chance, scroll_type):
    modificator = 0
    if scroll_type == "ritual_stone":
        modificator = 10
    elif scroll_type == "god_seal":
        modificator = 15

    if isinstance(basic_chance, list):
        increased_chance = [min(100, chance + modificator) for chance in basic_chance]
        return [int(chance) for chance in increased_chance]
    elif isinstance(basic_chance, dict):
        increased_chance = {k: min(100, v + modificator) for k, v in basic_chance.items()}
        return {k: int(v) for k, v in increased_chance.items()}
    else:
        return basic_chance

def start_simulate(start_level, number_of_attemps, item_type, scroll_type):
    if item_type == "talisman":
        basic_chance = [55, 50, 45, 40, 35, 30, 25, 20, 15, 10]
    elif item_type == "serpent_equipment":
        basic_chance = {
            1: 90, 2: 75, 3: 60, 4: 50, 5: 40, 6: 30,
            7: 25, 8: 15, 9: 8, 10: 5, 11: 5, 12: 5,
            13: 5, 14: 3, 15: 3
        }
    else:
        return None, None
    total_chance = increase_chance(basic_chance, scroll_type)
    actual_level = start_level
    upgrade_history = [start_level]

    for _ in range(number_of_attemps):
        if (item_type == "serpent_equipment" and actual_level >= 15) or \
           (item_type == "talisman" and actual_level >= 200):
            upgrade_history.append(actual_level)
            continue
        chance_index = (actual_level - 1) % 10 if item_type == "talisman" else actual_level
        if isinstance(total_chance, dict):
            chance = total_chance.get(actual_level + 1, 0)
        else:
            chance = total_chance[chance_index]
        if chance == 0:
            upgrade_history.append(actual_level)
            continue

        random_number = random.randint(1, 100)
        if random_number <= chance:
            actual_level += 1
            upgrade_history.append(actual_level)
        else:
            upgrade_history.append(actual_level)

    return actual_level, upgrade_history

@app.route("/", methods=["GET", "POST"])
def index():
    global start_level, number_of_attemps, item_type, scroll_type, number_of_simulations

    results = None
    error_message = None

    if request.method == "POST":
        try:
            item_type = request.form.get("item_type")
            start_level = int(request.form.get("start_level"))
            number_of_attemps = int(request.form.get("number_of_attemps"))
            scroll_type = request.form.get("scroll_type")
            number_of_simulations = int(request.form.get("number_of_simulations"))

            if item_type == "please_choice":
                error_message = "Proszę wybrać rodzaj przedmiotu."
            elif item_type == "serpent_equipment" and scroll_type == "please_choice":
                error_message = "Proszę wybrać rodzaj zwoju dla broni."
            elif not 1 <= number_of_simulations <= 1000:
                error_message = "Ilość symulacji musi być w zakresie od 1 do 1000."
            elif start_level < 0:
                error_message = "Startowy poziom nie może być ujemny."
            elif number_of_attemps <= 0:
                error_message = "Ilość prób musi być większa od 0."
            elif item_type == "serpent_equipment" and start_level >= 15:
                error_message = "Maksymalny poziom ulepszenia wężowego ekwipunku to +15."
            elif item_type == "talisman" and start_level >= 200:
                error_message = "Maksymalny poziom ulepszenia talizmanu to +200."    

            if error_message:
                return render_template("index.html", results=results, start_level=start_level, number_of_attemps=number_of_attemps, item_type=item_type, scroll_type=scroll_type, number_of_simulations=number_of_simulations, error_message=error_message), 400

            end_levels = []
            for _ in range(number_of_simulations):
                end_level, _ = start_simulate(start_level, number_of_attemps, item_type, scroll_type)
                if end_level is None:
                    return "Niepoprawny rodzaj przedmiotu", 400
                end_levels.append(end_level)

            average = statistics.mean(end_levels)
            mediana = statistics.median(end_levels)
            try:
                domina = statistics.mode(end_levels)
            except statistics.StatisticsError:
                domina = "Brak jednoznacznej dominanty"

            level_counters = {}
            for level in end_levels:
                level_counters[level] = level_counters.get(level, 0) + 1

            results = {
                "average": average,
                "mediana": mediana,
                "domina": domina,
                "start": start_level,
                "attemps": number_of_attemps,
                "item_type": item_type,
                "scroll_type": scroll_type,
                "counters": level_counters,
                "number_of_simulations": number_of_simulations
            }
        except ValueError:
            error_message = "Wprowadź poprawne dane liczbowe."
            return render_template("index.html", results=results, start_level=start_level, number_of_attemps=number_of_attemps, item_type=item_type, scroll_type=scroll_type, number_of_simulations=number_of_simulations, error_message=error_message), 400

    return render_template("index.html", results=results, start_level=start_level, number_of_attemps=number_of_attemps, item_type=item_type, scroll_type=scroll_type, number_of_simulations=number_of_simulations, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)