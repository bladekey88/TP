from .forms import *
from .models import Document, Question, Subject, Topic, User

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect,get_object_or_404

import random
import json
###################################
######## SUBJECT SECTION ##########
###################################
######### CONTAINS ALL ############
######### VIEWS RELATING ##########
########## TO SUBJECT ############
###################################

def index(request): #TO CHANGE TO PROPER NAME
    return render(request, 'questions/landingpage.html')

def subject(request):
    subjects = Subject.objects.all().order_by("subjectname")
    return render(request, 'questions/subject.html', {'subjects':subjects})

@login_required
@permission_required('questions.add_subject',raise_exception=True)
def addsubject(request):   
    if request.method == 'POST':       
        form = AddSubjectForm(request.POST)
        subject_name_entry = request.POST['subjectname']
        subject_name = request.POST['subjectname'].lower()        
        all_subjects =  [x.upper() for x in  Subject.objects.all().values_list('subjectname',flat=True)]
        
        if subject_name.upper() in all_subjects:
            messages.error(request, '<b>Error: </b><em>{}</em> already exists. Validation is case-insensitive (e.g. it and IT will be treated the same for validation against existing subjects).'.format(subject_name_entry))
        
        elif form.is_valid():
            upload_data = form.save(commit=False)
            upload_data = form.save()
            messages.success(request, '<b>Success</b>: </b><em>{}</em> has been added successfully and is now available for use.'.format(subject_name_entry))
    
        else:
            messages.error(request, '<b>Error:</b> The value entered "{}" is invalid. This may be due to an character or a processing error.<br>Please try again. If you encounter further errors please contact a staff member.'.format(subject_name_entry))
        
        return redirect('questions:addsubject')

    else:
        form = AddSubjectForm()
        return render(request, 'questions/subject_add.html', {'form': form, })

def editSubject(request, subjectname):
    subject = get_object_or_404(Subject,subjectname=subjectname)
    
    if request.method =="POST":
        form = EditSubjectForm(request.POST,instance=subject)
        new_subjectname = request.POST['subjectname']
        all_subjects =  [x.upper() for x in  Subject.objects.all().values_list('subjectname',flat=True)]
        
        if new_subjectname.upper() in all_subjects:
            messages.error(request, '<b>Error: </b><em>{}</em> already exists. Validation is case-insensitive (e.g. it and IT will be treated the same for validation against existing subjects).'.format(new_subjectname))
            new_subjectname = subjectname
        
        elif form.is_valid():
            form.save()
            messages.success(request, '<b>Success</b>: </b><em>{}</em> has been updated successfully'.format(new_subjectname))

        return redirect('questions:editsubject', subjectname=new_subjectname)
    
    else:
        form = EditSubjectForm(instance = subject)

    return render(request, 'questions/subject_edit.html', {'subject':subject,'subjectname':subjectname, 'form':form})


@permission_required('questions.delete_subject',raise_exception=True)
def deleteSubject(request, subjectname):
    
    from .utils import createTicketForSubjectDelete
    subject = Subject.objects.get(subjectname=subjectname)
    raiseTicket = createTicketForSubjectDelete(subject,request.user)
    if raiseTicket==201:
        messages.success(request, "<b>Success:</b> The subject '<em>{}</em>' has been flagged for deletion.".format(subject))
    else:
        messages.error(request, "<b>Error:</b> The subject '<em>{}</em>' could not be flagged for deletion - you may have already requested its deletion. Please try again in 60 seconds, or contact a Staff Member.".format(subject))
   
    return redirect("questions:editsubject",subjectname=subjectname)

###################################
######## TOPIC SECTION ##########
###################################
######### CONTAINS ALL ############
######### VIEWS RELATING ##########
########## TO TOPIC ############
###################################
    
def topic(request):    
    topics = Topic.objects.all()
    return render(request, 'questions/topic.html', {'topics':topics})    

@login_required
@permission_required('questions.add_topic',raise_exception=True)
def addtopic(request):
     
    if request.method == 'POST':       
        form = AddTopicForm(request.POST)
        topic_name = request.POST['topicname']
        all_topics =  [x.upper() for x in  Topic.objects.all().values_list('topicname',flat=True)]
        
        if topic_name.upper() in all_topics:
            messages.error(request, '<b>Error: </b><em>{}</em> already exists. Validation is case-insensitive (e.g. C1 and c1 will be treated the same for validation against existing topics).'.format(topic_name))                  
        
        elif form.is_valid():
            upload_data = form.save(commit=False)
            upload_data = form.save()
            messages.success(request, '<b>Success</b>: </b><em>{}</em> has been added successfully and is now available for use.'.format(topic_name))
            
        else:
            messages.error(request, '<b>Error:</b> The value entered "{}" is invalid. This may be due to an character or a processing error.<br>Please try again. If you encounter further errors please contact a staff member.'.format(topic_name))

        
    
    else:
        form = AddTopicForm()
        return render(request, 'questions/topic_add.html', {'form': form, })

