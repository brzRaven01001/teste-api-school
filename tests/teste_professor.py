import unittest
import requests

class ProfessoresTestCase(unittest.TestCase):

    def setUp(self):
        requests.post('http://127.0.0.1:5000/professor/reseta')

    def test_000_professores_retorna_lista(self):
        r = requests.get('http://127.0.0.1:5000/professor/listar')
        self.assertNotEqual(r.status_code, 404, "Você não definiu a página /professor no seu server")
        try:
            obj_retornado = r.json()
        except:
            self.fail("Esperado um JSON como resposta")

        self.assertIn("professores", obj_retornado)
        self.assertIsInstance(obj_retornado["professores"], list)

    def test_001_adiciona_professores(self):
        r_marcos = requests.post('http://127.0.0.1:5000/professor/criar', json={
            'id': 2, 'nome': 'Marcos Paulo', 'idade': 44, 'data_nascimento': "01/07/1984",
            'disciplina': 'Linguagem de Programação', 'salario': 3750.00
        })
        r_joao = requests.post('http://127.0.0.1:5000/professor/criar', json={
            'id': 3, 'nome': 'João Silva', 'idade': 25, 'data_nascimento': '01/01/2000',
            'disciplina': 'Banco de Dados', 'salario': 4000.00
        })

        self.assertEqual(r_marcos.status_code, 201)
        self.assertEqual(r_joao.status_code, 201)

        r_lista = requests.get('http://127.0.0.1:5000/professor/listar')
        self.assertEqual(r_lista.status_code, 200)

        lista_retornada = r_lista.json()["professores"]
        nomes = [prof['nome'] for prof in lista_retornada]
        self.assertIn('Marcos Paulo', nomes)
        self.assertIn('João Silva', nomes)

    def test_002_professor_por_id(self):
        r = requests.post('http://127.0.0.1:5000/professor/criar', json={
            'id': 4, 'nome': 'Sérgio Perez', 'idade': 50, 'data_nascimento': '12/03/1980',
            'disciplina': 'Linguagem SQL', 'salario': 2500.00
        })
        self.assertEqual(r.status_code, 201)

        resposta = requests.get('http://127.0.0.1:5000/professor/filtrar/4')
        self.assertEqual(resposta.status_code, 200)
        data = resposta.json()
        self.assertEqual(data['nome'], 'Sérgio Perez')

    def test_003_reseta(self):
        requests.post('http://127.0.0.1:5000/professor/criar', json={
            'id': 1, 'nome': 'Pedro Santos', 'idade': 65, 'data_nascimento': '23/05/1960',
            'disciplina': 'Soft Skills', 'salario': 3000.00
        })
        r_lista = requests.get('http://127.0.0.1:5000/professor/listar')
        self.assertGreater(len(r_lista.json()["professores"]), 0)

        r_reset = requests.post('http://127.0.0.1:5000/professor/reseta')
        self.assertEqual(r_reset.status_code, 200)

        r_lista_depois = requests.get('http://127.0.0.1:5000/professor/listar')
        self.assertEqual(len(r_lista_depois.json()["professores"]), 0)

    def test_004_deleta(self):
        requests.post('http://127.0.0.1:5000/professor/criar', json={
            'id': 1, 'nome': 'Marcos Paulo', 'idade': 44, 'data_nascimento': "01/07/1984",
            'disciplina': 'Linguagem de Programação', 'salario': 3750.00
        })
        requests.post('http://127.0.0.1:5000/professor/criar', json={
            'id': 2, 'nome': 'João Silva', 'idade': 25, 'data_nascimento': '01/01/2000',
            'disciplina': 'Banco de Dados', 'salario': 4000.00
        })
        requests.post('http://127.0.0.1:5000/professor/criar', json={
            'id': 3, 'nome': 'Gisele', 'idade': 43, 'data_nascimento': '06/05/1978',
            'disciplina': 'Full-Stack', 'salario': 4000.00
        })

        r_delete_2 = requests.delete('http://127.0.0.1:5000/professor/2')
        self.assertEqual(r_delete_2.status_code, 200)

        r_lista = requests.get('http://127.0.0.1:5000/professor/listar').json()["professores"]
        nomes = [prof['nome'] for prof in r_lista]
        self.assertIn('Marcos Paulo', nomes)
        self.assertIn('Gisele', nomes)
        self.assertNotIn('João Silva', nomes)

    def test_005_edita(self):
        requests.post('http://127.0.0.1:5000/professor/criar', json={
            'id': 1, 'nome': 'Luis Araujo', 'idade': 56, 'data_nascimento': '03/04/1980',
            'disciplina': 'Logica de Programação', 'salario': 4000.00
        })

        r_editar = requests.put('http://127.0.0.1:5000/professor/atualizar/1', json={'nome': 'Jorge'})
        self.assertEqual(r_editar.status_code, 200)

        r_depois = requests.get('http://127.0.0.1:5000/professor/filtrar/1')
        self.assertEqual(r_depois.json()['nome'], 'Jorge')

    def test_006_id_inexistente(self):
        r = requests.get('http://127.0.0.1:5000/professor/filtrar/999')
        self.assertIn(r.status_code, [400, 404])
        self.assertEqual(r.json().get('error'), 'Professor não encontrado')

        r = requests.delete('http://127.0.0.1:5000/professor/999')
        self.assertIn(r.status_code, [400, 404])
        self.assertEqual(r.json().get('error'), 'Professor não encontrado.')

    def test_007_criar_com_id_ja_existente(self):
        requests.post('http://127.0.0.1:5000/professor/criar', json={"id": 1, "nome": "Junior Santos", "idade": 34, "data_nascimento": "13/04/1980", "disciplina": "Desenvolvimento mobile", "salario": 7000.00})
        r_duplicado = requests.post('http://127.0.0.1:5000/professor/criar', json={"id": 1, "nome": "Carlos Miranda", "idade": 37, "data_nascimento": "05/04/1980", "disciplina": "Banco de Dados", "salario": 7000.00})
        self.assertEqual(r_duplicado.status_code, 400)
        self.assertEqual(r_duplicado.json().get('error'), 'ID já utilizado.')

    def test_008_validacoes_de_nome(self):
        r = requests.post('http://127.0.0.1:5000/professor/criar', json={'id': 1})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json().get('error'), 'Nome é obrigatório.')

        requests.post('http://127.0.0.1:5000/professor/criar', json={"nome": "Minimus"})
        r_editar = requests.put('http://127.0.0.1:5000/professor/atualizar/1', json={})
        self.assertEqual(r_editar.status_code, 400)
        self.assertEqual(r_editar.json().get('error'), 'Professor sem nome')


def runTests():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ProfessoresTestCase)
    unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)

if __name__ == '__main__':
    runTests()
