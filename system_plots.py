# Vishal Chotara, 20307118
"""
This program will run a simulation for 90 days using the SimulateData class and then plot a bar chart showing the
number of covid patients at each hospital in the recorded states and a scatter plot showing the severity status of all
patients at the hospitals over the recorded states.
"""
import csv
import matplotlib.pyplot as plt
import numpy as np
from simulate_data import SimulateData


class SystemPlots:
    def __init__(self):
        self.simulation = SimulateData()
        self.hospitals = None

    @staticmethod
    def read_in_csv():
        """
        read_in_csv reads in all the day states created from the simulation of the patient management system
        :return: dict
        """
        files = []
        for file in range(1, 10):
            file_name = 'hospital_state_0' + str(file) + '.csv'
            files.append(file_name)

        # keep track of patients per hospital for each state file
        hospitals = {"kingston": [], "hamilton": [], "toronto": []}
        for file in files:
            # hold the patients for 1 day state
            kingston_patients = []
            hamilton_patients = []
            toronto_patients = []
            try:
                with open(file, 'r') as csv_file:
                    patient_reader = csv.reader(csv_file, delimiter=',')
                    next(patient_reader)  # skip header
                    for row in patient_reader:
                        # append patients for the day state to the correct hospital
                        if row[2] == "kingston":
                            kingston_patients.append([row[1], row[3], row[4]])
                        elif row[2] == "hamilton":
                            hamilton_patients.append([row[1], row[3], row[4]])
                        else:
                            toronto_patients.append([row[1], row[3], row[4]])

                # add patients to the dict
                hospitals["kingston"].append(kingston_patients)
                hospitals["hamilton"].append(hamilton_patients)
                hospitals["toronto"].append(toronto_patients)
            except:
                print("There was a problem opening {} for reading, therefore it has not been loaded"
                      " into the program.".format(file))

        return hospitals

    def get_hospital_covid_nums(self, hospital):
        """
        get_hospital_covid_nums will find the number of covid positive patients in hospital per day state and return a
            list of these numbers
        :param hospital: str
        :return: List of int
        """
        covid_nums = []
        for day in self.hospitals[hospital]:
            count_covid = 0
            for patient in day:
                if patient[2] == 'true':
                    count_covid += 1
            covid_nums.append(count_covid)
        return covid_nums

    def get_severity_states(self, hospital):
        """
        get_severity_states will return x (sev_days) and y (sev_states) values for a scatter plot where the x values
            represent the state days and the y values represent the severity statuses for the hospital.
        :param hospital: str
        :return: list of [list of int, list of int]
        """
        sev_days = []
        sev_states = []
        for day in range(len(self.hospitals[hospital])):
            status = []
            for patient in self.hospitals[hospital][day]:
                sev_states.append(int(patient[1]))
                sev_days.append(day + 1)
        return [sev_days, sev_states]

    def plot_hospital_covid_patients(self):
        """
        plot_hospital_covid_patients will plot a bar chart that shows the number of patients with covid in each of the
            3 hospitals in each of the states generated from SimulateData() class
        :return: None
        """
        # get number of patients with covid at each hospital
        kingston_covid_numbers = self.get_hospital_covid_nums('kingston')
        hamilton_covid_numbers = self.get_hospital_covid_nums('hamilton')
        toronto_covid_numbers = self.get_hospital_covid_nums('toronto')

        # plot bar graph
        x = np.arange(1, 10)  # states
        width = 0.2  # width of bars
        plt.figure(figsize=(12, 4))
        # making each bar so they fit side by side
        plt.bar(x - width, kingston_covid_numbers, width, label='Kingston')
        plt.bar(x, hamilton_covid_numbers, width, label='Hamilton')
        plt.bar(x + width, toronto_covid_numbers, width, label='Toronto')

        plt.legend()
        plt.xticks(x, x)
        plt.xlabel("States")
        plt.ylabel("Number of Patients")
        plt.locator_params(axis="y", integer=True)
        plt.title("Bar chart showing the number of patients with COVID at \n3 hospitals over 9 day states")
        plt.show()

    def severity_scatter_plot(self):
        """
        severity_scatter_plot will plot a scatter plot for the severity status of all patients in each of the saved
            states differentiated by hospital
        :return: None
        """
        # get all the severity statuses for each hospital
        kingston_statuses = self.get_severity_states('kingston')
        hamilton_statuses = self.get_severity_states('hamilton')
        toronto_statuses = self.get_severity_states('toronto')

        # plot the scatter plot
        plt.figure(figsize=(12, 4))
        plt.scatter(kingston_statuses[0], kingston_statuses[1], label="Kingston")
        plt.scatter(hamilton_statuses[0], hamilton_statuses[1], label="Hamilton")
        plt.scatter(toronto_statuses[0], toronto_statuses[1], label="Toronto")
        x = np.arange(1, 10)  # states
        plt.xticks(x)
        plt.yticks([1, 2, 3])
        plt.legend()
        plt.xlabel("States")
        plt.ylabel("Severity Status")
        plt.title("Scatter plot showing the severity of all patients in \neach of the hospitals over the 9 day states")
        plt.show()

    def run_plots(self):
        """
        run_plots will start the simulation of the hospital and generate plots for the 9 collected states
        :return: None
        """
        # start simulation to generate the state files
        self.simulation.start_simulation()

        # read in the state files
        self.hospitals = self.read_in_csv()

        # make the plots
        self.plot_hospital_covid_patients()
        self.severity_scatter_plot()


def main():
    """
    This program will first run a simulation of 90 days and generate the hospital state files which are then used
        to plot the charts. Although Line 20 in this file can be changed to use any other hospital state files
        previously generated!
    :return: None
    """
    plots = SystemPlots()
    plots.run_plots()


main()
