from django.db import transaction
from rest_framework.authtoken.models import Token
from rest_framework.decorators import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *
from django.contrib import auth

from faq.models import Question, Answer
from faq.serializers import QuestionSer, Answerser
from utils.decorators import need_login
from .models import User
from wenda_backend.respones_content import *
from .serializers import UserLoginSer, UserDetailSer, UserUpdataSer
from utils.shortcuts import paginate


class LoginView(APIView):
    def post(self, request, **kwargs):
        """用户登陆"""
        data = request.data.copy()
        username = data.get('phone')
        password = data.get('password')  # 手机号和用户名相同
        user = auth.authenticate(username=username, password=password)
        if user:
            request.session.set_expiry(60 * 60)
            auth.login(request, user)
            token, ok = Token.objects.get_or_create(user=user)
            ret_dict = UserDetailSer(user).data
            ret_dict['token'] = token.key
            return Response(ret_dict)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    @need_login
    def post(self, request, **kwargs):
        """"用户登出"""
        auth.logout(request)
        return Response(status=HTTP_202_ACCEPTED)


class ChangePassWord(APIView):
    @need_login
    def put(self, request, **kwargs):
        """修改密码"""
        old_password = request.data.get('old_password', '')
        new_password = request.data.get('new_password', '')
        if new_password == '':
            return Response({'status': NEW_PASSWORD_CAN_NOT_NULL},
                            status=HTTP_400_BAD_REQUEST)
        user = auth.authenticate(username=request.user.username,
                                 password=old_password)
        if user is None:
            return Response(status=HTTP_401_UNAUTHORIZED)
        user.set_password(new_password)
        user.save()
        return Response(status=HTTP_201_CREATED)


class UserView(APIView):
    @need_login
    def get(self, request, **kwargs):
        """'获取用户自己简单的个人信息(user表)"""
        user = request.user
        return Response(UserDetailSer(user).data)

    def post(self, request, **kwargs):
        """"注册"""
        phone_number = request.data.get("phone_number")
        # 默认密码为注册手机号
        password = request.data.get("password", phone_number)
        # 用户是否存在
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({'status': PHONE_NUMBER_HAS_BEEN_AUTHED}
                            , status=HTTP_400_BAD_REQUEST)
        with transaction.atomic():  # 事务处理 出错回滚
            user = User.objects.create(username=phone_number, phone_number=phone_number)
            user.set_password(password)
            user.save()
        return Response(UserDetailSer(user).data, status=HTTP_201_CREATED)

    @need_login
    def put(self, request, **kwargs):
        """"用户修改自己的可修改信息(user表)"""
        data = request.data.copy()
        ser = UserUpdataSer(request.user, data=data, partial=True)
        if ser.is_valid():
            ser.save()
        else:
            Response(status=HTTP_400_BAD_REQUEST)
        return Response(UserDetailSer(request.user).data, status=HTTP_201_CREATED)


class UserObjectView(APIView):
    @need_login
    def get(self, request, **kwargs):
        """'获取用户指定id的个人信息(user表)"""
        user = User.objects.get(id=kwargs.get('id'))
        return Response(UserDetailSer(user).data)


# 查看用户提问过的问题 ---------------------------------------------
# TODO 分页
@api_view(['GET'])
def look_ones_questions(request, **kwargs):
    """查看某个用户提问的问题列表,默认查看自己的"""
    user_id = kwargs.get('id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=HTTP_400_BAD_REQUEST)
    else:
        user = request.user
    questions = Question.objects.filter(user=user, is_deleted=False). \
        order_by('-created_time')
    ser = QuestionSer(questions, many=True)
    return Response({'content': ser.data})


# 查看用户所有回答----------------------------------------------------
@api_view(['GET'])
def look_ones_answers(request, **kwargs):
    """查看某个用户所有回答,默认查看自己"""
    user_id = kwargs.get('id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=HTTP_400_BAD_REQUEST)
    else:
        user = request.user
    answers = Answer.objects.filter(user=user, is_deleted=False). \
        order_by('-created_time')
    ser = Answerser(answers, many=True)
    return Response({'content': ser.data})
