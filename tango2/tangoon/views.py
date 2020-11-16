from django.shortcuts import render, redirect
from django.http import HttpResponse
from tango2.settings import BASE_DIR, TANGO_ANNOTATION_DIR
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from tangoweb.functions import examDotsInput
from tangoweb.models import UserCompetition, UserCompetitionBoard
from django.utils import timezone
from django.db.models import Sum
from django.db.models import F

from PIL import Image
from pathlib import Path

import os
import json
import datetime
import random
import math

def getOnePracticePatch(username, level):
    # get all patches
    patchDataPath = Path(os.path.join(BASE_DIR, 'static/patch/competition/', level, 'image/'))
    patchFiles = [ 
        p for p in patchDataPath.iterdir() if not p.name.startswith('.') 
    ]
    patchStems = [ p.stem for p in patchFiles ]
    for eachStem in patchStems: # because some files have prefix, it has to be removed...
        pos = eachStem.find('_')
        eachStem = eachStem[pos + 1:]

    # get user done patches
    userAnnotationPath = os.path.join(BASE_DIR, TANGO_ANNOTATION_DIR, username)
    userCompetitionPath = Path(os.path.join(userAnnotationPath, 'competition', level))
    if userCompetitionPath.exists():
        doneFiles = [ p for p in userCompetitionPath.iterdir() if not p.name.startswith('.') ]
        doneStems = [ p.stem for p in doneFiles ]
 
    else:
        doneFiles = []
        doneStems = []

    # select one image
    availableStems = [ file for file in patchStems if file not in doneStems ]
    availableStem = None
    if len(availableStems):
        availableStem = f'{random.choice(availableStems)}.png' 

    return availableStem, len(patchFiles), len(doneFiles)


def getCompetitionLevel(request):
    aUserBoards = UserCompetitionBoard.objects.filter(user=request.user).order_by('level')
    level = 1
    for aBoard in aUserBoards:
        if aBoard.questioncount == 0: continue
        score = math.ceil(aBoard.correctcount / aBoard.questioncount * 100)
        if level >= aBoard.level and score >= 50:
            level = aBoard.level + 1

    level = 4 if level > 4 else level 
    return str(level)


@login_required
def home(request):
    # this is tempoary but if there are many levels, change the code below
    aUserBoards = UserCompetitionBoard.objects.filter(user=request.user).order_by('correctcount')
    level2 = level3 = level4 = 0
    for aBoard in aUserBoards:
        if aBoard.questioncount == 0: continue
        score = math.ceil(aBoard.correctcount / aBoard.questioncount * 100)
        if aBoard.level == 1 and score >= 50:
            level2 = 1
        elif aBoard.level == 2  and score >= 50:
            level3 = 1
        elif aBoard.level == 3  and score >= 50:
            level4 = 1         

    context = {
        'top': 'competition',
        'boards': aUserBoards,
        'level1': 1,            # Always make active
        'level2': level2,
        'level3': level3, 
        'level4': level4
    }
    return render(request, 'tangoon/home.html', context)


# Create your views here.
@login_required
def competition(request, level=1, attempt=0):
    username = request.user.username

    patchFile, cntTotal, cntDone = getOnePracticePatch(username, level)
    patch_width = 256
    patch_height = 256

    if patchFile is not None:
        fullImagePath = os.path.join(BASE_DIR, 'static/patch/competition/', level, 'image/', patchFile)
        try:
            aImage = Image.open(fullImagePath)
            patch_width, patch_height = aImage.size
        except Exception as e:
            print("Competition Error:", e)
            return redirect('tangoon-home')
    else:
        return redirect('tangoon-end', level, attempt)

    context = {
        'top': 'competition',
        'patch' : patchFile,
        'patch_total': cntTotal,
        'patch_done': cntDone + 1, # the existing number + 1
        'patch_width' : patch_width,
        'patch_height' : patch_height,
        'level': level,
        'attempt': attempt
    }
    return render(request, 'tangoon/competition.html', context)


@login_required
def save(request, level=1, attempt=0):
    # check whether no patch is or not
    patchFile = request.POST.get('patch')
    if patchFile == '': return redirect('tangoon-home')

    # Create user path if it is not existed.
    username = request.user.username
    userAnnotationPath = os.path.join(BASE_DIR, TANGO_ANNOTATION_DIR, username)
    userCompetitionPath = os.path.join(userAnnotationPath, 'competition')
    userCompetitionLevelPath = os.path.join(userCompetitionPath, level)
    try:
        if not os.path.isdir(userAnnotationPath): os.mkdir(userAnnotationPath)
        if not os.path.isdir(userCompetitionPath): os.mkdir(userCompetitionPath)
        if not os.path.isdir(userCompetitionLevelPath): os.mkdir(userCompetitionLevelPath)
    except Exception as e:
        print("Save Error:", e)
        return redirect('tangoweb-home')

    patchName = Path(patchFile).stem

    # Load JSON form data of coordinates
    dotsString = request.POST.get('dots')
    if dotsString is None or dotsString == '':
        dots = []
    else:
        dots = json.loads(dotsString)
    
    # Create a dictionary for annotation data
    dicAnnotation = {
        'name': username,
        'dots': dots,
        'ip': request.META.get("REMOTE_ADDR"),
        'serverUTCDate': datetime.datetime.utcnow().isoformat(),
        'clientDate': '',
        'userAgent': {
            'browser': request.META.get("HTTP_USER_AGENT"),
            'version': request.META.get("TERM_PROGRAM_VERSION"),
            'language': request.META.get("LANG"),
        },
    }
    
    annotationFile = os.path.join(userCompetitionLevelPath, f'{patchName}.json')
    json.dump(dicAnnotation, open(str(annotationFile), 'w'), indent=2)
    
    # save result to database
    if request.method == 'POST':
        patchFile, answerDots, cntAnswer, cntMatched, cntQuestion = examDotsInput(request, level)

        # Add competition result to Database.
        aCompetition  = UserCompetition()
        aCompetition.patch = Path(patchFile).stem
        aCompetition.answercount = cntAnswer
        aCompetition.correctcount = cntMatched
        aCompetition.questioncount = cntQuestion
        aCompetition.user = request.user
        aCompetition.level = level
        aCompetition.attempt = attempt
        aCompetition.save()

    return redirect('tangoon-competition', level=level, attempt=attempt)

