from tortoise.models import Model
from tortoise import fields
from enum import Enum
from core import state_machine


class User(Model):
    telegram_id = fields.IntField(unique=True)
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        table = "party_maker_users"


class Category(Model):
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        table = "party_maker_categories"


class StateEnum(Enum):
    wait_description = "wait_description"
    wait_categories = "wait_categories"
    wait_dates = "wait_dates"
    wait_location = "wait_location"
    wait_address = "wait_address"
    is_active = "is_active"
    finished = "finished"


state_alias = {
    "wait_description": "Wait Description",
    "wait_categories": "Wait Categories",
    "wait_dates": "Wait dates",
    "wait_location": "Wait location",
    "wait_address": "Wait address",
    "is_active": "Active Event",
    "finished": "Finished Event"
}


class Event(Model, state_machine.StateMachineMixin):
    STATE_ENUM = StateEnum
    ALIAS = state_alias

    name = fields.CharField(max_length=255, index=True)
    description = fields.TextField(null=True)
    categories = fields.ManyToManyField("models.Category", related_name="events", through="event_category")

    address = fields.CharField(max_length=500, null=True)
    longitude = fields.FloatField(null=True)
    latitude = fields.FloatField(null=True)

    start = fields.DatetimeField()
    end = fields.DatetimeField()

    user = fields.ForeignKeyField("models.User", related_name="user_events")
    followers = fields.ManyToManyField("models.User", related_name="follow_events", through="event_follow")

    state = fields.CharEnumField(StateEnum, max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        table = "party_maker_events"


class FeedBack(Model):
    event_owner = fields.ForeignKeyField("models.User", related_name="owner_feedback")
    client = fields.ForeignKeyField("models.User", related_name="client_feedback")
    event = fields.ForeignKeyField("models.Event", related_name="feedback")
    mark = fields.IntField()
