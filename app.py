def registrar_abastecimento():
    abastecimento =  list()     
    valor_abastecido = float(input("Digite o valor abastecido: "))
    data_abastecimento = input("Digite a data do abastecimento (dd/mm/yyyy): ")
    obs = input("Digite a observação (ou pressione Enter para continuar): ")
    abastecimento.append((valor_abastecido, data_abastecimento, obs))
    return abastecimento