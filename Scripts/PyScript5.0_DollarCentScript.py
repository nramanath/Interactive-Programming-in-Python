# Script to convert value to dollars and cents in text

def convert_units(val, name):
    converted_string = str(val) + " " + name
    if val > 1:
        converted_string = converted_string + 's'
    return converted_string


def convert(val):
    dollar = int(val)
    cent = round(100 * (val - dollar))

    dollar_string = convert_units(dollar, "dollar")
    cent_string = convert_units(cent, "cent")

    if(dollar == 0):
        return cent_string
    elif(cent == 0):
        return dollar_string
    elif(dollar == 0 and cent ==0):
        return "broke"
    else:
        return dollar_string+" and "+cent_string

print convert(11.23)
print convert(0)
print convert(1)
print convert(0.01)