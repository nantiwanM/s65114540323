from .models import UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib import messages


# แบบฟอร์มสำหรับการลงทะเบียนผู้ใช้ใหม่
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'mt-1 w-full border-gray-300 rounded-md shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 w-full border-gray-300 rounded-md shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm',
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm',
            'id': 'password1'
        }),
        help_text="รหัสผ่านควรมีความยาวอย่างน้อย 8 ตัวอักษร และห้ามเป็นตัวเลขล้วน"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm',
            'id': 'password2'
        })
    )

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password1', 'password2']

    # ฟังก์ชันสำหรับตรวจสอบอีเมล โดย .exists() ใช้ตรวจสอบว่า queryset มีข้อมูลหรือไม่ โดยไม่ดึงข้อมูลจากฐานข้อมูล
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

# แบบฟอร์มสำหรับการลงทะเบียนสำหรับแอดมิน
class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password1', 'password2', 'gender', 'date_of_birth', 'phone_number', 'address', 'profile_picture']

    date_of_birth = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}),
    )

    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        widget=forms.RadioSelect(attrs={'class': 'form-select w-full p-3 border rounded-md mt-2'})
    )

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.role = 'admin'  # กำหนด role เป็น admin
    #     user.is_staff = True  # ให้เข้าถึง admin panel
    #     user.is_superuser = True  # กำหนดให้เป็น superuser
    #     if commit:
    #         user.save()
    #     return user

# แบบฟอร์มสำหรับการแก้ไขโพรไฟล์สำหรับผู้ใช้
class UserProfileForm(forms.ModelForm):

    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'file-input file-input-bordered file-input-sm w-full max-w-xs mt-2',
            'accept': '.jpg, .jpeg, .png',
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'mt-1 w-full border-gray-300 rounded-md sm:text-sm focus:ring-gray-500 focus:border-gray-500',
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 w-full border-gray-300 rounded-md sm:text-sm focus:ring-gray-500 focus:border-gray-500',
        })
    )

    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 w-full border-gray-300 rounded-md sm:text-sm focus:ring-gray-500 focus:border-gray-500',
        })
    )

    birthday = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
        })
    )

    GENDER_CHOICES = [
        ('male', 'ชาย'),
        ('female', 'หญิง'),
        ('other', 'อื่น ๆ'),
    ]

    gender = forms.ChoiceField(
        required=False,
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': ''
        })
    )

    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'mt-1 w-full border-gray-300 rounded-md sm:text-sm focus:ring-gray-500 focus:border-gray-500',
            'rows': 3
        })
    )

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'username', 'email', 'phone_number', 'birthday', 'gender', 'address']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # ตรวจสอบว่า username ซ้ำหรือไม่ (ไม่รวมผู้ใช้ที่กำลังแก้ไข)
        if UserProfile.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("ชื่อผู้ใช้นี้มีอยู่ในระบบแล้ว กรุณาเลือกชื่ออื่น")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # ตรวจสอบว่าอีเมลซ้ำหรือไม่ (ไม่รวมผู้ใช้ที่กำลังแก้ไข)
        if UserProfile.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("อีเมลนี้มีอยู่ในระบบแล้ว กรุณากรอกอีเมลอื่น")

        return email
