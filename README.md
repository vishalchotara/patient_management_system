# **Patient Management System**

*patient_management_system.py*

**requires**: hospitals.py, patients.py

Description: A simple patient management system for a 3-hospital system (Kingston, Hamilton, Toronto)

Hospital Name: Total # of ICU Beds

- Kingston: 10
- Hamilton: 13
- Toronto: 20

### Description of System:
In this system, as patients are admitted to the ICU they are assigned a unique ID, a “Severity status” from 0 to 3, and it is noted whether or not they are positive for Covid-19.
A list of all patients currently in the hospital system can be found in **initial_hospital_state.csv**.

Allows the user to select one of four actions: *Add, Transfer, Update, and Discharge*. *Add* allows the user to admit a new patient to the hospital system. *Transfer* allows the user to move a patient from one hospital to another that has open beds. *Update* will allow the user to modify the severity status of a patient. Finally, *Discharge* will remove the patient from the hospital system. After any action, the system should save the new state of the hospital system to a csv file called **final_hospital_state.csv**.

Your system should enforce the following restrictions:
- Patients with a severity status of 3 are not stable enough to be transferred. The system
should suggest the first patient in the current hospital with the lowest severity status. If
there are no patients with a status <3, the system should inform the user that no transfers
are possible.
- Patients may only be discharged if they have a severity status of 0



## Simulate the system

*simulate_data.py*
requires: patient_management_system.py

Description: Simulates the use of the patient management system for 90 days. 

All hospitals begin with an empty ICU (initial_hospital_state.csv should be empty)
- Each hospital only admits one patient to the ICU every 7 days, except Toronto which
admits 1 every 4 days
- Patients are automatically discharged when their severity status reaches 0
- It takes 5 days for a patient’s severity status to drop from 3 to 2, 3 days for it to drop from
2 to 1, and only 1 day for it to drop to 0. (we’re assuming no one dies in this fictional
scenario).
o We also assume that everyone recovers and no one gets worse
- If a patient must be transferred, they are transferred to the hospital with the most available
ICU beds.
© 2021, Rebecca Hisey
- The probability that a patient comes in with Covid starts at 10% and increases
exponentially by 5% every day
o E.g. the second day should be 10.5%, tenth day should be 16.3%, etc
- We can also assume that no one contracts Covid while in hospital
- If a patient does not have covid, the probability that they have a severity status upon
admission is 3 is 1%, there’s a 3% probability that their severity status is 2, and a 6% chance
that their severity status is 1. No one is admitted with a severity status < 1.
- If a patient does have covid the probability of each severity status at time of admission is
as follows:
o 3% severity status of 3
o 3% severity status of 2
o 4% severity status of 1

For every 10 simulated days, saves the state of the hospital to a separate csv file called hospital_state_<Day #>.csv (e.g. 1st day would
be hospital_state_01.csv).

## System Plots
Description: Produces 2 different plots using the state files produced from *simulate_system.py*

Requires: patient_management_system.py, simulate_system.py

Plots the following:
1. Hospital Occupancy by Covid patients:
  - a single bar chart that shows the number of patients with Covid in each of
the 3 hospitals in each of the states generated in part 2.
2. Severity of cases
  - a scatter plot that maps the severity status of all patients in each of the saved
states. Your figure should contain 9 time points on the x axis, and severity status of
each patient on the y-axis. Each hospital should be plotted in a different colour.
