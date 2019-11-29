from rest_framework import generics
from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import User, Profile, Duty
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
# from rest_framework.filters import SearchFilter, OrderingFilter
#
# from .permissions import OwnerCanManageReadOnly
#
from .serializers import *
from datetime import datetime
from rest_framework import exceptions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.core import serializers
import json
from django.contrib.auth import login, logout
import django.contrib.auth.password_validation as validators


class CreateProfile(APIView):#ایجاد پروفایل برای افراد(ثبت نام)
    serializer_class = UserSerializer

    def post(self, request):
        user = User()

        password = request.data.get('password')

        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except :
            raise exceptions.ValidationError("password is incorrect")

        if request.data.get("username"):
            user.username = request.data.get("username")
        else:
            raise exceptions.ValidationError("username is required")

        if request.data.get("password"):
            user.set_password(password)
        else:
            raise exceptions.ValidationError("password is required")

        user.save()
        profile = Profile()
        profile.user = user
        profile.status = 'em'
        profile.save()
        return Response({"username": request.data.get("username"), "password": request.data.get("password")},
                        status=200)


class RequestEMtoODAPIView(APIView):#ارسال درخواست ارتقا کارمند به مدیر سازمان
    serializer_class = RequestEMtoODSerializer

    def post(self, request):
        if request.user.is_authenticated:

            if request.user.profile.status == 'em':
                re = RequestEMtoOD()

                re.user = request.user

                if request.data.get("organization"):
                    re.organization =request.data.get("organization")
                else:
                    raise exceptions.ValidationError("سازمان درخواستی ارسال نشده است !")

                re.status = 'w'

                re.save()

                return Response('درخواست ثبت شد!!!', status=200)
            else:
                raise exceptions.ValidationError('شما کارمند نیستید!!! این  قسمت برای درخواست ارتقا کارمند به مدیر سازمان هست!')
        else:
            raise exceptions.ValidationError('شما لاگین نکردید')

class RequestEMtoOEAPIView(APIView):#ارسال درخواست ارتقا کارمند به کارمند سازمان
    serializer_class = RequestEMtoOESerializer

    def post(self, request):
        if request.user.is_authenticated:

            if request.user.profile.status == 'em':
                re = RequestEMtoOE()

                re.user = request.user

                if request.data.get("organization"):
                    try:
                        re.organization = Organization.objects.get(id = request.data.get("organization"))
                    except:
                        raise exceptions.ValidationError("سازمان  درخواستی شما وجود ندارد!!!")
                else:
                    raise exceptions.ValidationError("سازمان درخواستی ارسال نشده است!")

                re.status = 'w'

                re.save()

                return Response('درخواست ثبت شد!!!', status=200)
            else:
                raise exceptions.ValidationError('شما کارمند نیستید!!! این  قسمت برای درخواست ارتقا کارمند به کارمند سازمان هست!')
        else:
            raise exceptions.ValidationError('شما لاگین نکردید!!!')

class RequestOEtoODAPIView(APIView):#ارسال درخواست ارتقا کارمند سازمان به مدیر سازمان
    serializer_class = RequestOEtoODSerializer

    def post(self, request):
        if request.user.is_authenticated:

            if request.user.profile.status == 'oe':
                re = RequestOEtoOD()

                re.user = request.user
                re.status = 'w'

                re.save()

                return Response('درخواست ثبت شد', status=200)
            else:
                raise exceptions.ValidationError('شما کارمند سازمان نیستید!!! این  قسمت برای درخواست ارتقا کارمند سازمان به مدیر سازمان هست!')
        else:
            raise exceptions.ValidationError('شما لاگین نکردید!!!')

