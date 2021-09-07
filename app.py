#!usr/bin/python3   
import json,random,re
from flask import Flask,render_template,request,url_for
from werkzeug.utils import redirect

app = Flask(__name__)

@app.route('/')
def homepage():
    # Allow to modify global variables
    global lifes,inserted_letters,current_word,original_name,feedback
    # Opening JSON file
    with open('ufc.json') as filename :
        fighters = json.load(filename)['Fighters']
        filename.close()
    # Adding to a set to avoid repeated names
    set_of_names=set()
    for f in fighters:
        set_of_names.add(f['Name'])
    #Choosing a random ufc fighter name 
    original_name = random.choice(list(set_of_names)).upper()
    #Replacing the letters into _ 
    current_word=re.sub(r'\w','_',original_name)

    lifes=6
    inserted_letters=set()
    feedback='Good Luck'
    return render_template('home.html')


@app.route('/hangman', methods=['GET', 'POST'])
def game():
    # Allow to modify global variables
    global lifes,inserted_letters,current_word,original_name,feedback

    if request.method == 'GET':
        return render_template('hangman.html',current_word=current_word,inserted_letters=inserted_letters,lifes=lifes,feedback=feedback)
    else:
        letter=request.form['letter'].upper()
        
        if '_' in current_word and lifes>0:
            if (letter in original_name) and (letter not in inserted_letters):
                feedback=f'You guessed right, {letter} is on the word .'
                inserted_letters.add(letter)
                index_of_inserted_letter=[pos for pos, char in enumerate(original_name) if char == letter]

                for p in index_of_inserted_letter:
                    current_word = current_word[:p] + letter + current_word[p+1:]


            elif (letter in original_name and letter  in inserted_letters) or (letter not in original_name and letter  in inserted_letters) :
                feedback=f'You already inserted that letter {letter}, try another one'

            elif letter not in original_name :
                feedback=f"You guessed wrong, {letter} doesn't belong to the original word. Try another one !"
                inserted_letters.add(letter)
                lifes-=1

        if '_' not in current_word and lifes>0:
            return render_template('winner.html',feedback=f'Congrats you guessed right: {original_name}')


        if lifes==0:
            return render_template('loser.html',feedback=f'Unfortunately you lost, better luck next time.',guess=f'The right answer was : {original_name}')

        return render_template('hangman.html',current_word=current_word,inserted_letters=inserted_letters,lifes=lifes,feedback=feedback)


if __name__ == '__main__':
   app.run(host="0.0.0.0", port=8000)