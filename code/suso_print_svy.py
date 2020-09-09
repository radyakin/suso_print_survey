# ======= PRINT INTERVIEWS REPORT ON SURVEY SOLUTIONS EXPORTED DATA =========
# ======== Sergiy RADYAKIN, The World Bank, 2020 ============================


import bleach
import json
from sfi import Data, Macro, Scalar, Missing, SFIToolkit

def PrintInterview(data,i):
  ikey=Data.get(var='interview__key', obs=i)[0][0]
  print("")
  print("Interview: ", i+1)
  print("Key: ", ikey)
  SFIToolkit.stata("putpdf sectionbreak, pagesize(A5)")
  SFIToolkit.stata("putpdf paragraph")
  SFIToolkit.stata('''putpdf text ("'''+ikey+'''"), bold font("Arial", 18, "green")''')  
  TraverseSections(data['Children'],i)

def PrintQText(item,i):
  qt=bleach.clean(item['QuestionText'], tags=[], strip=True)
  SFIToolkit.stata("putpdf paragraph")
  SFIToolkit.stata('''putpdf text (`"''' + qt + '''"'), bold font("Arial", 8)''')

def PrintAnswer(s):
  SFIToolkit.stata('''putpdf text (`"\n''' + s + '''"'), italic font("Arial", 8, blue)''')

def PrintText(item,i):
  vn=item['VariableName']
  answer=Data.get(var=vn, obs=i)[0][0]
  if (answer=="##N/A##"):
    answer="[NO ANSWER RECORDED]"
  if (answer!=''):
    PrintQText(item,i)
    PrintAnswer(answer)
    
def PrintDate(item,i):
  vn=item['VariableName']
  answer=Data.get(var=vn, obs=i)[0][0]
  if (answer=="##N/A##"):
    answer="[NO ANSWER RECORDED]"
  if (answer!=''):
    PrintQText(item,i)
    PrintAnswer(answer)
  
def PrintNumeric(item,i):
  vn=item['VariableName']
  answer=Data.get(var=vn, obs=i)[0][0]
  sanswer=str(answer)
  if (answer==-999999999):
    sanswer="[NO ANSWER RECORDED]"
  if (Missing.isMissing(answer)==False):
    PrintQText(item,i)  
    PrintAnswer(sanswer)
    
def PrintGPS(item,i):
  vn=item['VariableName']
  latitude=Data.get(var=vn+"__Latitude", obs=i)[0][0]
  
  if (Missing.isMissing(latitude)):
    return()
  
  PrintQText(item,i) 

  sanswer=""
  if (latitude==-999999999):
    sanswer="[NO ANSWER RECORDED]"
  else:
    longitude=Data.get(var=vn+"__Longitude", obs=i)[0][0]
    sanswer="Lat="+str(latitude)+"; Lon="+str(longitude)
    
  PrintAnswer(sanswer)

def PrintMulti(item,i):
  vn=item['VariableName']
  PrintQText(item,i)  
  for opt in item['Answers']:
    vvv=vn+"__"+str(opt['AnswerValue'])
    v=Data.get(var=vvv, obs=i)[0][0]
    if (v==1):
      sanswer="☑ " + opt['AnswerText']
      PrintAnswer(sanswer)

def PrintSingle(item,i):
  vn=item['VariableName']
  answer=Data.get(var=vn, obs=i)[0][0]
  sanswer=str(answer)
  if (answer==-999999999):
    sanswer="[NO ANSWER RECORDED]"
  if (answer< 1.0e300):
    # need to get the value label here from Stata
    sanswer=Data.get(var=vn,obs=i,valuelabel=True)[0][0]
    PrintQText(item,i)
    if (item['LinkedToRosterId']!=None or item['LinkedToQuestionId']!=None):
      print("Linked questions not supported, skipping")
    else:
      PrintAnswer("✓ " + sanswer)
    