class InboxAPIView(APIView):# صندوق جهت مشاهده درخواست های ارتقا برای ادمین و مدیر سازمان
    def get(self, request):
        if request.user.is_authenticated:

            if request.user.is_superuser:
                query = RequestEMtoOD.objects.filter(status = 'w')
                query_serialized = serializers.serialize('json', query)
                wating_request = json.loads(query_serialized)

                for i in wating_request:
                    i['title'] = 'درخواست ارتقا کارمند به مدیر سازمان'

                return Response(wating_request, status=200)
            elif request.user.profile.status == 'od':
                query = RequestEMtoOE.objects.filter(status = 'w').filter(organization = request.user.profile.organization)
                query_serialized = serializers.serialize('json', query)
                wating_request = json.loads(query_serialized)

                for i in wating_request:
                    i['title'] = 'درخواست ارتقا کارمند به کارمند سازمان'

                query2 = RequestOEtoOD.objects.filter(status = 'w').filter(user__profile__organization = request.user.profile.organization)
                query_serialized2 = serializers.serialize('json', query2)
                wating_request2 = json.loads(query_serialized2)

                for i in wating_request2:
                    i['title'] = 'درخواست ارتقا کارمند سازمان به مدیر سازمان'

                all_request = wating_request + wating_request2

                return Response(all_request, status=200)

            else:
                raise exceptions.ValidationError('شما ادمین و یا مدیر سازمان نیستید!!!')
        else:
            raise exceptions.ValidationError('شما لاگین نکردید!!!')


class DeterminationEMtoODAPIView(APIView):#تعیین وضعیت درخواست های ارتقا کارمند به مدیر سازمان توسط ادمین
    serializer_class = Answerserializer

    def post(self, request, id):
        if request.user.is_authenticated:

            if request.user.is_superuser:
                if request.data.get("answer") == 'true':
                    try:
                        p = Profile.objects.get(user__requestemtood__id=id)
                    except:
                        raise exceptions.ValidationError('آیدی درخواست فرستاده شده موجود نیست!!!')

                    re = RequestEMtoOD.objects.get(id = id)
                    if re.status != 'c':
                        raise exceptions.ValidationError('این درخواست انجام شده است!!!')

                    re.status = 'c'

                    o = Organization()
                    o.name = re.organization
                    o.save()

                    p.status = 'od'
                    p.organization = o
                    p.save()
                    re.save()

                    return Response({"status": 'ارتقا کارمند به مدیر سازمان انجام شد'}, status=200)

                elif request.data.get("answer") == 'false':
                    re = RequestEMtoOD.objects.get(id=id)
                    re.status = 'f'
                    re.save()

                    return Response({"status": 'وضعیت درخواست به رد شده تغییر یافت!!!'}, status=200)

                else:
                    raise exceptions.ValidationError(
                        'جواب  ارسال شما صحیح نمی باشد!!!!')

            else:
                raise exceptions.ValidationError('شما مدیر سازمان نیستید!!!')
        else:
            raise exceptions.ValidationError('شما لاگین  نکردید!!!')

class DeterminationEMtoOEAPIView(APIView):#تعیین وضعیت درخواست های ارتقا کارمند به کارمند سازمان توسط ادمین
    serializer_class = Answerserializer

    def post(self, request, id):
        if request.user.is_authenticated:

            if request.user.is_superuser or request.user.profile.status == 'od':
                try:
                    re = RequestEMtoOE.objects.get(id=id)
                except:
                    raise exceptions.ValidationError('درخواست فرستاده شده موجود نیست!!!')

                if request.user.profile.status == 'od' and request.user.profile.organization != re.organization:
                    raise exceptions.ValidationError('درخواستی که میخواهید تعیین وضعیت مربوط به سازمان شما نیست!!!')

                elif request.data.get("answer") == 'true':
                    if re.status != 'c':
                        raise exceptions.ValidationError('این درخواست تایید شده است!!!')

                    re.status = 'c'
                    p = Profile.objects.get(user__requestemtooe__id=id)
                    p.status = 'oe'
                    p.organization = re.organization

                    p.save()
                    re.save()

                    return Response({"status": 'ارتقا کارمند به کارمند سازمان انجام شد'}, status=200)
                elif request.data.get("answer") == 'false':
                    re.status = 'f'
                    re.save()

                    return Response({"status": 'وضعیت درخواست به رد شده تغییر یافت!!!'}, status=200)

                else:
                    raise exceptions.ValidationError(
                        'جواب  ارسالی شما صحیح نمی باشد!!!!')

            else:
                raise exceptions.ValidationError('شما مدیر سازمان و یا ادمین نیستید!!!')
        else:
            raise exceptions.ValidationError('شما لاگین نکردید!!!')

