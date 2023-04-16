from flask import Flask,request
from resources import Entry,EntryManager

app = Flask(__name__)

FOLDER = 'D:\\rainm\pythonProject\\todo-list-backend\\tmp'


@app.route('/')
def hello_world():
    return '<p>Hello, Alex</p>'


@app.route('/api/entries/')
def get_entries():
    entry_manager = EntryManager(FOLDER)
    entry_manager.load()
    return [i.json() for i in entry_manager.entries]



@app.route('/api/save_entries/', methods=['POST'])
def save_entries():
    entry_manager = EntryManager(FOLDER)
    for i in request.get_json():
        entry_manager.entries.append(Entry.from_json(i))
    entry_manager.save()
    return {'status': 'success'}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=False)
