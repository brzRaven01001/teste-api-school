import requests
import unittest

class AlunosTestCase(unittest.TestCase):

    def test_000_alunos_retorna_lista(self):
        r = requests.get('http://127.0.0.1:5000/alunos/listar')
        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /alunos no seu server")
        try:
            obj_retornado = r.json()
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))
        for aluno in obj_retornado:
            print(f"Aluno ID: {aluno['id']}, Nome: {aluno['nome']}, idade: {aluno['idade']}, ,data_nascimento: {aluno['data_nascimento']},nota_primeiro_semestre: {aluno['nota_primeiro_semestre']},nota_segundo_semestre: {aluno['nota_segundo_semestre']},media_final: {aluno['media_final']}")

    def test_001_adiciona_alunos(self):

        r_1 = requests.post('http://127.0.0.1:5000/alunos/criar', json={'id': 3, 'nome': 'João', 'idade': 18, 'data_nascimento': '20/02/2007',"nota_primeiro_semestre": 9,"nota_segundo_semestre": None,"media_final": None})
        r_2 = requests.post('http://127.0.0.1:5000/alunos/criar', json={'id': 5, 'nome': 'Catia', 'idade': 28, 'data_nascimento': '12/08/1996',"nota_primeiro_semestre": 10,"nota_segundo_semestre": None,"media_final": None})
        
        print(f"Status Code: {r_1.status_code}")
        print(f"Status Code: {r_2.status_code}")
        self.assertEqual(r_1.status_code, 201, "Erro ao criar aluno")
        self.assertEqual(r_2.status_code, 201, "Erro ao criar aluno")
        
        r_lista = requests.get('http://127.0.0.1:5000/alunos/listar')
        
        print(f"Status Code Listar alunos: {r_lista.status_code}")
        self.assertEqual(r_lista.status_code, 200, "Erro ao listar alunos")

        lista_retornada = r_lista.json()
        print(f"Lista de alunos atualizada: {lista_retornada}")
        
        achei_João = False
        achei_Catia = False
        for aluno in lista_retornada:
            if aluno['nome'] == 'João':
                achei_João = True
            if aluno['nome'] == 'Catia':
                achei_Catia = True

        if not achei_João:
            self.fail('aluno "João" não apareceu na lista de alunos')
        if not achei_Catia:
            self.fail('aluno "Catia" não apareceu na lista de alunos')
        if achei_João and achei_Catia:
            print("Ambas as alunos foram encontradas com sucesso na lista!")

    def test_002_aluno_por_id(self):
        r = requests.post('http://127.0.0.1:5000/alunos/criar', json={'id': 4, 'nome': 'Rosa', 'idade': 21, 'data_nascimento': '01/11/1999 ',"nota_primeiro_semestre": 6.5,"nota_segundo_semestre": 6,"media_final": None})
    
        print("Resposta da criação da aluno:", r.status_code, r.text)
        self.assertEqual(r.status_code, 201, "Erro ao criar aluno")

        resposta = requests.get('http://127.0.0.1:5000/alunos/filtrar/4')
        dict_retornado = resposta.json()
    
        print("Resposta da consulta da aluno:", resposta.status_code, dict_retornado)

        self.assertEqual(type(dict_retornado), dict, "Resposta não é um dicionário")
        self.assertIn('nome', dict_retornado, "A chave 'nome' não foi encontrada na resposta")
        self.assertEqual(dict_retornado['nome'], 'Rosa', f"Esperado 'Rosa', mas obtido: {dict_retornado['nome']}")



    def test_003_reseta(self):
        r = requests.post('http://127.0.0.1:5000/alunos/criar', json={'id': 5, 'nome': 'Raimundo', 'idade': 62, 'data_nascimento': '20/12/1996 ',"nota_primeiro_semestre": 6.5,"nota_segundo_semestre": 6,"media_final": None})
        
        print("Resposta da criação da aluno:", r.status_code, r.text)
        self.assertEqual(r.status_code, 201, "Erro ao criar aluno")

        r_lista = requests.get('http://127.0.0.1:5000/alunos/listar')
        print("Lista de alunos antes do reset:", r_lista.status_code, r_lista.json())
        self.assertTrue(len(r_lista.json()) > 0)

        r_reset = requests.post('http://127.0.0.1:5000/alunos/reseta')
        print("Resposta do reset de alunos:", r_reset.status_code, r_reset.text)

        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://127.0.0.1:5000/alunos/listar')
        print("Lista de alunos após o reset:", r_lista_depois.status_code, r_lista_depois.json())
        
        self.assertEqual(len(r_lista_depois.json()),0)

    def test_004_deleta(self):
        r_reset = requests.post('http://127.0.0.1:5000/alunos/reseta')
        print("Resposta do reset de alunos:", r_reset.status_code, r_reset.text)
        self.assertEqual(r_reset.status_code,200)

        r_1 = requests.post('http://127.0.0.1:5000/alunos/criar', json={'id': 1, 'nome': 'Catia', 'idade': 28, 'data_nascimento': '12/08/1996',"nota_primeiro_semestre": 10,"nota_segundo_semestre": None,"media_final": None})
        r_2 = requests.post('http://127.0.0.1:5000/alunos/criar', json={'id': 2, 'nome': 'Rosa', 'idade': 21, 'data_nascimento': '01/11/1999 ',"nota_primeiro_semestre": 6.5,"nota_segundo_semestre": 6,"media_final": None})
        r_3 = requests.post('http://127.0.0.1:5000/alunos/criar', json={'id': 3, 'nome': 'Raimundo', 'idade': 62, 'data_nascimento': '20/12/1996 ',"nota_primeiro_semestre": 6.5,"nota_segundo_semestre": 6,"media_final": None})
        
        print("Criação da aluno:", r_1.status_code, r_1.text)
        print("Criação da aluno:", r_2.status_code, r_2.text)
        print("Criação da aluno:", r_3.status_code, r_3.text)


        r_lista = requests.get('http://127.0.0.1:5000/alunos/listar')
        lista_retornada = r_lista.json()
        print("Lista de alunos após criação:", r_lista.status_code, lista_retornada)
        self.assertEqual(len(lista_retornada),3)
        
        r_delete_2 = requests.delete('http://127.0.0.1:5000/alunos/2')
        print("aluno:", r_delete_2.status_code, r_delete_2.text)

        r_lista2 = requests.get('http://127.0.0.1:5000/alunos/listar')
        lista_retornada2 = r_lista2.json()
        print("Lista de alunos após deleção da aluno 2:", r_lista2.status_code, lista_retornada2)
        self.assertEqual(len(lista_retornada2),2) 

        acheiCatia = False
        acheRaimundo = False
        for aluno in lista_retornada:
            if aluno['nome'] == 'Catia':
                acheiCatia=True
            if aluno['nome'] == 'Raimundo':
                acheRaimundo=True
        if not acheiCatia or not acheRaimundo:
            self.fail("voce parece ter deletado o aluno errado!")

        requests.delete('http://127.0.0.1:5000/alunos/3')

        r_delete_3 = r_lista3 = requests.get('http://127.0.0.1:5000/alunos/listar')
        print("Resposta da deleção da aluno Banco de Dados:", r_delete_3.status_code, r_delete_3.text)
        lista_retornada3 = r_lista3.json()
        print("Lista de alunos após deleção da aluno 3:", r_lista3.status_code, lista_retornada3)
        self.assertEqual(len(lista_retornada3),1) 

        if lista_retornada3[0]['nome'] == 'Catia':
            pass
        else:
            self.fail("voce parece ter deletado o aluno errado!")
    
    def test_005_edita(self):
        r_reset = requests.post('http://127.0.0.1:5000/alunos/reseta')
        print("Resposta do reset de alunos:", r_reset.status_code, r_reset.text)
        self.assertEqual(r_reset.status_code,200)

        r_criar =requests.post('http://127.0.0.1:5000/alunos/criar', json={'id': 3, 'nome': 'Raimundo', 'idade': 62, 'data_nascimento': '20/12/1996 ',"nota_primeiro_semestre": 6.5,"nota_segundo_semestre": 6,"media_final": None})
        print("Resposta da criação da aluno:", r_criar.status_code, r_criar.text)

        r_antes = requests.get('http://127.0.0.1:5000/alunos/filtrar/1')
        print("Resposta antes da edição:", r_antes.status_code, r_antes.json())
        self.assertEqual(r_antes.json()['nome'],'Raimundo')

        r_editar = requests.put('http://127.0.0.1:5000/alunos/atualizar/1', json={'nome':'Jasmine'})
        print("Resposta da edição da aluno:", r_editar.status_code, r_editar.text)

        r_depois = requests.get('http://127.0.0.1:5000/alunos/filtrar/1')
        print("Resposta depois da edição:", r_depois.status_code, r_depois.json())

        self.assertEqual(r_depois.json()['nome'],'Jasmine')
        self.assertEqual(r_depois.json()['id'],1)


    def test_006b_id_inexistente_no_get(self):

        r_reset = requests.post('http://127.0.0.1:5000/alunos/reseta')
        print("Resposta do reset de alunos:", r_reset.status_code, r_reset.text)

        self.assertEqual(r_reset.status_code,200)

        r = requests.get('http://127.0.0.1:5000/alunos/filtrar/15')
        print("Resposta da requisição GET para ID inexistente:", r.status_code, r.text)
        self.assertIn(r.status_code,[400,404])

        error_retornado = r.json().get('error', '')
        print("Resposta JSON do erro:", error_retornado)
        self.assertEqual(r.json()['error'],'Aluno não encontrado')
     
    def test_006c_id_inexistente_no_delete(self):
     
        r_reset = requests.post('http://127.0.0.1:5000/alunos/reseta')
        print("Resposta do reset de alunos:", r_reset.status_code, r_reset.text)
        self.assertEqual(r_reset.status_code,200)

        r = requests.delete('http://127.0.0.1:5000/alunos/15')
        print("Resposta da requisição DELETE para ID inexistente:", r.status_code, r.text)
        self.assertIn(r.status_code,[400,404])

        error_retornado = r.json().get('error', '')
        print("Resposta JSON do erro:", error_retornado)
        self.assertEqual(error_retornado, 'Aluno não encontrado.')
    
    def test_007_criar_com_id_ja_existente(self):

        r_reset = requests.post('http://127.0.0.1:5000/alunos/reseta')
        print("Resposta do reset de alunos:", r_reset.status_code, r_reset.text)
        self.assertEqual(r_reset.status_code, 200, "Erro ao resetar as alunos")

        r_1 = requests.post('http://127.0.0.1:5000/alunos/criar', json={'id': 1, 'nome': 'Raimundo', 'idade': 62, 'data_nascimento': '20/12/1996 ',"nota_primeiro_semestre": 6.5,"nota_segundo_semestre": 6,"media_final": None})
        print("Resposta da criação da aluno 'Raimundo':", r_1.status_code, r_1.text)
        self.assertEqual(r_1.status_code, 201, "Erro ao criar a aluno 'Raimundo'")

        r_2 = requests.post('http://127.0.0.1:5000/alunos/criar', json={'id': 1, 'nome': 'Rosa', 'idade': 21, 'data_nascimento': '01/11/1999 ',"nota_primeiro_semestre": 6.5,"nota_segundo_semestre": 6,"media_final": None})
        print("Resposta ao tentar criar aluno com ID já existente:", r_2.status_code, r_2.text)

        self.assertEqual(r_2.status_code, 400, "O código de status não foi 400.")
        error_retornado = r_2.json().get('error', '')
        print("Resposta JSON do erro:", error_retornado)
        self.assertEqual(error_retornado, 'ID já utilizado')

    def test_008a_post_sem_nome(self):
        r_reset = requests.post('http://127.0.0.1:5000/alunos/reseta')
        print("Resposta do reset de aluno:", r_reset.status_code, r_reset.text)
        self.assertEqual(r_reset.status_code, 200, "Erro ao resetar as aluno")

        r = requests.post('http://127.0.0.1:5000/alunos/criar', json={'id': 1})
        print("Resposta ao tentar criar aluno sem nome:", r.status_code, r.text)

        self.assertEqual(r.status_code, 400, "O código de status não foi 400.")
        error_retornado = r.json().get('error', '')
        print("Resposta JSON do erro:", error_retornado)
        self.assertEqual(error_retornado, 'Nome e idade são obrigatórios.')

    def test_008b_put_sem_nome(self):
        r_reset = requests.post('http://127.0.0.1:5000/alunos/reseta')
        print(f"Resposta do reset de alunos: {r_reset.status_code} {r_reset.json()}")
        self.assertEqual(r_reset.status_code,200)

        r = requests.post('http://127.0.0.1:5000/alunos/criar',json={'id': 1,'nome':'Raimundo', 'idade': 21})
        print(f"Resposta ao criar alunos: {r.status_code} {r.json()}")
        self.assertEqual(r.status_code,201)

        r = requests.put('http://127.0.0.1:5000/alunos/atualizar/1',json={'id':1})
        print(f"Resposta ao editar alunos sem nome: {r.status_code} {r.json()}")
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['error'],'alunos sem nome')
        
        
def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(AlunosTestCase)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()
