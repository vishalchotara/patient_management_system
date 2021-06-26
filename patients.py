class Patient:
    def __init__(self, patient_id, hospital, status, covid_positive):
        self.__patient_id = patient_id
        self.__hospital = hospital
        self.__status = status
        self.__covid_positive = covid_positive

    def update_hospital(self, new_hospital):
        """
        update_hospital changes the name of the hospital the Patient object is registered at
        :param new_hospital:
        :return: None
        """
        self.__hospital = new_hospital.lower()

    def update_status(self, new_status):
        """
        update_status changes the status of the Patient to a new one
        :param new_status: str
        :return: None
        """
        self.__status = new_status

    def get_info(self):
        """
        get_info returns the Patient's id, hospital, severity status and covid positive status in a list
        :return: List of str
        """
        return [self.__patient_id, self.__hospital, self.__status, self.__covid_positive]

    def get_status(self):
        """
        get_status returns the status of the Patient
        :return: str
        """
        return self.__status

    def get_id(self):
        """
        get_id returns the id of the Patient
        :return: str
        """
        return self.__patient_id
