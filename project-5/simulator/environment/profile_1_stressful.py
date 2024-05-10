from .fogg_behavioural_model import Patient

class Profile1Stressful(Patient):
  """
  Description:
    These patients do not respond well to interventions during stressful times,
    suggesting that their interactions should be timed during moments of calm.
  """
  def __init__(self):
    super().__init__()
