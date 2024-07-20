from enum import Enum

# Definindo a Enum para os estados possíveis
class State(Enum):
    WALKING = "walking"
    ELECTING = "electing"


# Definindo a Enum para os status possíveis
class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Token:
    def __init__(self, status: Status):
        self._status = status # ACTIVE ou INACTIVE
        self._id = 0
        self._leader = None
        self._state = State.WALKING  # WALKING ou ELECTING
        self._nodeClocks = []

    @property
    def status(self):
        return self._status  


    @status.setter
    def status(self, value):
        if isinstance(value, Status):
            self._status = value  
        else:
            raise ValueError("Invalid status. Must be an instance of Status Enum.")

    @status.setter
    def status(self, value):
        self._status = value 

    @property
    def id(self):
        return self._id  

    @id.setter
    def id(self, value):
        self._id = value  

    @property
    def leader(self):
        return self._leader  

    @leader.setter
    def leader(self, value):
        self._leader = value  

    @property
    def state(self):
        return self._state  

    @state.setter
    def state(self, value):
        if isinstance(value, State):
            self._state = value  
        else:
            raise ValueError("Invalid state. Must be an instance of State Enum.")

    @property
    def nodeClocks(self):
        return self._nodeClocks  

    @nodeClocks.setter
    def nodeClocks(self, id_value_tuple):
        if (self.state == State.ELECTING):
            insertType, info, currentClocksList = id_value_tuple

            self._nodeClocks = currentClocksList 

            if (insertType == "first"):
                self._nodeClocks.insert(0, info)
            elif (insertType == "end"):
                self._nodeClocks.append(info) 


    def clearNodeClocks(self):
        self.nodeClocks = []

