from app.utils.generator import UPPERCASE, LOWERCASE, NUMBERS, SYMBOLS


LABEL_COLORS = {
    "Very Weak": "purple",
    "Weak": "red",
    "Decent": "orange",
    "Strong": "#5f13ff",
    "Fantastic": "#6eff00"
}


def evaluate_strength(password: str) -> tuple[int, str]:
    checks = {
        "length": len(password),
        "uppercase_chars": 0,
        "lowercase_chars": 0,
        "numbers": 0,
        "symbols": 0,
    }

    for char in password:
        if char in UPPERCASE:
            checks["uppercase_chars"] += 1
        elif char in LOWERCASE:
            checks["lowercase_chars"] += 1
        elif char in NUMBERS:
            checks["numbers"] += 1
        elif char in SYMBOLS:
            checks["symbols"] += 1

    has_length = checks["length"] >= 12
    has_upper_and_lower = checks["uppercase_chars"] > 0 and checks["lowercase_chars"] > 0
    has_numbers = checks["numbers"] > 0
    has_symbols = checks["symbols"] > 0

    strength = sum([has_length, has_upper_and_lower, has_numbers, has_symbols])

    strength_labels = {
        0: "Very Weak",
        1: "Weak",
        2: "Decent",
        3: "Strong",
        4: "Fantastic",
    }

    return strength, strength_labels[strength]
