# Copyright (c) 2012-2015 Netforce Co. Ltd.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

from netforce.controller import Controller
from netforce.model import Model, fields, get_model
from netforce import database
import traceback
import time
import datetime
from netforce import access


class ReturnPaypal(Controller):
    _path = "/ecom_return_paypal"

    def post(self):
        print("POST ARGUMENT >>>>>>>>>>>>>>>>>>>")
        print(self.request.body)
        f = open("paypal_return", "a")
        s = "################################################################################################################" + \
            "\n"
        s += "Date : " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
        s += "Request : " + str(self.request) + "\n"
        if self.request.body:
            s += "Body : " + str(self.request.body) + "\n"
        s += "################################################################################################################" + \
            "\n"
        f.write(s)
        f.close()
        cart_id = int(self.get_argument("cart_id"))
        token = self.get_argument("token", None)
        payer_id = self.get_argument("PayerID", None)
        cart = get_model("ecom.cart").browse(cart_id)
        if not cart.is_paid:
            access.set_active_user(1)
            access.set_active_company(1)
            cart.import_paypal_payment(token, context={})
            db = database.get_connection()
            db.commit()
        self.redirect("/ecom_order_confirmed?cart_id=%s" % cart_id)

ReturnPaypal.register()
