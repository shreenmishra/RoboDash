from robot.api import ResultVisitor

class TagResults(ResultVisitor):

    def __init__(self, tag_list):
        self.tag_list = tag_list

    def visit_test(self, test):
        for tag in test.tags:
            tag_json = {
                "Tag Name": tag,
                "Suite Name": test.parent,
                "Test Name": test,
                "Test Id": test.id,
                "Status": test.status,
                "Time": test.elapsedtime,
                "Message": test.message,
            }
            self.tag_list.append(tag_json)
