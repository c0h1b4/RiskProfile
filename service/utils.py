def process(value):
    """
    This algorithm results in a final score for each line of insurance, 
    which should be processed using the following ranges:
    -99 maps to "ineligible"
    0 and below maps to "economic"
    1 and 2 maps to "regular"
    3 and above maps to "responsible"
    Args:
        value (int): the value to be processed
    Returns:
        the processed value (string)
    """
    if value == -99:
        return "ineligible"
    elif value <= 0:
        return "economic"
    elif value <= 2:
        return "regular"
    elif value > 2:
        return "responsible"
    else:
        return "error"
