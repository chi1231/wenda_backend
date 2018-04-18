import datetime

from rest_framework import serializers

from utils import pretty
from .models import Question, Answer


class AddQuestionSer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('title', 'dec', 'img', 'user', 'tag')


class PutQuestionSer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('title', 'dec', 'img', 'tag')


class QuestionSer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()

    def get_time(self, obj):
        return pretty.date(datetime.datetime.fromtimestamp(obj.created_time))

    class Meta:
        model = Question
        fields = ('id', 'user', 'time', 'title', 'dec', 'img', 'is_solved', 'tag')


class QuestionDeatilSer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()

    def get_time(self, obj):
        return pretty.date(datetime.datetime.fromtimestamp(obj.created_time))

    def get_answers(self, obj):
        answers = obj.answers.filter(is_deleted=False).order_by('zan')
        return AnswerObjectSer(answers, many=True).data

    class Meta:
        model = Question
        fields = ('id', 'user', 'title', 'dec', 'img', 'tag', 'is_solved',
                  'time', 'answers')


class AddAnswerSer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('question', 'user', 'dec', 'img')


class PutAnswerSer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('dec', 'img')


class AnswerObjectSer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()

    def get_time(self, obj):
        return pretty.date(datetime.datetime.fromtimestamp(obj.created_time))

    class Meta:
        model = Answer
        exclude = ('uuid', "created_time", 'is_deleted')


class Answerser(AnswerObjectSer):
    """回答详情的序列化 包含问题本身"""
    question = serializers.SerializerMethodField()

    def get_question(self, obj):
        question = obj.question
        return QuestionSer(question).data
