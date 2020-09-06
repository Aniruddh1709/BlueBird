# from flask import make_response
# from flask.views import MethodView

# from app import db
# from app.utils.constants import HTTP_STATUS_OK


# # class HealthCheckView(MethodView):
# #     def get(self):
# #         try:
# #            # row = db.engine.execute("SELECT 1")
# #             if row is None:
# #                 raise Exception("DB not accessible")
# #         except:
# #             raise Exception("DB not accessible")
# #         return make_response("Success", HTTP_STATUS_OK)
