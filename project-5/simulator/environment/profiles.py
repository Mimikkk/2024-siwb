from typing import TypedDict, Type

from .profile_0_indifferent import Profile0Indifferent
from .profile_1_stressed import Profile1Stressed
from .profile_2_motivated import Profile2Motivated
from .profile_3_responsive import Profile3Responsive

profiles: TypedDict(
  "Profiles",
  {
    "Indifferent": Type[Profile0Indifferent],
    "Stressed": Type[Profile1Stressed],
    "Motivated": Type[Profile2Motivated],
    "Responsive": Type[Profile3Responsive]
  }
) = {
  "Indifferent": Profile0Indifferent,
  "Stressed": Profile1Stressed,
  "Motivated": Profile2Motivated,
  "Responsive": Profile3Responsive
}
