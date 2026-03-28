def avstand_score(avstand, min, maks, k=0.0005):
    score = min+((maks-min)/(1+avstand*k))
    return score