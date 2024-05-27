import random
from .fogg_behavioural_model import Patient

class Profile1Stressed(Patient):
  """
  Description:
    These patients do not respond well to interventions during stressful times,
    suggesting that their interactions should be timed during moments of calm.
  """
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.stress = 0  # {0, 1, 2} Stress = high arousal and negative valence. Calculated as  arousal - valence. 
    self.tiredness = 0  # (0, 2) insufficient_sleep + up_hours/12  <- number of hours since waking up
    self.responsiveness = 0


  def fogg_behaviour(self, motivation: int, ability: int, trigger: bool) -> bool:
      behaviour = (motivation * ability * trigger) + self.responsiveness
      return behaviour > self.behaviour_threshold
  
  def update_state(self):
    self._update_time()
    self._update_awake()
    if self.awake_list[-1] == 'awake':
        self._update_motion_activity()
        self._update_location()
        self._update_emotional_state()
        self.responsiveness = - max(self.stress, self.tiredness) 
    else:
        self.location = 'home'
        self.motion_activity_list.append('stationary')
        self.arousal = 0
        self.cognitive_load = 0
        self.valence_list.append(self.valence)
        self.arousal_list.append(self.arousal)
    
  def _update_patient_stress_level(self):
        insufficient_exercise = 1 if self.motion_activity_list[-24:].count('walking') < 1 else 0
        annoyed = 1 if self.activity_s > self.max_notification_tolerated else 0
        number_of_hours_slept = self.awake_list[-24:].count('sleeping')
        insufficient_sleep = 1 if number_of_hours_slept < 7 else 0
        neg_factors = insufficient_exercise + annoyed + insufficient_sleep

        if self.motion_activity_list[-1] == 'walking':
            self.valence,  self.arousal = 1, 1
        else:
            if neg_factors >= 2:
                self.valence = 0
                self.arousal = 2
            elif neg_factors == 1:
                self.valence = random.choices([0, 1], weights=(0.5, 0.5), k=1)[0]
                self.arousal = random.choices([0, 1, 2], weights=(0.3,0.3, 0.4), k=1)[0]  
            else:
                self.valence = 1
                self.arousal = random.choices([0, 1, 2], weights=(0.3, 0.4, 0.3), k=1)[0]
        self.stress = self.arousal - self.valence
        up_hours = self.awake_list[-12:].count('awake')
        self.tiredness = insufficient_sleep + up_hours/12
        self.valence_list.append(self.valence)
        self.arousal_list.append(self.arousal)