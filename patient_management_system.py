# Vishal Chotara, 20307118
"""
This program creates a Patient Management System in which patients admitted to a hospital's ICU are assigned a
unique ID, severity status between 0 - 3 and noted whether they are covid positive or not. A user can add new patients,
transfer patients from hospital to hospital as long as there is space available, discharge patients and update the
severity status of a patient.
"""
import csv
import random
import string
import pandas as pd
from hospitals import Hospital
from patients import Patient

class PatientManagementSystem:
    """
    PatientManagementSystem holds a dictionary of the hospitals and all the functions that are needed for the
        Patient Management Program.
    """

    def __init__(self):
        self.hospitals = {"kingston": Hospital("Kingston", 10, 0, {}),
                          "hamilton": Hospital("Hamilton", 13, 0, {}),
                          "toronto": Hospital("Toronto", 20, 0, {})}

    def get_values_or_keys(self, option):
        """
        get_values_or_keys returns a list of all patients with either the Patient classes or the patient ids based on
            if option = "keys" or "values"
        :param option: str
        :return: List of Patient or List of str
        """
        data = []
        if option == "values":
            data = list(self.hospitals.get("kingston").get_patients().values()) + \
                           list(self.hospitals.get("hamilton").get_patients().values()) + \
                           list(self.hospitals.get("toronto").get_patients().values())
        if option == "keys":
            data = list(self.hospitals.get("kingston").get_patients().keys()) + \
                       list(self.hospitals.get("hamilton").get_patients().keys()) + \
                       list(self.hospitals.get("toronto").get_patients().keys())
        return data

    def read_in_csv(self):
        """
        reads in the initial_hospital_state.csv file into the hospitals dictionary of a PatientManagementSystem object
        :return: None
        """
        try:
            with open('initial_hospital_state.csv', 'r') as csv_file:
                patient_reader = csv.reader(csv_file, delimiter=',')
                next(patient_reader)  # skip header

                for row in patient_reader:
                    # make a new Patient object
                    new_patient = Patient(row[1], row[2], row[3], row[4])
                    # add Patient object to the correct hospital
                    self.hospitals.get(row[2].lower()).add_patients(row[1], new_patient)
        except:
            print("There was a problem with opening initial_hospital_state.csv, the system is currently empty.")

    def write_out_csv(self):
        """
        writes out to final_hospital_state.csv from the hospitals dictionary of a PatientManagementSystem object
        :return: None
        """
        with open('final_hospital_state.csv', 'w') as csv_file:
            patient_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
            # all existing ids
            all_patients = self.get_values_or_keys("values")

            fieldnames = ["", "Patient_ID", "Hospital", "Status", "Covid_Positive"]  # header
            patient_writer.writerow(fieldnames)
            patient_number = 0
            for patient in all_patients:
                patient_writer.writerow([str(patient_number)] + patient.get_info())  # write patient info to csv file
                patient_number += 1

    def addPatient(self, hospital_name, sev_status, covid_positive):
        """
        addPatient generates a new unique id across all the hospitals and creates a new Patient using this newly
            created key, sev_status and covid_positive value. This Patient is then assigned to the Hospital that
            corresponds with hospital_name. When this method is called, the Hospital should have available space or
            a new patient cannot be admitted.
        :param hospital_name: str
        :param sev_status: str
        :param covid_positive: str
        :return: None
        """
        # all existing ids
        all_patients = self.get_values_or_keys("keys")

        # generating new unique id
        random_id = str(random.randint(0, 9)) \
                    + str(random.randint(0, 9)) \
                    + str(random.randint(0, 9)) \
                    + random.choice(string.ascii_letters)

        while random_id in all_patients:
            random_id = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) \
                        + random.choice(string.ascii_letters)

        # create new Patient object
        patient = Patient(random_id, "Kingston", sev_status, covid_positive)

        # assign Patient to appropriate hospital
        self.hospitals.get(hospital_name.lower()).add_patients(random_id, patient)

        print("Patient successfully added to the {} hospital.".format(hospital_name))

    def transferPatient(self, patient_id, new_hospital_name):
        """
        transferPatient will transfer a patient from their current hospital to another hospital by moving the Patient
            object from the current Hospital object it is stored in to another Hospital object. The current hospital
            will discharge the patient from their hospital. When this method is called, the Patient object must have
            a severity status value of less than 3 to be transferred.
        :param patient_id: str
        :param new_hospital_name: str
        :return: None
        """

        curr_hospital = self.find_patient_hospital(patient_id)  # get the current hospital of the patient
        new_hospital = self.hospitals.get(new_hospital_name.lower())  # get the new hospital of the patient
        patient = curr_hospital.discharge_patient(patient_id)  # discharges patient from old hospital

        # transfer to new hospital
        new_hospital.add_patients(patient_id, patient)
        print("Patient transferred successfully to the {} hospital.".format(new_hospital_name))

    def dischargePatient(self, patient_id):
        """
        dischargePatient removes the patient from the hospital they are admitted to by removing the Patient object
            that is stored in that Hospital object. When this method is called the patient must have a severity status
            of 0.
        :param patient_id: str
        :return: None
        """
        hospital = self.find_patient_hospital(patient_id)  # find the patient's current hospital
        # remove the Patient object from the Hospital object by calling Hospital object's discharge_patient() method
        hospital.discharge_patient(patient_id)

        print("Patient {} has been discharged from the {} hospital.".format(patient_id,
                                                                            hospital.get_name().capitalize()))

    def updateStatus(self, patient_id, new_status):
        """
        updateStatus changes the severity status of the patient by changing the stored status value in the
            Patient object
        :param patient_id: str
        :param new_status: str
        :return: None
        """
        hospital = self.find_patient_hospital(patient_id)  # get the hospital of the patient
        patient = hospital.get_patient(patient_id)  # get the patient object from the Hospital object

        if patient.get_status() == new_status:  # if the new status of the patient is the same as the current one
            print("The patient already has a status of {}".format(new_status))
        else:
            patient.update_status(new_status)
        print("The status of {} has been successfully updated.".format(patient_id))

    def hospital_availability(self):
        """
        hospital_availability iterates through all the Hospital objects and appends the names of those that have
            space available to take new patients by using the available_beds() method from the Hospital class. The
            list of strings is then returned.
        :return: List of Str
        """
        available = []
        for hospital in self.hospitals.values():  # iterate Hospital objects
            if hospital.available_beds() > 0:  # determine if beds are available at the current Hospital
                available.append(hospital.get_name().lower())
        return available

    def get_patient(self):
        """
        get_patient is used to get the user_id of a patient from the user (used for transferring, discharging or
            updating a Patient object). The method checks if the user_id inputted exists in any of the hospitals
            and then returns it if it does, otherwise the user is asked to enter an existing patient id
        :return: str
        """
        patient_id = input()
        # find patients' hospital if patient exists
        patient_hospital = self.find_patient_hospital(patient_id.lower())

        while patient_hospital == False:  # keep asking until a valid id is entered
            print("This patient ID does not exist, please make sure the ID "
                  "consists of 3 numbers followed by a letter.")
            patient_id = input()
            # check if a Patient object with this id exists
            patient_hospital = self.find_patient_hospital(patient_id.lower())

        return patient_id

    def find_patient_hospital(self, patient_id):
        """
        find_patient_hospital uses the string patient_id to find the Hospital of the patient and returns the Hospital
            object if its found, otherwise it will return False.
        :param patient_id: str
        :return: Hospital or Bool
        """
        # returns the kingston hospital
        if patient_id in self.hospitals.get("kingston").get_patients().keys():
            return self.hospitals.get("kingston")

        # returns the hamilton hospital
        if patient_id in self.hospitals.get("hamilton").get_patients().keys():
            return self.hospitals.get("hamilton")

        # returns the toronto hospital
        if patient_id in self.hospitals.get("toronto").get_patients().keys():
            return self.hospitals.get("toronto")

        return False  # patient id doesnt exist

    def get_hospital_choice(self, available_hospitals):
        """
        get_hospital_choice is a method that is used to interact with the user and get the name of the hospital that
            they will perform an action with. It will list all hospitals with the number of available beds and only
            let the user choose from those hospitals. Returns the a string with the name of the chosen hospital
        :param available_hospitals: List of str
        :return: str
        """

        # list all the Hospitals
        for hospital in available_hospitals:
            print("{} -> Beds available: {}".format(
                hospital.capitalize(), self.hospitals[hospital].available_beds()))

        choice = input("\nType in the name of the hospital you want to choose here: ")

        # checks if the input is one of the names of the hospitals available
        while choice.lower() not in available_hospitals:
            print("Please type the name of one of the hospitals from the available hospitals!")
            choice = input("\nPlease try again: ")

        return choice

    def make_rows_df(self, max_length):
        """
        make_rows_df returns a list of (list of str) which is a list of patient ids for each hospital used to create
            a dataframe
            e.g.
            ["123f", "345d", "654h"]
            Kingston    Hamilton    Toronto
              123f        345d       654h
        :param max_length: int
        :return: list of (list of str)
        """
        # adding all patients ids to patients list to create each row for the table. patient ids appended as long as
        #   they exist in that index, otherwise an empty string appended
        patients = []

        for i in range(max_length):
            temp = []
            if i < len(self.hospitals.get("kingston").get_patients()):
                temp.append(list(self.hospitals.get("kingston").get_patients().keys())[i])
            else:
                temp.append("")
            if i < len(self.hospitals.get("hamilton").get_patients()):
                temp.append(list(self.hospitals.get("hamilton").get_patients().keys())[i])
            else:
                temp.append("")
            if i < len(self.hospitals.get("toronto").get_patients()):
                temp.append(list(self.hospitals.get("toronto").get_patients().keys())[i])
            else:
                temp.append("")
            if len(temp) > 0:
                patients.append(temp)
            temp = []
        return patients

    def print_patients(self):
        """
        print_patients prints all the patient ids under each Hospital in a table format using the pandas module
            for the user to see the current patients.
        :return: None
        """

        # finding the greatest number of patients in any Hospital
        max_length = max([len(self.hospitals.get("kingston").get_patients()),
                          len(self.hospitals.get("hamilton").get_patients()),
                          len(self.hospitals.get("toronto").get_patients())])

        # adding all patients ids to patients list to create each row for the table. patient ids appended as long as
        #   they exist in that index, otherwise an empty string appended
        patients = self.make_rows_df(max_length)

        # creating a pandas dataframe to use to represent the table
        df = pd.DataFrame(patients, columns=["Kingston", "Hamilton", "Toronto"])

        # printing the table
        print(df.to_string(justify="center"))

    def option_1(self):
        """
        option_1 gives a text interface to user for adding a patient to a hospital. the user is presented will hospitals
            that have available beds and therefore they can only select from those hospitals.
        :return: None
        """
        available_hospitals = self.hospital_availability()  # find the available hospitals

        # user chooses the hospital

        if len(available_hospitals) < 1:  # if no hospitals are available
            print("Sorry, there are currently no hospitals that can admit new patients!"
                  " A patient needs to be discharged first to proceed further.")
        else:
            print("The following hospitals are available to admit a new patient, please choose one of them"
                  " by typing out the name of the hospital:\n")

            # choosing hospital
            choice = self.get_hospital_choice(available_hospitals)  # get input for hospital name

            # Severity Status of the patient
            print("Please enter the Severity status of the patient (Must be 1, 2 or 3):")
            sev_status = self.get_sev_status()  # get input for sev status

            # asking if patient is covid positive or not
            print("Please enter \"True\" if the patient is Covid positive, otherwise enter \"False\":")
            covid_positive = input()
            while covid_positive.lower() not in ["true", "false"]:
                print("There was a problem with your input, please try again "
                      "(Covid status must be either \"True\" or \"False\"):")
                covid_positive = input()

            # adding patient to the hospital
            self.addPatient(choice, sev_status, covid_positive.lower())

        self.write_out_csv()  # save
        print("The system has now saved its state!")
        print("You will now be returned to the main menu.\n")
        self.print_menu()

    def option_2(self):
        """
        option_2 gives a text interface for user to transfer a patient. A list of available hospitals with space
            is given to the user alongside a list of current patients. The user can only choose from the available
            hospitals and a patient can only be transferred if they have a status of less than 3, a patient with the
            lowest severity status will be suggested. The user will be informed if no patient can be transferred.
        :return: None
        """
        #  get patient id and their hospital
        print("Here is a list of patients at their respective hospitals:")
        self.print_patients()
        print("Please enter the ID of the patient that you want to transfer:")
        patient = self.get_patient()  # getting input for patient id
        patient_hospital = self.find_patient_hospital(patient)

        # if patient has severity status of 3
        if int(patient_hospital.get_patient(patient).get_status()) == 3:
            print("This patient has a severity status of 3, and therefore cannot be transferred.")

            # get the patient id of the patient with lowest status, if nothing below 3 exists then
            # low_status_patient will be an empty string
            low_status_patient = self.find_lowest_status_patient(patient_hospital)

            if low_status_patient != "":  # lowest status patient is suggested to user
                print("The system suggests that you transfer patient {} as they have the lowest severity"
                      " status currently.".format(low_status_patient))
            else:
                print("Currently all patients in this hospital are at a severity status of level 3. Therefore,"
                      " it is not possible to transfer any patients from here!")

        else:
            # remove the hospital the patient is currently at
            available_hospitals = self.hospital_availability()
            available_hospitals.remove(patient_hospital.get_name().lower())

            if len(available_hospitals) < 1:  # if no hospitals are available
                print("Sorry, there are currently no hospitals that can admit new patients!"
                      " A patient needs to be discharged first to proceed further.")
            else:
                print("The following hospitals are available to accept a transfer, please choose one of them"
                      " by typing out the name of the hospital:\n")
                # choosing hospital
                choice = self.get_hospital_choice(available_hospitals)  # getting user input for hospital name

                self.transferPatient(patient, choice)

        self.write_out_csv()  # save
        print("The system has now saved its state!")
        print("\nYou will now be returned to the main menu.")
        self.print_menu()

    def option_3(self):
        """
        option_3 gives a text interface for user to discharge a patient. a patient cannot be discharged if they don't
            have a severity status of 0
        :return: None
        """
        #  get the patient id and the hospital
        print("Here is a list of patients at their respective hospitals:")
        self.print_patients()
        print("Please enter the ID of the patient that you want to discharge:")
        patient = self.get_patient()  # get user input for patient id
        patient_hospital = self.find_patient_hospital(patient)

        if int(patient_hospital.get_patient(patient).get_status()) != 0:
            print("A patient can only be discharged if they have a severity status of 0, {} has a severity "
                  "status of {}.".format(patient, patient_hospital.get_patient(patient).get_status()))
        else:
            self.dischargePatient(patient)

        self.write_out_csv()  # save
        print("The system has now saved its state!")
        print("\nYou will now be returned to the main menu.")
        self.print_menu()

    def option_4(self):
        """
        option_4 gives a text interface for user to update the status of a patient
        :return: None
        """
        #  get the patient id
        print("Here is a list of patients at their respective hospitals:")
        self.print_patients()
        print("Please enter the ID of the patient that you want to update the severity status of:")
        patient = self.get_patient()  # get user input for patient id

        # getting new severity status
        print("Please enter the new severity status of the patient (Must be 0, 1, 2 or 3):")
        new_sev_status = self.get_sev_status()  # get user input for severity status

        # updating the patient's status
        self.updateStatus(patient, new_sev_status)

        self.write_out_csv()  # save
        print("The system has now saved its state!")
        print("\nYou will now be returned to the main menu.")
        self.print_menu()

    @staticmethod
    def find_lowest_status_patient(hospital):
        """
        find_lowest_status_patient finds the patient in a hospital object, Hospital, with the lowest severity status
            and returns the patient id of that patient
        :param hospital: Hospital
        :return: str
        """
        # find a patient with the lowest severity status
        low_status_patient_id = ""
        minimum_status = 3
        patients = hospital.get_patients()

        # finding minimum status value and keeping track of that patient's id
        for patient in patients.values():
            if int(patient.get_status()) < minimum_status:
                minimum_status = int(patient.get_status())
                low_status_patient_id = patient.get_id()

        return low_status_patient_id

    @staticmethod
    def get_sev_status():
        """
        get_sev_status is used to interact with the user to get a severity status from them as an input and returns a
            string. the user must enter either 0, 1, 2 or 3 or they will be prompted to reenter another input
        :return: str
        """
        sev_status = input()
        # continuous loop until user enters a valid input
        while sev_status not in ["0", "1", "2", "3"]:
            print("There was a problem with your input, please try again "
                  "(Severity status must be 0, 1, 2 or 3):")
            sev_status = input()
        sev_status = sev_status
        return sev_status

    @staticmethod
    def print_menu():
        """
        print_menu prints the options that a user has in the main menu
        :return: None
        """
        print("Please select from one of the following options by typing in the number:")
        print("     1. Add a new patient.")
        print("     2. Transfer a patient to another hospital.")
        print("     3. Request to discharge a patient.")
        print("     4. Update the Severity status of a patient.")
        print("     Type in \"exit\" to stop this program.")

    def run_program(self):
        """
        run_program is the main driver of the Patient Management System and acts as the text interface for the user
        :return: None
        """
        # read in csv file
        self.read_in_csv()
        print("             ---------------------------------------------------------------------")
        print("             -                                                                   -")
        print("             -                   Patient Management System                       -")
        print("             -                                                                   -")
        print("             ---------------------------------------------------------------------")

        self.print_menu()
        option = input("Type in the number here: ")

        while option.lower() != "exit":

            if option == "1":  # adding a new patient
                self.option_1()

            elif option == "2":  # transferring a patient
                self.option_2()

            elif option == "3":
                self.option_3()

            elif option == "4":
                self.option_4()

            else:  # invalid input
                print("That was an invalid option! Please try again by typing a number from 1 - 4 that corresponds"
                      " to one of the options or type \"exit\" to exit the program.")
            option = input()

        print("The program has now stopped!")


def main():
    patient_management_system = PatientManagementSystem()
    patient_management_system.run_program()

main()