def getCompetitionAttempt(userHistoryPath):
    # get attempt count
    cntAttempt = 0
    if userHistoryPath.exists():
        attemptDirs = [ p for p in userHistoryPath.iterdir() if not p.name.startswith('.') ]
        cntAttempt = len(attemptDirs)
    
    return cntAttempt

def getCompetionInformation(username, level):
    # get user done patches
    userAnnotationPath = os.path.join(BASE_DIR, TANGO_ANNOTATION_DIR, username)

    # get attempt count
    userHistoryPath  = Path(os.path.join(userAnnotationPath, 'history', level))
    cntAttempt = getCompetitionAttempt(userHistoryPath)

    # get competition count
    userCompetitionPath = Path(os.path.join(userAnnotationPath, 'competition', level))
    cntDone = 0
    if userCompetitionPath.exists():
        doneFiles = [ p for p in userCompetitionPath.iterdir() if not p.name.startswith('.') ]
        cntDone = len(doneFiles)

    # get total competition count
    competitionPatchPath = Path(os.path.join(BASE_DIR, 'static/patch/competition/', level, 'image/'))
    cntToal = 0
    if competitionPatchPath.exists():
        patchFiles = [ p for p in competitionPatchPath.iterdir() if not p.name.startswith('.') ]
        cntTotal = len(patchFiles)

    cntRemaining = cntTotal - cntDone
    return cntAttempt, cntDone, cntTotal, cntRemaining


@login_required
def start(request, level=1):
    userLevel = getCompetitionLevel(request)
    if level > userLevel:
        return redirect('tangoon-home')

    username = request.user.username
    cntAttempt, cntDone, cntTotal, cntRemaining = getCompetionInformation(username, level)

    context = {
        'top': 'competition',
        'attempt': cntAttempt + 1,
        'done': cntDone,
        'total': cntTotal,
        'remaining': cntRemaining,
        'level': level
    }
    return render(request, 'tangoon/start.html', context)


@login_required
def end(request, level=1, attempt=0):
    username = request.user.username
    cntAttempt, cntDone, cntTotal, cntRemaining = getCompetionInformation(username, level)

    userAnnotationPath = os.path.join(BASE_DIR, TANGO_ANNOTATION_DIR, username)
    levelPass = False
    score = 0
    # Move files and Save the result to database
    if cntDone == cntTotal:
        cntAttempt += 1 # add new attemp

        try:
            userHistoryPath = Path(os.path.join(userAnnotationPath, 'history'))
            if userHistoryPath.exists() == False: userHistoryPath.mkdir()

            userHistoryLevelPath  = Path(os.path.join(userHistoryPath, level))
            if userHistoryLevelPath.exists() == False: userHistoryLevelPath.mkdir()
            
            userHistoryLevelAtemptPath = Path(os.path.join(userHistoryLevelPath, str(cntAttempt)))
            if userHistoryLevelAtemptPath.exists() == False: userHistoryLevelAtemptPath.mkdir()

            userCompetitionPath = Path(os.path.join(userAnnotationPath, 'competition', level))
            doneFiles = [ p for p in userCompetitionPath.iterdir() if not p.name.startswith('.') ]
            for aFile in doneFiles:
                aFile.rename(os.path.join(userAnnotationPath, 'history', level, str(cntAttempt), aFile.name))

        except Exception as e:
            return redirect('tangoweb-home')

        # Save the result to database
        sumCounts = UserCompetition.objects.filter(user=request.user, level=level, attempt=attempt).aggregate(Sum('questioncount'), Sum('answercount'), Sum('correctcount'))
        # print(sumCounts)
        aCompetitionBoard = UserCompetitionBoard()
        aCompetitionBoard.user = request.user
        aCompetitionBoard.questioncount = sumCounts['questioncount__sum']
        aCompetitionBoard.answercount = sumCounts['answercount__sum']
        aCompetitionBoard.correctcount = sumCounts['correctcount__sum']
        aCompetitionBoard.level = level
        aCompetitionBoard.attempt = cntAttempt
        aCompetitionBoard.save() 

        # print(aCompetitionBoard.correctcount)
        # print(aCompetitionBoard.questioncount)
        score = math.ceil(aCompetitionBoard.correctcount / aCompetitionBoard.questioncount * 100)
        if score >= 50:
            levelPass = True
    
    aUserBoards = UserCompetitionBoard.objects.filter(user=request.user, level=level).order_by('correctcount')
    context = {
        'top': 'competition',
        'boards': aUserBoards,
        'attempt': cntAttempt,
        'level': level,
        'levelpass': levelPass,
        'score': score
    }
    return render(request, 'tangoon/end.html', context)

@login_required
def leaderboardCompetition(request, level):
    # aUserBoards = UserCompetitionBoard.objects.filter(level=level).order_by('-correctcount')
    aUserBoards = UserCompetitionBoard.objects.filter(level=level).annotate(score=F('correctcount') / F('questioncount')).order_by('-score')
    context = {
        'top': 'leaderboard',
        'boards': aUserBoards,
        'level': level
    }
    return render(request, 'tangoon/leaderboard.html', context)

