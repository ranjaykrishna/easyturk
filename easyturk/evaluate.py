"""Script to render a completed EasyTurk task.
"""

from flask import Flask
from flask import render_template
from flask import request

import json
import os

from easyturk import EasyTurk


# Global server variables.
app = Flask(__name__)


def get_e_filename(filename):
    """Modifies the filename to include _e_ in front.

    Args:
        filename: A filename (ex, directory/filename.json)

    Returns:
        A string directory/_e_filename.json
    """
    dirname = os.path.dirname(filename)
    index = len(dirname) + 1
    dirname = filename[0:index]
    filename = filename[index:]
    return dirname + '_e_' + filename


def convert(results):
    """Converts the results to include metadata for navigation.

    Args:
        results: A dictionary mapping from hit_id to hit data.

    Returns:
        A dictionary containing:
            - hits: All hits ordered by workers.
            - workers: Mapping from worker_id to indices into hits.
    """
    # Organize all the data by worker id.
    worker_map = {}
    for hit_id, hit in results.items():
        for assignment in hit:
            worker_id = assignment['worker_id']
            if worker_id not in worker_map:
                worker_map[worker_id] = []
            worker_map[worker_id].append(assignment)

    # Create the hits and worker index mapping structures.
    hits = []
    worker_indices = {}
    worker_ids = []
    for worker_id, assignments in worker_map.items():
        worker_indices[worker_id] = range(
                len(hits), len(hits) + len(assignments))
        hits.extend(assignments)
        worker_ids.append(worker_id)
    output = {'hits': hits,
              'workers': worker_indices,
              'worker_ids': worker_ids}
    return output


@app.route('/task')
def task():
    """Visualizes the results received for a given task.
    """
    # Compile the template.
    task = request.args['task']
    results_file = request.args['results']
    eresults_file = get_e_filename(results_file)
    if os.path.exists(eresults_file):
        results = json.load(open(eresults_file))
    else:
        results = json.load(open(results_file))
        results = convert(results)
        json.dump(results, open(eresults_file, 'w'))
    return render_template(
            'evaluation/' + task,
            results=results,
            task=results_file,
            eresults_file=eresults_file)


@app.route('/interface', methods=['POST'])
def interface():
    """Endpoint that rejects and approves work.
    """
    et = EasyTurk(sandbox=False)
    if request.method != 'POST':
        return 'Fail'
    assignment_ids = json.loads(request.form['assignment_ids'])
    approve = json.loads(request.form['approve'])
    for assignment_id in assignment_ids:
        if approve:
            et.approve_assignment(assignment_id)
        else:
            et.reject_assignment(assignment_id)
    eresults_file = request.form['eresults_file']
    results = json.load(open(eresults_file))
    for hit in results['hits']:
        if hit['assignment_id'] in assignment_ids:
            hit['approve'] = approve
    json.dump(results, open(eresults_file, 'w'))
    return 'Succcess'


@app.route('/')
def home():
    return render_template('evaluation/home.html')


if __name__=='__main__':
    app.run()
