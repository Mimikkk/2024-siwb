from typing import TypedDict

from .profile_0_motivationless import Profile0Motivationless
from .profile_1_stressful import Profile1Stressful
from .profile_2_motivated import Profile2Motivated
from .profile_3_responsive import Profile3Responsive

profiles: TypedDict(
  "Profiles",
  {
    "Motivationless": type[Profile0Motivationless],
    "Stressful": type[Profile1Stressful],
    "Motivated": type[Profile2Motivated],
    "Responsive": type[Profile3Responsive]
  }
) = {
  "Motivationless": Profile0Motivationless,
  "Stressful": Profile1Stressful,
  "Motivated": Profile2Motivated,
  "Responsive": Profile3Responsive
}
