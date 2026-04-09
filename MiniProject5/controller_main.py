def decision_controller(freqs):
    """
    freqs = [f1, f2, f3]
    """

    avg_freq = sum(freqs) / len(freqs)

    # Always-on "breathing" action
    breathing_intensity = 0.2 + (avg_freq / 50)

    # Movement logic
    if avg_freq > 18:
        action = "FAST_MOVE"
    elif avg_freq > 12:
        action = "MOVE"
    else:
        action = "IDLE"

    # Optional: conflict detection
    active_brain_areas = sum(f > 15 for f in freqs)

    if active_brain_areas >= 2:
        action = "COORDINATED_MOVE"

    return {
        "action": action,
        "breathing": breathing_intensity,
        "raw": freqs
    }