from app import db, login_manager
from app import app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
@login_manager.request_loader
def load_user_from_request(request):

    auth_str = request.headers.get('Authorization')
    token = auth_str.split(' ')[1] if auth_str else ''
    if token:
        user_id = User.decode_token(token)
        user = User.query.get(int(user_id))
        if user:
            return user
    return None

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(25),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    info = db.relationship('Information',backref='author',lazy=True)

    def get_reset_token(self,expires_sec=300):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id': self.user_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"User('{self.user_id}','{self.username}','{self.email}')"

class Information(db.Model):
    info_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)
    email = db.Column(db.String(120),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow) 
    link = db.Column(db.String(150),nullable=False)
    current_price = db.Column(db.Integer,nullable=False)
    target_price = db.Column(db.Integer,nullable=False)
    new_price = db.Column(db.Integer,nullable=False)
    status = db.Column(db.String(10),nullable=False)
    

    def __repr__(self):
        return f"User('{self.user_id}','{self.info_id}','{self.email}','{self.date_posted}','{self.link}','{self.current_price}','{self.status}')"
