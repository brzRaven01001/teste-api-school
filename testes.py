import unittest
from professores import professor_bp
import requests

class ProfessoresTestCase(unittest.TestCase):

    def test_000_professores_retorna_lista(self):
        r = requests.get('http://127.0.0.1:5000/professores/listar')
        if r.status_code == 404:
            self.fail("Você não definiu a página / professores no seu server")
        try:
            obj_retornado = r.json()
        except:
            self.fail("Queria um JSON mas você retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))
        for turma in obj_retornado:
            print(f"Professor ID: {turma['id']}, Nome: {professor_bp['nome']}, Idade: {professor_bp['idade']}, Data de Nasc: {turma['data_nascimento']}, Disciplina{professor_bp['disciplina']}, Salário{professor_bp['salario']}")

    def test_001_adiciona_professores(self):

        r_estevao = requests.post('http://127.0.0.1:5000/professores/criar', json={'id': 2, 'nome': 'Marcos Paulo', 'idade': 44, 'datanasc': "01/07/1984", 'disciplina': 'Linguagem de Programação', 'salario': 3750.00})
        r_joao = requests.post('http://127.0.0.1:5000/professores/criar', json={'id': 3, 'nome': 'João Silva', 'idade': 25, 'datanasc': '01/01/2000', 'disciplina': 'Banco de Dados', 'salario': 4000.00})
        
        print(f"Status Code Estevão Ferreira: {r_estevao.status_code}")
        print(f"Status Code Silva: {r_joao.status_code}")
        self.assertEqual(r_estevao.status_code, 201, "Erro ao criar professor Estevão Ferreira")
        self.assertEqual(r_joao.status_code, 201, "Erro ao criar professor João Silva")
        
        r_lista = requests.get('http://127.0.0.1:5000/professores/listar')
        
        print(f"Status Code Listar Professores: {r_lista.status_code}")
        self.assertEqual(r_lista.status_code, 200, "Erro ao listar professores")

        lista_retornada = r_lista.json()
        print(f"Lista de professores atualizada: {lista_retornada}")
        
        achei_estevao = False
        achei_joao = False
        for professor in lista_retornada:
            if professor['nome'] == 'Estevão Ferreira':
                achei_estevao = True
            if professor['nome'] == 'João Silva':
                achei_joao = True

        if not achei_estevao:
            self.fail('Professor "Estevão Ferreira" não apareceu na lista de professores')
        if not achei_joao:
            self.fail('Professor "João Silva" não apareceu na lista de turmas')
        if achei_estevao and achei_joao:
            print("Ambas os professores foram encontrados com sucesso na lista!")

    def test_002_professor_por_id(self):
        r = requests.post('http://127.0.0.1:5000/professores/criar', json={'id': 4, 'nome': 'Sérgio Perez', 'idade': 50, 'datanasc': '12/03/1980', 'disciplina': 'Linguagem SQL', 'salario': 2500.00})
    
        print("Resposta da criação de professores:", r.status_code, r.text)
        self.assertEqual(r.status_code, 201, "Erro ao criar professor")

        resposta = requests.get('http://127.0.0.1:5000/professores/filtrar/4')
        dict_retornado = resposta.json()
    
        print("Resposta da consulta do professor:", resposta.status_code, dict_retornado)

        self.assertEqual(type(dict_retornado), dict, "Resposta não é um dicionário")
        self.assertIn('nome', dict_retornado, "A chave 'nome' não foi encontrada na resposta")
        self.assertEqual(dict_retornado['nome'], 'Estevão Ferreira', f"Esperado 'Sistemas', mas obtido: {dict_retornado['nome']}")



    def test_003_reseta(self):
        r = requests.post('http://127.0.0.1:5000/professores/criar', json={'id': 5, 'nome': 'Pedro Santos', 'idade': 65, 'datanasc': '23/05/1960', 'disciplina': 'Soft Skills', 'salario': 3000.00})
        
        print("Resposta da criação de professor:", r.status_code, r.text)
        self.assertEqual(r.status_code, 201, "Erro ao criar professor")

        r_lista = requests.get('http://127.0.0.1:5000/professores/listar')
        print("Lista de professores antes do reset:", r_lista.status_code, r_lista.json())
        self.assertTrue(len(r_lista.json()) > 0)

        r_reset = requests.post('http://127.0.0.1:5000/professores/reseta')
        print("Resposta do reset de professores:", r_reset.status_code, r_reset.text)

        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://127.0.0.1:5000/professores/listar')
        print("Lista de professores após o reset:", r_lista_depois.status_code, r_lista_depois.json())
        
        self.assertEqual(len(r_lista_depois.json()),0)

    def test_004_deleta(self):
        r_reset = requests.post('http://127.0.0.1:5000/professores/reseta')
        print("Resposta do reset de professores:", r_reset.status_code, r_reset.text)
        self.assertEqual(r_reset.status_code,200)

        r_1 = requests.post('http://127.0.0.1:5000/professores/criar', json={'id': 2, 'nome': 'Marcos Paulo', 'idade': 44, 'datanasc': "01/07/1984", 'disciplina': 'Linguagem de Programação', 'salario': 3750.00})
        r_2 = requests.post('http://127.0.0.1:5000/professores/criar', json={'id': 3, 'nome': 'João Silva', 'idade': 25, 'datanasc': '01/01/2000', 'disciplina': 'Banco de Dados', 'salario': 4000.00})

        print("Criação do professor Marcos Paulo:", r_1.status_code, r_1.text)
        print("Criação do professor João Silva:", r_2.status_code, r_2.text)


        r_lista = requests.get('http://127.0.0.1:5000/professores/listar')
        lista_retornada = r_lista.json()
        print("Lista de professores após criação:", r_lista.status_code, lista_retornada)
        self.assertEqual(len(lista_retornada),3)
        
        r_delete_2 = requests.delete('http://127.0.0.1:5000/professoress/2')
        print("Professor Marcos Paulo:", r_delete_2.status_code, r_delete_2.text)

        r_lista2 = requests.get('http://127.0.0.1:5000/professores/listar')
        lista_retornada2 = r_lista2.json()
        print("Lista de professores após deleção do professor 2:", r_lista2.status_code, lista_retornada2)
        self.assertEqual(len(lista_retornada2),2) 

        acheiMarcos = False
        acheiJoao = False
        for professor in lista_retornada:
            if professor['nome'] == 'Marcos Paulo':
                acheiMarcos=True
            if professor['nome'] == 'João Silva':
                acheiJoao=True
        if not acheiMarcos or not acheiJoao:
            self.fail("voce parece ter deletado o professor errado!")

        requests.delete('http://127.0.0.1:5000/professores/3')

        r_delete_3 = r_lista3 = requests.get('http://127.0.0.1:5000/professores/listar')
        print("Resposta da deleção do professor Marcos Paulo:", r_delete_3.status_code, r_delete_3.text)
        lista_retornada3 = r_lista3.json()
        print("Lista de turmas após deleção do professor 3:", r_lista3.status_code, lista_retornada3)
        self.assertEqual(len(lista_retornada3),1) 

        if lista_retornada3[0]['nome'] == 'João Silva':
            pass
        else:
            self.fail("Você parece ter deletado o professor errado")
    
    def test_005_edita(self):
        r_reset = requests.post('http://127.0.0.1:5000/professores/reseta')
        print("Resposta do reset de professores:", r_reset.status_code, r_reset.text)
        self.assertEqual(r_reset.status_code,200)

        r_criar =requests.post('http://127.0.0.1:5000/professores/criar', json={'id': 1, 'nome': 'Analise', 'turno': 'Vespertino', 'ativo': True})
        print("Resposta da criação  'Analise':", r_criar.status_code, r_criar.text)

        r_antes = requests.get('http://127.0.0.1:5000/turmas/filtrar/1')
        print("Resposta antes da edição:", r_antes.status_code, r_antes.json())
        self.assertEqual(r_antes.json()['nome'],'Analise')

        r_editar = requests.put('http://127.0.0.1:5000/turmas/atualizar/1', json={'nome':'Full-Stack'})
        print("Resposta da edição da turma:", r_editar.status_code, r_editar.text)

        r_depois = requests.get('http://127.0.0.1:5000/turmas/filtrar/1')
        print("Resposta depois da edição:", r_depois.status_code, r_depois.json())

        self.assertEqual(r_depois.json()['nome'],'Full-Stack')
        self.assertEqual(r_depois.json()['id'],1)


    def test_006b_id_inexistente_no_get(self):

        r_reset = requests.post('http://127.0.0.1:5000/turmas/reseta')
        print("Resposta do reset de turmas:", r_reset.status_code, r_reset.text)

        self.assertEqual(r_reset.status_code,200)

        r = requests.get('http://127.0.0.1:5000/turmas/filtrar/15')
        print("Resposta da requisição GET para ID inexistente:", r.status_code, r.text)
        self.assertIn(r.status_code,[400,404])

        error_retornado = r.json().get('error', '')
        print("Resposta JSON do erro:", error_retornado)
        self.assertEqual(r.json()['error'],'turma nao encontrada')
     
    def test_006c_id_inexistente_no_delete(self):
     
        r_reset = requests.post('http://127.0.0.1:5000/turmas/reseta')
        print("Resposta do reset de turmas:", r_reset.status_code, r_reset.text)
        self.assertEqual(r_reset.status_code,200)

        r = requests.delete('http://127.0.0.1:5000/turmas/15')
        print("Resposta da requisição DELETE para ID inexistente:", r.status_code, r.text)
        self.assertIn(r.status_code,[400,404])

        error_retornado = r.json().get('error', '')
        print("Resposta JSON do erro:", error_retornado)
        self.assertEqual(error_retornado, 'Turma não encontrada')
    
    def test_007_criar_com_id_ja_existente(self):

        r_reset = requests.post('http://127.0.0.1:5000/turmas/reseta')
        print("Resposta do reset de turmas:", r_reset.status_code, r_reset.text)
        self.assertEqual(r_reset.status_code, 200, "Erro ao resetar as turmas")

        r_1 = requests.post('http://127.0.0.1:5000/turmas/criar', json={'id': 1, 'nome': 'Analise', 'turno': 'Vespertino', 'ativo': True})
        print("Resposta da criação da turma 'Analise':", r_1.status_code, r_1.text)
        self.assertEqual(r_1.status_code, 200, "Erro ao criar a turma 'Analise'")

        r_2 = requests.post('http://127.0.0.1:5000/turmas/criar', json={'id': 1, 'nome': 'Desenvolvimento Web', 'turno': 'Vespertino', 'ativo': True})
        print("Resposta ao tentar criar turma com ID já existente:", r_2.status_code, r_2.text)

        self.assertEqual(r_2.status_code, 400, "O código de status não foi 400.")
        error_retornado = r_2.json().get('error', '')
        print("Resposta JSON do erro:", error_retornado)
        self.assertEqual(error_retornado, 'ID já utilizado')



        
        
        
def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TurmasTestCase)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()


#  python testes.py