# analyzer.py
import re
import math
import string
import itertools
import time
from zxcvbn import zxcvbn

# ── Common password list (top 20 for demo) ──────────────────────────────────
COMMON_PASSWORDS = {
    "password", "123456", "password1", "qwerty", "abc123",
    "letmein", "monkey", "1234567890", "iloveyou", "admin",
    "welcome", "login", "passw0rd", "master", "hello",
    "shadow", "sunshine", "princess", "dragon", "football"
}

# ── Character set sizes ──────────────────────────────────────────────────────
CHARSET_SIZES = {
    "lowercase":   26,
    "uppercase":   26,
    "digits":      10,
    "symbols":     32,
}

def calculate_entropy(password: str) -> float:
    """Shannon entropy: H = L * log2(N) where L=length, N=charset size."""
    pool = 0
    if re.search(r'[a-z]', password): pool += CHARSET_SIZES["lowercase"]
    if re.search(r'[A-Z]', password): pool += CHARSET_SIZES["uppercase"]
    if re.search(r'[0-9]', password): pool += CHARSET_SIZES["digits"]
    if re.search(r'[^a-zA-Z0-9]', password): pool += CHARSET_SIZES["symbols"]
    if pool == 0:
        return 0.0
    return round(len(password) * math.log2(pool), 2)

def crack_time_estimate(entropy: float) -> dict:
    """
    Estimates crack time at different attack speeds.
    Returns human-readable strings.
    """
    # Attempts per second for different scenarios
    SCENARIOS = {
        "Online (throttled)":    100,           # 100/s  — login with rate limiting
        "Online (unthrottled)":  10_000,        # 10K/s  — no rate limit
        "Offline (slow hash)":   10_000_000,    # 10M/s  — bcrypt
        "Offline (fast hash)":   100_000_000_000,  # 100B/s — MD5/GPU rig
    }

    def seconds_to_human(seconds: float) -> str:
        if seconds < 1:
            return "Instant"
        intervals = [
            (60, "second"),
            (60, "minute"),
            (24, "hour"),
            (365, "day"),
            (float('inf'), "year"),
        ]
        value = seconds
        unit = "second"
        for factor, name in intervals:
            if value < factor:
                unit = name
                break
            value /= factor

        value = round(value)
        if value > 1_000_000:
            return f"{value:.2e} {unit}s"
        return f"{value:,} {unit}{'s' if value != 1 else ''}"

    results = {}
    total_combinations = 2 ** entropy
    for scenario, speed in SCENARIOS.items():
        # Average case = half of total combinations
        avg_seconds = (total_combinations / 2) / speed
        results[scenario] = seconds_to_human(avg_seconds)
    return results

def check_patterns(password: str) -> list:
    """Detect common weak patterns."""
    warnings = []

    if password.lower() in COMMON_PASSWORDS:
        warnings.append("⚠️ This is one of the most commonly used passwords")
    if re.search(r'(.)\1{2,}', password):
        warnings.append("⚠️ Contains repeated characters (e.g. 'aaa')")
    if re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def|qwe|wer|ert|rty|tyu|yui|uio|iop)', password.lower()):
        warnings.append("⚠️ Contains sequential pattern (e.g. '123', 'abc')")
    if re.search(r'^[A-Z][a-z]+\d{1,4}$', password):
        warnings.append("⚠️ Follows predictable format: Capital + word + numbers")
    if re.search(r'(password|pass|pwd|admin|user|login)', password.lower()):
        warnings.append("⚠️ Contains dictionary word related to authentication")
    if len(password) < 8:
        warnings.append("⚠️ Password is too short (minimum 8 characters recommended)")
    if not re.search(r'[^a-zA-Z0-9]', password):
        warnings.append("💡 Add special characters to significantly increase strength")

    return warnings

def brute_force_simulation(password: str, max_length: int = 4) -> dict:
    """
    Simulates a brute-force attack on SHORT passwords only (≤4 chars).
    For longer passwords, returns a projection instead.
    Educational demo only.
    """
    if len(password) > max_length:
        # Estimate only — do NOT actually attempt
        charset = ""
        if re.search(r'[a-z]', password): charset += string.ascii_lowercase
        if re.search(r'[A-Z]', password): charset += string.ascii_uppercase
        if re.search(r'[0-9]', password): charset += string.digits
        if re.search(r'[^a-zA-Z0-9]', password): charset += string.punctuation

        total = sum(len(charset) ** i for i in range(1, len(password) + 1))
        return {
            "simulated": False,
            "message": f"Password too long to simulate safely. Estimated {total:,} combinations to try.",
            "attempts": None,
            "time_ms": None,
        }

    # Only simulate for short passwords (demo purposes)
    charset = string.ascii_lowercase + string.digits
    attempts = 0
    import time

    start = time.time()
    found = False
    for length in range(1, len(password) + 1):
        for combo in itertools.product(charset, repeat=length):
            attempts += 1
            if "".join(combo) == password.lower():
                found = True
                break
        if found:
            break

    elapsed_ms = round((time.time() - start) * 1000, 2)

    return {
        "simulated": True,
        "found": found,
        "attempts": attempts,
        "time_ms": elapsed_ms,
        "message": f"Found after {attempts:,} attempts in {elapsed_ms}ms" if found else "Not found in charset"
    }

def analyze_password(password: str) -> dict:
    """Master function — returns full analysis."""
    if not password:
        return {"error": "No password provided"}

    # zxcvbn deep analysis
    zx = zxcvbn(password)

    entropy = calculate_entropy(password)
    crack_times = crack_time_estimate(entropy)
    patterns = check_patterns(password)
    brute = brute_force_simulation(password)

    # Strength label
    score = zx['score']  # 0-4
    labels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
    colors = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#10b981"]

    # Improvement suggestions
    suggestions = zx['feedback']['suggestions']
    if zx['feedback']['warning']:
        suggestions.insert(0, zx['feedback']['warning'])

    return {
        "password_length": len(password),
        "entropy_bits": entropy,
        "score": score,
        "strength_label": labels[score],
        "strength_color": colors[score],
        "crack_times": crack_times,
        "pattern_warnings": patterns,
        "suggestions": suggestions,
        "brute_force": brute,
        "character_analysis": {
            "has_lowercase": bool(re.search(r'[a-z]', password)),
            "has_uppercase": bool(re.search(r'[A-Z]', password)),
            "has_digits": bool(re.search(r'[0-9]', password)),
            "has_symbols": bool(re.search(r'[^a-zA-Z0-9]', password)),
            "unique_chars": len(set(password)),
        }
    }