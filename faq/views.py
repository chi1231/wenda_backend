from rest_framework.decorators import APIView, api_view
from django.db import transaction
from rest_framework.response import Response
from rest_framework.status import *

from utils.decorators import need_login
from .models import Question, Answer
from .serializers import AddQuestionSer, QuestionSer, QuestionDeatilSer, \
    PutQuestionSer, AddAnswerSer, AnswerObjectSer, Answerser, PutAnswerSer
from utils.shortcuts import paginate
from wenda_backend.respones_content import *


# 问题 -------------------------------------------------

class QuestionView(APIView):

    def get(self, request, **kwargs):
        """查看问题列表
            默认/time：问题时间排序
            hot:根据回答数量排序
            latest:最近一个回答时间排序
        """
        tag = request.GET.get('tag')  # 标签
        flag = request.GET.get('flag')
        if tag:
            questions_filter = Question.objects.filter(is_deleted=False, tag=tag)
        else:
            questions_filter = Question.objects.filter(is_deleted=False)
        if flag == 'time' or flag is None:
            questions = questions_filter.order_by('-created_time')
        elif flag == 'hot':
            questions = sorted(questions_filter, key=lambda x: -x.answers.count())
        elif flag == 'latest':
            questions = []
            questions_list = questions_filter.order_by('-answers__created_time')
            for i in questions_list:  # 数据库不支持distinct() 只能这么做了 不知道性能好不好
                if i not in questions:
                    questions.append(i)
        else:
            return Response({'status': FLAG_ARGUMENT_ERRORS},
                            status=HTTP_400_BAD_REQUEST)
        return Response({'content': QuestionSer(questions, many=True).data})

    @need_login
    def post(self, request, **kwargs):
        """用户添加一个问题"""
        data = request.data.copy()
        data['user'] = request.user.id
        ser = AddQuestionSer(data=data)
        if ser.is_valid():
            question = ser.save()
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
        return Response(QuestionSer(question).data, status=HTTP_201_CREATED)


