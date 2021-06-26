class Hospital:
    def __init__(self, name, total_beds, num_beds_occupied, curr_patients):
        self.__name = name
        self.__total_beds = total_beds
        self.__occupied_beds = num_beds_occupied
        self.__patients_list = curr_patients

    def get_name(self):
        """
        get_name returns the name of the Hospital capitalized
        :return: str
        """
        return self.__name.capitalize()

    def add_patients(self, patient_id, patient):
        """
        add_patients adds the patient_id and Patient object, patient, to the dictionary of patients stored in the
            hospital object
        :param patient_id: str
        :param patient: Patient
        :return: None
        """
        self.__patients_list[patient_id] = patient
        self.__occupied_beds += 1

    def get_patients(self):
        """
        get_patients returns the dictionary of Patients
        :return: dictionary of Patients
        """
        return self.__patients_list

    def get_patient(self, patient_id):
        """
        get_patient returns the Patient object with the id, patient_id.
        :param patient_id: str
        :return: Patient
        """
        return self.__patients_list.get(patient_id)

    def discharge_patient(self, patient_id):
        """
        discharge_patient pops the Patient object that corresponds with the patient_id from the dictionary of
            Patients in the hospital object and returns the Patient object
        :param patient_id: str
        :return: Patient
        """
        self.__occupied_beds -= 1
        return self.__patients_list.pop(patient_id)

    def available_beds(self):
        """
        available_beds returns the number of beds still available in the Hospital
        :return: int
        """
        return self.__total_beds - self.__occupied_beds
