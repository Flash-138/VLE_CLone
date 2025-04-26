from flask import Flask
from routes.auth_routes import auth_bp
from routes.course_routes import course_bp
from routes.content_routes import content_bp
from routes.forum_routes import forum_bp
from routes.calender_routes import calendar_bp
from routes.report_routes import report_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET")

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(course_bp, url_prefix="/course")
app.register_blueprint(content_bp, url_prefix="/<string:course_id>/content")
app.register_blueprint(forum_bp, url_prefix="/<string:course_id>/forum")
app.register_blueprint(calendar_bp, url_prefix="/calendar")
app.register_blueprint(report_bp, url_prefix="/reports")


def list_routes(app):
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        url = urllib.parse.unquote(str(rule))
        line = f"{rule.endpoint:30s} | {methods:20s} | {url}"
        output.append(line)
    return output


if __name__ == '__main__':
        
    app.run(port=15000, debug=True)
