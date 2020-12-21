def export():
    """작업자 통계 출력본 _320,324"""
    """
    ExportBackend(
        # price_per_hour_min= 1000,
        # price_per_hour_max= 100000,

        projects=Project.objects.filter(id__in=[320,324]),
        configuration={
            'statuses': ['confirmed', 'inspecting', 'inspected', 'confirmed'],
            'export_path': 'metrix_pet/1208/',
            'price_per_hour_min': 1000,
            'price_per_hour_max': 100000

        }
        ).do_export()
    """