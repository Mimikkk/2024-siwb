from .fogg_behavioural_model import Patient

class Profile0Indifferent(Patient):
  """
  Description:
    Patients of this cluster have low motivation from both self-improvement and social competition aspects,
    indicating a preference for self-directed activities without external pressures.
    On the other hand they are equally responsive while tired or under stress.

    narcisstic = no {0, 1}
    self_motivated = no (0, 1) depending on previous responses to interventions, 
    competition_driven = no {0, 1}
    responsive = 2 {0, 1, 2}

    I would change this profile name to "wywalone" ;)
  """
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.responsiveness = 0


  def fogg_behaviour(self, motivation: int, ability: int, trigger: bool) -> bool:
      """"
      Function that decides if the behaviour will be performed or not based on Fogg's Behavioural Model
      """
      behaviour = (motivation * ability * trigger) + self.responsiveness
      return behaviour > self.behaviour_threshold
    