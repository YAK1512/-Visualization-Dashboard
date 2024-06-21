from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from flask_cors import CORS

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:yash@localhost:5432/sampledb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class JsonData(db.Model):
    __tablename__ = 'energy_data'

    id = db.Column(db.Integer, primary_key=True)
    end_year = db.Column(db.Integer)
    intensity = db.Column(db.String(50))
    sector = db.Column(db.String(255))
    topic = db.Column(db.String(255))
    insight = db.Column(db.Text)
    url = db.Column(db.String(255))
    region = db.Column(db.String(255))
    start_year = db.Column(db.Integer)
    impact = db.Column(db.String(255))
    added = db.Column(db.String(50))
    published = db.Column(db.String(50))
    country = db.Column(db.String(255))
    relevance = db.Column(db.String(50))
    pestle = db.Column(db.String(255))
    source = db.Column(db.String(255))
    title = db.Column(db.String(255))
    likelihood = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'end_year': self.end_year,
            'intensity': self.intensity,
            'sector': self.sector,
            'topic': self.topic,
            'insight': self.insight,
            'url': self.url,
            'region': self.region,
            'start_year': self.start_year,
            'impact': self.impact,
            'added': self.added,
            'published': self.published,
            'country': self.country,
            'relevance': self.relevance,
            'pestle': self.pestle,
            'source': self.source,
            'title': self.title,
            'likelihood': self.likelihood
        }

@app.route('/api/json_data', methods=['GET'])
def get_json_data():
    data = JsonData.query.all()
    return jsonify([item.to_dict() for item in data])

@app.route('/api', methods=['GET'])
def get_data():
    try:
        filters = request.args.to_dict()
        query = db.session.query(JsonData)

        for key, value in filters.items():
            if key in ['id', 'end_year', 'start_year']:
                query = query.filter(getattr(JsonData, key) == int(value))
            elif key in ['intensity', 'impact', 'relevance', 'likelihood']:
                query = query.filter(getattr(JsonData, key) == value)
            elif key in ['topic', 'region', 'pestle', 'source', 'country', 'added', 'published']:
                query = query.filter(getattr(JsonData, key).ilike(f'%{value}%'))

        results = query.all()
        data = [item.to_dict() for item in results]
        return jsonify(data)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return jsonify({'error': error}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    try:
        with app.app_context():
            db.session.execute(text('SELECT 1'))
        app.run(debug=True)
    except SQLAlchemyError as e:
        print(f"Database connection failed: {str(e)}")
