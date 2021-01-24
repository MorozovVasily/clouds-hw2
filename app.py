from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


import socket
my_ip = socket.gethostbyname(socket.gethostname())


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:vasya@178.154.253.212:5432/healthcheck"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class HealthCheck(db.Model):
    __tablename__ = 'healthcheck'

    ip = db.Column(db.String(), primary_key=True)
    status = db.Column(db.String())

    def __init__(self, ip, status):
        self.ip = ip
        self.status = status

    def __repr__(self):
        return f"<healthcheck {self.ip} {self.status}>"


@app.route('/', methods=['POST', 'GET'])
def handle_health():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_car = HealthCheck(ip=data['ip'], status=data['status'])
            db.session.add(new_car)
            db.session.commit()
            return {"message": f"entry {new_car.ip} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        server = HealthCheck.query.all()
        if server is None:
            return {"error": "Database is unavailable"}
        results = [
            {
                "ip": car.ip,
                "status": car.status,
            } for car in server]

        return {"ip": str(my_ip), "services": results}