def PrintList(item, i):

    PrintQText(item,i)
    answer=Data.get(var=item['VariableName']+"__0", obs=i)[0][0]
    if (answer=="##N/A##"):
      answer="[NO ANSWER RECORDED]"
    else:
      count=item['MaxAnswerCount']
      for c in range(0, count-1):
        vn=item['VariableName']+"__"+str(c)
        eachanswer=Data.get(var=vn, obs=i)[0][0]
        if (eachanswer=="##N/A##"):
          break
        PrintAnswer("* " + eachanswer)

def PrintQuestion(q,i):
  vn=q['VariableName']
  SFIToolkit.stata("capture unab varlst : "+vn+"__*")
  if (Scalar.getValue("_rc"))!=0:
    if (Macro.getLocal("varlst")=="") :
      try:
        vindex=Data.getVarIndex(vn)
        # SERGIY: this kicks out all the questions where the variable name 
		# has been transformed, such as option__1, or location__Longitude.
      except:
        print("Data for " + vn + " in roster, skipped")
        return
  qt=q['QuestionType']
  
  # Single-select categorical
  if (qt==0): 
    PrintSingle(q,i)
    return()
    
  # Multi-select categorical
  if (qt==3):
    PrintMulti(q,i)
    return()
  
  # Numeric
  if (qt==4):
    PrintNumeric(q,i)
    return()
    
  # Date
  if (qt==5):
    PrintDate(q,i)
    return()
    
  # GPS
  if (qt==6):
    PrintGPS(q,i)
    return()
    
  # Text
  if (qt==7):
    PrintText(q,i)
    return()

  # List
  if (qt==9):
    PrintList(q,i)
    return
    
  print("%%%%%%%%%%%%%%%%%%%%%%%%UNKNOWN QUESTION TYPE:", str(qt))
  print(q['QuestionText'])


def PrintSection(ch):
  SFIToolkit.display("{text}   "+ch['Title'])
  SFIToolkit.stata("putpdf paragraph")
  SFIToolkit.stata('putpdf text ("'+ch['Title']+'"), bold font("Arial", 14, "navy")')

def PrintRoster(roster,i):
  SFIToolkit.display("{text}   "+roster['Title'])
  SFIToolkit.stata("putpdf paragraph")
  SFIToolkit.stata('putpdf text ("'+roster['Title']+'"), font("Arial", 14, "darkgreen")')

  # preserve current data frame name, switch to roster data frame
  # TraverseChildren(roster['Children'],i)
  # switch to the preserved data frame
  
def ProcessChild(ch,i):
    if 'IsRoster' in ch:
      if ch['IsRoster']==False:
        TraverseChildren(ch['Children'],i)
      else:
        PrintRoster(ch,i)
    else:
      if 'QuestionType' in ch:
        PrintQuestion(ch,i)
    
def TraverseSections(children,i):
  for ch in children:
    PrintSection(ch)
    ProcessChild(ch,i)

def TraverseChildren(children,i):
  for ch in children:
    ProcessChild(ch,i)

pdfname="C:/temp/" + Macro.getLocal("f")
fn=Macro.getLocal("path")+"/"+Macro.getLocal("f")+".json"

with open(fn, 'r', encoding='utf-8') as f:
  data = json.load(f)

qtitle=data['Title']
n=Data.getObsTotal()

SFIToolkit.stata("putpdf begin, pagesize(A5)")
SFIToolkit.stata("putpdf paragraph")
SFIToolkit.stata('''putpdf text ("''' + qtitle + '''"), bold font("Arial", 18, "maroon") linebreak(1)''')
SFIToolkit.stata('''putpdf text ("Generated on:''' + Macro.getGlobal("c(current_date)") + " at " + Macro.getGlobal("c(current_time)") + '''"), bold font("Arial", 14, "green") linebreak(1)''')
SFIToolkit.stata('''putpdf text ("Interviews:''' + str(n) + '''"), bold font("Arial", 14, "green") linebreak(1)''')
i=0
while (i<n):
  PrintInterview(data, i)
  i=i+1

print("")
print("Saving the report to "+pdfname)
SFIToolkit.stata('''putpdf text (`" test "'), bold font("Arial", 8)''')
SFIToolkit.stata('''putpdf save "''' + pdfname + '''", replace''')


# END OF FILE
