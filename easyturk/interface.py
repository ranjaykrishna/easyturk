"""Functions to launch, retrieve, and parse specific EasyTurk tasks.
"""

from easyturk import EasyTurk


def launch_verify_question_answer(data, reward=1.00, tasks_per_hit=50, sandbox=False):
    """Launches HITs to ask workers to verify bounding boxes.

    Args:
        data: List containing image urls, questions and answers, for the task.
        reward: A postive valued dollar amount per task.
        tasks_per_hit: Number of images per hit.
        sandbox: Whether to interact on sandbox or production.

    Returns:
        A list of hit ids that have been launched.
    """
    et = EasyTurk(sandbox=sandbox)
    template = 'verify_question_answer.html'
    hit_ids = []
    i = 0
    while i < len(data):
        hit = et.launch_hit(
            template, data[i:i+tasks_per_hit], reward=reward,
            title='Verify the answer to a question about an picture',
            description=('Verify whether an answer to a question about a picture is correct.'),
            keywords='image, text, picture, answer, question, relationship')
        hit_id = hit['HIT']['HITId']
        hit_ids.append(hit_id)
        i += tasks_per_hit
    return hit_ids


def launch_verify_relationship(data, reward=1.00, tasks_per_hit=30, sandbox=False):
    """Launches HITs to ask workers to verify bounding boxes.

    Args:
        data: List containing image urls, relationships, for the task.
        reward: A postive valued dollar amount per task.
        tasks_per_hit: Number of images per hit.
        sandbox: Whether to interact on sandbox or production.

    Returns:
        A list of hit ids that have been launched.
    """
    et = EasyTurk(sandbox=sandbox)
    template = 'verify_relationship.html'
    hit_ids = []
    i = 0
    while i < len(data):
        hit = et.launch_hit(
            template, data[i:i+tasks_per_hit], reward=reward,
            title='Verify relationships between objects in pictures',
            description=('Verify whether the relationships are correctly identified in pictures.'),
            keywords='image, text, picture, object, bounding box, relationship')
        hit_id = hit['HIT']['HITId']
        hit_ids.append(hit_id)
        i += tasks_per_hit
    return hit_ids


def launch_verify_bbox(data, reward=1.00, tasks_per_hit=30, sandbox=False):
    """Launches HITs to ask workers to verify bounding boxes.

    Args:
        data: List containing image urls, objects, for the task.
        reward: A postive valued dollar amount per task.
        tasks_per_hit: Number of images per hit.
        sandbox: Whether to interact on sandbox or production.

    Returns:
        A list of hit ids that have been launched.
    """
    et = EasyTurk(sandbox=sandbox)
    template = 'verify_bbox.html'
    hit_ids = []
    i = 0
    while i < len(data):
        hit = et.launch_hit(
            template, data[i:i+tasks_per_hit], reward=reward,
            title='Verify objects in pictures',
            description=('Verify whether objects are correctly identified in pictures.'),
            keywords='image, text, picture, object, bounding box')
        hit_id = hit['HIT']['HITId']
        hit_ids.append(hit_id)
        i += tasks_per_hit
    return hit_ids


def launch_caption(data, reward=1.00, tasks_per_hit=10, sandbox=False):
    """Launches HITs to ask workers to caption images.

    Args:
        data: List containing image urls for the task.
        reward: A postive valued dollar amount per task.
        tasks_per_hit: Number of images per hit.
        sandbox: Whether to interact on sandbox or production.

    Returns:
        A list of hit ids that have been launched.
    """
    et = EasyTurk(sandbox=sandbox)
    template = 'write_caption.html'
    hit_ids = []
    i = 0
    while i < len(data):
        hit = et.launch_hit(
            template, data[i:i+tasks_per_hit], reward=reward,
            title='Caption some pictures',
            description=('Write captions about the contents of images.'),
            keywords='image, caption, text')
        hit_id = hit['HIT']['HITId']
        hit_ids.append(hit_id)
        i += tasks_per_hit
    return hit_ids


def fetch_completed_hits(hit_ids, approve=True, sandbox=False):
    """Grabs the results for the hit ids.

    Args:
        hit_ids: A list of hit ids to fetch.
        approve: Whether to approve the hits that have been submitted.
        sandbox: Whether to interact on sandbox or production.

    Returns:
        A dictionary from hit_id to the result, if that hit_id has
        been submitted.
    """
    et = EasyTurk(sandbox=sandbox)
    output = {}
    for hit_id in hit_ids:
        results = et.get_results(hit_id, reject_on_fail=False)
        if len(results) > 0:
            output[hit_id] = results
            if approve:
                for assignment in results:
                    assignment_id = assignment['assignment_id']
                    et.approve_assignment(assignment_id)
    return output
