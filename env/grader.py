def grade(pred, gt):
    total_score = 0

    for p, g in zip(pred, gt):
        score = 0

        # name
        if str(p.get("name", "")).strip().lower() == g["name"].lower():
            score += 0.3

        # age
        try:
            if int(p.get("age")) == int(g["age"]):
                score += 0.3
        except:
            pass

        # email
        if p.get("email") == g["email"]:
            score += 0.4

        total_score += score

    return total_score / len(gt)