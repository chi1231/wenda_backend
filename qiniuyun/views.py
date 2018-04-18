from rest_framework.decorators import APIView
from rest_framework.response import Response
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
from .qiniu_settings import access_key, secret_key, bucket_name


# 构建鉴权对象
# q = Auth(access_key, secret_key)


# 上传到七牛后保存的文件名
# key = 'my-test.png'
# 生成上传 Token，可以指定过期时间等
# token = q.upload_token(bucket_name, key, 3600)
# 要上传文件的本地路径
# localfile = '/home/dell/test.png'

# ret, info = put_file(token, key, localfile)


class ImgTokenView(APIView):
    def post(self, request, **kwargs):
        """七牛图片上传Token获取"""
        q = Auth(access_key, secret_key)
        token = q.upload_token(bucket_name, expires=3600)
        return Response(token)
