from datetime import datetime, timedelta


def subtrair_intervalos(base_inicio, base_fim, ocupados):
    livres = [(base_inicio, base_fim)]

    for inicio, fim in ocupados:
        novos = []

        for l_inicio, l_fim in livres:
            if fim <= l_inicio or inicio >= l_fim:
                novos.append((l_inicio, l_fim))
            else:
                if inicio > l_inicio:
                    novos.append((l_inicio, inicio))
                if fim < l_fim:
                    novos.append((fim, l_fim))

        livres = novos

    return livres


def calcular_horarios_livres(jornada, agendamentos, bloqueios, data):

    ocupados = []

    for a in agendamentos:
        ini = a["data_hora"]
        fim = ini + timedelta(minutes=a["duracao_minutos"])
        ocupados.append((ini, fim))

    for b in bloqueios:
        ini = datetime.combine(data, b["hora_inicio"])
        fim = datetime.combine(data, b["hora_fim"])
        ocupados.append((ini, fim))

    ocupados.sort()

    livres_total = []

    for j in jornada:
        base_ini = datetime.combine(data, j["hora_inicio"])
        base_fim = datetime.combine(data, j["hora_fim"])

        livres = subtrair_intervalos(base_ini, base_fim, ocupados)
        livres_total.extend(livres)

    return livres_total
