from datetime import datetime
from collections import OrderedDict

FIXED_VALUE = 0.36
VALUE_PER_MINUTE = 0.09
FULL_VALUE = 960 * 0.09
NIGHT_HOUR = 22
DAY_HOUR = 6
MINUTES_IN_AN_HOUR = 60
DECIMAL_PLACES = 2

records = [
    {
        'source': '48-996355555',
        'destination': '48-666666666',
        'end': 1564610974,
        'start': 1564610674
    },
    {
        'source': '41-885633788',
        'destination': '41-886383097',
        'end': 1564506121,
        'start': 1564504821
    },
    {
        'source': '48-996383697',
        'destination': '41-886383097',
        'end': 1564630198,
        'start': 1564629838
    },
    {
        'source': '48-999999999',
        'destination': '41-885633788',
        'end': 1564697158,
        'start': 1564696258
    },
    {
        'source': '41-833333333',
        'destination': '41-885633788',
        'end': 1564707276,
        'start': 1564704317
    },
    {
        'source': '41-886383097',
        'destination': '48-996384099',
        'end': 1564505621,
        'start': 1564504821
    },
    {
        'source': '48-999999999',
        'destination': '48-996383697',
        'end': 1564505721,
        'start': 1564504821
    },
    {
        'source': '41-885633788',
        'destination': '48-996384099',
        'end': 1564505721,
        'start': 1564504821
    },
    {
        'source': '48-996355555',
        'destination': '48-996383697',
        'end': 1564505821,
        'start': 1564504821
    },
    {
        'source': '48-999999999',
        'destination': '41-886383097',
        'end': 1564610750,
        'start': 1564610150
    },
    {
        'source': '48-996383697',
        'destination': '41-885633788',
        'end': 1564505021,
        'start': 1564504821
    },
    {
        'source': '48-996383697',
        'destination': '41-885633788',
        'end': 1564627800,
        'start': 1564626000
    }
]


def price_calculation(source, price):
    currente_value = e_result.get(source)
    if currente_value is not None:
        price = price + currente_value
    partial_result = {}
    partial_result[source] = price
    e_result.update(partial_result)


def rule_1(source, end, start):
    total_call_in_minutes = (end - start).total_seconds() // 60
    price = (total_call_in_minutes * VALUE_PER_MINUTE) + FIXED_VALUE
    price_calculation(source, price)


def rule_2(source, end, start):
    new_hour = datetime(start.year, start.month, start.day, NIGHT_HOUR, 0, 0)
    total_call_in_minutes = (new_hour - start.hour).total_seconds() // 60
    price = (total_call_in_minutes * VALUE_PER_MINUTE) + FIXED_VALUE
    price_calculation(source, price)


def rule_3(source, end, start):
    new_hour = datetime(start.year, start.month, start.day, DAY_HOUR, 0, 0)
    total_call_in_minutes = (end.hour - new_hour).total_seconds() // 60
    price = (total_call_in_minutes * VALUE_PER_MINUTE) + FIXED_VALUE
    price_calculation(source, price)


def rule_4(source):
    price = FIXED_VALUE
    price_calculation(source, price)


def rule_5(source):
    price = FULL_VALUE + FIXED_VALUE
    price_calculation(source, price)


def charging_rule(source, end, start):
    if start.hour >= DAY_HOUR and start.hour < NIGHT_HOUR:
        if ((DAY_HOUR <= end.hour < NIGHT_HOUR) or
                (end.hour == NIGHT_HOUR and end.minute == 0)):
            rule_1(source, end, start)
        else:
            rule_2(source, end, start)
    else:
        if ((DAY_HOUR <= end.hour < NIGHT_HOUR) or
                (end.hour == NIGHT_HOUR and end.minute == 0)):
            rule_3(source, end, start)
        else:
            if ((start.hour <= end.hour < DAY_HOUR) or
                    (end.hour == DAY_HOUR and end.minute == 0)):
                rule_4(source)
            elif start.hour < DAY_HOUR and end.hour >= NIGHT_HOUR:
                rule_5(source)
            else:
                rule_4(source)


def classify_by_phone_number(records):
    global e_result
    e_result = {}
    for data in records:
        source = data.get('source')
        end = datetime.fromtimestamp(data.get('end'))
        start = datetime.fromtimestamp(data.get('start'))
        charging_rule(source, end, start)
    dict_aux = {}
    record = []
    ordered_result = OrderedDict(sorted(e_result.items(), key=lambda x: x[1]))
    for elemento in ordered_result:
        dict_aux['source'] = elemento
        dict_aux['total'] = round(ordered_result.get(elemento), DECIMAL_PLACES)
        record.append(dict_aux)
        dict_aux = {}
    return list(reversed(record))
