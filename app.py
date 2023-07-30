from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace this with your actual secret key
socketio = SocketIO(app)

# List of page names
pages = ["Eisenhower Matrix", "Google Calendar", "Custom Pomodoro Timer", "Feedback Form"]

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/select_mood', methods=['POST'])
def select_mood():
    mood = request.form.get('mood')
    if mood not in ['bad', 'okay', 'great']:
        return "Invalid mood selection. Please go back and try again."
    return redirect(url_for('eisenhower_matrix', mood=mood))

@app.route('/eisenhower_matrix/<string:mood>')
def eisenhower_matrix(mood):
    return render_template('eisenhower_matrix.html', mood=mood)

@app.route('/google_calendar/<string:mood>')
def google_calendar(mood):
    return render_template('google_calendar.html', mood=mood)

@app.route('/custom_pomodoro_timer/<string:mood>')
def custom_pomodoro_timer(mood):
    return render_template('custom_pomodoro_timer.html', mood=mood)

@app.route('/feedback_form/<string:mood>', methods=['GET', 'POST'])
def feedback_form(mood):
    if request.method == 'POST':
        focus_rating = request.form.get('focus_rating')
        feel_rating = request.form.get('feel_rating')
        timeblock_rating = request.form.get('timeblock_rating')

        # Store the feedback data in your database or perform any necessary actions

        return redirect(url_for('index'))
    return render_template('feedback_form.html', mood=mood, pages=pages)

@app.route('/page/<int:page_num>/<string:mood>')
def page(page_num, mood):
    if 1 <= page_num <= len(pages):
        return render_template('page.html', page_name=pages[page_num - 1], mood=mood)
    else:
        return "Page not found!"

if __name__ == '__main__':
    socketio.run(app, debug=True)
