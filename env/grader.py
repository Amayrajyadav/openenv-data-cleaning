class Grader:
    def grade(self, output, expected):
        if not isinstance(output, list) or not isinstance(expected, list):
            return 0.15
        if len(output) == 0 or len(expected) == 0:
            return 0.15

        score = 0.0
        total = 0

        for o, e in zip(output, expected):
            row_score = 0.0

            o_name = str(o.get("name", "")).strip().title()
            e_name = str(e.get("name", "")).strip().title()
            if o_name == e_name:
                row_score += 0.33

            try:
                o_age = int(str(o.get("age", "")).strip())
                e_age = int(e.get("age"))
                if o_age == e_age:
                    row_score += 0.33
            except (ValueError, TypeError):
                pass

            o_email = str(o.get("email", "")).strip().lower()
            e_email = str(e.get("email", "")).strip().lower()
            if o_email == e_email:
                row_score += 0.34

            score += row_score
            total += 1

        if total == 0:
            return 0.15

        raw_score = score / total
        final_score = 0.1 + (0.8 * raw_score)
        final_score = max(0.11, min(0.89, round(final_score, 4)))
        return final_score
