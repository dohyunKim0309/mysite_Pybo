from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Question(models.Model):  # 질문 클래스
    # author & voter: 질문을 작성한 사람 및 질문을 추천한 사람.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    # on_delete=models.CASCADE: 계정 삭제 ==> 생성 답변 모두 삭제
    voter = models.ManyToManyField(User, related_name='voter_question')  # 질문을 추천한 사람
    # cf) 다대다 관계 데이터베이스 저장 ==> ManyToManyField.

    # on_delete=models.CASCADE: 계정 삭제 ==> 생성 질문 모두 삭제
    subject = models.CharField(max_length=200)  # 질문의 제목
    content = models.TextField()  # 질문의 내용
    create_date = models.DateTimeField()  # 질문 생성 날짜
    modify_date = models.DateTimeField(null=True, blank=True)  # 질문 수정 날짜

    def __str__(self):
        return self.subject


# 답변 클래스(모델)
class Answer(models.Model):
    # author & voter: 답변을 작성한 사람 및 답변을 추천한 사람.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    # on_delete=models.CASCADE: 계정 삭제 ==> 생성 답변 모두 삭제
    voter = models.ManyToManyField(User, related_name='voter_answer')
    # cf) 다대다 관계 데이터베이스 저장 ==> ManyToManyField.

    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # 답변이 쓰여진 대상 질문
    content = models.TextField()  # 답변 내용
    create_date = models.DateTimeField()  # 답변 생성 날짜
    modify_date = models.DateTimeField(null=True, blank=True)  # 답변 수정 날짜(default: null)

    def __str__(self):
        return 'Q={}, A={}'.format(self.question, self.content)
