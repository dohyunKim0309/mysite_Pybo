from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer


# <HTTP request>
# 1. GET is used to request data from a specified resource.
# 2. POST is used to send data to a server to create/update a resource.
@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    # 질문 객체 받아오기(question_id에 해당하는 질문 객체)
    question = get_object_or_404(Question, pk=question_id)
    # Send Answer data to server
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)  # answer 객체 임시로 생성
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()  # 저장 시간 저장
            answer.question = question  # answer.question 요소에 question 저장!
            answer.save()  # 정답에 저장하기
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm()

    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


# answer을 수정하는 기능
# --------------------------------------------------------------------------------------------
# *** [중요 질문] ==> answer_id는 각 question이 바뀌면 다시 1부터 시작하는가, 아니면 그냥 1부터 계속 번호가 매겨지는가? ***
# --------------------------------------------------------------------------------------------

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    # answer 객체 가져오기
    answer = get_object_or_404(Answer, pk=answer_id)

    # 사용자가 answer을 만든 사람이 아닐 경우
    if request.user != answer.author:
        # 에러메세지 객체 만들기 ==> 출력은 html에서 구현
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    # [중요] 사용자가 질문수정 창에서 질문을 수정한 후 적용하기 위해 버튼을 눌렀을 때 ==> 질문상세 창 load
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():  # form이 유효할 경우,
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    # [중요] 사용자가 질문을 수정하기 위해 질문수정 버튼을 눌렀을 때 ==> 질문수정 창 load
    else:
        # 기존에 존재하는 answer 데이터를 이용해서 answer form 만들기
        form = AnswerForm(instance=answer)
        # html 로드를 위한 데이터 전송을 위한 변수 선언
        context = {'answer': answer, 'form': form}
        return render(request, 'pybo/answer_form.html', context)


# 답변 삭제 기능
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)


# 답변  기능
@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        answer.voter.add(request.user)

    return redirect('{}#answer_{}'.format(resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
