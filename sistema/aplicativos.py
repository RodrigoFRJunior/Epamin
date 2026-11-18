
import os
import subprocess
import webbrowser
from pathlib import Path


# ==========================================
# CONFIGURAÇÕES
# ==========================================

APLICATIVOS = {

    "league_of_legends": {
        "tipo": "riot",
        "produto": "league_of_legends"
    },

    "valorant": {
        "tipo": "riot",
        "produto": "valorant"
    },

    "rocket_league": {
        "tipo": "steam",
        "id": "252950"
    },

    "whatsapp": {
        "tipo": "windows",
        "id": "5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"
    },

    "youtube": {
        "tipo": "site",
        "url": "https://www.youtube.com"
    },

    "steam": {
        "tipo": "steam_app"
    },

    "discord": {
        "tipo": "windows",
        "id": "com.squirrel.Discord.Discord"
    },

    "vscode": {
        "tipo": "windows",
        "id": "Microsoft.VisualStudioCode"
    },

    "spotify": {
        "tipo": "executavel",
        "caminho": Path(
            os.environ["APPDATA"]
        ) / "Spotify" / "Spotify.exe"
    },

    "fortnite": {
        "tipo": "epic",
        "produto": "Fortnite"
    },

    "gta_v": {
        "tipo": "epic",
        "produto": "8769e24080ea413b8ebca3f1b8c50951"
    }
}


# ==========================================
# CAMINHOS DOS LAUNCHERS
# ==========================================

RIOT_CLIENT = Path(
    r"C:\Riot Games\Riot Client\RiotClientServices.exe"
)


# ==========================================
# INICIALIZAÇÃO DE APLICATIVOS
# ==========================================

def abrir_windows(app_id):

    destino = f"shell:AppsFolder\\{app_id}"

    subprocess.Popen(
        ["explorer.exe", destino],
        shell=False
    )


def abrir_executavel(caminho):

    caminho = Path(caminho)

    if not caminho.exists():
        raise FileNotFoundError(
            f"Executável não encontrado: {caminho}"
        )

    subprocess.Popen([str(caminho)])


def abrir_riot(produto):

    if not RIOT_CLIENT.exists():
        raise FileNotFoundError(
            "Riot Client não encontrado."
        )

    subprocess.Popen([
        str(RIOT_CLIENT),
        "--launch-product=" + produto,
        "--launch-patchline=live"
    ])


def abrir_steam_jogo(id_jogo):

    os.startfile(
        f"steam://rungameid/{id_jogo}"
    )


def abrir_steam():

    os.startfile("steam://open/main")


def abrir_epic(produto):

    endereco = (
        f"com.epicgames.launcher://apps/"
        f"{produto}?action=launch&silent=true"
    )

    os.startfile(endereco)


# ==========================================
# EXECUTOR PRINCIPAL
# ==========================================

def abrir_aplicativo(nome):

    aplicativo = APLICATIVOS.get(nome)

    if aplicativo is None:
        print(f"Aplicativo desconhecido: {nome}")
        return False

    tipo = aplicativo["tipo"]

    try:

        if tipo == "windows":

            abrir_windows(aplicativo["id"])

        elif tipo == "executavel":

            abrir_executavel(
                aplicativo["caminho"]
            )

        elif tipo == "riot":

            abrir_riot(
                aplicativo["produto"]
            )

        elif tipo == "steam":

            abrir_steam_jogo(
                aplicativo["id"]
            )

        elif tipo == "steam_app":

            abrir_steam()

        elif tipo == "epic":

            abrir_epic(
                aplicativo["produto"]
            )

        elif tipo == "site":

            webbrowser.open(
                aplicativo["url"]
            )

        print(f"Iniciando {nome}...")
        return True

    except Exception as erro:

        print(f"Erro ao abrir {nome}: {erro}")
        return False
