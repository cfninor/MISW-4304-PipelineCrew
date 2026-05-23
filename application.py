import newrelic.agent
try:
    newrelic.agent.initialize('newrelic.ini')
except Exception:
    pass

from app import create_app

application = create_app()
#print(application.url_map)

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000, debug=True)