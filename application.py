import argparse
from flask import Flask, Response
from flask_graphql import GraphQLView
import json

from schemas import schema


application = Flask(__name__)


@application.route("/", methods=["GET"])
def health_check():
    return Response(
        response=json.dumps({'error': 'none', 'data': 'Health check good.'}),
        status=200,
        mimetype='application/json'
    )


application.add_url_rule('/graphql',
                         view_func=GraphQLView.as_view('graphql',
                                                       schema=schema,
                                                       graphiql=True))

if __name__ == "__main__":
    parser = argparse.ArgumentParser("""
    Creates a flask.Flask instance and runs it. Parses
    command-line flags to configure the app.
    """)
    msg = 'Hostname of Flask app [{}]'.format("0.0.0.0")
    parser.add_argument("-H", "--host",
                        help=msg,
                        default="0.0.0.0")
    msg = 'Port for Flask app [{}]'.format("80")
    parser.add_argument("-P", "--port",
                        help=msg,
                        default="80")
    parser.add_argument("-d", "--debug",
                        action="store_true", dest="debug")

    args = parser.parse_args()

    application.run(
        debug=args.debug,
        host=args.host,
        port=int(args.port)
    )
