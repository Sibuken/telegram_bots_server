from enum import Enum


class StateMachineMixin():
    STATE_FIELD_NAME = "state"
    STATE_ENUM: Enum = None
    ALIAS = {}

    @property
    def state_alias(self):
        value = getattr(self, self.STATE_FIELD_NAME)
        return self.ALIAS.get(value, value)

    @classmethod
    def states(cls):
        states = []
        for value in cls.STATE_ENUM.__members__.values():
            states.append({"name": value.value, "label": cls.ALIAS.get(value.value, value.value)})

        return states

    class Meta:
        abstract = True
