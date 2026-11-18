import subprocess
from teste_voz import ouvir
import webbrowser

def abrir_plano_aula():
    webbrowser.open("https://docs.google.com/spreadsheets/d/1Gru8fde-cISpkwAxOc_72EwHXjiO_X7LwdiREeOy4To/edit?gid=615737568#gid=615737568")
    print("Abrindo o plano de aula")

def abrir_calculadora():
    subprocess.Popen("calc.exe")
    print("Abrindo a calculadora!")

def abrir_paint():
    subprocess.Popen("mspaint.exe")
    print("Abrindo o Paint!")


def executar_comando(comando):
    match comando:
        case "abrir calculadora" | "calculadora":
            abrir_calculadora()

        case "abrir jorge" | "jorge":
            abrir_paint()
            
        case "aulas":
            abrir_plano_aula()

        case "sair" | "tchau" :
            print("Até logo!")
            return False
        case _:
            print("Ainda não conheço esse comando.")

    return True


FRASE_ATIVACAO = "epamin"
print(f"Olá! Eu sou o {FRASE_ATIVACAO}.")

while True:
  print("\nAguardando a frase de ativação...")
  
  frase = ouvir()
  
  if FRASE_ATIVACAO in frase:
      print("Assistente ativado! Diga seu comando.")
      
      comando = ouvir()
      continuar = executar_comando(comando)
      
      if not continuar:
          break
      
      print("Voltando ao modo de espera.")