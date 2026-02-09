from datetime import datetime, timedelta, time


def time_from_db(valor):
    """
    Converte TIME do MariaDB que pode vir como timedelta
    para datetime.time (padrão do Python)
    """
    if isinstance(valor, timedelta):
        total = int(valor.total_seconds())
        horas = total // 3600
        minutos = (total % 3600) // 60
        return time(horas, minutos)

    return valor


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
        hora_ini = time_from_db(b["hora_inicio"])
        hora_fim = time_from_db(b["hora_fim"])

        ini = datetime.combine(data, hora_ini)
        fim = datetime.combine(data, hora_fim)

        ocupados.append((ini, fim))

    ocupados.sort()

    livres_total = []

    for j in jornada:
        hora_ini = time_from_db(j["hora_inicio"])
        hora_fim = time_from_db(j["hora_fim"])

        base_ini = datetime.combine(data, hora_ini)
        base_fim = datetime.combine(data, hora_fim)

        livres = subtrair_intervalos(base_ini, base_fim, ocupados)
        livres_total.extend(livres)

    return livres_total
