from .forms import AddSubjectForm, AddTopicForm,EditSubjectForm, AddTopicForm,EditTopicForm
from .models import Subject, Topic, Question

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect,get_object_or_404


###################################
######## SUBJECT SECTION ##########
###################################
######### CONTAINS ALL ############
######### VIEWS RELATING ##########
########## TO SUBJECT ############
###################################

def index(request): #TO CHANGE TO PROPER NAME
    subjects = Subject.objects.all().order_by("subjectname")
    return render(request, 'questions/subject.html', {'subjects':subjects})

@login_required
@permission_required('questions.add_subject',raise_exception=True)
def addsubject(request):   
    if request.method == 'POST':       
        form = AddSubjectForm(request.POST)
        subject_name = request.POST['subjectname'].lower()        
        all_subjects =  [x.upper() for x in  Subject.objects.all().values_list('subjectname',flat=True)]
        
        if subject_name.upper() in all_subjects:
            messages.error(request, '<b>Error: </b><em>{}</em> already exists. Validation is case-insensitive (e.g. it and IT will be treated the same for validation against existing subjects).'.format(subject_name))
        
        elif form.is_valid():
            upload_data = form.save(commit=False)
            upload_data = form.save()
            messages.success(request, '<b>Success</b>: </b><em>{}</em> has been added successfully and is now available for use.'.format(subject_name))
    
        else:
            messages.error(request, '<b>Error:</b> The value entered "{}" is invalid. This may be due to an character or a processing error.<br>Please try again. If you encounter further errors please contact a staff member.'.format(subject_name))
        
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
  
        if form.is_valid():
            upload_data = form.save(commit=False)
            upload_data = form.save()
            messages.success(request, '<b>Success</b>: </b><em>{}</em> has been added successfully and is now available for use.'.format(topic_name))
    
            return redirect('questions:addtopic')
        
        else:
            all_topics =  [x.upper() for x in  Topic.objects.all().values_list('topicname',flat=True)]

            if topic_name.upper() in all_topics:
                messages.error(request, '<b>Error: </b><em>{}</em> already exists. Validation is case-insensitive (e.g. C1 and c1 will be treated the same for validation against existing topics).'.format(topic_name))
            else:
                messages.error(request, '<b>Error:</b> The value entered "{}" is invalid. This may be due to an character or a processing error.<br>Please try again. If you encounter further errors please contact a staff member.'.format(topic_name))

            return redirect('questions:addtopic')
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
            

        return redirect('questions:topic-detail', topicid=topicid)
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
######## QUESTIONS SECTION ##########
###################################
######### CONTAINS ALL ############
######### VIEWS RELATING ##########
########## TO QUESTIONS ############
###################################    
    
def question(request):
    question_count = Question.objects.values('subjectid', 'subjectid__subjectname').order_by('subjectid').annotate(dcount=Count('subjectid'))
    return render(request, 'questions/questions.html', {'question_count':question_count})