@login_required
@permission_required('questions.change_topic',raise_exception=True)
def editTopic(request, topicid):
    topic = get_object_or_404(Topic,pk=topicid)
    
    if request.method =="POST":
        form = EditTopicForm(request.POST,instance=topic)
        new_topicname = request.POST['topicname']
        all_topics =  [x.upper() for x in  Topic.objects.all().values_list('topicname',flat=True)]
        
        if new_topicname.upper() in all_topics:
            messages.error(request, '<b>Error: </b><em>{}</em> already exists. Validation is case-insensitive (e.g. C1 and c1 will be treated the same for validation against existing topics).'.format(new_topicname))
        
        elif form.is_valid():
            form.save()
            messages.success(request, '<b>Success</b>: </b><em>{}</em> has been updated successfully.'.format(new_topicname))
            
        return redirect('questions:edittopic', topicid=topicid)
    
    else:
        form = EditTopicForm(instance = topic)

    return render(request, 'questions/topic_edit.html', {'topic':topic,'topicid':topicid, 'form':form})


@permission_required('questions.delete_topic',raise_exception=True)
def deleteTopic(request, topicid):
    from .utils import createTicketForTopicDelete
    topic = Topic.objects.get(pk=topicid)
    raiseTicket = createTicketForTopicDelete(topic,request.user)
    if raiseTicket==201:
        messages.success(request, "<b>Success:</b> The topic '<em>{}</em>' has been flagged for deletion.".format(topic))
    else:
        messages.error(request, "<b>Error:</b> The topic '<em>{}</em>' could not be flagged for deletion - you may have already requested its deletion. Please try again in 60 seconds, or contact a Staff Member.".format(topic))

    return redirect("questions:edittopic",topicid=topicid)


def topicdetail(request, topicid):
    try:
        
        #questions_linked_to_topic = Question.objects.filter(topicid=topicid)
        topic  = Topic.objects.get(pk=topicid)
        questions_linked_to_topic = topic.question_set.all()
        subjects = set()
        for s in questions_linked_to_topic:
            subjects.add((int(s.subjectid_id), s.subjectid))
        subject = sorted(subjects)
    except Topic.DoesNotExist:
        raise Http404("The Topic does not exist or is not currently accessible to you.")
    return render(request, 'questions/topicdetail.html', {'topic':topic, 'question': questions_linked_to_topic, 'subject' : subject})
    #return HttpResponse("Looking at topic details for TopicID: {} ".format(topicid))
    
###################################
######## QUESTIONS SECTION ########
###################################
######### CONTAINS ALL ############
######### VIEWS RELATING ##########
########## TO QUESTIONS ###########
###################################    
    
def question(request):
    question_count = Question.objects.values('subjectid', 'subjectid__subjectname').order_by('subjectid').annotate(dcount=Count('subjectid'))
    return render(request, 'questions/questions.html', {'question_count':question_count})

@login_required
@permission_required('question.view_question',raise_exception=True)
def questionlist(request,subjectname):
    try:
        question  = Question.objects.filter(subjectid__subjectname=subjectname)        
    except Question.DoesNotExist:
        raise Http404("The Question does not exist or it not currently accessible to you.")

    if len(question) == 0:
        raise Http404("The Question does not exist or it not currently accessible to you.")

    return render(request, 'questions/questionsubject.html', {'question':question} )
 
###################################
######## UPLOAD SECTION ########
###################################
######### CONTAINS ALL ############
######### VIEWS RELATING ##########
########## TO UPLOAD ###########
###################################    
@login_required
@permission_required('questions.add_document',raise_exception=True)
def fileupload(request):
    uploader = User.objects.get(pk=request.user.id)
    if request.method == 'POST':       
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            upload_data = form.save(commit=False)
            upload_data.uploaded_by = uploader
            upload_data = form.save()
            #form.user = request.user
            
            request.session['filepath'] = str(upload_data)
            # sendMessage(request,getSystemID(),request.user.id,"File Upload",fileUploadMessage(request,request.session['filepath']))
            return redirect('questions:fileuploadsuccess')
    else:
        form = DocumentForm()
    return render(request, 'questions/model_form_upload.html', {'form': form, })



@login_required
@permission_required('questions.add_document',raise_exception=True)
def fileupload_success(request):

    if "filepath" not in request.session:
        return redirect('questions:fileupload')
    else:
        #return HttpResponse(settings.MEDIA_URL)
        uploaded_url = request.session['filepath']
        media_url = str(settings.MEDIA_URL[1:])
        return render(request, 'questions/fileupload_success.html', {'full_url': media_url + uploaded_url})
    
    
    
