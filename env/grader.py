class Grader:
    def grade(self, output, expected):
        if not output or not expected:
            return 0.05  # never 0

        score = 0.0
        total = 0

        for o, e in zip(output, expected):
            row_score = 0.0

            if o.get("name") == e.get("name"):
                row_score += 0.33

            try:
                if int(o.get("age")) == int(e.get("age")):
                    row_score += 0.33
            except:
                pass

            if o.get("email") == e.get("email"):
                row_score += 0.34

            score += row_score
            total += 1

        if total == 0:
            return 0.05

        raw_score = score / total

        # 🔥 SMOOTHING (CRITICAL FIX)
        final_score = 0.05 + (0.9 * raw_score)

        return round(final_score, 2)
