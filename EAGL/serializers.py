from rest_framework import serializers
from .models import VillagerDetail,GoatDetails,InsuranceClaim,Vaccine

class VillagerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VillagerDetail
        fields = '__all__'


class GoatDetailsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.get_username")
    class Meta:
        model = GoatDetails
        fields = [
            "id",
            "user",
            "goat_gender",
            "tag_number",
            "policy_number",
            "is_alive",
            "goat_hand_over_date"
        ]


class InsuranceClaimSerializer(serializers.ModelSerializer):
    goat = serializers.CharField()
    class Meta:
        model = InsuranceClaim
        fields = [
            "id",
            "goat",
            "death_place",
            "death_date",
            "death_time",
            "toll_free_no",
            "intimation",
            "panchnama_doc",
            "police_doc",
            "sarpanch_doc",
            "pm_doc",
            "submission_claim_date",
            "submitted_person",
            "claim_number",
            "claim_settlement_date",
            "neft_intimation_date",
            "goat_replacement_date",
            "replaced_tag_number",
            "claim_status"
        ]
