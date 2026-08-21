from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class PhoneticConstraints:
    """Constraints for phonetic validation."""

    max_syllables: Optional[int] = None
    max_length: Optional[int] = None
    avoid_sounds: Optional[List[str]] = None


@dataclass
class PhoneticAssessment:
    """Result of phonetic validation."""

    is_valid: bool
    notes: Optional[str] = None


def estimate_syllables(name: str) -> int:
    """Estimate syllable count by counting vowel groups.
    Vowels: a, e, i, o, u, y (case-insensitive).
    Consecutive vowels count as one group.
    """
    name = name.lower()
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for ch in name:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
            prev_vowel = True
        elif not is_vowel:
            prev_vowel = False
    return max(1, count)  # At least one syllable if name is not empty


def check_phonetic_constraints(
    name: str, constraints: PhoneticConstraints
) -> PhoneticAssessment:
    """Validate name against phonetic constraints."""
    notes = []

    # Check max_length
    if constraints.max_length is not None and len(name) > constraints.max_length:
        notes.append(
            f"Name length {len(name)} exceeds maximum {constraints.max_length}"
        )

    # Check max_syllables
    if constraints.max_syllables is not None:
        syllables = estimate_syllables(name)
        if syllables > constraints.max_syllables:
            notes.append(
                f"Estimated syllable count {syllables} exceeds maximum "
                f"{constraints.max_syllables}"
            )

    # Check avoid_sounds
    if constraints.avoid_sounds:
        name_lower = name.lower()
        for sound in constraints.avoid_sounds:
            if sound.lower() in name_lower:
                notes.append(f"Name contains avoided sound '{sound}'")
                break  # One note is enough for this constraint

    is_valid = len(notes) == 0
    notes_str = "; ".join(notes) if notes else None

    return PhoneticAssessment(is_valid=is_valid, notes=notes_str)
