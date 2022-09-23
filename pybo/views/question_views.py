from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


# 질문등록 페이지를 리턴하거나, 질문등록이 완료되면 데이터를 저장하고 질문 목록 페이지로 redirect
@login_required(login_url='common:login')
def question_create(request):
    # When send data to server
    # ==> 질문등록 페이지에서 질문을 작성하고, '등록하기'를 눌러 데이터를 서버에 보낼 때
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        # form이 유효할 경우
        if form.is_valid():
            question = form.save(commit=False)  # 임시 저장하고 question 객체 생성
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')  # 질문 목록으로 웹 페이지 이동!
    # When request data from server
    # ==> 질문등록 페이지에 들어가서 페이지 보여주기를 위한 html을 받아와야 할 때
    elif request.method == 'GET':
        form = QuestionForm()

    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


# question을 수정하는 기능
@login_required(login_url='common:login')
def question_modify(request, question_id):
    """

    :param request: user의 request
    :param question_id: 수정하려는 question의 id
    :return: 조건을 충족한다면 question 수정 창으로 리디렉션, 충족하지 않으면 그대로 넘어가기
    """
    # 수정하려는 질문 객체 받아오기(주어진 question_id에 해당하는 질문 객체)
    question = get_object_or_404(Question, pk=question_id)

    # request한 유저가 question을 만든 사람이 아닐 경우
    if request.user != question.author:
        # 에러메세지 출력하기
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question_id)

    # [중요] 페이지에서 유저가 작성한 데이터를 이용해 question 수정 후 데이터베이스에 업로드
    if request.method == 'POST':  # HTTP request POST: 데이터베이스에 있는 데이터 수정/업데이트
        # 사용자가 페이지에서 입력한 데이터와 원래 question의 데이터를 합칠 수 있도록 form 객체 만들기
        form = QuestionForm(request.POST, instance=question)

        # 사용자가 입력한 form이 조건을 충족할 경우, form의 데이터를 저장 후, 다시 로드하기 위해 pybo:detail로 redirect
        if form.is_valid():
            question = form.save(commit=False)  # commit 없이 form으로 들어온 데이터를 이용해 question 객체 만들기
            question.modify_date = timezone.now()  # 현재시간을 수정시간으로 저장하기
            question.save()  # question 객체 저장하기(데이터베이스에 저장)
            return redirect('pybo:detail', question_id=question.id)

    # [중요] question_detail 페이지에서 질문 수정 버튼을 눌렀을 때 질문 수정 페이지 로드
    else:  # HTTP request GET method: 데이터를 데이터베이스에서 가져올 때 호출
        # Question을 수정하기 위한 form 받아오기, 이 때 instance=question으로 기존 데이터도 불러오기!
        form = QuestionForm(instance=question)

    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


# question을 삭제하는 기능
@login_required(login_url='common:login')
def question_delete(request, question_id):
    # question 객체 가져오기
    question = get_object_or_404(Question, pk=question_id)

    # 사용자와 question을 만든 당사자가 아닐 경우, 에러메세지 객체 생성
    if request.user != question.author:
        # 에러메세지 객체 생성. ==> 이후 실제 보여주는 것은 html Code로!
        messages.error(request, '삭제권한이 없습니다')
        # 질문 상세 창으로 redirect(다시 원래대로 돌아오는것)
        return redirect('pybo:detail', question_id=question.id)
    else:
        # 질문 삭제하기(데이터베이스에서)
        question.delete()
        # 질문 글들이 모여 있는 창으로 redirect
        return redirect('pybo:index')


# question에 vote하는 기능(질문 추천 기능)
@login_required(login_url='common:login')
def question_vote(request, question_id):
    # question 객체 가져오기
    question = get_object_or_404(Question, pk=question_id)

    # 사용자가 question을 만든 당사자일 경우, vote 불가능, 에러메세지 출력
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다!')
    # 사용자가 question을 만든 당사자가 아닐 경우, vote 실행
    elif request.user != question.author:
        question.voter.add(request.user)

    # 작업이 끝나면 원래 있던 question detail 창으로 redirect하기!
    return redirect('pybo:detail', question_id=question_id)
