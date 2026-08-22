import re

from .models import ParticipanteTreinamento


def parse_participant_lines(text):
    participants = []
    for raw_line in text.splitlines():
        line = re.sub(r'\s+', ' ', raw_line).strip(' -;\t')
        if not line:
            continue

        parts = [part.strip() for part in re.split(r'[;|,]\s*', line) if part.strip()]
        name = parts[0] if parts else line
        if len(name.split()) < 2:
            continue

        participants.append(
            {
                'nome': name[:160],
                'matricula': parts[1][:60] if len(parts) > 1 else '',
                'turno': parts[2][:80] if len(parts) > 2 else '',
                'area': parts[3][:120] if len(parts) > 3 else '',
                'empresa': parts[4][:140] if len(parts) > 4 else '',
            }
        )

    return participants


def sync_participants(treinamento):
    treinamento.participantes.all().delete()
    participants = parse_participant_lines(treinamento.texto_participantes)

    for participant in participants:
        ParticipanteTreinamento.objects.create(
            treinamento=treinamento,
            nome=participant['nome'],
            matricula=participant['matricula'],
            empresa=participant['empresa'] or treinamento.empresa,
            turno=participant['turno'],
            area=participant['area'] or treinamento.area,
        )

    treinamento.total_participantes = len(participants)
    if participants and treinamento.status == treinamento.Status.AGENDADO:
        treinamento.status = treinamento.Status.REALIZADO
    treinamento.save(update_fields=['total_participantes', 'status', 'atualizado_em'])
    return participants
