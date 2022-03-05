from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True, nullable=False)
    name=db.Column(db.String(100), nullable=False )
    username=db.Column(db.String(100), unique=True, nullable=False)
    email=db.Column(db.String(100), unique=True, nullable=False)
    password=db.Column(db.String(100), nullable=False)
    created_date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts= db.relationship('Post', backref='owner', lazy=True)

    def __init__(self, name, username, email, password):
        self.name= name
        self.username = username
        self.email=email
        self.password = password
    
    def __repr__(self):
        return f"<User({self.id}, {self.username}, {self.password}, {self.posts}> "
    
    @classmethod
    def insert(self, name, username, email, password):

        user = User(name=name, username=username, email=email, password=password)

        db.session.add(user)
        db.session.commit()
    
    @classmethod
    def update(self, id, name, username, email, password):

        query = self.query.filter_by(id=id).first()

        query.name = name
        query.username = username
        query.email=email
        query.password = password

        db.session.commit()

    @classmethod
    def getUser(self, id):

        query = self.query.filter_by(id=id).first()
        return query
    
    @classmethod
    def getByUsername(self, username):

        query = self.query.filter_by(username=username).first()
        return query
    
    @classmethod
    def getByEmail(self, email):

        query = self.query.filter_by(email=email).first()
        return query
    
    @classmethod
    def getUserPosts(self, username):

        query = self.query.filter_by(username=username).first()
        posts = query.posts

        return posts
    

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True, nullable=False)
    title=db.Column(db.String(100), nullable=False )
    description=db.Column(db.Text, nullable=False)
    created_date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, description, user_id):
        self.title= title
        self.description = description
        self.user_id=user_id
    
    def __repr__(self):
        return f"<User({self.id}, {self.title}, {self.description}, {self.user_id}> "

    @classmethod
    def insert(self, title, description, user_id):
        
        post=Post(title=title, description=description, user_id=user_id)

        db.session.add(post)
        db.session.commit()
    
    @classmethod
    def update(self, id, title, description):

        post= self.query.get(id)

        post.title=title
        post.description=description

        db.session.commit() 

    @classmethod
    def delete(self,id):

        post=self.query.get(id)
        db.session.delete(post)
        db.session.commit()

    @classmethod
    def get(self,id):

        post=self.query.get(id)
        return post
