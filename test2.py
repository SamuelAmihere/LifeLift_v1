class AmbulanceOwner:
    available_ambulances = []
    available_drivers = []

    @property
    def ambulances(self):
        """This method returns a list of all ambulances
        owned by this operator
        """
        if len(self.available_ambulances) > 0:
            return self.available_ambulances
        return None

    @ambulances.setter
    def ambulances(self, value):
        """This method sets the list of all ambulances
        owned by this operator
        """
        print("Setter called")
        if value not in self.available_ambulances:
            print(value)
            self._ambulances = value

# Usage:
owner = AmbulanceOwner()
owner.ambulances = ['ambulance1', 'ambulance2', 'ambulance3']  # Update the list for this instance
