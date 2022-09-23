from django.contrib import admin
from .models import Question

# 사용자이름: admin_sci3037
# 이메일 주소: dkim7800@gmail.com
# 비밀번호: love0309@

# 사용자이름: testid
# 비밀번호: love0309@


# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)
