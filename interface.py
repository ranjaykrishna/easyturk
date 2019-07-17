"""Functions to launch, retrieve, and parse specific EasyTurk tasks.
"""

from random import shuffle

import json
import logging

from easyturk import EasyTurk


def launch_example(data, reward=1.00, tasks_per_hit=10):
    """Launches HITs to ask workers to caption images.

    Args:
        data: List containing image urls for the task.
        reward: A postive valued dollar amount per task.
        tasks_per_hit: Number of images per hit.

    Returns:
        A list of hit ids that have been launched.
    """
    et = EasyTurk()
    template = 'templates/example.html'
    hit_ids = []
    i = 0
    while i < len(data):
        hit_id = et.launch_hit(
            template, data[i:i+tasks_per_hit], reward=reward,
            title='Caption some pictures',
            description=('Write captions about the contents of images.'),
            keywords='image, caption, text')
        hit_ids.append(hit_id)
        i += tasks_per_hit
    return hit_ids


def fetch_completed_hits(hit_ids, approve=True):
    """Grabs the results for the hit ids.

    Args:
        hit_ids: A list of hit ids to fetch.
        approve: Whether to approve the hits that have been submitted.

    Returns:
        A dictionary from hit_id to the result, if that hit_id has
        been submitted.
    """
    et = EasyTurk()
    output = {}
    for hit_id in hit_ids:
        results = et.get_results(hit_id, results_on_fail=False)
        if len(results) > 0:
            output[hit_id] = results
            if approve:
                for assignment in results:
                    assignment_id = assignment['assignment_id']
                    et.approve_assignment(assignment_id)
    return output
