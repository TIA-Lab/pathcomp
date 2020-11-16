from django.shortcuts import render, redirect
from django.http import HttpResponse
from tango2.settings import BASE_DIR, TANGO_ANNOTATION_DIR
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from tangoweb.models import UserPractice, UserPracticeBoard
from tangoweb.functions import examDotsInput

from PIL import Image
from pathlib import Path
from dotmap import DotMap

import os
import json
import datetime
import random

# def getOnePracticePatch(username, practiceImagePath='static/patch/practice/image/'):
#     # get all patches
#     patchDataPath = Path(os.path.join(BASE_DIR, practiceImagePath))
#     patchFiles = [ 
#         p for p in patchDataPath.iterdir() if not p.name.startswith('.') 
#     ]
#     patchStems = [ p.stem for p in patchFiles ]
#     for eachStem in patchStems: # because some files have prefix, it has to be removed...
#         pos = eachStem.find('_')
#         eachStem = eachStem[pos + 1:]

#     # get user done patches
#     userAnnotationPath = os.path.join(BASE_DIR, TANGO_ANNOTATION_DIR, username)
#     userPracticePath = Path(os.path.join(userAnnotationPath, 'practice'))

#     if userPracticePath.exists():
#         doneFiles = [ p for p in userPracticePath.iterdir() if not p.name.startswith('.') ]
#         doneStems = [ p.stem for p in doneFiles ]
#     else:
#         doneFiles = []
#         doneStems = []

#     # select one image
#     availableStems = [ file for file in patchStems if file not in doneStems ]
#     availableStem = None
#     if len(availableStems):
#         availableStem = f'{random.choice(availableStems)}.png' 

#     return availableStem, len(patchFiles), len(doneFiles)


def getOnePracticePatch(level, patch, practiceImagePath='static/patch/practice/'):
    # get all patches
    patchDataPath = Path(os.path.join(BASE_DIR, practiceImagePath, level, 'image'))
    patchFiles = [ 
        p for p in patchDataPath.iterdir() if not p.name.startswith('.') 
    ]
    patchStems = [ p.stem for p in patchFiles ]
    for eachStem in patchStems: # because some files have prefix, it has to be removed...
        pos = eachStem.find('_')
        eachStem = eachStem[pos + 1:]

    doneStems = []
    if patch != None:
        doneStems.append(Path(patch).stem)

    # select one image
    availableStems = [ file for file in patchStems if file not in doneStems ]
    availableStem = None
    if len(availableStems):
        availableStem = f'{random.choice(availableStems)}.png' 

    return availableStem, len(patchFiles)

# Create your views here.
@login_required
def home(request):
    context = {}
    return render(request, 'tangooff/home.html', context)


@login_required
def practice(request, level, patch=None):
    if level != '1' and level != '2': 
        return redirect('tangoweb-home')

    patchFile, cntTotal = getOnePracticePatch(level, patch)
    patch_width = 256
    patch_height = 256

    if patchFile is not None:
        fullImagePath = os.path.join(BASE_DIR, 'static/patch/practice/', level, 'image/', patchFile)
        try:
            aImage = Image.open(fullImagePath)
            patch_width, patch_height = aImage.size
        except Exception as e:
            print(e)
            return redirect('tangoweb-home')

    aPracticeBoard = UserPracticeBoard.objects.filter(user=request.user).first()
    patch_point = 0
    if aPracticeBoard is not None:
        patch_point = aPracticeBoard.point
    context = {
        'top': 'practice',
        'level': level,
        'patch' : patchFile,
        'patch_total': cntTotal,
        'patch_width': patch_width,
        'patch_height': patch_height,
        'patch_point': patch_point 
    }
    return render(request, 'tangooff/practice.html', context)

@login_required
def display(request):
    if request.method == 'POST':
        patchFile, answerDots, cntAnswer, cntMatched, cntQuestion = examDotsInput(request)
        aDocument = {
            'patch': patchFile,
            'data': answerDots,
            'matched': cntMatched
        }

        # Add practice result to Database.
        # aPractice  = UserPractice()
        # aPractice.patch = Path(patchFile).stem
        # aPractice.answercount = cntAnswer
        # aPractice.correctcount = cntMatched
        # aPractice.questioncount = cntQuestion
        # aPractice.user = request.user
        # aPractice.save()

        # aPracticeBoard = UserPracticeBoard.objects.filter(user=request.user).first()
        # if aPracticeBoard is None:
        #     aPracticeBoard = UserPracticeBoard()
        #     aPracticeBoard.user = request.user
        #     aPracticeBoard.point = 0
        #     aPracticeBoard.save() 
        # else:
        #     aPracticeBoard.point += cntMatched
        #     aPracticeBoard.updated = timezone.now()
        #     aPracticeBoard.save()

    response = JsonResponse(aDocument)
    response.status_code = 200
    return response


@login_required
def leaderboardPractice(request):
    aUserBoards = UserPracticeBoard.objects.filter().order_by('-point')
    context = {
        'top': 'leaderboard',
        'boards': aUserBoards,
    }
    return render(request, 'tangooff/leaderboard.html', context)


