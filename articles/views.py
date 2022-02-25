from http import HTTPStatus
from django.forms import model_to_dict

from django.http import Http404, HttpRequest
from django.views.decorators.csrf import csrf_exempt

from myproject.utils import success, error
from myproject.middleware import is_auth, parseJson

from users.models import User

from .models import Article, Comment

@csrf_exempt
@parseJson
@is_auth()
def articles(request: HttpRequest): 
    if request.method == 'GET':
        articles = Article.objects.values()
        articles = list(articles)
        return success(HTTPStatus.OK, data=articles)

    if request.method == 'POST':
        userId = request.user['data']['user_id'] 
        
        try:
            User.objects.get(pk=userId)
        except User.DoesNotExist:
            return error(HTTPStatus.NOT_FOUND, "User not found")

        data = request.json
        title = data.get('title', None)
        subtitle = data.get('subtitle', None)
        thumbnail = data.get('thumbnail', None)
        content = data.get('content', None)

        newArticle = Article(user_id = userId, title=title, subtitle=subtitle, thumbnail=thumbnail, content=content)
        try:
            newArticle.save()
        except Exception as e:
            print(e)
            return error(message='Something went wrong')
        
        return success(HTTPStatus.CREATED, data=model_to_dict(newArticle))

    if request.method == 'PUT':
        data = request.json
        articleId = data.get('id', None)

        try:
            article = Article.objects.get(pk=articleId)
        except Article.DoesNotExist:
            return error(HTTPStatus.NOT_FOUND, "Article not found")

        userId = request.user['data']['user_id']
        if article.user_id != userId:
            return error(HTTPStatus.FORBIDDEN, "You can't edit this article")

        article.title = data.get('title', article.title)
        article.subtitle = data.get('subtitle', article.subtitle)
        article.thumbnail = data.get('thumbnail', article.thumbnail)
        article.content = data.get('content', article.content)

        try:
            article.save()
        except Exception as e:
            print(e)
            return error(message='Something went wrong')

        return success(HTTPStatus.OK, data=model_to_dict(article))

    raise Http404

@csrf_exempt
@parseJson
@is_auth()
def article_detail(request: HttpRequest, pk): 
    if request.method == 'GET':
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return error(HTTPStatus.NOT_FOUND, "Article not found")

        return success(HTTPStatus.OK, data=model_to_dict(article))
    
    if request.method == 'DELETE':
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return error(HTTPStatus.NOT_FOUND, "Article not found")

        userId = request.user['data']['user_id']
        if article.user_id != userId:
            return error(HTTPStatus.FORBIDDEN, "You can't delete this article")

        try:
            article.delete()
        except Exception as e:
            print(e)
            return error(message='Something went wrong')
        
        return success(HTTPStatus.OK, data=model_to_dict(article))

def article_comments(request: HttpRequest, pk):
    if request.method == 'GET':
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return error(HTTPStatus.NOT_FOUND, "Article not found")

        comments = Comment.objects.filter(article_id=pk)
        comments = list(comments.values())
        return success(HTTPStatus.OK, data=comments)

@csrf_exempt
@parseJson
@is_auth()
def comments(request: HttpRequest):
    if request.method == 'POST':
        data = request.json
        article_id = data.get('article_id', None)
        content = data.get('content', None)

        try:
            Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return error(HTTPStatus.NOT_FOUND, "Article not found")

        user_id = request.user['data']['user_id']
        newComment = Comment(user_id = user_id, article_id = article_id, content=content)
        try:
            newComment.save()
        except Exception as e:
            print(e)
            return error(message='Something went wrong')
        
        return success(HTTPStatus.CREATED, data=model_to_dict(newComment))

    if request.method == 'PUT':
        data = request.json
        article_id = data.get('article_id', None)
        comment_id = data.get('comment_id', None)
        content = data.get('content', None)

        try:
            Article.objects.get(pk=article_id)
            comment = Comment.objects.get(pk=comment_id)
        except (Article.DoesNotExist, Comment.DoesNotExist) as e:
            print(e)
            return error(HTTPStatus.NOT_FOUND, "Comment not found")

        user_id = request.user['data']['user_id']
        if user_id != comment.user_id:
            return error(HTTPStatus.FORBIDDEN, "You can't edit this comment")

        try:
            comment.content = content
            comment.save()
        except Exception as e:
            print(e)
            return error(message='Something went wrong')

        return success(HTTPStatus.OK, data=model_to_dict(comment))

@csrf_exempt
@parseJson
@is_auth()
def detail_comment(request: HttpRequest, pk):
    if request.method == 'DELETE':
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return error(HTTPStatus.NOT_FOUND, "Comment not found")

        user_id = request.user['data']['user_id']
        if comment.user_id != user_id:
            return error(HTTPStatus.FORBIDDEN, "You can't delete this comment")

        try:
            comment.delete()
        except Exception as e:
            print(e)
            return error(message='Something went wrong')
        
        return success(HTTPStatus.OK, data=model_to_dict(comment))