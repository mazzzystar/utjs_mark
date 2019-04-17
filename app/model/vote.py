from sqlalchemy import Column, Boolean
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.event import listens_for

from model.base import Base


class Vote(Base):
    __tablename__ = 'vote'

    voter = Column('voter', String(20), ForeignKey("user.username"), primary_key=True)
    lecturer = Column('lecturer', String(20), ForeignKey("user.username"), primary_key=True)
    content = Column('content', Integer())
    gesture = Column('gesture', Integer())
    voice = Column('voice', Integer())
    event_id = Column('event_id', Integer(), ForeignKey("vote_event.event_id"), primary_key=True)


class VoteEvent(Base):
    __tablename__ = 'vote_event'
    event_id = Column('event_id', Integer(), primary_key=True, autoincrement=True)
    lecture_team = Column('lecture_team', Integer(), nullable=False)
    vote_team = Column('vote_team', Integer(), nullable=False)
    is_active = Column('is_active', Boolean(), default=False)


@listens_for(VoteEvent, "before_update")
def receive_modified(mapper, connection, instance):
    if instance.is_active:
        connection.execute('update vote_event set is_active=false where is_active=true')


@listens_for(VoteEvent, "before_insert")
def receive_before_insert(mapper, connection, instance):
    if instance.is_active:
        connection.execute('update vote_event set is_active=false where is_active=true')
        # todo:无法在回调函数中使用SQLAlchemy更改数据
