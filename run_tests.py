import subprocess
import sys
import os

def main():
    # Define o diretório raiz do projeto
    root_dir = os.path.dirname(os.path.abspath(__file__))
    tests_dir = os.path.join(root_dir, 'tests')
    env = os.environ.copy()
    env['PYTHONPATH'] = root_dir
    print('Executando testes automatizados...')
    result = subprocess.run([sys.executable, '-m', 'pytest', tests_dir], env=env)
    if result.returncode == 0:
        print('\nTodos os testes passaram com sucesso!')
    else:
        print('\nAlguns testes falharam. Veja o log acima.')
    sys.exit(result.returncode)

if __name__ == '__main__':
    main()
