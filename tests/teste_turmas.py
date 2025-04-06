import requests
import unittest
from flask import Flask
from sqlalchemy import true
from models.turmas import turmas_bp

class TurmasTestCase(unittest.TestCase):

    def test_000_alunos_retorna_lista(self):
        r = requests.get('http://127.0.0.1:5000/turmas/listar')
        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /turmas no seu server")
        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))
        for turma in obj_retornado:
            print(f"Turma ID: {turma['id']}, Nome: {turma['nome']}, turno: {turma['turno']}, ativo: {turma['ativo']}")

    def test_001_adiciona_turmas(self):

        r_matematica = requests.post('http://127.0.0.1:5000/turmas/criar', json={'id': 2, 'nome': 'Matematica', 'turno': 'Matutino', 'ativo': True})
        r_desenvolvimento_web = requests.post('http://127.0.0.1:5000/turmas/criar', json={'id': 3, 'nome': 'Desenvolvimento Web', 'turno': 'Vespertino', 'ativo': False})
        
        print(f"Status Code Matematica: {r_matematica.status_code}")
        print(f"Status Code Desenvolvimento Web: {r_desenvolvimento_web.status_code}")
        self.assertEqual(r_matematica.status_code, 201, "Erro ao criar turma Matematica")
        self.assertEqual(r_desenvolvimento_web.status_code, 201, "Erro ao criar turma Desenvolvimento Web")
        
        r_lista = requests.get('http://127.0.0.1:5000/turmas/listar')
        
        print(f"Status Code Listar Turmas: {r_lista.status_code}")
        self.assertEqual(r_lista.status_code, 200, "Erro ao listar turmas")

        lista_retornada = r_lista.json()
        print(f"Lista de turmas atualizada: {lista_retornada}")
        
        achei_matematica = False
        achei_desenvolvimento = False
        for turma in lista_retornada:
            if turma['nome'] == 'Matematica':
                achei_matematica = True
            if turma['nome'] == 'Desenvolvimento Web':
                achei_desenvolvimento = True

        if not achei_matematica:
            self.fail('Turma "Matematica" não apareceu na lista de turmas')
        if not achei_desenvolvimento:
            self.fail('Turma "Desenvolvimento Web" não apareceu na lista de turmas')
        if achei_matematica and achei_desenvolvimento:
            print("Ambas as turmas foram encontradas com sucesso na lista!")

    def test_002_turma_por_id(self):
        r = requests.post('http://127.0.0.1:5000/turmas/criar', json={'id': 4, 'nome': 'Matematica', 'turno': 'Matutino', 'ativo': True})
    
        print("Resposta da criação da turma:", r.status_code, r.text)
        self.assertEqual(r.status_code, 201, "Erro ao criar turma")

        resposta = requests.get('http://127.0.0.1:5000/turmas/filtrar/4')
        dict_retornado = resposta.json()
    
        print("Resposta da consulta da turma:", resposta.status_code, dict_retornado)

        self.assertEqual(type(dict_retornado), dict, "Resposta não é um dicionário")
        self.assertIn('nome', dict_retornado, "A chave 'nome' não foi encontrada na resposta")
        self.assertEqual(dict_retornado['nome'], 'Matematica', f"Esperado 'Matematica', mas obtido: {dict_retornado['nome']}")



    def test_003_reseta(self):
        r = requests.post('http://127.0.0.1:5000/turmas/criar', json={'id': 5, 'nome': 'Desenvolvimento Web', 'turno': 'Vespertino', 'ativo': False})
        
        print("Resposta da criação da turma:", r.status_code, r.text)
        self.assertEqual(r.status_code, 201, "Erro ao criar turma")

        r_lista = requests.get('http://127.0.0.1:5000/turmas/listar')
        print("Lista de turmas antes do reset:", r_lista.status_code, r_lista.json())
        self.assertTrue(len(r_lista.json()) > 0)

        r_reset = requests.post('http://127.0.0.1:5000/turmas/reseta')
        print("Resposta do reset de turmas:", r_reset.status_code, r_reset.text)

        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://127.0.0.1:5000/turmas/listar')
        print("Lista de turmas após o reset:", r_lista_depois.status_code, r_lista_depois.json())
        
        self.assertEqual(len(r_lista_depois.json()),0)

    def test_004_deleta(self):
        r_reset = requests.post('http://127.0.0.1:5000/turmas/reseta')
        print("Resposta do reset de turmas:", r_reset.status_code, r_reset.text)
        self.assertEqual(r_reset.status_code,200)

        r_1 = requests.post('http://127.0.0.1:5000/turmas/criar', json={'id': 1, 'nome': 'Desenvolvimento Web', 'turno': 'Vespertino', 'ativo': True})
        r_2 = requests.post('http://127.0.0.1:5000/turmas/criar', json={'id': 2, 'nome': 'Matematica', 'turno': 'Matutino', 'ativo': False})
        r_3 = requests.post('http://127.0.0.1:5000/turmas/criar', json={'id': 3, 'nome': 'Banco de Dados', 'turno': 'Noturno', 'ativo': False})

        print("Criação da turma Desenvolvimento Web:", r_1.status_code, r_1.text)
        print("Criação da turma Matemática:", r_2.status_code, r_2.text)
        print("Criação da turma Banco de Dados:", r_3.status_code, r_3.text)


        r_lista = requests.get('http://127.0.0.1:5000/turmas/listar')
        lista_retornada = r_lista.json()
        print("Lista de turmas após criação:", r_lista.status_code, lista_retornada)
        self.assertEqual(len(lista_retornada),3)
        
        r_delete_2 = requests.delete('http://127.0.0.1:5000/turmas/2')
        print("Turma Matemática:", r_delete_2.status_code, r_delete_2.text)

        r_lista2 = requests.get('http://127.0.0.1:5000/turmas/listar')
        lista_retornada2 = r_lista2.json()
        print("Lista de turmas após deleção da turma 2:", r_lista2.status_code, lista_retornada2)
        self.assertEqual(len(lista_retornada2),2) 

        acheiDesenvolvimento = False
        acheiBanco = False
        for turma in lista_retornada:
            if turma['nome'] == 'Desenvolvimento Web':
                acheiDesenvolvimento=True
            if turma['nome'] == 'Banco de Dados':
                acheiBanco=True
        if not acheiDesenvolvimento or not acheiBanco:
            self.fail("voce parece ter deletado o aluno errado!")

        requests.delete('http://127.0.0.1:5000/turmas/3')

        r_delete_3 = r_lista3 = requests.get('http://127.0.0.1:5000/turmas/listar')
        print("Resposta da deleção da turma Banco de Dados:", r_delete_3.status_code, r_delete_3.text)
        lista_retornada3 = r_lista3.json()
        print("Lista de turmas após deleção da turma 3:", r_lista3.status_code, lista_retornada3)
        self.assertEqual(len(lista_retornada3),1) 

        if lista_retornada3[0]['nome'] == 'Desenvolvimento Web':
            pass
        else:
            self.fail("voce parece ter deletado o aluno errado!")
    
    def test_005_edita(self):
        r_reset = requests.post('http://127.0.0.1:5000/turmas/reseta')
        print("Resposta do reset de turmas:", r_reset.status_code, r_reset.text)
        self.assertEqual(r_reset.status_code,200)

        r_criar =requests.post('http://127.0.0.1:5000/turmas/criar', json={'id': 1, 'nome': 'Analise', 'turno': 'Vespertino', 'ativo': True})
        print("Resposta da criação da turma 'Analise':", r_criar.status_code, r_criar.text)

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
        self.assertEqual(r_1.status_code, 201, "Erro ao criar a turma 'Analise'")

        r_2 = requests.post('http://127.0.0.1:5000/turmas/criar', json={'id': 1, 'nome': 'Desenvolvimento Web', 'turno': 'Vespertino', 'ativo': True})
        print("Resposta ao tentar criar turma com ID já existente:", r_2.status_code, r_2.text)

        self.assertEqual(r_2.status_code, 400, "O código de status não foi 400.")
        error_retornado = r_2.json().get('error', '')
        print("Resposta JSON do erro:", error_retornado)
        self.assertEqual(error_retornado, 'ID já utilizado')

    def test_008a_post_sem_nome(self):
        r_reset = requests.post('http://127.0.0.1:5000/turma/reseta')
        print("Resposta do reset de turma:", r_reset.status_code, r_reset.text)
        self.assertEqual(r_reset.status_code, 200, "Erro ao resetar as turma")

        r = requests.post('http://127.0.0.1:5000/turmas/criar', json={'id': 1})
        print("Resposta ao tentar criar turma sem nome:", r.status_code, r.text)

        self.assertEqual(r.status_code, 400, "O código de status não foi 400.")
        error_retornado = r.json().get('error', '')
        print("Resposta JSON do erro:", error_retornado)
        self.assertEqual(error_retornado, 'Turma sem nome')

    def test_008b_put_sem_nome(self):
        r_reset = requests.post('http://127.0.0.1:5000/turmas/reseta')
        print(f"Resposta do reset de turmas: {r_reset.status_code} {r_reset.json()}")
        self.assertEqual(r_reset.status_code,200)

        r = requests.post('http://127.0.0.1:5000/turmas/criar',json={'nome':'Analise','id':1})
        print(f"Resposta ao criar turmas: {r.status_code} {r.json()}")
        self.assertEqual(r.status_code,200)

        r = requests.put('http://127.0.0.1:5000/turmas/atualizar/1',json={'id':1})
        print(f"Resposta ao editar turmas sem nome: {r.status_code} {r.json()}")
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'turmas sem nome')
        
        
def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TurmasTestCase)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()


#  python -m unittest tests/teste_turmas.py
