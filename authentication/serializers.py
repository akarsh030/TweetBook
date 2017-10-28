from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = (
            'id', 'email', 'username', 'phone', 'faculty','dp','is_faculty', 'date_created', 'date_modified',
            'firstname', 'lastname', 'password', 'confirm_password')
        read_only_fields = ('date_created', 'date_modified')

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.faculty=validated_data.get('faculty', instance.faculty)
        instance.phone = validated_data.get('phone', instance.phone)
        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)
        if password and password == confirm_password:
            instance.set_password(password)
        instance.save()
        return instance

    def validate(self, data):
        '''
        Ensure the passwords are the same
        '''
        if 'is_faculty' in data.keys():
            if data['is_faculty']==False:
                per=Account.objects.filter(faculty=data['faculty'])
                if len(per)==0:
                    raise serializers.ValidationError(
                        "The Join Code is wrong"
                    )
        if 'password' in data.keys():
            print "Here"
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError(
                    "The passwords have to be the same"
                )
        return data