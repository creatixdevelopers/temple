from app.services import db, jwt, r, ModelMixin, CreatedMixin, LastUpdatedMixin, DeletedMixin, PasswordMixin, MediaMixin, Json


class Role(ModelMixin, db.Model):
    name = db.Column(db.String(20), unique=True, nullable=False)
    users = db.relationship('User', backref=db.backref('role', lazy=True))


class User(ModelMixin, CreatedMixin, DeletedMixin, PasswordMixin, db.Model):
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), default=2)
    email = db.Column(db.Text, unique=True, nullable=False)

    @classmethod
    def by_role(cls, role):
        return cls.filter([cls.role.has(name=role)])


class Post(ModelMixin, CreatedMixin, LastUpdatedMixin, MediaMixin, DeletedMixin, db.Model):
    type = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

    UPLOADS_PATH = 'posts'


class Volunteer(ModelMixin, CreatedMixin, db.Model):
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    occupation = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text)
    identification = db.Column(db.Text)
    age = db.Column(db.Integer)
    address = db.Column(db.Text)
    city = db.Column(db.Text)
    pincode = db.Column(db.Integer)
    comments = db.Column(db.Text)


class Donation(ModelMixin, CreatedMixin, db.Model):
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text)
    identification = db.Column(db.Text)
    type = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    recurring = db.Column(db.Boolean, nullable=False, default=True)
    recurring_interval = db.Column(db.Text, nullable=False, default='monthly')


class Pooja(ModelMixin, db.Model):
    temple = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)


class Booking(ModelMixin, CreatedMixin, db.Model):
    temple = db.Column(db.Text, nullable=False)
    pooja = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text)
    gotra = db.Column(db.Text)
    nakshatra = db.Column(db.Text)


@jwt.user_lookup_loader
def user_lookup_callback(_, payload):
    return User.get_by(first=True, uid=payload["sub"])


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(_, payload):
    return r.get(payload['jti']) is not None
