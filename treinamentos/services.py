import re

from pypdf import PdfReader

from .models import ParticipanteTreinamento


def extract_text_from_document(document):
    if not document:
        return ''

    name = (document.name or '').lower()
    if not name.endswith('.pdf'):
        return ''

    try:
        document.open('rb')
        reader = PdfReader(document)
        text_parts = [page.extract_text() or '' for page in reader.pages]
        return '\n'.join(part.strip() for part in text_parts if part.strip())
    except Exception:
        return ''
    finally:
        try:
            document.close()
        except Exception:
            pass


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


def fill_participants_from_pdf(treinamento):
    if treinamento.texto_participantes.strip() or not treinamento.documento:
        return False

    extracted_text = extract_text_from_document(treinamento.documento)
    if not extracted_text.strip():
        return False

    treinamento.texto_participantes = extracted_text.strip()
    treinamento.save(update_fields=['texto_participantes', 'atualizado_em'])
    return True


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
