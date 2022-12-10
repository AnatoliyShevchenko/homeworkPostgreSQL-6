from flask import (Flask, render_template, request, redirect)
from services import Connecting


app = Flask(__name__)
conn: Connecting = Connecting()

conn.connect_db()
conn.create_tables()

@app.route('/')
def main():
    return('<h1>TEST</h1>')

@app.route('/set-genres', methods=['GET', 'POST'])
def add_genre():
    message = ''
    data = conn.get_genres()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if title and description:
            message = 'Genre was added'
            conn.set_genres(title, description)
            return render_template('set-genres.html', data=data, message=message)
        message = 'Fields must be not empty'
        return render_template('set-genres.html', data=data, message=message)
    
    return render_template('set-genres.html', data=data)

@app.route('/add-game', methods=['GET', 'POST'])
def add_game():
    genre_data = conn.get_genres()
    games_data = conn.get_games()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        genre = request.form.get('genre')
        print(genre)
    return render_template('add-game.html', genre_data=genre_data)


if __name__ == '__main__':
    app.run(port=1234, debug=True)