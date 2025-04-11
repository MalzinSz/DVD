from enum import Enum
from datetime import datetime

class Genero(Enum):
    COMEDIA = "Comédia"
    ROMANCE = "Romance"
    AVENTURA = "Aventura"
    ACAO = "Ação"
    TERROR = "Terror"
    DRAMA = "Drama"
    FICCAO_CIENTIFICA = "Ficção Científica"
    DOCUMENTARIO = "Documentário"

class Amigo:
    def __init__(self, id, nome, telefone, email):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email

    def __repr__(self):
        return f"Amigo({self.id}, {self.nome})"

class DVD:
    def __init__(self, id, titulo, sinopse, diretor, ator_principal, genero, faixa_etaria):
        self.id = id
        self.titulo = titulo
        self.sinopse = sinopse
        self.diretor = diretor
        self.ator_principal = ator_principal
        self.genero = genero
        self.faixa_etaria = faixa_etaria

    def __repr__(self):
        return f"DVD({self.id}, {self.titulo})"

class Emprestimo:
    def __init__(self, id, data_emprestimo, amigo, dvd):
        self.id = id
        self.data_emprestimo = data_emprestimo
        self.data_devolucao = None
        self.amigo = amigo
        self.dvd = dvd

    def __repr__(self):
        return f"Emprestimo({self.id}, {self.amigo.nome}, {self.dvd.titulo})"

class AmigoRepository:
    def __init__(self):
        self.amigos = []
        self.next_id = 1

    def salvar(self, amigo):
        self.amigos.append(amigo)

    def criar(self, nome, telefone, email):
        amigo = Amigo(self.next_id, nome, telefone, email)
        self.next_id += 1
        self.salvar(amigo)
        return amigo

    def listar(self):
        return self.amigos

    def buscar_por_id(self, id):
        for amigo in self.amigos:
            if amigo.id == id:
                return amigo
        return None

class DVDRepository:
    def __init__(self):
        self.dvds = []
        self.next_id = 1

    def salvar(self, dvd):
        self.dvds.append(dvd)

    def criar(self, titulo, sinopse, diretor, ator_principal, genero, faixa_etaria):
        dvd = DVD(self.next_id, titulo, sinopse, diretor, ator_principal, genero, faixa_etaria)
        self.next_id += 1
        self.salvar(dvd)
        return dvd

    def listar(self):
        return self.dvds

    def buscar_por_id(self, id):
        for dvd in self.dvds:
            if dvd.id == id:
                return dvd
        return None

class EmprestimoRepository:
    def __init__(self):
        self.emprestimos = []
        self.next_id = 1

    def salvar(self, emprestimo):
        self.emprestimos.append(emprestimo)

    def criar(self, amigo, dvd):
        emprestimo = Emprestimo(self.next_id, datetime.now(), amigo, dvd)
        self.next_id += 1
        self.salvar(emprestimo)
        return emprestimo

    def listar(self):
        return self.emprestimos

    def listar_ativos(self):
        return [e for e in self.emprestimos if e.data_devolucao is None]

    def devolver(self, id):
        for emprestimo in self.emprestimos:
            if emprestimo.id == id:
                emprestimo.data_devolucao = datetime.now()
                return emprestimo
        return None

    def esta_disponivel(self, dvd_id):
        for e in self.emprestimos:
            if e.dvd.id == dvd_id and e.data_devolucao is None:
                return False
        return True

class AmigoService:
    def __init__(self, repo):
        self.repo = repo

    def cadastrar(self, nome, telefone, email):
        return self.repo.criar(nome, telefone, email)

    def listar(self):
        return self.repo.listar()

    def buscar_por_id(self, id):
        return self.repo.buscar_por_id(id)

class DVDService:
    def __init__(self, repo):
        self.repo = repo

    def cadastrar(self, titulo, sinopse, diretor, ator_principal, genero, faixa_etaria):
        return self.repo.criar(titulo, sinopse, diretor, ator_principal, genero, faixa_etaria)

    def listar(self):
        return self.repo.listar()

    def buscar_por_id(self, id):
        return self.repo.buscar_por_id(id)

class EmprestimoService:
    def __init__(self, repo, amigo_repo, dvd_repo):
        self.repo = repo
        self.amigo_repo = amigo_repo
        self.dvd_repo = dvd_repo

    def emprestar(self, amigo_id, dvd_id):
        amigo = self.amigo_repo.buscar_por_id(amigo_id)
        dvd = self.dvd_repo.buscar_por_id(dvd_id)
        if not amigo or not dvd:
            raise Exception("Amigo ou DVD não encontrado")
        if not self.repo.esta_disponivel(dvd_id):
            raise Exception("DVD indisponível")
        return self.repo.criar(amigo, dvd)

    def devolver(self, emprestimo_id):
        return self.repo.devolver(emprestimo_id)

    def listar_ativos(self):
        return self.repo.listar_ativos()

# Exemplo de uso
if __name__ == "__main__":
    amigos_repo = AmigoRepository()
    dvds_repo = DVDRepository()
    emprestimos_repo = EmprestimoRepository()

    amigo_service = AmigoService(amigos_repo)
    dvd_service = DVDService(dvds_repo)
    emprestimo_service = EmprestimoService(emprestimos_repo, amigos_repo, dvds_repo)

    amigo = amigo_service.cadastrar("João", "123456789", "joao@email.com")
    dvd = dvd_service.cadastrar("Matrix", "Ficção", "Wachowski", "Keanu Reeves", Genero.FICCAO_CIENTIFICA, 14)
    emprestimo = emprestimo_service.emprestar(amigo.id, dvd.id)

    print("Empréstimo realizado:")
    print(emprestimo)

    print("\nEmpréstimos ativos:")
    print(emprestimo_service.listar_ativos())

    emprestimo_service.devolver(emprestimo.id)

    print("\nApós devolução:")
    print(emprestimo_service.listar_ativos())