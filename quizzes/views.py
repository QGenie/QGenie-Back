from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from quizzes.models import Session, Question
from quizzes.serializers import SessionSerializer, QuestionSerializer
from quizzes.model_api import get_questions
import json

class SessionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request): 
        request.data['user'] = request.user.id
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def get(self, request):
        sessions = Session.objects.filter(user=request.user)
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def delete(self, request):
        session = Session.objects.get(id=request.data['id'])
        if session.user != request.user:
            return Response('You are not authorized to delete this session', status=403)
        if not  session:
            return Response('Session does not exist', status=404)
        session.delete()
        return Response('Session deleted successfully')
    

class SimpleQuestionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        questions = get_questions(request.data['text'], request.data['lang'])
        questions_str = str(questions)
        request.data['question'] = questions_str
        print(request.data)
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print('############')
            print(request.data)
            print('############')
            print(serializer.data)
            print('############')
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def get(self, request):
        questions = Question.objects.filter(session=request.data['session'])
        serializer = QuestionSerializer(questions, many=True)
        for question in serializer.data:
            question['question'] = eval(question['question'])
        return Response(serializer.data)

    def delete(self, request):
        question = Question.objects.get(id=request.data['id'])
        if question.session.user != request.user:
            return Response('You are not authorized to delete this question', status=403)
        if not  question:
            return Response('Question does not exist', status=404)
        question.delete()
        return Response('Question deleted successfully')

