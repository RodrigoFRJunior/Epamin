
from teste_voz import ouvir

print("\n===== PRIMEIRA CAPTURA =====")
primeira = ouvir()
print(f"Primeiro resultado: {primeira!r}")

input("\nPressione ENTER para iniciar a segunda captura...")

print("\n===== SEGUNDA CAPTURA =====")
segunda = ouvir()
print(f"Segundo resultado: {segunda!r}")
