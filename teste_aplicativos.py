
from sistema.aplicativos import abrir_aplicativo

aplicativos = [
    "whatsapp",
    "youtube",
    "steam",
    "discord",
    "vscode",
    "spotify",
    "fortnite",
    "gta_v",
    "league_of_legends",
    "valorant",
    "rocket_league"
]

for nome in aplicativos:
    print(f"\nTestando: {nome}")
    abrir_aplicativo(nome)
