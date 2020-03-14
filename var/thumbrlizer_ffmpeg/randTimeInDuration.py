#!/usr/bin/python3
#!/usr/bin/python3
#Copyright Andrea Di Iorio
#This file is part of scripts
#scripts is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#scripts is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with scripts.  If not, see <http://www.gnu.org/licenses/>.
#!/usr/bin/env python3

import datetime,random,sys
from math import floor

#parse from duration string in form h:m:s.subsec and output a random time inside it.

if len(sys.argv)<4:
    print("usage DURATION h:m:s.subsec, fps , output either FRAME or TIME")
duration=sys.argv[1]
h, m, s = map(float, duration.split(':'))
deltha = datetime.timedelta(hours=h, minutes=m, seconds=s)
fps=float(sys.argv[2])
delthaFrames= floor(deltha.total_seconds()*fps)
if sys.argv[3]=="TIME":     #return random frame time
    randTimeInDeltha=random.randint(1,floor(deltha.total_seconds()))
    selectedTime=datetime.timedelta(seconds=randTimeInDeltha)
    outTime='0'+selectedTime.__str__()+'.000')
    print(outTime)
    return outTime
else:           #FRAME MODE-> return random frame index
    randFrameIndx=random.randint(delthaFrames)
    print(randFrameIndx)
    return randFrameIndx

