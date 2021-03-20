#!/usr/bin/env python3

from flask import Response, Flask, request
import time
import json


app = Flask(__name__)
tasks = {}


def add_task(data):
    '''Adds a task to tasks.'''

    try:
        next_id = max(i for i in tasks.keys())
        next_id += 1
    except ValueError as e:
        next_id = 1

    tasks[next_id] = { 'id': next_id,
            'created_at': get_time(),
            'updated_at': None
            }
    tasks[next_id].update(json.loads(data))


def update_task(idd, data):
    '''Updates a task.'''

    idd = int(idd)
    data = json.loads(data)
    tasks[idd].update(data)
    tasks[idd]['updated_at'] = get_time()
    return json.dumps(get_task(idd))


def get_task(idd=None):
    '''Get task(s).'''

    if idd == None:
        task = []
        for key, value in tasks.items():
            task.append(value)
        return json.dumps(task)

    return json.dumps(tasks[int(idd)])


def delete_task(idd):
    '''Delete a given task.'''

    if idd == None:
        return False
    try:
        tasks.pop(int(idd))
        return True
    except KeyError:
        return False


def get_time():
    '''Returns the current time in the format DD-MM-YY-HH-MM-SS'''

    return time.strftime("%m-%d-%y-%H-%M-%S")


@app.route('/task', methods = ['POST', 'GET'])
def task():
    if request.method == 'POST':
        add_task(request.data)
        return Response(status=201)
    if request.method == 'GET':
        return Response(response=get_task(), status=200)


@app.route('/task/<idd>', methods = ['GET', 'PUT', 'DELETE'])
def task_id(idd):
    error = json.dumps({'error': 'Invalid task ID'})
    if request.method == 'GET':
        try:
            return Response(response=get_task(idd), status=200)
        except KeyError as e:
            return Response(response=error, status=404)
    if request.method == 'PUT':
        task = update_task(idd, request.data)
        if task:
            return Response(response=task, status=200)
        else:
            return Response(status=404)
    if request.method == 'DELETE':
        if delete_task(idd):
            return Response(status=200)
        else:
            return Response(response=error,status=404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000)