class DeterminationOEtoODAPIView(APIView):#تعیین وضعیت درخواست های ارتقا کارمند سازمان به مدیر سازمان توسط ادمین
    serializer_class = Answerserializer

    def post(self, request, id):
        if request.user.is_authenticated:

            if request.user.is_superuser or request.user.profile.status == 'od':
                try:
                    re = RequestOEtoOD.objects.get(id=id)
                except:
                    raise exceptions.ValidationError('درخواست فرستاده شده موجود نیست!!!')

                if request.user.profile.status == 'od' and request.user.profile.organization != re.user.profile.organization:
                    raise exceptions.ValidationError('درخواستی که میخواهید تغییر دهید مربوط به سازمان شما نیست!!!')

                if request.data.get("answer") == 'true':
                    if re.status != 'c':
                        raise exceptions.ValidationError('این درخواست انجام شده است!!!')

                    p = Profile.objects.get(user__requestoetood__id=id)
                    p.status = 'od'
                    p.save()
                    re.status = 'c'
                    re.save()

                    return Response({"status": 'ارتقا کارمند سازمان به مدیر سازمان انجام شد'}, status=200)

                elif request.data.get("answer") == 'false':
                    re.status = 'f'
                    re.save()

                    return Response({"status": 'وضعیت درخواست به رد شده تغییر یافت!!!'}, status=200)

                else:
                    raise exceptions.ValidationError(
                        'جواب  ارسال شما صحیح نمی باشد!!!!')

            else:
                raise exceptions.ValidationError('شما مدیر سازمان و یا ادمین نیستید!!!')
        else:
            raise exceptions.ValidationError('شما لاگین نکردید!!!')



class ManageAPIView(APIView):#مدیریت پروفایل کابران جهت تغییر نقش و سازمان افراد توسط ادمین و مدیر سازمان
    serializer_class = Manageserializer

    def post(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.profile.status == 'od':
                try:
                    profile = Profile.objects.get(id=request.data.get('profile'))
                except:
                    raise exceptions.ValidationError('آیدی پروفایل نامعتبر است!!!')

                if request.user.profile.status == 'od' and profile.organization != request.user.profile.organization:
                    raise exceptions.ValidationError('این کاربر برای سازمان شما نیست!!!')

                if request.data.get("status"):
                    if request.data.get("status") in ['od', 'oe', 'em']:
                        if request.data.get("status") == 'em':
                            profile.organization = None

                        elif request.user.profile.status != 'od':
                                profile.organization = Organization.objects.get(id=request.data.get('organization'))

                        profile.status = request.data.get('status')
                        profile.save()

                        return Response({"status": 'وضعیت پروفایل تغییر یافت!!!'}, status=200)

                    else:
                        raise exceptions.ValidationError('وضعیت  نامعتبر است!!!')
                else:
                    raise exceptions.ValidationError('وضعیت ارسال  نشده است!!!')
            else:
                raise exceptions.ValidationError('شما ادمین و یا مدیر سازمان نیستید!!!')
        else:
            raise exceptions.ValidationError('شما لاگین نکردید!!!')


    def get(self, request):
        if request.user.is_authenticated:

            if request.user.is_superuser:
                query = Profile.objects.filter()
                query_serialized = serializers.serialize('json', query)
                all_profile = json.loads(query_serialized)

                return Response(all_profile, status=200)

            if request.user.profile.status == 'od':
                query = Profile.objects.filter(organization= request.user.profile.organization)
                query_serialized = serializers.serialize('json', query)
                od_profile = json.loads(query_serialized)

                return Response(od_profile, status=200)
            else:
                raise exceptions.ValidationError('شما ادمین یا مدیر سازمان نیستید!!!')
        else:
            raise exceptions.ValidationError('شما لاگین نکردید!!!')

class Login(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        logout(request)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"status": 'لاگین شد!!!'}, status=200)
        else:
            return Response({"status": 'کاربر نامعتبر !!!'}, status=200)


