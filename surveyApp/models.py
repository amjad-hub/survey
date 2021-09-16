from django.db import models

# My models

class Survey(models.Model):
    survey_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    end_date = models.DateTimeField()
    survey_description = models.CharField(max_length=200)


class Question(models.Model):
    class Type:
        TEXT = 'TEXT'
        OPTION = 'OPTION'
        MULTIOPTION = 'MULTIOPTION'

        choices = (
            (TEXT, 'TEXT'),
            (OPTION, 'OPTION'),
            (MULTIOPTION, 'MULTIOPTION'),
        )

    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=300)
    question_type = models.CharField(max_length=200, choices=Type.choices, default=Type.TEXT)



class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)




class Answer(models.Model):
    user_id = models.IntegerField()
    survey = models.ForeignKey(Survey, related_name='survey', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='question', on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, related_name='choice', on_delete=models.CASCADE, null=True)
    choice_text = models.CharField(max_length=200, null=True)
