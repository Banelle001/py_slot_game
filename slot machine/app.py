from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Define the fruits and their odds
fruits = {
    '🍏': 1.57,  # Apple
    '🍒': 1.10,  # Cherry
    '🍊': 1.80,  # Orange
    '🔔': 2,     # Bell
    '🍋': 2.2,   # Lemon
    '🍉': 20     # Watermelon
}

balance = 100.0  # Initial balance

@app.route('/')
def index():
    return render_template('index.html', balance=balance)

@app.route('/play', methods=['POST'])
def play():
    global balance
    try:
        bet = float(request.form['bet'])
        if bet <= 1:
            return jsonify({"error": "Bet start at R1."})
        if bet > balance:
            return jsonify({"error": "You cannot bet more than your balance."})

        # Spin the slot machine
        spin = random.choices(list(fruits.keys()), k=3)

        # Check if all 3 fruits are the same
        if spin[0] == spin[1] == spin[2]:
            win_fruit = spin[0]
            odds = fruits[win_fruit]
            winnings = bet * odds
            balance += winnings
            result_message = f"Congratulations! You matched 3 {win_fruit}s and won R{winnings:.2f}!"
        else:
            balance -= bet
            result_message = f"Sorry, you lost R{bet:.2f}. Better luck next time!"

        return jsonify({
            "spin": spin,
            "result": result_message,
            "balance": balance
        })

    except ValueError:
        return jsonify({"error": "Invalid bet amount."})

if __name__ == '__main__':
    app.run(debug=True)
