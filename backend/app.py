from flask import Flask, jsonify, request

app = Flask(__name__)

task = []

@app.route('/api/tasks', methods=['GET'])
def tasks():
    return jsonify(task)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()

    task = data.get('task', '')

    tasks.append(task)

    return jsonify({'message': 'Task added successfully!'})

@app.route('/api/tasks/<int:index>', methods=['DELETE'])

def remove_task(index):

    if 0 <= index < len(tasks):

        del tasks[index]

        return jsonify({'message': 'Task removed successfully!'})

    else:

        return jsonify({'error': 'Invalid index!'}), 400

if __name__ == '__main__':
    app.run()
