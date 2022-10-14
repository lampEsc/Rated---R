
from flask import Flask, render_template, redirect, request, url_for, session, g
from flask_session import Session
from forms import LoginForm, RegistrationForm, RateAlbum, AddAlbum, SortMain, SortYear, Search
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db, close_db
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = "daytime-nighttime-moonlight-sunshine"
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# before, after request

@app.teardown_appcontext
def close_db_at_end_of_request(e=None):
    close_db(e)

@app.before_request
def load_logged_in_user():
    g.user = session.get('user_id', None)

#use @login_required after decorator 

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user'))
        return view(**kwargs)
    return wrapped_view

@app.route('/', methods=['GET', 'POST'])
@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    db = get_db()
    session['admin'] = False

    users = db.execute('''SELECT name FROM users;''').fetchall()

    return render_template('welcome.html', title='Welcome!', users=users)

#main page

@app.route('/main', methods=['GET', 'POST'])
def main():
    db = get_db()
    form= SortMain()
    yform= SortYear()
    sform= Search()
    session['admin'] = False
    caption = 'Albums in Database'
    session['page'] = 'main'

    if form.validate_on_submit and form.order.data != None:
        order = form.order.data.split(' ')
        albums = db.execute('''SELECT * FROM albums ORDER BY '''+order[0]+ ' ' +order[1]+';').fetchall()
    
    elif yform.validate_on_submit and yform.years.data != None:
        if len(yform.years.data) > 4:
            years = yform.years.data.split(' ')
            albums = db.execute('SELECT * FROM albums WHERE year BETWEEN '+years[0]+ ' AND ' +(years[1])+';').fetchall()
        elif yform.years.data == '1975':
            albums = db.execute('''SELECT * FROM albums WHERE year < 1975;''').fetchall()
        else:
            albums = db.execute('''SELECT * FROM albums WHERE year > 2000;''').fetchall()
    
    elif sform.validate_on_submit and sform.search.data != None:
        search = sform.search.data
        if "'" in search:
            search = search.replace("'", '')
        albums = db.execute('''SELECT * FROM albums WHERE name LIKE '%'''+search+'''%' OR band LIKE '%'''+search+'''%'; ''').fetchall()
    
    else:
        albums = db.execute('''SELECT * FROM albums;''').fetchall()

    return render_template('main.html', sform=sform, yform=yform, albums=albums, caption=caption, title='Rated-A / Main Page', form=form)

#page for tracklistings of albums

@app.route('/tracklist_redirect', methods=['GET', 'POST'])
def tracklist_redirect():
    session['name']=request.form['button']
    return redirect(url_for('tracklist'))

@app.route('/tracklist', methods=['GET', 'POST'])
def tracklist():
    db = get_db()
    form = RateAlbum()
    rating = None
    added=False
    session['admin'] = False
    session['page'] = 'tracklist'

    name = session['name']
    songs = db.execute('''SELECT * FROM albums WHERE name=?;''', (name,)).fetchone()
    caption = 'Album Track Listing'

    tracklist = songs['songs'].split(',')
    title = songs['name']
    identity = songs['id']
    year = int(songs['year'])

    if form.validate_on_submit():
        rating = form.rating.data

        if 'albums' in session:
            session['albums'][identity] = rating
            savedata()


    if 'albums' in session and rating == None and identity in session['albums']:
        rating = session['albums'][identity]
    
    if 'albums' in session:
        if identity in session['albums']:
            added=True

    return render_template('tracklist.html', year=year, songs=songs, caption=caption, tracklist=tracklist, title=title, form=form, rating=rating, added=added, identity=identity)

#user profile page

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    db = get_db()
    user = g.user
    session['admin'] = False


    if db.execute('''SELECT albums FROM userdata WHERE name = ?''', (g.user,)).fetchone() is not None and 'albums' not in session:
        loaddata()
    elif 'albums' not in session:
        session['albums'] = {}

    ratings = {}
    albumsindbtemp = db.execute('''SELECT id FROM albums;''').fetchall()
    albumsindb = []
    
    for albumid in albumsindbtemp:
        albumsindb.append(list(albumid)[0])

    for album in session['albums'].copy().items():
        if album[0] not in albumsindb:
            session['albums'].pop(album[0])
        else:
            ratings[album[0]] = album[1]

    albums=[]
    for album in session['albums']:        
        albums.append(db.execute('''SELECT * FROM albums WHERE id=?;''', (album,)).fetchone())
    
    if request.method == 'POST':
        name=request.form['button']
        session['name'] = name
        return redirect(url_for('tracklist', name=name))

    return render_template('profile.html',user=user, caption='Your Albums', albums=albums, ratings=ratings, title='User: ' + g.user)

#adding/removing albums

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    album= int(request.form['button'])
    page=session['page']
    if 'albums' not in session:
        session['albums'] = {}
    if album not in session['albums']:
        session['albums'][album] = 0
    savedata()
    return redirect(url_for(page))

@app.route('/remove', methods=['GET', 'POST'])
@login_required
def remove():
    album= int(request.form['button'])
    if album in session['albums']:
        session['albums'].pop(album)
    savedata()
    return redirect(url_for('profile'))

#users stuff

