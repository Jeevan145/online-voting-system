from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

VOTE_FILE = 'votes.csv'

# Create votes.csv if it doesn't exist
if not os.path.exists(VOTE_FILE):
    with open(VOTE_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'category', 'choice'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        choice = request.form['choice']

        # Check if already voted for this category
        with open(VOTE_FILE, 'r') as f:
            existing_votes = list(csv.reader(f))
            for row in existing_votes:
                if row[0] == name and row[1] == category:
                    return "❌ You already voted in this category!"

        # Save the vote
        with open(VOTE_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, category, choice])
        return redirect('/results')

    return render_template('vote.html')

@app.route('/results')
def results():
    results_data = {}
    with open(VOTE_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for _, category, choice in reader:
            if category not in results_data:
                results_data[category] = {}
            results_data[category][choice] = results_data[category].get(choice, 0) + 1

    return render_template('results.html', results=results_data)

if __name__ == '__main__':
    app.run(debug=True)
