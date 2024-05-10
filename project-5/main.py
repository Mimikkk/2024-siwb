# 2.1 Getting familiar with the experimental environment
# Familiarize yourself with the computing environment provided for this project2. When installing
# the necessary packages, use the pip tool (you can also use Docker):
# pip install -r requirements.txt
# pip install jupyter

# After preparing the environment, run some example experiments defined in the experiments
# notebook (this notebook implements the calculations the results of which are presented in the
# paper [1]). Due to the long computation time, it is recommended to limit the number of
# repetitions (runs) to 100 (however, this may reduce the stability of the obtained models
# compared to those from the publication) and to omit the experiment with static random tree
# learning, defined in the supervised_after_three_weeks function. An experiment using the
# adaptive (incremental) learning implemented in supervised_adaptive_after_three_weeks
# takes a little longer but allows for more interesting results.)

# Part 1
# Prepare a new class based on fogg_behavioural_model.Patient, which will represent one of
# the patient (user) profiles presented in the paper [3] and identified on the basis of the analysis
# of the survey results. Suggest and briefly explain how the characteristics of the profile can be
# “implemented” (considered) in the simulation environment. Pay attention to the limitations of
# the current version of the environment (the ability to simulate only a single patient at a time),
# which may require some simplifications, e.g. when comparing a given patient with a group
# (peers) – the behavior of the group must be simulated.

# 1. Create a new class that represents a patient profile.
# 2. Implement the characteristics of the profile in the simulation environment.

# Part 2
# Perform a computational experiment verifying the behavior of the simulated patient (modeled
# in Part 1 of the task) and evaluating the quality of the selected stimulus generation models.
# Perform a computational experiment and visualize the results using a sample notebook using
# the following suggestions:
# 1. Perform the calculation for 500 repetitions (runs = 500).
# 2. Assume the patient's characteristics and initial state as described in the paper [1] (m.in.,
# acceptance of up to 3 reminders per day).
# 3. Assume that the patient's preference and activity threshold do not change during the
# simulation.
# 4. Perform experiments for the following stimulus generation techniques:
# a. random (random_notification),
# b. Incremental machine learning (supervised_adaptive_after_three_weeks)
# c. reinforcement learning (DQN, PPO, A2C).
# 5. As part of the visualization of the results, present graphs illustrating the percentage of
# stimuli resulting in an action and the average number of reminders.
# After completing the simulation experiments, prepare a notebook describing how the patient
# profile was modeled and the results obtained during the simulation. It is recommended to
# perform the project in groups of 4 people, in which each person is involved in modeling one
# profile and conducting simulations for this profile. It is worth considering modifications
# common to the group (e.g. additional variables) that will allow for differentiation of patient
# profiles

# 1. Perform a computational experiment.
# 2. Assume the patient's characteristics and initial state.
# 3. Assume that the patient's preference and activity threshold do not change.
# 4. Perform experiments for the following stimulus generation techniques:
#   a. random (random_notification),
#   b. Incremental machine learning (supervised_adaptive_after_three_weeks),
#   c. reinforcement learning (DQN, PPO, A2C).
# 5. Visualize the results using graphs.
# 6. Prepare a notebook describing the patient profile and the simulation results.


def main():
  return 0

if __name__ == "__main__":
  main()
