def randomSeed(seed, maxVal):
    '''
    Returns a seeded random number (always the same out put for one input) from 0 to the max value
    '''
    a = 893415793148314538745901465145831897
    c = 143678578634156403985604793467093041
    
    seededNumber = (a * seed + c) % maxVal
    
    return seededNumber
