from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy 
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:launchcode@localhost:8889/Blogz'
app.config['SQLALCHEMY_ECHO']= True
app.secret_key = "launchcode"
db = SQLAlchemy(app)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    entries = db.relationship('Entry', backref= 'owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password


class Entry(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(150))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, owner):
        self.name = name
        self.body = body
        self.owner = owner


@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    
    if request.method == 'POST':
       
        entry = request.form['entry']
        body = request.form['body']
        if len(entry) < 1 or len(body) < 1:
            entry = request.form['entry']
            owner = User.query.filter_by(email=session['email']).first()
            body = request.form['body']
            flash('Error entry and body must be at least 1 character long')
            return render_template('blog.html', title= "New Post!", entry=entry, body=body)
        else:
            owner = User.query.filter_by(email=session['email']).first()
            new_entry = Entry(entry,body,owner)
            db.session.add(new_entry)
            db.session.commit()
            return redirect(url_for('blog', id = [new_entry.id]))
            
            
              
    else:
     
            return render_template('blog.html',title='New Post!')

def input_length(input):
    if len(str(input)) > 2 and len(str(input)) < 120:
        return True
    else:
        return False

def password_check(password, verify):
    if str(password) == str(verify):
        return True
    else:
        return False

@app.route('/register', methods= ['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
         
           
            
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            
            flash('email already exists')
            if not input_length(email):
                flash('email lenght is invalid')

            if not input_length(password):
                flash('password length is invalid')

            if not input_length(verify):
                flash('password does not match')

            if not password_check(password, verify):
                flash('password does not match')

        if not existing_user:
            if not input_length(email):
                flash('email lenght is invalid')

            if not input_length(password):
                flash('password length is invalid')

            if not input_length(verify):
                flash('password does not match')

            if not password_check(password, verify):
                    flash('password does not match')

            else:
                new_user = User(email, password)
                db.session.add(new_user)
                db.session.commit()
                session['email'] = email

                return redirect('/blog')


    return render_template('signup.html')

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')


@app.route('/login', methods= ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['email'] = email
            return redirect ('/new_post')
        else:
            flash('wrong password or username ')
            return redirect('/login')
        
        
    
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/login')

@app.route('/')
def list_users():
    names = User.query.all()
    
    return render_template('index.html', posts= names)


@app.route('/blog', methods= ['POST', 'GET'])
def blog():
    
    userId = request.args.get('user')
    post_id = request.args.get('id')
    
    if userId == None and post_id == None:
        
        blogs = Entry.query.all()
        
        return render_template('posts.html', posts=blogs)


    elif userId != None:
        user = User.query.filter_by(email = userId).first()
        # posts = Entry.query.filter_by(owner_id=user.id)
        
        return render_template('individual_user_page.html', posts=user.entries)

   
            
    elif post_id != None:
        
        blog = Entry.query.filter_by(id = post_id).first()
            
            
        return render_template('individual_post.html', title = "blogs.entry", entry = blog.name, body= blog.body, blog=blog)

        

if __name__ == "__main__":
    app.run()