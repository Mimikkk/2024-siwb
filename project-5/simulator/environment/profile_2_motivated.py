import random

import numpy as np
from .fogg_behavioural_model import Patient

class Profile2Motivated(Patient):
  """
  Description:
    Motivated by visible progress and achievements, this group benefits from features that track and
    display their health progress, enhancing their engagement through tangible results.
  """
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.prompt_answers = []
    self.peer_comparison = np.random.randint(0, 2)  # 0 negative, 1 positive Q1
    self.motivation = 0 # grows with each performed activity up to 1 Q2
    self.peer_competition = np.random.randint(0, 2)  # 0 negative, 1 positive Q3 at_home->0
    self.stress = 0  # {0, 1, 2} Stress = high arousal and negative valence. Calculated as  arousal - valence. 
    self.tiredness = 0  # (0, 2) insufficient_sleep + up_hours/12  <- number of hours since waking up
    self.responsiveness = 0 # Q4 Q5
    
  def fogg_behaviour(self, motivation: int, ability: int, trigger: bool) -> bool:
      profile_characteristics = self.responsiveness + self.peer_comparison + self.peer_competition + self.motivation
      behaviour = (motivation * ability * trigger) + profile_characteristics
      behaviour = behaviour > self.behaviour_threshold
      self.prompt_answers.append(behaviour)
      return behaviour
  
  def update_state(self):
    self._update_time()
    self._update_awake()
    self.peer_comparison = np.random.randint(0, 2)  # 0 negative, 1 positive Q1
    self.motivation = self.prompt_answers[-10:].count(1) / 10
    if self.awake_list[-1] == 'awake':
        self._update_motion_activity()
        self._update_location()
        self._update_emotional_state() # valence, arousal, stress
        self.peer_competition = np.random.randint(0, 2)
        self.responsiveness = 2 - max(self.stress, self.tiredness)
    else:
        self.location = 'home'
        self.peer_competition = 0
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

    