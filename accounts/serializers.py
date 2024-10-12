from accounts.models import DonorRegistrationModel,DonorProfile
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission
from events.models import DonationHistory


class DonorRegistrationSerializer(serializers.ModelSerializer):
    mobaile_no = serializers.CharField(max_length=12, required=True)
    age = serializers.IntegerField(required=True)
    address = serializers.CharField(required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','mobaile_no','address','age', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        age = self.validated_data['age']
        address = self.validated_data['address']
        mobaile_no = self.validated_data['mobaile_no']

        # Validate password confirmation
        if age<18:
            raise serializers.ValidationError("Age must be greater than 18 or equal.")
        
        if password != confirm_password:
            raise serializers.ValidationError({'error': "Passwords don't match"})
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email already exists"})
        
        # Create the User object
        user = User(username=username, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()
        DonorRegistrationModel.objects.create(
            user=user,
            age=age,
            mobaile_no=mobaile_no,
            address=address
        )
        # Create DonorProfile
        # Fetch the latest donation history for the user

        # Create the DonorProfile
        donor_profile = DonorProfile.objects.create(
            user=user,
            age=age,
            address=address,
            mobaile_no=mobaile_no,
        )
        donor_profile.save()
        
        return user



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)





class DonorProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', required=False, allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', required=False, allow_blank=True)
    email = serializers.EmailField(source='user.email', required=False, allow_blank=True)
    mobaile_no = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    blood_group = serializers.CharField(required=False, allow_blank=True)
    image = serializers.CharField(required=False, allow_blank=True)
    age = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = DonorProfile
        fields = [
            'id', 'user', 'first_name', 'username', 'last_name', 'email',
            'age', 'mobaile_no', 'address', 'image', 'blood_group',
            'is_available', 'health_screening_passed'
        ]
        extra_kwargs = {
            'user': {'read_only': True},
            'health_screening_passed': {'read_only': True},
            'is_available': {'read_only': True},
        }

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        # ইউজার ফিল্ডগুলো আপডেট করুন যদি ডেটা দেওয়া থাকে
        if 'first_name' in user_data and user_data['first_name'] != '':
            user.first_name = user_data['first_name']
        if 'last_name' in user_data and user_data['last_name'] != '':
            user.last_name = user_data['last_name']
        if 'email' in user_data and user_data['email'] != '':
            user.email = user_data['email']
        user.save()

        # DonorProfile ফিল্ডগুলো আপডেট করুন যদি ডেটা দেওয়া থাকে
        for field in ['age', 'mobaile_no', 'address', 'blood_group']:
            if field in validated_data and validated_data[field] is not None and validated_data[field] != '':
                setattr(instance, field, validated_data[field])

        # শুধু তখনই ইমেজ আপডেট করুন যদি এটি None না হয়
        if 'image' in validated_data and validated_data['image'] is not None:
            instance.image = validated_data['image']

        instance.save()
        return instance
