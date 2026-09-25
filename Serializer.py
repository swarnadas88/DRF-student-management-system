from .models import Student,Course,StudentProfile,Subject
from rest_framework import serializers

class SubjectSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Subject 
        fields = [ 
            "id", 
            "name" 
        ] 

class  StudentSerializer(serializers.ModelSerializer):

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True
    )

    subjects = serializers.PrimaryKeyRelatedField( 
        many=True, 
        queryset=Subject.objects.all()
        ) 

    subject_details = SubjectSerializer(
        source="subjects",
        many=True,
        read_only=True
    )
    
    class Meta:
        model=Student
        fields = [
            "id",
            "Name",
            "Age",
            "Email",
            "Phone",
            "Course",
            "Image",
            "status",
            "status_display",
            "subjects",
            "subject_details"
        ]

# custom validation(name field validation)
    def validate_Name(self,value):
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters")
        return value

    # custom validation( age field validation)
    def validate_Age(self,value):
        if value <= 0:
            raise serializers.ValidationError("Age must be greater than 0")
        return value

    # custom validation(phone field validation)
    def validate_Phone(self,value):
        if len(str(value)) != 10:
            raise serializers.ValidationError("Phone number must be 10 characters")
        return value

    # custom validation( age and course object validation)
    def validate(self, attrs):
        age = attrs.get("Age")
        course = attrs.get("Course")

        restricted_courses = [
            "CEBA",
            "HEBA"
        ]

        if age < 18 and course.name in restricted_courses:
            raise serializers.ValidationError(
                "Students below 18 cannot select this course."
            )

        return attrs


class CourseSerializer(serializers.ModelSerializer):
    student=StudentSerializer(many=True,read_only=True)
    class Meta:
        model=Course
        fields= [
            "id",
            "name",
            "student"
        ]

class StudentProfileSerializer(serializers.ModelSerializer):

    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        write_only=True
    )

    student_details = StudentSerializer(
        source="student",
        read_only=True
    )

    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "student",
            "student_details",
            "address",
            "date_of_birth"
        ]

    # custom validation(name field validation)
    def validate_Name(self,value):
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters")
        return value

    # custom validation( age field validation)
    def validate_Age(self,value):
        if value <= 18:
            raise serializers.ValidationError("Age must be 18 or above")
        return value

    # custom validation(phone field validation)
    def validate_Phone(self,value):
        if len(str(value)) != 10:
            raise serializers.ValidationError("Phone number must be 10 characters")
        return value

    # custom validation( age and course object validation)
    def validate(self, attrs):
        age = attrs.get("Age")
        course = attrs.get("Course")

        restricted_courses = [
            "CEBA",
            "HEBA"
        ]

        if age < 18 and course.name in restricted_courses:
            raise serializers.ValidationError(
                "Students below 18 cannot select this course."
            )

        return attrs







