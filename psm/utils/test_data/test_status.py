from internment_management.models import InternmentStatus

STATUS_LIST = [
    {
        "label": 'awaits_care_house',
        "name": 'Aguarda Aprovação Casa Saúde',
        "type": 'referral',
        "next_states": ['awaits_reviewer', 'awaits_opening', 'referral_rejected'],
        "prev_states": None
    },
    {
        "label": 'awaits_reviewer',
        "name": 'Aguarda Aprovação do Avaliador',
        "type": 'referral',
        "next_states": ['referral_approved', 'referral_rejected'],
        "prev_states": ['awaits_care_house']
    },
    {
        "label": 'referral_approved',
        "name": 'Aprovado',
        "type": 'referral',
        "next_states": None,
        "prev_states": ['awaits_reviewer']
    },
    {
        "label": 'referral_rejected',
        "name": 'Rejeitado',
        "type": 'referral',
        "next_states": None,
        "prev_states": ['awaits_care_house', 'awaits_reviewer', 'awaits_opening']
    },
    {
        "label": 'awaits_opening',
        "name": 'Aguarda Vaga',
        "type": 'referral',
        "next_states": ['referral_rejected', 'awaits_reviewer'],
        "prev_states": ['awaits_care_house', ]
    },
    {
        "label": 'interned',
        "name": 'Internado',
        "type": 'internment',
        "next_states": ['external_consultation', 'deceased', 'medical_discharge', 'transfer', 'non_medical_discharge'],
        "prev_states": ['awaits_admission', ]
    },
    {
        "label": 'awaits_admission',
        "name": 'Aguarda Entrada na Casa de Saúde',
        "type": 'internment',
        "next_states": ['interned'],
        "prev_states": None
    },
    {
        "label": 'external_consultation',
        "name": 'Consulta Externa',
        "type": 'internment',
        "next_states": ['interned', "deceased"],
        "prev_states": ['interned']
    },
    {
        "label": 'deceased',
        "name": 'Falecido',
        "type": 'internment',
        "next_states": None,
        "prev_states": ['interned', "external_consultation"]
    },
    {
        "label": 'medical_discharge',
        "name": 'Alta Médica',
        "type": 'internment',
        "next_states": None,
        "prev_states": ['interned',]
    },
    {
        "label": 'transfer',
        "name": 'Transferência',
        "type": 'internment',
        "next_states": None,
        "prev_states": ['interned']
    },
    {
        "label": 'non_medical_discharge',
        "name": 'Saída sem Alta Médica',
        "type": 'internment',
        "next_states": None,
        "prev_states": ['interned']
    },
]


def create_test_status():
    for state in STATUS_LIST:
        try:
            status = InternmentStatus.objects.get(label=state['label'])
            status.name = state['name']
            status.type = state['type']
            status.next_states = state['next_states']
            status.prev_states = state['prev_states']
        except InternmentStatus.DoesNotExist:
            status = InternmentStatus(
                label=state['label'],
                name=state['name'],
                type=state['type'],
                next_states=state['next_states'],
                prev_states=state['prev_states'],
            )
        status.save()