class DutyCreateAPIView(APIView):
    serializer_class = Dutyserializer

    def post(self, request):
        if request.user.is_authenticated:

            if request.user.profile.status == 'em':
                raise exceptions.ValidationError('شما کاربر عادی هستید و وظیفه ای نمی توانید تعریف کنید!!!')

            if request.user.is_superuser:
                raise exceptions.ValidationError('شما ادمین هستید و وظیفه ای نمی توانید تعریف کنید!!!')

            else:
                duty = Duty()
                if request.data.get('profile'):
                    try:
                        profile = Profile.objects.get(id = request.data.get('profile'))
                    except:
                        raise exceptions.ValidationError('پروفایل ارسالی شما نامعتبر است!!!')


                    if request.user.profile.status == 'oe':
                        duty.profile = request.user.profile

                    elif request.user.profile.status == 'od':
                        if profile.status == 'oe':
                            if profile.organization == request.user.profile.organization:
                                duty.profile = profile
                            else:
                                raise exceptions.ValidationError('کاربر ارسالی شما عضو سازمان شما نیست!!!')
                        else:
                            raise exceptions.ValidationError('کاربر ارسالی شما کارمند سازمان نیست!!!')
                    else:
                        duty.profile = profile

                else:
                    raise exceptions.ValidationError('پروفایل ارسال نشده است !!!')


                if request.data.get('title'):
                    try:
                        duty.title = request.data.get('title')
                    except:
                        raise exceptions.ValidationError('عنوان وظیفه ارسالی شما نامعتبر است!!!')
                else:
                    raise exceptions.ValidationError('عنوان وظیف ارسال نشده است !!!')


                if request.data.get('explanation'):
                    try:
                        duty.explanation = request.data.get('explanation')
                    except:
                        raise exceptions.ValidationError('شرح وظیفه ارسالی شما نامعتبر است!!!')
                else:
                    raise exceptions.ValidationError('شرح وظیفه ارسال نشده است !!!')


                if request.data.get('deadline_time'):
                    try:
                        duty.deadline_time = request.data.get('deadline_time')
                    except:
                        raise exceptions.ValidationError('زمان موعد ارسالی شما نامعتبر است!!!')
                else:
                    raise exceptions.ValidationError('زمان موعد ارسال نشده است !!!')

                duty.inscription_time = datetime.now()
                duty.save()

                return Response('وظیفه افزوده شد!!!', status=200)
        else:
            raise exceptions.ValidationError('شما لاگین نکردید!!!')
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                query = Duty.objects.filter()
                query_serialized = serializers.serialize('json', query)
                all_duty = json.loads(query_serialized)

                return Response(all_duty, status=200)


            if request.user.profile.status == 'oe':
                query = Duty.objects.filter(profile = request.user.profile)
                query_serialized = serializers.serialize('json', query)
                all_duty = json.loads(query_serialized)

                return Response(all_duty, status=200)



            if request.user.profile.status == 'od':
                query = Duty.objects.filter(profile__organization= request.user.profile.organization)
                query_serialized = serializers.serialize('json', query)
                all_duty = json.loads(query_serialized)

                return Response(all_duty, status=200)

            if request.user.profile.status == 'em':
                raise exceptions.ValidationError('شما کاربر عادی هستید و وظیفه ای برای شما تعریف نشده است!!!')

            else:
                raise exceptions.ValidationError('شما وظیفه ای ندارید!!!')
        else:
            raise exceptions.ValidationError('شما لاگین نکردید!!!')

class DutyEditAPIView(APIView):
    serializer_class = Dutyserializer

    def put(self, request, id):
        try:
            duty = Duty.objects.get(id = id)
        except:
            raise exceptions.ValidationError('وظیفه ای با این آیدی موجود نیست!!!')
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.profile.status in ['od', 'oe']:
                if request.user.profile.status == 'oe' and duty.profile != request.user.profile:
                    raise exceptions.ValidationError('این وظیفه متعلق به شما نیست و نمیتوانید انرا ویرایش کنید!!!')

                if request.user.profile.status == 'od':
                    if duty.profile.organization != request.user.profile.organization:
                        raise exceptions.ValidationError('این وظیفه متعلق به کارمند سازمان شما نیست و نمیتوانید انرا ویرایش کنید!!!')

                if request.data.get('profile'):
                    try:
                        profile = Profile.objects.get(id=request.data.get('profile'))
                    except:
                        raise exceptions.ValidationError('پروفایل ارسالی شما نامعتبر است!!!')

                    if request.user.profile.status == 'oe' :
                        duty.profile = request.user.profile

                    else:
                        duty.profile = profile
                else:
                    raise exceptions.ValidationError('پروفایل ارسال نشده است !!!')

                if request.data.get('title'):
                    try:
                        duty.title = request.data.get('title')
                    except:
                        raise exceptions.ValidationError('عنوان وظیفه ارسالی شما نامعتبر است!!!')
                else:
                    raise exceptions.ValidationError('عنوان وظیف ارسال نشده است !!!')

                if request.data.get('explanation'):
                    try:
                        duty.explanation = request.data.get('explanation')
                    except:
                        raise exceptions.ValidationError('شرح وظیفه ارسالی شما نامعتبر است!!!')
                else:
                    raise exceptions.ValidationError('شرح وظیفه ارسال نشده است !!!')

                if request.data.get('deadline_time'):
                    try:
                        duty.deadline_time = request.data.get('deadline_time')
                    except:
                        raise exceptions.ValidationError('زمان موعد ارسالی شما نامعتبر است!!!')
                else:
                    raise exceptions.ValidationError('زمان موعد ارسال نشده است !!!')

                duty.inscription_time = datetime.now()
                duty.save()

                return Response('وظیفه ویرایش شد!!!', status=200)
        else:
            raise exceptions.ValidationError('شما لاگین نکردید!!!')



    def delete(self, request, id):
        try:
            duty = Duty.objects.get(id = id)
        except:
            raise exceptions.ValidationError('وظیفه ای با این آیدی موجود نیست!!!')
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.profile.status in ['od', 'oe']:
                if request.user.profile.status == 'oe' and duty.profile != request.user.profile:
                    raise exceptions.ValidationError('این وظیفه متعلق به شما نیست و نمیتوانید انرا حذف کنید!!!')

                if request.user.profile.status == 'od':
                    if duty.profile.organization != request.user.profile.organization:
                        raise exceptions.ValidationError('این وظیفه متعلق به کارمند سازمان شما نیست و نمیتوانید انرا حذف کنید!!!')

                duty.delete()

                return Response('وظیفه حذف شد!!!', status=200)
        else:
            raise exceptions.ValidationError('شما لاگین نکردید!!!')

    def get(self, request, id):
        query = Duty.objects.filter(id = id)
        query_serialized = serializers.serialize('json', query)
        duty = json.loads(query_serialized)

        return Response(duty, status=200)