##########################################
##########################################
##########################################
####################################################
######### SELECT QUESTIONS FOR RANDOMNESS ##########
####################################################
# @login_required
def makeQuestion(request):
        if request.method == 'POST':
            
            form = QuestionForm(request.POST)
 
            response_data = {}
            response_data['topicid'] = request.POST.getlist('topicid[]')
            response_data['subjectid'] = request.POST['subjectid']
            response_data['choice_field'] = request.POST['customRadio']
            # response_data['choice_field'] = request.POST['choice_field']
            if 'number_of_questions' in request.POST:
                response_data['number_of_questions'] = request.POST['number_of_questions']
            
            request.session['questiondata'] = response_data
            
            return redirect('questions:createquestions')
        else:
            form = QuestionForm()

        # return render(request, 'upload/question_form.html', {'form': form, })
        return render(request, 'questions/question_generator_form.html', {'form': form, })

# @login_required
def createQuestions(request):


    if "questiondata" not in request.session:
        return redirect('questions:subject_add')
    else:
        subject_id = request.session['questiondata']['subjectid']
        topic_id = request.session['questiondata']['topicid']
        choice_field = request.session['questiondata']['choice_field']
    
        subject_name = Subject.objects.get(pk=subject_id) 
        #choice 1 'oneFromEach'  - 1 Question From Each Selected Topic 
        #choice 2 - 'tenFromEach'  ALl Questions For subject by topic   
        #choice 3  - 'fromMany' ANy Questions from selected topics
        
        # raise Exception()
        if choice_field == 'fromMany':
            number_of_questions = str(request.session['questiondata']['number_of_questions'])
        elif choice_field=='tenFromEach':
            request.session['subject'] = subject_id
            subject =  request.session['subject']
            return render(request,'questions/createquestions.html', {'subject':subject, 'choice_field' : choice_field, 'subject_name':subject_name })
        else:
            number_of_questions = str(1)
          
        

        question_list = []
        
        for topic in topic_id:

            question_dict = {}
            question_dict[topic] = []
            question = Question.objects.filter(subjectid = subject_id, topicid = topic)

            
            for q in question:
                # raise Exception(topic, q.questiontext, q.questionanswer)
                question_dict[topic].append([str(q.topicid),q.questiontext,q.questionanswer])
            question_list.append(question_dict)
        del(question_dict)

        

        question_output = {}
        question_multi_output = []

   

        for topics in question_list:
            for k,v in topics.items():
                question_output[k] = []
                if number_of_questions=='1' and choice_field=='oneFromEach':
                    question_output[k].append(random.choice(v))
                    qm = None
                    qm_json = question_output   
                else:
                    for topic in v:
                        if topic not in question_multi_output:
                            question_multi_output.append(topic)
        
        
        if question_multi_output:
            #randomise the list 
            random.shuffle(question_multi_output)
            qm = []

            ## Do a check to make sure that if we have fewer questions in the bank then specified, 
            ## return them all

            if len(question_multi_output) < (int(number_of_questions)):
                for x in range(0,len(question_multi_output)):
                    qm.append(question_multi_output[x])
                    question_output = None
                messages.warning(request, '<b>Warning:</b> The number of questions requested was greater than the total number of questions available for the selected subject and topic(s). Therefore, the  system has returned all possible questions. ')
                
            else:
                for x in range(0, int(number_of_questions)):
                    qm.append(question_multi_output[x])
                    question_output = None  

            qm_json = json.dumps(qm)   
        
        subject_name = Subject.objects.get(pk=subject_id)       

        context = {
            'subject' : subject_id,
            'subject_id' : subject_id,
            'subject_name': subject_name,
            'topic_id' : topic_id, 
            'choice_field' : choice_field, 
            'number_of_questions' : int(number_of_questions),
            'qo':question_output,
            'qm':qm,
            'qm_json': qm_json,
        }

        return render(request, 'questions/createquestions.html', context)

def load_topics(request):
    subject_id = request.GET.get('subject')
    topics = Question.objects.filter(subjectid=subject_id).order_by('topicid__topicname').values_list('topicid_id','topicid__topicname', flat=False).distinct()
    question_count =  Question.objects.filter(subjectid=subject_id).count()
    
    top_topics = Question.objects.filter(subjectid=subject_id).values_list("topicid__topicname").annotate(total=Count("topicid__topicname")).order_by('-total')
    top_ten_topic = "{}".format(",".join("'" + t[0] + "'" for t in top_topics))
    top_ten_totals = [topic[1] for topic in top_topics]

    context = {
        'top_topics' : str(top_ten_topic),
        'totals' : top_ten_totals,
        'topics':topics,
        'question_count': question_count
    }

    return render(request, 'questions/topic_dropdown_list_options.html', context)
