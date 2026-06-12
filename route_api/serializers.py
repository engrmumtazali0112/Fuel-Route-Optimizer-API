from rest_framework import serializers


class RouteRequestSerializer(serializers.Serializer):
    start = serializers.CharField(
        required=True,
        help_text="Starting location within the USA (e.g. 'New York, NY')"
    )
    finish = serializers.CharField(
        required=True,
        help_text="Destination within the USA (e.g. 'Los Angeles, CA')"
    )

    def validate_start(self, value):
        if not value.strip():
            raise serializers.ValidationError("Start location cannot be empty.")
        return value.strip()

    def validate_finish(self, value):
        if not value.strip():
            raise serializers.ValidationError("Finish location cannot be empty.")
        return value.strip()
