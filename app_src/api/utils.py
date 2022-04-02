def update_object(instance, validated_data):
    instance.__class__.objects.filter(pk=instance.pk).update(**validated_data)
    return instance.__class__.objects.get(pk=instance.pk)
