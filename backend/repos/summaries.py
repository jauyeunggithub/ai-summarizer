from models.summary import Summary
from db import session
from sqlalchemy import or_


def get_summary(id):
    return session.query(Summary).filter(Summary.id == id).first()


def get_paginated_summary_results(page=1, per_page=10, conditions=[]):
    query = session.query(Summary).filter(or_(*conditions))
    results = query.offset((page - 1) * per_page).limit(per_page).all()
    return results


def count_summary_results(conditions=[]):
    query = session.query(Summary).filter(or_(*conditions))
    return query.count()


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
