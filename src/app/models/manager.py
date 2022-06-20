from .user import User


class Manager(User):

    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }
