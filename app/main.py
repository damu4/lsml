from celery import Celery
from celery.result import AsyncResult
from flask import (
    Flask,
    make_response,
    render_template,
    request,
)


celery_app = Celery('tasks', backend='redis://redis', broker='redis://redis')
app = Flask(__name__)


@app.route('/iris', methods=['GET', 'POST'])
def iris_handler():
    if request.method == 'POST':
        sl = request.form['sl']
        sw = request.form['sw']
        pl = request.form['pl']
        pw = request.form['pw']
        sample = [[int(sl), int(sw), int(pl), int(pw)]]

        task = celery_app.send_task('tasks.predict', sample)

        return render_template('check.html', value=task.id)


@app.route('/iris/<task_id>', methods=['GET', 'POST'])
def iris_check_handler(task_id):
    task = AsyncResult(task_id, app=celery_app)
    if task.ready():
        labels = {
            0: 'iris-setosa',
            1: 'iris-versicolor',
            2: 'iris-virginica',
        }
        text = f'DONE, result {labels[int(task.result[0])]}'
    else:
        text = 'IN_PROGRESS'
    response = make_response(text, 200)
    response.mimetype = "text/plain"
    return response


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
