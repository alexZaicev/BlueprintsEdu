from flask_restful import Resource


class Help(Resource):

    def get(self):
        r = dict()
        r["/help"] = "[GET] Lists all available API calls to the generator"
        r["/car-sim"] = "Car simulator API"
        r["/car-sim/generate"] = "[POST] Call to generate Car Simulator game"
        return r

