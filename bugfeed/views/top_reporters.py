from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from bugfeed.permissions import ReadOnlyPermissions
from bugfeed.models.users import Users

class TopDebuggersView(APIView):
    permission_classes = [IsAuthenticated & ReadOnlyPermissions]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        topDebuggersList = []
        userIssuesTallyDict = {}
        for user in Users.objects.all():
            userIssuesTallyDict["username"] = user.name
            userIssuesTallyDict["num_issues"] = len(user.issue_creator.all())   
            topDebuggersList.append(userIssuesTallyDict.copy()) 

        def returnNumIssues(user):
            return user['num_issues']

        topDebuggersList.sort(reverse=True, key=returnNumIssues)

        return Response(
            data = topDebuggersList[:4],
            status = status.HTTP_200_OK
        )