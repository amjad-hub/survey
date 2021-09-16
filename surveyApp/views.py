from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Question, Survey, Choice,Answer
from .serializers import SurveySerializer, QuestionSerializer, ChoiceSerializer,AnswerSerializer

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# import different status
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.utils import timezone


@csrf_exempt
@api_view(["GET"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

# views for survey model
@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def survey_create(request):
    serializer = SurveySerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        survey = serializer.save()
        return Response(SurveySerializer(survey).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def survey_update(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    if request.method == 'PATCH':
        serializer = SurveySerializer(survey, data=request.data, partial=True)
        if serializer.is_valid():
            survey = serializer.save()
            return Response(SurveySerializer(survey).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        survey.delete()
        return Response("survey deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def survey_view(request):
    surveys = Survey.objects.all()
    serializer = SurveySerializer(surveys, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def active_surveys_view(request):
    surveys = Survey.objects.filter(end_date__gte=timezone.now()).filter(pub_date__lte=timezone.now())
    serializer = SurveySerializer(surveys, many=True)
    return Response(serializer.data)

# views for question model
@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def question_create(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save()
        return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def question_update(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'PATCH':
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionSerializer(question).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return Response("Question deleted", status=status.HTTP_204_NO_CONTENT)

# views for choice model
@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def choice_create(request):
    serializer = ChoiceSerializer(data=request.data)
    if serializer.is_valid():
        choice = serializer.save()
        return Response(ChoiceSerializer(choice).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def choice_update(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    if request.method == 'PATCH':
        serializer = ChoiceSerializer(choice, data=request.data, partial=True)
        if serializer.is_valid():
            choice = serializer.save()
            return Response(ChoiceSerializer(choice).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        choice.delete()
        return Response("Choice deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def answer_create(request):
    serializer = AnswerSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        answer = serializer.save()
        return Response(AnswerSerializer(answer).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# views for answer model
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def answer_view(request, user_id):
    answers = Answer.objects.filter(user_id=user_id)
    serializer = AnswerSerializer(answers, many=True)
    return Response(serializer.data)


@api_view(['PATCH', 'DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser,))
def answer_update(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'PATCH':
        serializer = AnswerSerializer(answer, data=request.data, partial=True)
        if serializer.is_valid():
            answer = serializer.save()
            return Response(AnswerSerializer(answer).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        answer.delete()
        return Response("Answer deleted", status=status.HTTP_204_NO_CONTENT)