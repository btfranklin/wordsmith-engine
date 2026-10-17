"""Build names from specialized reusable components."""

import random

from wordsmith import (
    BusinessAnimal, BusinessColor, BusinessTrade, CompoundCreatureName,
    CompoundLandmarkName, HeraldicSymbol, NaturalNameRoot,
)

rng = random.Random(5343)
for component in (
    (BusinessColor() | BusinessAnimal() | BusinessTrade()).title_case(),
    CompoundCreatureName(),
    CompoundLandmarkName(),
    HeraldicSymbol(),
    NaturalNameRoot(context="landmark"),
    NaturalNameRoot(context="creature"),
):
    print(component(rng))
