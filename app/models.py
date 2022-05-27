from app.services import db, jwt, r, ModelMixin, CreatedMixin, DeletedMixin, PasswordMixin


class Role(ModelMixin, db.Model):
    name = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship('User', backref=db.backref('role', lazy=True))


class User(ModelMixin, CreatedMixin, DeletedMixin, PasswordMixin, db.Model):
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), default=2)
    email = db.Column(db.Text, unique=True, nullable=False)

    @classmethod
    def by_role(cls, role):
        return cls.filter([cls.role.has(name=role)])


@jwt.user_lookup_loader
def user_lookup_callback(_, payload):
    return User.get_by(first=True, uid=payload["sub"])


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(_, payload):
    return r.get(payload['jti']) is not None
