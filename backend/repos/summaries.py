from ..models.summary import Summary
from ..db import session


def create_summary(**args):
    new_summary = Summary(**args)
    session.add(new_summary)
    session.commit()
