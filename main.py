
import subprocess


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

        case "abrir paint" | "paint":
            abrir_paint()

        case "sair":
            print("Até logo!")
            return False

        case _:
            print("Ainda não conheço esse comando.")

    return True


nome = input("Como você quer chamar seu assistente? ")
print(f"Olá! Eu sou o {nome}.")

while True:
    comando = input("O que você quer que eu faça? ").lower().strip()

    continuar = executar_comando(comando)

    if not continuar:
        break