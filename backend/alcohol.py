from datetime import datetime
import csv

alcohol_amount = 0.0
profile = {}
profile["age"] = "18"
profile["sex"] = "male"
profile["weight"] = "65.0"
alcoholic_drinks = []
waterPercent = {'male': 0.7, 'female': 0.6 }

def water():
    return float(profile["weight"]) * float(waterPercent[profile["sex"]])


def set_profile(request):
    profile["age"] = request["age"]
    profile["sex"] = request["sex"]
    profile["weight"] = request["weight"]


def calculate_bac(alc_drink=0.05, vol_drink=500):
    alc = alc_drink * 0.78924 * vol_drink / 100
    alc_blood = (alc / water()) * 100
    return alc_blood


def reduced_bac(bac, seconds):
    return max(0, bac - 0.15 * (seconds / 3600.0))


def alcohol_for_drink(drink):
    drink_alc_vol = {}
    with open('backend/alcohol_contents.csv', newline='\n') as csvfile:
        for row in csv.reader(csvfile, delimiter=',', quotechar='"'):
            drink_alc_vol[row[0].lower()] = (float(row[1]), float(row[2]))
    (amount, serving) = drink_alc_vol.get(drink)
    if amount is not None:
        return (float(amount), serving)
    else:
        contains_matches = [value for key, value in drink_alc_vol.items() if drink in key]
        if len(contains_matches) > 0:
            return (max(contains_matches), serving)
        else:
            return (0.0, serving)


def alcohol_contents(drink, serving, current_time):
    global alcohol_amount
    (alc_vol, default_serving) = alcohol_for_drink(drink.lower())
    if serving == 500:
        used_serving = default_serving
    else:
        used_serving = serving
    amount = calculate_bac(alc_vol, used_serving)
    if amount == 0.0:
        return 0.0
    if len(alcoholic_drinks) > 0:
        last_element = alcoholic_drinks[-1]
        diff = (current_time - last_element["timestamp"]).total_seconds()
        alcohol_amount = reduced_bac(alcohol_amount, diff)
    alcohol_amount += amount
    history_object = {}
    history_object["drink"] = drink.lower()
    history_object["serving"] = used_serving
    history_object["alcohol_volume"] = alc_vol
    history_object["alcohol"] = amount
    history_object["total_alcohol"] = alcohol_amount
    history_object["timestamp"] = current_time
    alcoholic_drinks.append(history_object)
    return amount
