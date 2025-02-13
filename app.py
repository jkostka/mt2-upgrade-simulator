from flask import Flask, request, render_template
import random
import statistics

app = Flask(__name__)

# Inicjalizacja wartości poza funkcją index
start_level = 0
ilosc_prob = 0
rodzaj_przedmiotu = "proszę wybrać"
rodzaj_zwoju = "proszę wybrać"
ilosc_symulacji = 100

def modyfikuj_szanse(szanse_bazowe, rodzaj_zwoju):
    modyfikator = 0
    if rodzaj_zwoju == "rytualny kamień":
        modyfikator = 10
    elif rodzaj_zwoju == "pieczęć boga smoków":
        modyfikator = 15

    if isinstance(szanse_bazowe, list):
        szanse_zmodyfikowane = [min(100, szansa + modyfikator) for szansa in szanse_bazowe]
        return [int(szansa) for szansa in szanse_zmodyfikowane]
    elif isinstance(szanse_bazowe, dict):
        szanse_zmodyfikowane = {k: min(100, v + modyfikator) for k, v in szanse_bazowe.items()}
        return {k: int(v) for k, v in szanse_zmodyfikowane.items()}
    else:
        return szanse_bazowe

def symuluj_ulepszanie(start_level, ilosc_prob, rodzaj_przedmiotu, rodzaj_zwoju):
    if rodzaj_przedmiotu == "talizman":
        szanse_bazowe = [55, 50, 45, 40, 35, 30, 25, 20, 15, 10]
    elif rodzaj_przedmiotu == "bron":
        szanse_bazowe = {
            1: 90, 2: 75, 3: 60, 4: 50, 5: 40, 6: 30,
            7: 25, 8: 15, 9: 8, 10: 5, 11: 5, 12: 5,
            13: 5, 14: 3, 15: 3
        }
    else:
        return None, None
    szanse = modyfikuj_szanse(szanse_bazowe, rodzaj_zwoju)
    aktualny_level = start_level
    historia_ulepszen = [start_level]

    for _ in range(ilosc_prob):
        if (rodzaj_przedmiotu == "bron" and aktualny_level >= 14) or \
           (rodzaj_przedmiotu == "talizman" and aktualny_level >= 199):
            historia_ulepszen.append(aktualny_level)
            continue
        indeks_szansy = (aktualny_level - 1) % 10 if rodzaj_przedmiotu == "talizman" else aktualny_level
        if isinstance(szanse, dict):
            szansa = szanse.get(aktualny_level + 1, 0)
        else:
            szansa = szanse[indeks_szansy]
        if szansa == 0:
            historia_ulepszen.append(aktualny_level)
            continue

        losowa_liczba = random.randint(1, 100)
        if losowa_liczba <= szansa:
            aktualny_level += 1
            historia_ulepszen.append(aktualny_level)
        else:
            historia_ulepszen.append(aktualny_level)

    return aktualny_level, historia_ulepszen

@app.route("/", methods=["GET", "POST"])
def index():
    global start_level, ilosc_prob, rodzaj_przedmiotu, rodzaj_zwoju, ilosc_symulacji

    wyniki = None
    error_message = None

    if request.method == "POST":
        try:
            rodzaj_przedmiotu = request.form.get("rodzaj_przedmiotu")
            start_level = int(request.form.get("start_level"))
            ilosc_prob = int(request.form.get("ilosc_prob"))
            rodzaj_zwoju = request.form.get("rodzaj_zwoju")
            ilosc_symulacji = int(request.form.get("ilosc_symulacji"))

            if rodzaj_przedmiotu == "proszę wybrać":
                error_message = "Proszę wybrać rodzaj przedmiotu."
            elif rodzaj_przedmiotu == "bron" and rodzaj_zwoju == "proszę wybrać":
                error_message = "Proszę wybrać rodzaj zwoju dla broni."
            elif not 1 <= ilosc_symulacji <= 1000:
                error_message = "Ilość symulacji musi być w zakresie od 1 do 1000."
            elif start_level < 0:
                error_message = "Startowy poziom nie może być ujemny."
            elif ilosc_prob <= 0:
                error_message = "Ilość prób musi być większa od 0."
            elif rodzaj_przedmiotu == "bron" and start_level >= 15:
                error_message = "Maksymalny poziom ulepszenia wężowego ekwipunku to +15."
            elif rodzaj_przedmiotu == "talizman" and start_level >= 200:
                error_message = "Maksymalny poziom ulepszenia talizmanu to +200."    

            if error_message:
                return render_template("index.html", wyniki=wyniki, start_level=start_level, ilosc_prob=ilosc_prob, rodzaj_przedmiotu=rodzaj_przedmiotu, rodzaj_zwoju=rodzaj_zwoju, ilosc_symulacji=ilosc_symulacji, error_message=error_message), 400

            koncowe_levele = []
            for _ in range(ilosc_symulacji):
                koncowy_level, _ = symuluj_ulepszanie(start_level, ilosc_prob, rodzaj_przedmiotu, rodzaj_zwoju)
                if koncowy_level is None:
                    return "Niepoprawny rodzaj przedmiotu", 400
                koncowe_levele.append(koncowy_level)

            sredni = statistics.mean(koncowe_levele)
            mediana = statistics.median(koncowe_levele)
            try:
                domina = statistics.mode(koncowe_levele)
            except statistics.StatisticsError:
                domina = "Brak jednoznacznej dominanty"

            liczniki_poziomow = {}
            for level in koncowe_levele:
                liczniki_poziomow[level] = liczniki_poziomow.get(level, 0) + 1

            wyniki = {
                "sredni": sredni,
                "mediana": mediana,
                "domina": domina,
                "start": start_level,
                "prob": ilosc_prob,
                "rodzaj_przedmiotu": rodzaj_przedmiotu,
                "rodzaj_zwoju": rodzaj_zwoju,
                "liczniki": liczniki_poziomow,
                "iloscsymulacji": ilosc_symulacji
            }
        except ValueError:
            error_message = "Wprowadź poprawne dane liczbowe."
            return render_template("index.html", wyniki=wyniki, start_level=start_level, ilosc_prob=ilosc_prob, rodzaj_przedmiotu=rodzaj_przedmiotu, rodzaj_zwoju=rodzaj_zwoju, ilosc_symulacji=ilosc_symulacji, error_message=error_message), 400

    return render_template("index.html", wyniki=wyniki, start_level=start_level, ilosc_prob=ilosc_prob, rodzaj_przedmiotu=rodzaj_przedmiotu, rodzaj_zwoju=rodzaj_zwoju, ilosc_symulacji=ilosc_symulacji, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)