from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from source import dbconnect, er

"""
This module generates the personnel page for admins.
This page uses dbconnect to update a person's status
and delete a status if it was updated by msitake.
"""

# Create your views here.
def index(request, refreshToken):
    response = er.refresh(refreshToken)
	
    if 'error' in response.keys():
        template = loader.get_template('login.html')
        context = {"error":"access_error"}
        return HttpResponse(template.render(context, request))

    connection = dbconnect.dbconnect()
    firstQuery = "SELECT fname FROM PERSON;"
    firsts = connection.s_query(firstQuery)
    lastQuery = "SELECT lname FROM PERSON;"
    lasts = connection.s_query(lastQuery)
    numsQuery = "SELECT id FROM PERSON;"
    nums = connection.s_query(numsQuery)
    connection.close()
    i = len(firsts)
    x = 0
    emps = []
    while x < i:
        empfirst = firsts[x][0]
        emplast = lasts[x][0]
        empNum = nums[x][0]
        emp = "%s, %s %s" % (emplast, empfirst, empNum)
        emps.append(emp)
        x += 1
    template = loader.get_template('admin_personnel.html')
    context = {
		'employees' : emps, 
		'refreshToken': response['refresh_token']
	}
    return HttpResponse(template.render(context, request))

def update(request, refreshToken):
    response = er.refresh(refreshToken)
	
    if 'error' in response.keys():
        template = loader.get_template('login.html')
        context = {"error":"access_error"}
        return HttpResponse(template.render(context, request))

    try:
        connection = dbconnect.dbconnect()
        employee = request.POST["employee"]
        nums = [int(s) for s in employee.split() if s.isdigit()]
        empNum = nums[-1]
        status = request.POST["status"]
        date = request.POST["date"]
        note = request.POST["text"]
        connection.load_person_status(status, date, str(empNum), note)
        connection.close()
        template = loader.get_template('admin_submit.html')
        context = {
			'refreshToken': response['refresh_token']
		}
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print(e)
        template = loader.get_template('admin_error.html')
        context = {'refreshToken': response['refresh_token']}
        return HttpResponse(template.render(context, request))
		
def error(request, refreshToken):
	response = er.refresh(refreshToken)
	
	if 'error' in response.keys():
		template = loader.get_template('login.html')
		context = {"error":"access_error"}
		return HttpResponse(template.render(context, request))
		
	template = loader.get_template('admin_error.html')
	context = {
		'refreshToken': response['refresh_token']
	}
	return HttpResponse(template.render(context, request))
	
def get(request, refreshToken):
    response = er.refresh(refreshToken)
	
    if 'error' in response.keys():
        template = loader.get_template('login.html')
        context = {"error":"access_error"}
        return HttpResponse(template.render(context, request))

    try:	
        connection = dbconnect.dbconnect()
		
        firstQuery = "SELECT fname FROM PERSON;"
        firsts = connection.s_query(firstQuery)
        lastQuery = "SELECT lname FROM PERSON;"
        lasts = connection.s_query(lastQuery)
        numsQuery = "SELECT id FROM PERSON;"
        nums = connection.s_query(numsQuery)
        i = len(firsts)
        x = 0
        emps = []
        while x < i:
            empfirst = firsts[x][0]
            emplast = lasts[x][0]
            empNum = nums[x][0]
            emp = "%s, %s %s" % (emplast, empfirst, empNum)
            emps.append(emp)
            x += 1
		
        employee = request.POST["employee"]
        nums = [int(s) for s in employee.split() if s.isdigit()]
        empNum = nums[-1]
        statuses = connection.get_statuses(str(empNum))
        stats = []
        for s in statuses:
            status = s[0]
            date = s[1]
            emp = s[2]
            note = s[3]
            stat = "%s, %s, %s, %s" % (status, date, note, emp)
            stats.append(stat)
        template = loader.get_template('admin_personnel.html')
        context = {
			'statuses' : stats,
			'employees': emps,
			'refreshToken' : response['refresh_token']
		}
        return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('admin_error.html')
        context = {}
        return HttpResponse(template.render(context, request))

def delete(request, refreshToken):
    response = er.refresh(refreshToken)
	
    if 'error' in response.keys():
        template = loader.get_template('login.html')
        context = {"error":"access_error"}
        return HttpResponse(template.render(context, request))
    try:
        connection = dbconnect.dbconnect()		
        statuses = request.POST.getlist("status")
        for status in statuses:
            data = status.split(',')
            emp = data[3]
            emp = emp[1:]
            date = data[1]
            date = date[1:]
            change = data[0]
            connection.delete_status(emp, date, change)
        connection.close()

        template = loader.get_template('admin_submit.html')
        context = {
            'refreshToken': response['refresh_token']
        }
        return HttpResponse(template.render(context, request))
    except:    
        template = loader.get_template('admin_error.html')
        context = {'refreshToken': response['refresh_token']}
        return HttpResponse(template.render(context, request))
		
	
