from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .forms import AddSubjectForm, AddTopicForm,EditSubjectForm
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from .models import Subject, Topic


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
        if form.is_valid():
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
