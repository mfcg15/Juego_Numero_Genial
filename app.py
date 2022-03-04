from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'claveSecreta'

@app.route('/')
def index():
    numero = random.randint(1, 100)
    session.pop("numero")
    session.pop("TotalIntentos")
    session.pop("contador")
    session["numero"] = numero
    session["TotalIntentos"] = 5
    session["contador"] = 0
    print(session["numero"])
    return render_template("index.html", cantIntentos = session["TotalIntentos"])

@app.route('/guess',methods=['POST'])
def guess():
    num_buscar =  int(session["numero"])
    num_ingresado = int(request.form['num_ingresado'])

    if 'TotalIntentos' in session:
        session["contador"] += 1
        session["TotalIntentos"] -= 1

    if(int(session["TotalIntentos"]==0)):
        return render_template("endIntentos.html")
    else:
        if(num_buscar == num_ingresado):
            return redirect("/YouWin")
        elif (num_ingresado>num_buscar):
            return render_template("low.html", cantIntentos = session["TotalIntentos"])
        else:
            return render_template("high.html", cantIntentos = session["TotalIntentos"])

@app.route('/YouWin')
def NewWinner():
    return render_template("winner.html",numero=session["numero"],intentos=session["contador"])

@app.route('/winners',methods=['POST'])
def winner():
    User = []
    auxUser  = []
    if 'winner' in session:
        for i in session["winner"]:
            auxUser.append(i)
        newWinner = {'user': request.form['txt_winner'], 'oportunidades':session["contador"]}
        auxUser.append(newWinner)
        session["winner"] = auxUser
    else:
        newWinner = {'user': request.form['txt_winner'], 'oportunidades':session["contador"]}
        User.append(newWinner)
        session["winner"] = User
    return render_template("winners.html",students = session["winner"])

if __name__=="__main__":
    app.run(debug=True)