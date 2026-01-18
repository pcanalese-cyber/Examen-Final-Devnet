vlan = int(input("Ingrese el número de VLAN: "))

if 1 <= vlan <= 1005:
    print("Resultado: VLAN en rango NORMAL (1-1005).")
elif 1006 <= vlan <= 4094:
    print("Resultado: VLAN en rango EXTENDIDO (1006-4094).")
else:
    print("Resultado: Valor inválido, no corresponde a una VLAN (1-4094).")
