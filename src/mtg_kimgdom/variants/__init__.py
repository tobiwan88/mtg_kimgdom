"""Variant registry for Commander Kingdom.

Adding a new variant
--------------------
1. Create ``src/mtg_kimgdom/variants/my_variant.py`` that defines a ``VARIANT``
   dict with keys:

       id            – unique slug (str), must match the module's ``VARIANT_ID``
       name          – human-readable display name (str)
       description   – one-line description shown in the UI (str)
       characters    – dict[str, dict] following the standard character schema
       distributions – dict[int, dict[str, int]] mapping player count to role counts

2. Import the ``VARIANT`` dict below and insert it into ``VARIANTS`` at the
   desired position.  Insertion order = display order; the first entry is the
   default variant.
"""

from mtg_kimgdom.variants.advanced_kingdoms_156 import VARIANT as _AK156
from mtg_kimgdom.variants.advanced_kingdoms_200 import VARIANT as _AK200

# Insertion order: first entry is the default variant.
VARIANTS: dict[str, dict] = {
    _AK200["id"]: _AK200,
    _AK156["id"]: _AK156,
}

DEFAULT_VARIANT: str = next(iter(VARIANTS))

__all__ = ["DEFAULT_VARIANT", "VARIANTS"]
