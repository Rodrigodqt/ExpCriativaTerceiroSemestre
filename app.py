from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return "Adicionar aqui o Template do dashboard"

@app.route('/patiants')
def patiants():
    return "Adicionar aqui o Template da listagem de pacientes"

@app.route('/patiant/create', methods=['POST'])
def create_patiant():
    return "Adicionar aqui o Template da criação de um novo registro de paciente"

@app.route('/patiant/<uuid>/edit', methods=['GET', 'POST'])
def edit_patiant(uuid):
    #Não tenho certeza se vai precisar dessa parte mas ja deixei a rota setada.
    return "Adicionar aqui o Template da tela de edição do paciente"

#Acesso do administrador do sistema
@app.route('/doctors')
def doctors():
    return "Adicionar aqui o Template da listagem de médicos vinculados ao sistema atualmente"

@app.route('/doctor/profile', methods=['GET','POST'])
def doctor_profile():
    return "Adicione aqui o Template de edição do perfil pessoal do médico" # Não sei o tanto de informações que seria importante ele poder editar sobre si mesmo mas pelo menos a opção de mudar a senha deve ser possivel.





if __name__== "__main__":
    app.run(debug=True,host='0.0.0.0')