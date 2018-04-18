# coding=utf-8

# import simplejson as json

# from django.contrib.auth.models import Group
# from django.test import TestCase
#
# from django.core.urlresolvers import reverse
# from account.models import User
# from rest_framework.test import APIClient
# from cc_community.models import CommunityTopic
# from comment.models import Comment
# from message.models import RecentMessage
# from utils.key_value import GROUP_STUDENT
# from vote.models import Vote


# class RemoveUnread(TestCase):
#
#    def setUp(self):
#        self.client = APIClient()
#        self.user_data = {
#            "username": "123456",
#            "password": 'test_password',
#        }
#        self.user = User.objects.create(
#            username="123456")
#        self.user.set_password("test_password")
#        self.user.is_qdu_authed = True
#        self.user.save()
#        self.group, ok = Group.objects.get_or_create(name=GROUP_STUDENT)
#        self.group.user_set.add(self.user)
#
#        self.topic = CommunityTopic.objects.create(title="123",
#                                                   content="321")
#        self.topic.save()
#        self.another_user_data = {
#            "username": "chiaki",
#            "password": 'chiaki',
#        }
#        self.another_user = User.objects.create(username="chiaki")
#        self.another_user.set_password("chiaki")
#        self.another_user.is_qdu_authed = True
#        self.another_user.save()
#
#    def _login(self):
#        self.client.login(**self.user_data)
#
#    def _create_comments(self):
#        self.comment = Comment.objects.create(source='topic',
#                                              object_id=self.topic.id,
#                                              creater=self.user,
#                                              comment_to_user=self.user,
#                                              content='nnn')
#        self.comment.save()
#        self.comment = Comment.objects.create(source='topic',
#                                              object_id=self.topic.id,
#                                              creater=self.another_user,
#                                              comment_to_user=self.user,
#                                              content='nnn')
#        self.comment.save()
#
#    def _create_votes(self):
#        self.vote = Vote.objects.create(source="topic",
#                                        object_id=self.topic.id,
#                                        creater=self.user,
#                                        vote_to=self.user)
#        self.vote.save()
#        self.vote = Vote.objects.create(source="topic",
#                                        object_id=self.topic.id,
#                                        creater=self.another_user,
#                                        vote_to=self.user)
#        self.vote.save()
#
#    def _create_messages(self):
#        self.message = RecentMessage.objects.create(show_user=self.user,
#                                                    opposite_user=self.another_user,
#                                                    content='233',
#                                                    is_readed=False)
#        self.message.save()
#
#    # 测试登录 没有数据
#    def test_remove_unread_login(self):
#        self._login()
#        res = self.client.put(path=reverse('remove_unread_view'))
#        self.assertEqual(res.status_code, 200)
#
#    # 测试去除小红点
#    def test_remove_unread(self):
#        self._login()
#        self._create_comments()
#        self._create_votes()
#        self._create_messages()
#        data = {"source": "comment"}
#        res = self.client.put(path=reverse('remove_unread_view'), data=data, format="json")
#        self.assertEqual(res.status_code, 200)
#        comments = Comment.objects.filter(comment_to_user=self.user, is_readed=False).count()
#        self.assertEqual(comments, 0)
#        data = {"source": "vote"}
#        res = self.client.put(path=reverse('remove_unread_view'), data=data, format="json")
#        self.assertEqual(res.status_code, 200)
#        votes = Vote.objects.filter(vote_to=self.user, is_readed=False).count()
#        self.assertEqual(votes, 0)
#        data = {"source": "message"}
#        res = self.client.put(path=reverse('remove_unread_view'), data=data, format="json")
#        self.assertEqual(res.status_code, 200)
#        messages = RecentMessage.objects.filter(show_user=self.user, is_readed=False).count()
#        self.assertEqual(messages, 0)
#
#    # 测试没有登陆
#    def test_remove_unread_without_login(self):
#        res = self.client.put(path=reverse('remove_unread_view'))
#        self.assertEqual(res.status_code, 401)
