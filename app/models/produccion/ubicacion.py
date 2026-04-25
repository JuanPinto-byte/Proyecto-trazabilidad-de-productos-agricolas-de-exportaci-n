from app.extensions import db


class Departamento(db.Model):
    __tablename__ = 'departamentos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)

    municipios = db.relationship('Municipio', backref='departamento', lazy=True)

    def __repr__(self):
        return f'<Departamento {self.nombre}>'


class Municipio(db.Model):
    __tablename__ = 'municipios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    departamento_id = db.Column(db.Integer, db.ForeignKey('departamentos.id'), nullable=False)

    def __repr__(self):
        return f'<Municipio {self.nombre}>'
