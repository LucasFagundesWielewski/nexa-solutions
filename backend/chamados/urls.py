from django.urls import path

from .views import ChamadoDetailView, ChamadoIndicadoresView, ChamadoListCreateView

urlpatterns = [
    path(
        "chamados/",
        ChamadoListCreateView.as_view(),
        name="chamado-list-create",
    ),
    path(
        "chamados/<int:pk>/",
        ChamadoDetailView.as_view(),
        name="chamado-detail",
    ),
    path(
        "indicadores/",
        ChamadoIndicadoresView.as_view(),
        name="chamado-indicadores",
    ),
]