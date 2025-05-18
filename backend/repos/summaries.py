from ..models.summary import Summary
from ..db import session


def get_summary(id):
    return session.query(Summary).filter(Summary.id == id).first()


def create_summary(**args):
    new_summary = Summary(**args)
    session.add(new_summary)
    session.commit()


def update_summary(**args):
    summary = session.query(Summary).filter(Summary.id == id).first()
    summary.user_id = args['user_id']
    summary.file_path = args['file_path']
    summary.text_to_summarize = args['text_to_summarize']
    summary.summary_result = args['summary_result']
    session.commit()


def delete_summary(id):
    summary = session.query(Summary).filter(Summary.id == id).first()
    summary.delete()
    session.commit()
