def get_spn(toponym):
    lower_c, upper_c = toponym['boundedBy']['Envelope']['lowerCorner'].split(), \
                       toponym['boundedBy']['Envelope']['upperCorner'].split()
    delta_1 = str(float(upper_c[0]) - float(lower_c[0]))
    delta_2 = str(float(upper_c[1]) - float(lower_c[1]))
    return [delta_1, delta_2]
