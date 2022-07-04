from datetime import datetime

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


class Setting(ModelMixin, db.Model):
    key = db.Column(db.Text, nullable=False)
    value = db.Column(db.Text, nullable=False)

    @classmethod
    def by_key(cls, key):
        return cls.get_by(first=True, key=key).value


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


class Devotee(ModelMixin, CreatedMixin, db.Model):
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text)


class Donation(ModelMixin, CreatedMixin, db.Model):
    devotee_id = db.Column(db.Integer, db.ForeignKey('devotee.id'))
    devotee = db.relationship('Devotee', backref=db.backref('donations', lazy=True))
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.Text, nullable=False)
    aadhaar = db.Column(db.Text)
    pan = db.Column(db.Text)
    recurring_interval = db.Column(db.Text)
    number = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    payment_id = db.Column(db.Text, nullable=False)


class Pooja(ModelMixin, MediaMixin, db.Model):
    temple = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    specific = db.Column(db.Boolean, default=False, nullable=False)
    dates = db.Column(Json, default=[])
    description = db.Column(db.Text)
    link = db.Column(db.Text)

    def bookable_dates(self):
        now = datetime.now()
        return [date for date in self.dates if (datetime.fromtimestamp(round(date/1000)) - now).total_seconds() > 129600]  # 36 hours

    UPLOADS_PATH = 'poojas'


class Booking(ModelMixin, CreatedMixin, db.Model):
    devotee_id = db.Column(db.Integer, db.ForeignKey('devotee.id'))
    devotee = db.relationship('Devotee', backref=db.backref('bookings', lazy=True))
    temple = db.Column(db.Text, nullable=False)
    pooja = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    gotra = db.Column(db.Text)
    nakshatra = db.Column(db.Text)
    days = db.Column(Json, nullable=False)
    payment_id = db.Column(db.Text, nullable=False)


@jwt.user_lookup_loader
def user_lookup_callback(_, payload):
    return User.get_by(first=True, uid=payload["sub"])


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(_, payload):
    return r.get(payload['jti']) is not None
