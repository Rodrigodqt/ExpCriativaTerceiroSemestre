CREATE DATABASE IF NOT EXISTS xfragil CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE xfragil;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    cpf VARCHAR(14),
    crm VARCHAR(20),
    especialidade VARCHAR(120),
    ativo TINYINT(1) NOT NULL DEFAULT 1,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    data_nascimento DATE,
    sexo VARCHAR(1),
    cpf VARCHAR(14),
    contato VARCHAR(120),
    historico_familiar TEXT,
    usuario_id INT,
    ativo TINYINT(1) NOT NULL DEFAULT 1,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pacientes_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS sintomas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(80),
    peso_masculino FLOAT,
    peso_feminino FLOAT,
    ativo TINYINT(1) NOT NULL DEFAULT 1,
    ordem INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS avaliacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT,
    usuario_id INT,
    data_avaliacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    score_total FLOAT,
    limiar_aplicado FLOAT,
    resultado VARCHAR(60),
    observacoes TEXT,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_avaliacoes_paciente FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE,
    CONSTRAINT fk_avaliacoes_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS itens_avaliacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    avaliacao_id INT NOT NULL,
    sintoma_id INT NOT NULL,
    presente TINYINT(1) NOT NULL DEFAULT 0,
    CONSTRAINT fk_itens_avaliacao FOREIGN KEY (avaliacao_id) REFERENCES avaliacoes (id) ON DELETE CASCADE,
    CONSTRAINT fk_itens_sintoma FOREIGN KEY (sintoma_id) REFERENCES sintomas (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO sintomas (nome, descricao, categoria, peso_masculino, peso_feminino, ativo, ordem) VALUES
('Atraso na fala', 'Atraso no desenvolvimento da linguagem e da fala', 'Neurodesenvolvimento', 0.14, 0.01, 1, 1),
('Dificuldades de aprendizagem', 'Dificuldade em adquirir novos conhecimentos e habilidades', 'Cognitivo', 0.18, 0.28, 1, 2),
('Deficit de atencao', 'Dificuldade em manter o foco e a concentracao', 'Comportamental', 0.17, 0.12, 1, 3),
('Deficiencia intelectual', 'Limitacoes no funcionamento intelectual e adaptativo', 'Cognitivo', 0.32, 0.20, 1, 4),
('Hiperatividade', 'Atividade motora excessiva e inquietacao', 'Comportamental', 0.12, 0.04, 1, 5),
('Agressividade', 'Comportamento agressivo com outras pessoas', 'Comportamental', 0.01, 0.02, 1, 6),
('Evita contato visual', 'Dificuldade em manter contato visual durante interacoes', 'Social', 0.06, 0.08, 1, 7),
('Evita contato fisico', 'Aversao ao toque e ao contato fisico', 'Social', 0.04, 0.07, 1, 8),
('Movimentos repetitivos (estereotipias)', 'Movimentos repetitivos como balancar as maos', 'Comportamental', 0.17, 0.05, 1, 9),
('Hipermobilidade articular', 'Amplitude de movimento das articulacoes acima do normal', 'Fisico', 0.19, 0.04, 1, 10),
('Macro-orquidismo', 'Aumento do volume testicular, sinal tipico em homens', 'Fisico', 0.26, NULL, 1, 11),
('Face alongada/orelhas protuberantes', 'Caracteristicas faciais tipicas da sindrome', 'Fisico', 0.29, 0.09, 1, 12);
