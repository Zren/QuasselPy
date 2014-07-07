import os, sys

from flask import Flask, render_template, request
from flaskutil import jsonify
# from werkzeug import SharedDataMiddleware

# Init
## App
app = Flask(__name__)
# app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
#     '/': os.path.join(os.path.dirname(__file__), 'static')
# })

## Quassel Connection
session = None


@app.route('/')
def index():
    template_data = {}
    return render_template('page/index.html', **template_data)

from quassel import quassel_session, Message, Buffer, Sender, Network
from sqlalchemy.orm import joinedload, contains_eager

@app.route('/api.json')
def api():
    DEFAULT_LIMIT = 10
    draw = int(request.args.get('draw', 0))
    start = int(request.args.get('start', 0))
    limit = int(request.args.get('length', DEFAULT_LIMIT))
    limit = min(limit, 100)
    if limit == -1:
        limit = DEFAULT_LIMIT

    networkNameFilter = request.args['columns[1][search][value]']
    bufferNameFilter = request.args['columns[2][search][value]']
    senderNameFilter = request.args['columns[3][search][value]']
    messageFilter = request.args['columns[4][search][value]']
    messageTypeFilter = request.args['columns[5][search][value]']
    messageTypeFilter = int(messageTypeFilter) if len(messageTypeFilter) > 0 else 0

    query = session.query(Message)
    count = query.count()

    query = session.query(Message)
    filteredCount = count

    filtered = False
    # if len(networkNameFilter) > 2:
    #     query = query.filter(Network.name.contains(networkNameFilter))
    #     filtered = True
    # if len(bufferNameFilter) > 2:
    #     query = query.filter(Message.buffer.name.contains(bufferNameFilter))
    #     filtered = True
    

    # query = query.join(Sender, Message.senderid == Sender.id)
    # query = query.join(Message.buffer)
    # query = query.join(Network, Network.id == Message.buffer.id)

    query = query.options(joinedload(Message.sender))
    query = query.options(joinedload(Message.buffer))
    # query = query.options(joinedload(Message.buffer.network))

    if len(messageFilter) > 2:
        query = query.filter(Message.message.contains(messageFilter))
        filtered = True

    if len(senderNameFilter) > 2:
        query = query.join(Message.sender)
        query = query.filter(Sender.name.contains(senderNameFilter))
        filtered = True

    messageBufferJoined = False
    if len(bufferNameFilter) > 2:
        query = query.join(Message.buffer)
        messageBufferJoined = True
        query = query.filter(Buffer.name.contains(bufferNameFilter))
        filtered = True

    if len(networkNameFilter) > 2:
        if not messageBufferJoined:
            query = query.join(Message.buffer)
        query = query.join(Buffer.network)
        query = query.filter(Network.name.contains(networkNameFilter))
        filtered = True

    if 0 < messageTypeFilter:
        query = query.filter(Message.type == messageTypeFilter)
        filtered = True

    if filtered:
        filteredCount = query.count()

    results = query[start:start+limit]
    messages = []
    for result in results:
        print(result)
        message = result
        message.buffer # Populate
        message.buffer.network # Populate
        message.sender # Populate
        messages.append(message)

    
    result = {}
    result['data'] = [message.to_dict() for message in messages]
    result['recordsTotal'] = count
    result['recordsFiltered'] = filteredCount
    result['draw'] = draw

    session.commit()
    return jsonify(result)

if __name__ == '__main__':
    from config import uri
    session = quassel_session(uri)
    app.run()
    session.close()
