from app.core.db import Base, ProjectDonation

from sqlalchemy import Column, Text


class Donation(ProjectDonation):
    comment = Column(Text, nullable=True)
    # user_id = Column(Integer, ForeignKey('user.id', name='fk_donation_user_id_user'))