import datetime
from flask import request, jsonify
import app.db as Data
from app.api.token_required import token_required
from flask_restful import Resource

class UserDetails(Resource):
    @token_required
    def get(self, user):
        try:
            ret = Data.getuserdetials(user)
            return {"status": "success", "data": ret}
        except Exception as e:
            print(repr(e))
            return jsonify({"subject": "failure"})

    @token_required
    def put(self, user):
        try:
            data = request.get_json()
            name = data["name"]
            gender = data["gender"]
            mob = data["mob"]
            dob = data["dob"]
            bio = data["bio"][0:254]

            if not dob:
                dob = "0000-00-00"
                age = 0
            else:
                age = get_years(dob)

            if not mob:
                mob = 0

            u = Data.update(name=name, age=age, gender=gender, mob=mob,
                            dob=datetime.datetime.strptime(dob, "%Y-%m-%d").date(), uid=user.id, bio=bio)
            if u == mob:
                return {"status": "mob"}
            elif u:
                return {"status": "success"}
            else:
                return {"status": "failure"}
        except KeyError:
            return {"status": "logout"}



def get_years(dob: str) -> int:
    _y, _m, _d = dob[:4], dob[5:7], dob[8:]
    cur = str(datetime.date.today())
    c_y, c_m, c_d = cur[:4], cur[5:7], cur[8:]
    dif_y, dif_m, dif_d = int(c_y) - int(_y), int(c_m) - int(_m), int(c_d) - int(_d)
    if dif_m < 0:
        dif_y -= 1
    elif dif_m == 0 and dif_d < 0:
        dif_y -= 1
    return dif_y