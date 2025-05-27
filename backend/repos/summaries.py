from models.summary import Summary
from db import Session
from sqlalchemy import or_, and_


def get_summary(id):
    session = Session()
    return session.query(Summary).filter(Summary.id == id).first()


def get_paginated_summary_results(page=1, per_page=10, conditions=[]):
    session = Session()
    query = session.query(Summary) \
        .filter(or_(*conditions))  \
        .filter(or_(Summary.is_deleted == False, Summary.is_deleted.is_(None)))
    results = query.offset((page - 1) * per_page).limit(per_page).all()
    return results


def count_summary_results(conditions=[]):
    session = Session()
    query = session.query(Summary) \
        .filter(or_(*conditions)) \
        .filter(or_(Summary.is_deleted == False, Summary.is_deleted.is_(None)))
    return query.count()


def count_summary_results_and(conditions=[]):
    session = Session()
    query = session.query(Summary) \
        .filter(and_(*conditions)) \
        .filter(or_(Summary.is_deleted == False, Summary.is_deleted.is_(None)))
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
    if 'user_id' in args:
        summary.user_id = args['user_id']
    if 'file_path' in args:
        summary.file_path = args['file_path']
    if 'text_to_summarize' in args:
        summary.text_to_summarize = args['text_to_summarize']
    if 'summary_result' in args:
        summary.summary_result = args.get('summary_result')
    if 'status' in args:
        summary.status = args['status']
    if 'is_deleted' in args:
        summary.is_deleted = args['is_deleted']
    session.commit()


def delete_summary(id):
    session = Session()
    summary = session.query(Summary).filter(Summary.id == id).first()
    summary.is_deleted = True
    session.commit()
