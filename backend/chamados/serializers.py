from rest_framework import serializers

from .models import Chamado


class ChamadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamado

        fields = [
            "id",
            "titulo",
            "descricao",
            "status",
            "criado_em",
            "atualizado_em",
        ]

        extra_kwargs = {
            "titulo": {
                "required": True,
                "allow_blank": False,
                "error_messages": {
                    "required": "O campo título é obrigatório.",
                    "blank": "O campo título é obrigatório.",
                },
            },
        }

        read_only_fields = [
            "id",
            "criado_em",
            "atualizado_em",
        ]