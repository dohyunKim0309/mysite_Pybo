from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from ..models import Question

# 한 페이지에 들어가는 question의 개수
qNum_per_page = 10


# 게시판 기능: question을 list로 한 페이지에 보여주는 기능.
def index(request):
    # 페이지 Number 변수 가져오기. ==> default value: 1
    page: int = request.GET.get('page', '1')
    # question들의 list 만들기 (게시물 전체 데이터를 담는 list 생성)
    question_list = Question.objects.order_by('-create_date')

    # 검색어
    kw = request.GET.get('kw', '')
    # 검색어가 존재할 경우, question_list 중에서 조건에 부합하지 않는 것들 모두 제거!
    if kw:
        question_list = question_list.filter(
            # **__icontains=kw: **에 kw가 포함되었는지 대소문자 구분 없이 확인
            # **__contains=kw: **에 kw가 포함되었는지 확인
            # answer__author__username__icontains=kw: kw가 답변을 작성한 이름에 포함되는가?
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    paginator = Paginator(question_list, qNum_per_page)  # 한 페이지에 정해진 수의 question 넣기

    # 원하는 page Number에 해당하는 페이지에 필요한 데이터만 가져오기 (Query 문 실행해서!)
    # page_obj는 요청된 페이지에 해당하는 페이지 데이터 객체
    page_obj = paginator.get_page(page)

    # 페이지 생성을 위한 context 변수 만들기
    context = {'question_list': page_obj, 'page': page, 'kw': kw}  # question_list라는 변수에 page_obj(페이지 객체)가 저장!

    # context 변수를 사용해 return하기
    return render(request, 'pybo/question_list.html', context)


# question과 그 Answer을 자세하게 보여주는 역할
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}

    return render(request, 'pybo/question_detail.html', context)
