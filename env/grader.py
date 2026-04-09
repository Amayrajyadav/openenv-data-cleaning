class Grader:
    def grade(self, output, expected):
        if not output or not expected:
            return 0.0

        score = 0.0
        total = 0

        for o, e in zip(output, expected):
            row_score = 0.0

            # Name check
            if o.get("name") == e.get("name"):
                row_score += 0.33

            # Age check
            try:
                if int(o.get("age")) == int(e.get("age")):
                    row_score += 0.33
            except:
                pass

            # Email check
            if o.get("email") == e.get("email"):
                row_score += 0.34

            score += row_score
            total += 1

        final_score = round(score / total, 2)

        # clamp to (0,1)
        if final_score <= 0:
            final_score = 0.01
        elif final_score >= 1:
            final_score = 0.99
        
        return final_score
