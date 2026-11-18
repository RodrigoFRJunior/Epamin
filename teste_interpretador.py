
from sistema.interpretador import interpretar_comando

testes = [
    "abre o league of legends",
    "quero jogar lol",
    "inicie o valorant",
    "vamos jogar rocket league",
    "abre meu whatsapp",
    "coloca o youtube",
    "abre a steam",
    "quero entrar no discord",
    "abre o visual studio code",
    "coloca o spotify",
    "vamos jogar fortnite",
    "abre o gta cinco",
    "quero jogar grand theft auto"
]

for frase in testes:

    resultado = interpretar_comando(frase)

    print(f"{frase:<40} -> {resultado}")
