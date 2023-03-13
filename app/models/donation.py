from sqlalchemy import Column, Text

from .abstact_model import ProjectDonation


class Donation(ProjectDonation):
    comment = Column(Text, nullable=True)
    # user_id = Column(Integer, ForeignKey('user.id', name='fk_donation_user_id_user'))