#
    # def get(self, request):
    #     if request.user.profile.user_type.name == "staff":
    #
    #         gym = request.user.gym
    #         coach = Profile.objects.filter(user_type__name="coach", gym=gym)
    #         data = SportSerializer(coach, many=True)
    #         return Response(data.data, status=status.HTTP_200_OK)
    #     else:
    #         raise exceptions.ValidationError("only staff can get it")

#
# @method_decorator(csrf_exempt, name='dispatch')
# class Login222(generics.GenericAPIView):
#     serializer_class = LoginSerilizer
#
#     def post(self, request):
#         serializer = LoginSerilizer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         # django_login(request, user)
#         token, created = Token.objects.get_or_create(user=user)
#
#         return Response({"token": token.key, "userid": user.id, "user": Userserializer(user, many=False).data},
#                         status=200)
#
#
# class PostListAPIView(generics.ListAPIView):
#     serializer_class = PostListSerializer
#     filter_backends = (DjangoFilterBackend, SearchFilter)
#     filterset_fields = ('owner__username', 'content', 'title')
#     search_fields = ('owner__username', 'content', 'title')
#
#     def get_queryset(self, *args, **kwargs):
#         queryset = Posts.objects.all()
#
#         query = self.request.GET.get('q')
#         if query:
#             print('نیومده تو')
#             queryset = queryset.filter(
#                 Q(title__search=query) | Q(content__search=query) | Q(owner__first_name__search=query) | Q(
#                     owner__last_name__search=query) | Q(owner__username__search=query)).distinct().order_by(
#                 '-updateDateTime')
#         return queryset
#
#
# class PostDetailAPIView(generics.RetrieveAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostDetailSerializer
#     lookup_field = 'id'
#
#
# class PostDeleteAPIView(generics.RetrieveDestroyAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostDeleteSerializer
#     lookup_field = 'id'
#     permission_classes = [OwnerCanManageReadOnly, ]
#
#     def perform_destroy(self, serializer):
#         if serializer.owner != self.request.user:
#             raise PermissionDenied
#         else:
#             serializer.delete()
#
#     permission_classes = [IsAdminUser, ]
#
#
# class PostUpdateAPIView(generics.RetrieveUpdateAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostUpdateSerializer
#     lookup_field = 'id'
#     permission_classes = [OwnerCanManageReadOnly, ]
#
#     def perform_update(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class PostCreateAPIView(generics.CreateAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostCreateSerializer
#     lookup_field = 'id'
#     permission_classes = [IsAuthenticated, ]
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class PostDeleteUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostDeleteUpdateSerializer
#     lookup_field = 'id'
#     permission_classes = [OwnerCanManageReadOnly, ]
