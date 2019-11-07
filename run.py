import os
from phan_tan import init_app, db

app = init_app()


@app.teardown_appcontext
def shutdown_session(response_or_exc):
    db.session_factory.remove()
    return response_or_exc


if __name__ == '__main__':
    app.run(debug=os.getenv('ENVIRONMENT') == 'development')
