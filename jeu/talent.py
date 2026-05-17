#!/usr/bin/env python3


class Talent:
    """Interface for talents that can be acquired by a Personnage.

    A talent is attached via Personnage.gainTalent(), which appends it
    to personnage.talents and calls applyTo(personnage). The talent can
    then register rules, race observers, obstacle factories, etc. on
    the personnage to alter its behaviour.

    Talents are displayed by TalentsDisplay using displayRule() (static
    description) and stats() (dynamic strings: counters, progress, etc.).
    """
    def applyTo(self, personnage):
        """Hook the talent's behaviour into the given personnage."""
        pass

    def displayRule(self):
        """Return a human-readable description of the talent."""
        return ""

    def stats(self):
        """Return dynamic strings to display alongside the description.

        Override to expose runtime state (e.g. counters of triggers,
        remaining uses, progression toward a quest, etc.).
        """
        return []
