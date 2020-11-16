from tango2.settings import BASE_DIR
from pathlib import Path
from dotmap import DotMap
import json
import math
import os

def examDotsInput(request, level=None):
    # get user done patches
    patchFile = request.POST.get('patch')
    patchName = Path(patchFile).stem

    try:
        if level is None:
            level = request.POST.get('level')
            patchJSONFile = os.path.join(BASE_DIR, 'static/patch/practice/', level, 'json/', f'{patchName}.json')
        else:
            patchJSONFile = os.path.join(BASE_DIR, 'static/patch/competition/', level, 'json/', f'{patchName}.json')
        
        with open(patchJSONFile) as f:
            answerDots = json.load(f)
    except IOError:
        answerDots = {}
        print("File not accessible")

    aAnswer = DotMap(answerDots)

    # get user input
    dotsString = request.POST.get('dots')
    if dotsString is None or dotsString == '':
        listDots = []
    else:
        listDots = json.loads(dotsString)

    aInput = DotMap()
    aInput.dots = [ DotMap(aDot) for aDot in listDots ]
    for aAnswerDot in aAnswer.dots: aAnswerDot.Matched = False

    cntMatched = 0
    valueIntersection = 100 + 100 # Extra 50 because CTX lineWidth in JavaScript
    for aInputDot in aInput.dots:
        aInputDot.Result = False
        # print(aInputDot)
        for aAnswerDot in aAnswer.dots:
            # print(aAnswerDot)
            valueOverlay = math.pow(aInputDot.x - aAnswerDot.x, 2) + math.pow(aInputDot.y - aAnswerDot.y, 2)
            if valueOverlay <= valueIntersection and aInputDot.type == aAnswerDot.type and aAnswerDot.Matched == False:
                aInputDot.Result = True
                aAnswerDot.Matched = True
                cntMatched += 1
                break

    return patchFile, answerDots, len(aInput.dots), cntMatched, len(aAnswer.dots)

