from django.apps import AppConfig
from django import db
import time
import random
from multiprocessing import Process
from decimal import Decimal

class UpdatePrices(Process):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        print ('ye run hua')
        # This import needs to be delayed. It needs to happen after apps are
        # loaded so we put it into the method here (it won't work as top-level
        # import)
        from .models import Company, CompanyCMPRecord

        # Because this is a subprocess, we must ensure that we get new
        # connections dedicated to this process to avoid interfering with the
        # main connections. Closing any existing connection *should* ensure
        # this.
        db.connections.close_all()
        loop = 0
        # We can do an endless loop here because we flagged the process as
        # being a "daemon". This ensures it will exit when the parent exists
        while True:
            print ('increasing prices', loop)
            # print ('count: ', CompanyCMPRecord.objects.count())
            for company in Company.objects.all():
                company.current_market_price *= Decimal(random.uniform(0.95, 1.05))
                company.save()
                if loop == 0:
                    print ('saving record')
                    record = CompanyCMPRecord(company=company, cmp=company.current_market_price)
                    record.save()
            
            loop += 1
            loop = loop % 120
            time.sleep(0.5)

class VsmConfig(AppConfig):
    name = 'vsm'

    # def ready(self):
    #     print ('ready me aaaya na')
    #     update = UpdatePrices()
    #     update.start()

