# Vishal Chotara, 20307118
"""
This program will simulate 90 days of the use of a Patient Management System and record the state of the system everyday
in a csv file.
"""
import random
from patient_management_system import PatientManagementSystem
import csv
import pandas as pd


class SimulateData:
    def __init__(self):
        self.__system = PatientManagementSystem()
        self.__covid_chance = 0.1
        self.__track_patients = {}
        self.__save_file_days = 1

    def write_to_csv(self):
        """
        write_to_csv writes information of the patients from the PatientManagementSystem class to csv format
        :return: None
        """
        file_name = 'hospital_state_0' + str(self.__save_file_days) + '.csv'  # file_name based on the simulation

        with open(file_name, 'w') as csv_file:
            patient_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
            # all existing ids
            all_patients = self.__system.get_values_or_keys("values")

            fieldnames = ["", "Patient_ID", "Hospital", "Status", "Covid_Positive"]  # header
            patient_writer.writerow(fieldnames)
            patient_number = 0
            # writing information to csv file
            for patient in all_patients:
                patient_writer.writerow([str(patient_number)] + patient.get_info())  # write patient info to csv file
                patient_number += 1

            print("The state of the hospitals after {} days has been saved to {} in the working directory".format(
                self.__save_file_days * 10, file_name))
            self.__save_file_days += 1


    def find_most_beds(self):
        """
        find_most_beds looks through all Hospitals in the system and returns the name of the hospital with the most
            available beds
        :return: str
        """
        max_beds = 0
        name = ""
        for hospital in self.__system.hospitals.values():
            if hospital.available_beds() > max_beds:
                max_beds = hospital.available_beds()
                name = hospital.get_name()
        return name

    def admit_patient(self, curr_hospital):
        """
        admit_patient will admit a new patient to the Hospital, curr_hospital in the PatientManagementSystem, __system,
            with probabilities that determine if they are covid positive or not based on which the severity status is
            determined
        :param curr_hospital: str
        :return: None
        """
        has_covid = random.choices(['true', 'false'], [self.__covid_chance, 1 - self.__covid_chance])[0]
        if has_covid == 'true':
            sev_status = random.choices(['1', '2', '3'], [0.4, 0.3, 0.3])[0]
        else:
            sev_status = random.choices(['1', '2', '3'], [0.6, 0.3, 0.1])[0]

        # check if hospital full
        if self.__system.hospitals[curr_hospital].available_beds() > 0:
            self.__system.addPatient(curr_hospital, sev_status, has_covid)  # adding new patient

        else:
            # finding patient with lowest severity status
            low_status_patient = self.__system.find_lowest_status_patient(self.__system.hospitals[curr_hospital])
            # find hospital with most beds
            hospital_most_beds = self.find_most_beds()

            if hospital_most_beds != "" and low_status_patient != "":
                self.__system.transferPatient(low_status_patient, hospital_most_beds)  # transferring patient
                self.__system.addPatient(curr_hospital, sev_status, has_covid)  # adding new patient
                print("The patient with lowest severity, {}, was transferred to {}, which has the most available"
                      "beds. Then, a new patient was added to the {} hospital.".format(low_status_patient,
                                                                                       hospital_most_beds,
                                                                                       curr_hospital.capitalize()))
            else:
                print("Currently all patients in this hospital are at a severity status of level 3. Therefore,"
                      " it is not possible to transfer any patients from here!")

        # get id of the newly added patient
        patient_id = list(self.__system.hospitals[curr_hospital].get_patients().keys())[-1]
        # day 0 for this new patient
        self.__track_patients[patient_id] = 0

    def increment_days(self):
        """
        increment_days will increment the number of days a patient has stayed in a hospital by 1
        :return:None
        """
        # update number of days a patient has stayed in a hospital
        for key in self.__track_patients.keys():
            self.__track_patients[key] = int(self.__track_patients[key]) + 1

    @staticmethod
    def change_df_status(df, old_status, days_req, new_status):
        """
        change_df_status looks for the matching conditions required to change a patient's severity status and changes
            it. It will also reset the number of days to 0 once the status has changed.
        :param df: Dataframe
        :param old_status: str
        :param days_req: int
        :param new_status: str
        :return: Dataframe
        """
        # finding all patients with severity status of 2 and days spent in the hospital = 3
        df_status = df.loc[df["Status"] == old_status]
        df_status = df_status.index[df_status["Days"] == days_req]
        # get all indices of the patients to change their status from 2 to 1 in the main Dataframe (patient_status_df)
        index = df_status.tolist()
        for i in index:
            df.at[i, "Status"] = new_status
            df.at[i, "Days"] = 0
        return df

    def update_patient_tracking(self, df):
        """
        update_patient_tracking updates __track_patients dict to reflect the severity status changes made every
            simulated day
        :param df: Dataframe
        :return: None
        """
        # updating the days for patients in __track_patients dict and updating the Patient objects statuses to reflect
        #   new changes based on how long they have stayed in the hospital
        updated_patient_list = df['Patients'].tolist()
        updated_days_list = df["Days"].tolist()
        updated_status_list = df["Status"].tolist()

        # update Patient classes' statuses using patient_ids
        for patient in range(len(updated_patient_list)):
            self.__system.find_patient_hospital(updated_patient_list[patient]) \
                .get_patient(updated_patient_list[patient]).update_status(updated_status_list[patient])

        # updating the days in __track_patients from the modified Dataframe
        self.__track_patients = dict(zip(updated_patient_list, updated_days_list))

    def update_sev_status(self):
        """
        update_sev_status will update the severity status of all patients based on how long they have stay at a hospital
            with the following conditions:
            - If a patient of severity status of 3 has stayed at a hospital for 5 days, their status is changed to 2
            - If a patient of severity status of 2 has stayed at a hospital for 3 days, their status is changed to 1
            - If a patient of severity status of 1 has stayed at a hospital for 1 day, they are automatically discharged
                from the hospital
        :return: None
        """
        # get all patient ids
        all_patients = self.__system.get_values_or_keys("keys")
        # get all patients' severity statuses
        all_status = [self.__system.find_patient_hospital(patient).get_patient(patient).get_status()
                      for patient in all_patients]

        # get the days the patients have stay at their hospital
        days = []
        for patient in all_patients:
            days.append(self.__track_patients[patient])

        # create a dataframe to hold patient id, status and days stayed
        df_info = {"Patients": all_patients, "Status": all_status, "Days": days}
        patient_status_df = pd.DataFrame(df_info)

        # getting all patients with severity status of 1 and days stayed of 1 and discharging them
        #   the day isn't checked for because when this function is called their days stayed will be 1 as patients
        #   are added after this function is called in start_simulation
        df_status_1 = patient_status_df.loc[patient_status_df["Status"] == "1"]
        patients_to_discharge = df_status_1["Patients"].tolist()
        print("The following patients will now be discharged:")
        for patient in patients_to_discharge:
            self.__system.dischargePatient(patient)

        # removing patients from the Dataframe with severity status 1
        patient_status_df = patient_status_df.loc[patient_status_df["Status"] != "1"]

        # finding all patients with severity status of 2 and days spent in the hospital = 3
        patient_status_df = self.change_df_status(patient_status_df, "2", 3, "1")

        # finding all patients with severity status of 3 and days spent in the hospital = 5
        patient_status_df = self.change_df_status(patient_status_df, "3", 5, "2")

        # patient day tracking updated (__track_patients)
        self.update_patient_tracking(patient_status_df)

    def current_patients(self):
        """
        current_patients prints the current patients' ids, days stayed and the hospital they are at
        :return: None
        """

        print("Patient     Status     Days Stayed     Hospital")
        for patient in self.__track_patients.keys():
            hospital = self.__system.find_patient_hospital(patient)
            print(
                " {}         {}             {}          {}".format(patient, hospital.get_patient(patient).get_status(),
                                                                   self.__track_patients[patient],
                                                                   hospital.get_name()))

    def start_simulation(self):
        """
        start_simulation creates a simulation of the PatientManagementSystem for 90 days and works with the following
        conditions:
            - adds a patient to the Toronto Hospital every 4 days
            - adds a patient to the Kingston and Hamilton hospital every 7 days
            - probability of new patient having covid increases by 5% exponentially
            - if a patient doesnt have covid then the chances of being a severity status are as follows:
                - 3 -> 10%
                - 2 -> 30%
                - 1 -> 60%
            - if a patient does have covid then the chances of being a severity status are as follows:
                - 3 -> 30%
                - 2 -> 30%
                - 1 -> 40%
            - Patient severity status are changed as follows:
                - patient with severity status of 3 is given a status of 2 after 5 days
                - patient with severity status of 2 is given a status of 1 after 3 days
                - patient with severity status of 1 is automatically discharged after 1 day
        :return:None
        """
        for day in range(90):
            self.increment_days()
            # update sev-status of patients and discharge automatically if 0
            print("\nIt is day {}, patients' days stayed will now be updated!".format(day + 1))
            if day != 0 and self.__track_patients:
                self.update_sev_status()

            # increase covid chance by 5%
            self.__covid_chance *= 1.05
            print("Covid chance = {}".format(self.__covid_chance))

            if (day + 1) % 4 == 0:
                # admit a patient to Toronto hospital
                self.admit_patient("toronto")

            if (day + 1) % 7 == 0:
                # admit a patient to Kingston hospital
                self.admit_patient("kingston")
                # admit a patient to Hamilton hospital
                self.admit_patient("hamilton")

            if (day + 1) % 10 == 0:
                self.write_to_csv()

            print("The current patients are:")
            self.current_patients()

        print("\nThe simulation for 90 days has finished!")

def main():
    test = SimulateData()
    test.start_simulation()


main()
