from rest_framework import generics
from django.db import connection
from app.serializers.Vz_List_serializers import VetzoneGoodsSerializer

class VetzoneGoodsListAPIView(generics.ListAPIView):
    serializer_class = VetzoneGoodsSerializer

    def get_queryset(self):
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT
                   v.name AS "VetZone Name",
                   h.hq_name AS "HQ",
                   v.mobile_number AS "Mobile Number",
                   vg.sim_number AS "SIM Number",
                   vg.opening_goods AS "Opening Goods",
                   vg.machine AS "Machine",
                   vg.furniture AS "Furniture",
                   vg.furniture_file AS "Furniture File",
                   vg.machine_file AS "Machine File"                 
                FROM
                   vetzone v
                JOIN
                    vetzone_goods vg ON v.vetzone_id = vg.vetzone_id
                JOIN
                    vetzone_hq_div vhd ON v.vetzone_id = vhd.vetzone_id
                JOIN
                    headquarters h ON vhd.hq_id = h.hq_id;
            ''')
            result = cursor.fetchall()
        
        # Convert the result to a list of dictionaries for serialization, adding Sr. No.
        queryset = []
        for idx, row in enumerate(result, start=1):  # Start index from 1
            queryset.append({
                'sr_no': idx,
                'vetzone_name': row[0],
                'hq': row[1],
                'mobile_number': row[2],
                'sim_number': row[3],
                'opening_goods': row[4],
                'machine': row[5],
                'furniture': row[6],
                'furniture_file': row[7],
                'machine_file': row[8],
                'vetzone_agreement_copy': None 
            })
        
        return queryset
