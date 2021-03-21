import flask
from flask import jsonify, request
from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'job', 'work_size', 'collaborators',
                                    'start_date', 'end_start', 'is_finished', 'team_leader'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_jobs(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(only=('id', 'job', 'work_size', 'collaborators',
                                       'start_date', 'end_start', 'is_finished', 'team_leader'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'job', 'work_size', 'collaborators', 'start_date',
                  'end_start', 'is_finished', 'team_leader']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    news = Jobs(
        id=request.json['id'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=request.json['start_date'],
        end_start=request.json['end_start'],
        is_finished=request.json['is_finished'],
        team_leader=request.json['team_leader'],
    )
    db_sess.add(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})
