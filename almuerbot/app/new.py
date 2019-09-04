import json
import os

from flask import Flask, jsonify, render_template, request, url_for
from flask_restful import Api


def new():
    """Endpoint to redirect to new user, autopivot or autocohort."""
    return render_template('new.html.j2', url_for=url_for)


# def new_autopivot():
#     """Endpoint to create new autopivots."""
#     if request.method == 'GET':
#         return render_template(
#             'new_autopivot.html.j2',
#             constants=constants,
#             scheduling=Schedule(),
#             filters=Filters(),
#             series=Series(),
#             categories=Categories())
#     else:
#         params = parse_autopivot_form(request.form)
#         response = requests.post(
#             os.path.join(constants.WEB_APP_URL, 'autopivots'),
#             data=params)
#         return render_template(
#             'submit.html.j2',
#             kind='autopivot',
#             response=response,
#             dumps=json.dumps,
#             snake_case_to_human=snake_case_to_human,
#             get_description=get_description)
#
#
# def new_user():
#     """Endpoint to create new users."""
#     if request.method == 'GET':
#         return render_template('new_user.html.j2', constants=constants)
#     else:
#         email = request.form.get('email')
#         response = requests.post(
#             os.path.join(constants.WEB_APP_URL, 'users'),
#             data={'email': email})
#         return render_template(
#             'submit.html.j2',
#             kind='user',
#             response=response,
#             dumps=json.dumps,
#             snake_case_to_human=snake_case_to_human,
#             get_description=get_description)
#
#
# def new_autocohort():
#     """Endpoint for creating new autocohorts."""
#     if request.method == 'GET':
#         return render_template(
#             'new_autocohort.html.j2',
#             constants=constants,
#             cohorts=Cohorts(),
#             scheduling=Schedule(),
#             filters=Filters(),
#             series=Series(),
#             categories=Categories())
#     else:
#         params = parse_autocohort_form(request.form)
#         response = requests.post(
#             os.path.join(constants.WEB_APP_URL, 'autocohorts'),
#             data=params)
#         return render_template(
#             'submit.html.j2',
#             kind='autocohort',
#             response=response,
#             dumps=json.dumps,
#             snake_case_to_human=snake_case_to_human,
#             get_description=get_description)
#
#
# def parse_categories(form):
#     """Parse categories from new automated report request."""
#     return ','.join([v for k, v in form.lists() if k == 'cats'][0])
#
#
# def parse_series(form):
#     """Parse series from new automated report request."""
#     _series = [v for k, v in form.lists() if k == 'series'][0]
#     series = []
#     for serie in _series:
#         if serie in ['ev_count_{}_tracked', 'ev_value_{}_tracked']:
#             series.append(serie.format(form.get('special_series', None)))
#         else:
#             series.append(serie)
#     return ','.join(series)
#
#
# def parse_filters(form):
#     """Parse filters from new automated report request."""
#     filters = {}
#     for k, v in form.lists():
#         if k.startswith('filter_') and not k.endswith('_'):
#             if not v[0] == '':
#                 filters[k[7:]] = ','.join(v)
#     cleanup_value = form.get('filter_cleanup_value_', None)
#     cleanup_field = form.get('filter_cleanup_field_', None)
#     cleanup_operator = form.get('filter_cleanup_operator_', None)
#     if all(map(bool, [cleanup_field, cleanup_value, cleanup_operator])):
#         filters['cleanup'] = cleanup_field + cleanup_operator + cleanup_value
#     return filters
#
#
# def parse_scheduling(form):
#     """Parse scheduling from new automated report request."""
#     scheduling = {}
#     for k, v in form.lists():
#         if (k in constants.AUTOPIVOT_FILTERS
#                 and k not in ('id', 'pivot_params')):
#             scheduling[k] = ''.join(v)
#     worksheet_token = form.get('worksheet_name_token', False)
#     scheduling['worksheet_name'] += (
#         ' - ' * bool(worksheet_token) + worksheet_token)
#     return scheduling
#
#
# def parse_cohort(form):
#     """Parse cohort params from new automated report request."""
#     cohort = {'right': 'events'}
#     keys = [
#         'left',
#         'right',
#         'right_to',
#         'value',
#         'cohort_number_of_days',
#         'cohort_aggregation_kind'
#     ]
#     for k, v in form.lists():
#         if k in keys:
#             cohort[k] = ''.join(v)
#     cohort['right_to'] = cohort['right_to'].format(
#         cohort.pop('cohort_number_of_days', ''))
#     cohort['right_bins'] = ','.join([
#         f'{i + 1}d' for i in range(int(cohort['right_to'][0]))])
#     if cohort.pop('cohort_aggregation_kind', '') == 'count':
#         cohort['value'] = 'count({})'.format(cohort['value'])
#     return cohort
#
#
# def parse_autopivot_form(form):
#     """Parse arguments from autopivot form."""
#     lists = form.lists()
#     cats = parse_categories(form)
#     series = parse_series(form)
#     filters = parse_filters(form)
#     params = parse_scheduling(form)
#
#     pivot_params = filters.copy()
#     pivot_params['cats'] = cats
#     pivot_params['series'] = series
#
#     params['pivot_params'] = json.dumps(pivot_params)
#     params['spreadsheet_id'] = extract_spreadsheet_id(
#         params['spreadsheet_id'])
#     params['schedule_interval'] = format_random_execution_time(
#         params['schedule_interval'])
#     return params
#
#
# def parse_autocohort_form(form):
#     """Parse arguments from autocohort form."""
#     lists = form.lists()
#     cats = parse_categories(form)
#     series = parse_series(form)
#     filters = parse_filters(form)
#     params = parse_scheduling(form)
#     cohort = parse_cohort(form)
#
#     pivot_params = filters.copy()
#     pivot_params['cats'] = cats
#     pivot_params['series'] = series
#
#     cohort_params = {**cohort, **filters}
#     cohort_params['groups'] = cats
#     pivot_params['series'] = series
#
#     params['pivot_params'] = json.dumps(pivot_params)
#     params['cohort_params'] = json.dumps(cohort_params)
#     params['spreadsheet_id'] = extract_spreadsheet_id(
#         params['spreadsheet_id'])
#     params['schedule_interval'] = format_random_execution_time(
#         params['schedule_interval'])
#     return params