@login_required
def save(request):
    # check whether no patch is or not
    patch = request.POST.get('patch')
    level = request.POST.get('level')
    if patch == '': return redirect('tangooff-home')

    # # Create user path if it is not existed.
    # username = request.user.username
    # userAnnotationPath = os.path.join(BASE_DIR, TANGO_ANNOTATION_DIR, username)
    # userPracticePath = os.path.join(userAnnotationPath, 'practice')
    # try:
    #     if not os.path.isdir(userAnnotationPath): os.mkdir(userAnnotationPath)
    #     if not os.path.isdir(userPracticePath): os.mkdir(userPracticePath)
    # except Exception as e:
    #     return redirect('tangoweb-home')

    # patchName = Path(patchFile).stem

    # # Load JSON form data of coordinates
    # dotsString = request.POST.get('dots')
    # if dotsString is None or dotsString == '':
    #     dots = []
    # else:
    #     dots = json.loads(dotsString)
    
    # # Create a dictionary for annotation data
    # dicAnnotation = {
    #     'name': username,
    #     'dots': dots,
    #     'ip': request.META.get("REMOTE_ADDR"),
    #     'serverUTCDate': datetime.datetime.utcnow().isoformat(),
    #     'clientDate': '',
    #     'userAgent': {
    #         'browser': request.META.get("HTTP_USER_AGENT"),
    #         'version': request.META.get("TERM_PROGRAM_VERSION"),
    #         'language': request.META.get("LANG"),
    #     },
    # }
    
    # annotationFile = os.path.join(userPracticePath, f'{patchName}.json')
    # json.dump(dicAnnotation, open(str(annotationFile), 'w'), indent=2)
    return redirect('tangooff-practice', level=level, patch=patch)


# @login_required
# def test(request):
#     username = request.user.username

#     patchFile, cntTotal, cntDone = getOnePracticePatch(username, 'static/patch/practice/image_test/')
#     patch_width = 256
#     patch_height = 256

#     if patchFile is not None:
#         fullImagePath = os.path.join(BASE_DIR, 'static/patch/practice/image_test/', patchFile)
#         try:
#             aImage = Image.open(fullImagePath)
#             patch_width, patch_height = aImage.size
#         except Exception as e:
#             print(e)
#             return redirect('tangoweb-home')

#     context = {
#         'patch' : patchFile,
#         'patch_total': cntTotal,
#         'patch_done': cntDone,
#         'patch_width' : patch_width,
#         'patch_height' : patch_height
#     }
#     return render(request, 'tangooff/test.html', context)


# @login_required
# def testsave(request):
#     # check whether no patch is or not
#     patchFile = request.POST.get('patch')
#     if patchFile == '': return redirect('tangooff-home')

#     # Create user path if it is not existed.
#     username = request.user.username
#     userAnnotationPath = os.path.join(BASE_DIR, TANGO_ANNOTATION_DIR, username)
#     userPracticePath = os.path.join(userAnnotationPath, 'practice')
#     try:
#         if not os.path.isdir(userAnnotationPath): os.mkdir(userAnnotationPath)
#         if not os.path.isdir(userPracticePath): os.mkdir(userPracticePath)
#     except Exception as e:
#         return redirect('tangoweb-home')

#     patchName = Path(patchFile).stem

#     # Load JSON form data of coordinates
#     dotsString = request.POST.get('dots')
#     if dotsString is None or dotsString == '':
#         dots = []
#     else:
#         dots = json.loads(dotsString)
    
#     # Create a dictionary for annotation data
#     dicAnnotation = {
#         'name': username,
#         'dots': dots,
#         'ip': request.META.get("REMOTE_ADDR"),
#         'serverUTCDate': datetime.datetime.utcnow().isoformat(),
#         'clientDate': '',
#         'userAgent': {
#             'browser': request.META.get("HTTP_USER_AGENT"),
#             'version': request.META.get("TERM_PROGRAM_VERSION"),
#             'language': request.META.get("LANG"),
#         },
#     }
    
#     annotationFile = os.path.join(userPracticePath, f'{patchName}.json')
#     json.dump(dicAnnotation, open(str(annotationFile), 'w'), indent=2)
    
#     return redirect('tangooff-home')

# @login_required
# def testdisplay(request):
#     if request.method == 'POST':
#         patchFile, answerDots, cntAnswer, cntMatched, cntQuestion = examDotsInput(request)
#         aDocument = {
#             'patch': patchFile,
#             'data': answerDots,
#             'matched': cntMatched
#         }

#         # Add practice result to Database.
#         # aPractice  = UserPractice()
#         # aPractice.patch = Path(patchFile).stem
#         # aPractice.answercount = cntAnswer
#         # aPractice.correctcount = cntMatched
#         # aPractice.questioncount = cntQuestion
#         # aPractice.user = request.user
#         # aPractice.save()


#     response = JsonResponse(aDocument)
#     response.status_code = 200
#     return response
