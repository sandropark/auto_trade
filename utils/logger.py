from datetime import datetime 
from pytz import timezone
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)
logging.Formatter.converter = lambda *args: datetime.now(tz=timezone('Asia/Seoul')).timetuple()