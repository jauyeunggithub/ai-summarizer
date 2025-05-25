from models.summary import Summary
from db import Session
from sqlalchemy import or_, and_


def get_summary(id):
    session = Session()
    return session.query(Summary).filter(Summary.id == id).first()


def get_paginated_summary_results(page=1, per_page=10, conditions=[]):
    session = Session()
    query = session.query(Summary).filter(or_(*conditions))
    results = query.offset((page - 1) * per_page).limit(per_page).all()
    return results


def count_summary_results(conditions=[]):
    session = Session()
    query = session.query(Summary).filter(or_(*conditions))
    return query.count()


def count_summary_results_and(conditions=[]):
    session = Session()
    query = session.query(Summary).filter(and_(*conditions))
    return query.count()


def create_summary(**args):
    session = Session()
    new_summary = Summary(**args)
    session.add(new_summary)
    session.commit()


def update_summary(**args):
    session = Session()
    id = args['summary_id']
    summary = session.query(Summary).filter(Summary.id == id).first()
    summary.user_id = args['user_id']
    summary.file_path = args['file_path']
    summary.text_to_summarize = args['text_to_summarize']
    summary.summary_result = args.get('summary_result')
    summary.status = args['status']
    session.commit()


def delete_summary(id):
    session = Session()
    summary = session.query(Summary).filter(Summary.id == id).first()
    summary.delete()
    session.commit()
