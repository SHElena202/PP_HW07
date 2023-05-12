from django.contrib.gis import serializers

from questions.models import Questions, Answers


class QuestionSerializer(serializers.HyperlnkedModelSerialize):
    author = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = Questions
        fields = ['title', 'body', 'create_date', 'author', 'tags']

class AnswerSerializer(serializers.HyperlnkedModelSerializer):
    author = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')

    class Meta:
        model = Answers
        fields = ['body', 'author', 'create_date', 'correct']


class TrendsSerializer:
    pass