class QuestionObjectView(APIView):
    @need_login
    def post(self, request, **kwargs):
        """题主设置解决回答"""
        question_id = kwargs.get('id')
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({'status': QUESTION_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        if question.user != request.user:
            return Response(status=HTTP_403_FORBIDDEN)
        if question.is_deleted:
            return Response({'status': QUESTION_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        if question.is_solved:
            return Response({'status': QUESTION_HAD_SOLVED},
                            status=HTTP_400_BAD_REQUEST)
        answer_id = request.data.get('answer_id')
        answer = Answer.objects.filter(question=question, is_deleted=False, id=answer_id)
        if answer.exists():
            with transaction.atomic():
                answer = answer[0]  # answer[0].save()失效
                answer.is_solved = True
                answer.save()
                question.is_solved = True
                question.save()
            return Response(status=HTTP_201_CREATED)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

    # TODO 分页 回答排序 默认按点赞正序排序
    def get(self, request, **kwargs):
        """查看一个问题详情"""
        question_id = kwargs.get('id')
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({'status': QUESTION_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        if question.is_deleted:
            return Response({'status': QUESTION_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        ser = QuestionDeatilSer(question)
        return Response(ser.data)

    @need_login
    def put(self, request, **kwargs):
        """修改一个问题描述,被修改的问题必须自己提问的"""
        data = request.data.copy()
        question_id = kwargs.get('id')
        user = request.user
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({'status': QUESTION_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        if question.is_deleted:
            return Response({'status': QUESTION_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        if question.user != user:
            return Response(status=HTTP_403_FORBIDDEN)
        ser = PutQuestionSer(question, data=data)
        if ser.is_valid():
            ser.save()
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
        return Response(QuestionSer(question).data, status=HTTP_201_CREATED)

    @need_login
    def delete(self, request, **kwargs):
        """删除一个问题,被删除的问题必须自己提问的"""
        question_id = kwargs.get('id')
        user = request.user
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({'status': QUESTION_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        if question.is_deleted:
            return Response({'status': QUESTION_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        if question.user != user:
            return Response(status=HTTP_403_FORBIDDEN)
        question.is_deleted = True
        question.save()
        return Response(status=HTTP_202_ACCEPTED)


# 回答 --------------------------------------------------------------

class AnswerView(APIView):
    def get(self, request, **kwargs):
        """获取回答列表"""
        flag = request.GET.get('flag')
        answers_filter = Answer.objects.filter(is_deleted=False)
        if flag == 'time' or flag is None:
            answers = answers_filter.order_by('-created_time')
        elif flag == 'hot':
            answers = answers_filter.order_by('-zan')
        else:
            return Response({'status': FLAG_ARGUMENT_ERRORS},
                            status=HTTP_400_BAD_REQUEST)
        return Response(Answerser(answers, many=True).data)

    @need_login
    def post(self, request, **kwargs):
        """对一个问题添加一个回答"""
        data = request.data.copy()
        data['user'] = request.user.id
        try:
            question = Question.objects.get(id=data['question'])
        except Question.DoesNotExist:
            return Response({'status': QUESTION_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        if question.is_deleted:
            return Response({'status': QUESTION_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        if question.answers.filter(user=request.user).exists():
            return Response({'status': HAD_ANSWERED}, status=HTTP_400_BAD_REQUEST)
        ser = AddAnswerSer(data=data)
        if ser.is_valid():
            answer = ser.save()
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
        return Response(AnswerObjectSer(answer).data, status=HTTP_201_CREATED)


class AnswerObjectView(APIView):
    def get(self, request, **kwargs):
        """查看一个回答"""
        answer_id = kwargs.get('id')
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return Response({'status': ANSWER_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        if answer.question.is_deleted:
            return Response({'status': QUESTION_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        if answer.is_deleted:
            return Response({'status': ANSWER_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        return Response(Answerser(answer).data)

    @need_login
    def put(self, request, **kwargs):
        """修改回答，需本人操作"""
        answer_id = kwargs.get('id')
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return Response({'status': ANSWER_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        if answer.is_deleted:
            return Response({'status': ANSWER_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        if answer.user != request.user:
            return Response(status=HTTP_403_FORBIDDEN)
        data = request.data.copy()
        ser = PutAnswerSer(answer, data=data, partial=True)
        if ser.is_valid():
            ser.save()
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
        return Response(Answerser(answer).data, status=HTTP_201_CREATED)

    @need_login  # TODO 逻辑太烂 项目做能起来就建一个点赞应用重写
    def post(self, request, **kwargs):
        """给回答点赞点反对"""
        answer_id = kwargs.get('id')
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return Response({'status': ANSWER_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        if answer.is_deleted:
            return Response({'status': ANSWER_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        answer_id = kwargs.get('id')
        user_id = request.user.id
        flag = request.data.get('flag')  # zan or oppose
        session_zan = answer_id + str(user_id) + 'zan'
        session_oppose = answer_id + str(user_id) + 'oppose'
        if flag == 'zan' and request.session.get(session_zan, False) is False:  # 没点过赞
            answer.zan += 1
            answer.oppose = 0 if answer.oppose - 1 < 0 else answer.oppose - 1
            request.session[session_zan] = True
            request.session[session_oppose] = False
        elif flag == 'oppose' and request.session.get(session_oppose, False) is False:  # 没点过反对
            answer.oppose += 1
            answer.zan = 0 if answer.zan - 1 < 0 else answer.zan - 1
            request.session[session_oppose] = True
            request.session[session_zan] = False
        else:
            return Response({'status': REPETITIVE_OPERATION},
                            status=HTTP_400_BAD_REQUEST)
        answer.save()
        return Response(status=HTTP_201_CREATED)

    @need_login
    def delete(self, request, **kwargs):
        """删除一个回答,需回答者本身"""
        answer_id = kwargs.get('id')
        user = request.user
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return Response({'status': ANSWER_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        if answer.is_deleted:
            return Response({'status': ANSWER_DOES_NOT_EXIST_OR_DELETED},
                            status=HTTP_404_NOT_FOUND)
        if answer.user != user:
            return Response(status=HTTP_403_FORBIDDEN)
        answer.is_deleted = True
        answer.save()
        return Response(status=HTTP_202_ACCEPTED)

