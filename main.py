from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy 
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO']= True
app.secret_key = "launchcode"
db = SQLAlchemy(app)


class Entry(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(150))

    def __init__(self, name, body):
        self.name = name
        self.body = body


@app.route('/new_post', methods=['POST', 'GET'])
def new_post():
    
    if request.method == 'POST':
       
        entry = request.form['entry']
        body = request.form['body']
        if len(entry) < 1 or len(body) < 1:
            entry = request.form['entry']
            body = request.form['body']
            flash('Error entry and body must be at least 1 character long')
            return render_template('blog.html', title= "New Post!", entry=entry, body=body)
        else:
            new_entry = Entry(entry,body)
            db.session.add(new_entry)
            db.session.commit()
            return redirect(url_for('blog', id = [new_entry.id]))
            
            
              
    else:
     
            return render_template('blog.html',title='New Post!')


@app.route('/blog', methods= ['POST', 'GET'])
def blog():
    blogs = Entry.query.all()
    post_id = request.args.get('id') 
    
    if post_id == None:
            
           
        return render_template('posts.html', title= "Blog Posts!", posts=blogs)
            
    else:
        blog = Entry.query.filter_by(id = post_id).first()
            
            
        return render_template('individual_post.html', title = "blogs.entry", entry = blog.name, body= blog.body)


if __name__ == "__main__":
    app.run()