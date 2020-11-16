from django import template
import math

register = template.Library()

@register.simple_tag
def checkTopMenuActive(currentMenu, selectedMenu):
   return 'active' if currentMenu == selectedMenu else '' 

@register.simple_tag
def getScore(correctCount, questionCount):
   if questionCount == 0 or correctCount == 0: 
      return 0
   return math.ceil(correctCount / questionCount * 100)

@register.simple_tag
def getLevelString(level):
   if level == '1':
      lstring = 'Mild'
   elif level == '2':
      lstring = 'Hot'
   elif level == '3':
      lstring = 'Spicy'
   elif level == '4':
      lstring = 'Supercharger'
   return lstring

@register.simple_tag
def getLevelClassColor(level):
   if level == '1':
      lstring = 'text-success'
   elif level == '2':
      lstring = 'text-info'
   elif level == '3':
      lstring = 'text-primary'
   elif level == '4':
      lstring = 'text-danger'
   return lstring


@register.filter()
def to_nextlevel(value):
   nextLevel = int(value)
   nextLevel += 1
   return str(nextLevel) if nextLevel <= 4 else 4