@app.route('/registration_login', methods=['GET', 'POST'])
def user():
    lform = LoginForm()
    rform = RegistrationForm()
    response=''
    session['admin'] = False

    if lform.validate_on_submit():
        user_id = lform.user_id.data
        password = lform.password1.data
        if user_id == 'lamp' and password == 'reallysafepassword_121212':
            session['admin'] = True
            return redirect(url_for('delete'))
        
        db = get_db()
        user = db.execute('''SELECT * FROM users
                            WHERE name = ?;''', (user_id,)).fetchone()

        if user is None:
            lform.user_id.errors.append('Please make sure your User ID is spelled correctly.')
        elif not check_password_hash(user['password'], password):
            lform.password1.errors.append('Incorrect password!')
        else:
            session.clear()
            session['user_id'] = user_id

            return redirect(url_for('profile'))

    if rform.validate_on_submit():
        user_id = rform.user_id.data
        password = rform.password1.data
        password2 = rform.password2.data
        db = get_db()

        if db.execute('''SELECT * FROM users
            WHERE name = ?;''', (user_id,)).fetchone() is not None:
            rform.user_id.errors.append('User id already taken!')
        else:
            db.execute('''INSERT INTO users (name, password)
                            VALUES (?, ?)''', (user_id, generate_password_hash(password)))
            db.commit()
            response='Registration Successful'

    return render_template('user.html', lform=lform, rform=rform, title='Rated-A / Login', response=response)

#logout

@app.route('/logout')
@login_required
def logout():
    savedata()
    session.clear()

    return redirect(url_for('main'))

def savedata():
    db = get_db()
    if db.execute('''SELECT name FROM userdata WHERE name = ? ''', (g.user,)).fetchone() is None:
        db.execute('''INSERT INTO userdata (name, albums) VALUES (?, ?)''', (g.user, str(session['albums'])))
        db.commit()
    else:
        db.execute("UPDATE userdata SET albums = ? WHERE name=?;", (str(session['albums']), g.user))
        db.commit()
    return

def loaddata():
    db = get_db()
    session['albums'] = {}
    albums = []

    albumtemp = db.execute('''SELECT albums FROM userdata WHERE name = ?''', (g.user,)).fetchone()
    for album in albumtemp:
        albums.append(album.strip('{ }'))

    if '' not in albums:
        for album in albums:
            album.strip("'")
            if ',' in album:
                album = album.split(',')
                for a in album:  
                    (album_id, rating) = a.split(': ')
                    album_id = album_id.strip()
                    session['albums'][int(album_id)] = int(rating)
            else:
                (album_id, rating) = album.split(': ')
                album_id = album_id.strip()
                session['albums'][int(album_id)] = int(rating)

#adding new album to database

@app.route('/newalbum', methods=['GET', 'POST'])
@login_required
def newalbum():
    form = AddAlbum()
    db = get_db()  
    album = []
    response = ''
    session['admin'] = False
    
    if form.validate_on_submit():
        name = form.name.data
        band = form.band.data
        year = form.year.data
        songs = form.songs.data
        check = []

        if db.execute('''SELECT name FROM albums WHERE name = ?;''', (name,)).fetchone() != None:
            check = list(db.execute('''SELECT name FROM albums WHERE name = ?;''', (name,)).fetchone())
        
        if name in check:
            response = 'Album already in database.'
            album = db.execute('''SELECT * FROM albums WHERE name = ?;''', (name,)).fetchone()
        else:
            db.execute('''INSERT INTO albums (name, year, band, songs) VALUES(?,?,?,?);''',(name, year, band, songs))
            db.commit()      
            album = db.execute('''SELECT * FROM albums WHERE name = ?;''', (name,)).fetchone()
     
    return render_template('newalbum.html', form=form, album=album, response=response, title='Rated A / Database Entry')

@app.route('/delete', methods=['GET','POST'])
def delete():
    db = get_db()
    albums = {}

    if session['admin'] == True:
        if request.method == 'POST':
            album = int(request.form['button'])
            db.execute('''DELETE FROM albums WHERE id = ?;''', (album,))
            db.commit()
            
        albums = db.execute('''SELECT * FROM albums;''').fetchall()
    else: 
        return redirect(url_for('main'))

    return render_template('removal.html', albums=albums)
    
@app.route('/otheruser', methods=['GET','POST'])
def otheruser():
    db = get_db()
    user = request.form['button']
    session['admin'] = False

    ratings = {}
    albums = []
    albumstemp2 = []
    
    albumstemp1 = db.execute('''SELECT albums FROM userdata WHERE name = ?;''', (user,)).fetchone()
    if albumstemp1 == None:
        albums = {}
    else:
        for album in albumstemp1:
            albumstemp2.append(album.strip('{ }'))

        albumsindbtemp = db.execute('''SELECT id FROM albums;''').fetchall()
        albumsindb = []
    
        for albumid in albumsindbtemp:
            albumsindb.append(list(albumid)[0])

        if '' not in albumstemp2:
            for album in albumstemp2:
                album.strip("'")
                if ',' in album:
                    album = album.split(',')
                    for a in album:  
                        (album_id, rating) = a.split(': ')
                        album_id = album_id.strip()
                        ratings[int(album_id)] = int(rating)
                else:
                    (album_id, rating) = album.split(': ')
                    album_id = album_id.strip()
                    ratings[int(album_id)] = int(rating)
            for key in ratings:
                if key in albumsindb:
                    albums.append(db.execute("SELECT * FROM albums WHERE id = ? ", (key, )).fetchone())
    
    return render_template('profile.html', albums=albums, caption=user, ratings=ratings, title='Rated A / ' + user, user=user)
