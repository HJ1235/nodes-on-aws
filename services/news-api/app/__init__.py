from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)

    NEWS_DATA = [
        {"id": 1, "title": "Kubernetes news", "content": "Cluster is running well."},
        {"id": 2, "title": "CI/CD news", "content": "Jenkins pipeline will be added soon."},
        {"id": 3, "title": "Monitoring news", "content": "Prometheus and Grafana will be installed."}
    ]

    @app.route("/healthz", methods=["GET"])
    def healthz():
        return jsonify({"status": "ok"}), 200

    @app.route("/api/news", methods=["GET"])
    def get_news():
        return jsonify(NEWS_DATA), 200

    @app.route("/api/news/<int:news_id>", methods=["GET"])
    def get_news_detail(news_id):
        for item in NEWS_DATA:
            if item["id"] == news_id:
                return jsonify(item), 200
        return jsonify({"error": "news not found"}), 404

    return app
