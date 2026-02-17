from flask import jsonify
class ApiResponse:
    def success(self,data=None, message=None, status_code=200):
        response = {
            "success": True,
            "message": message,
            "data": data,
            "errors": None
        }
        return jsonify(response), status_code

    def error(self, message=None, errors=None, status_code=400):
        response = {
            "success": False,
            "message": message,
            "data": None,
            "errors": errors
        }
        return jsonify(response), status_code    
