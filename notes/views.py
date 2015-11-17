from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

from elasticsearch import Elasticsearch
import datetime
import re

from .forms import NoteForm, DeleteNoteForm

#def index(request):
#    return HttpResponse("Hello, world!")

class Note:
    def __init__(self, id, title, published, contents, tags):
        self.id = id;
        self.title = title
        self.published = published
        self.contents = contents
        self.tag = tags


def get_all_notes():
    es = Elasticsearch("s3.zserg.net:9200")
    res = es.search(index="notes", body={"query": {"match_all": {}}})
    notes = []
    for n in res['hits']['hits']:
        src = n['_source']
        spub = src['published']
        pub = datetime.datetime.strptime(spub, '%Y-%m-%dT%H:%M:%S.%f') 
        notes.append(Note(n['_id'],src['title'],pub,src['contents'],src['tags']))

    return notes


def get_one_notes(id):
    es = Elasticsearch("s3.zserg.net:9200")
    q = "_id:{0}".format(id)    
    res = es.search(index="notes", body={"query":{"query_string":{"query":q}}})
    n = res['hits']['hits'][0]
    src = n['_source']
    spub = src['published']
    pub = datetime.datetime.strptime(spub, '%Y-%m-%dT%H:%M:%S.%f') 
    
    note = Note(n['_id'],src['title'],pub,src['contents'],src['tags'])

    return note

def parse_note(text):
    re_tags = r'#([^\s]+)'
    re_title = r'#([^\s]+)'
    tags = re.findall(re_tags,text)
    stat = re.search(re_title,text,re.I|re.M)
    if stat:
        title = stat.group(1)
    else:
        title = '<no_title>'

    note = {
             'title': title,
             'contents': text,
             'published': datetime.datetime.now(),
             'tags': tags
    }
    return note




class IndexView(View):
    template_name = 'notes/index.html'

    def get(self, request, *args, **kwargs):
        notes = get_all_notes()
        context = {'notes':notes}
        return render(request, self.template_name, context)
    
class NoteView(View):
    form_class = DeleteNoteForm
    print("get_all_notes")
    template_name = 'notes/note.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        note_id = args[0]
        print("id = {}".format(note_id))
        note = get_one_notes(note_id)
        context = {'note':note, 'form':form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        print('delete {}'.format(self.note_id))
        return HttpResponseRedirect('/notes')
    

class DeleteNoteView(View):
    template_name = 'notes/delete.html'

    def get(self, request, *args, **kwargs):
        note_id = args[0]
        es = Elasticsearch("s3.zserg.net:9200")
        res = es.delete(index="notes", doc_type='note', id = note_id)

        context = {'result':res['found'], 'note_id':note_id}
        return render(request, self.template_name, context)


class PostNoteView(View):
    form_class = NoteForm
    template_name = 'notes/post.html'
    
    def get(self, request, *args, **kwargs):
       form = self.form_class()
       return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
       form = self.form_class(request.POST)
       if form.is_valid():
           note = parse_note(form.cleaned_data['note_text'])
           es = Elasticsearch("s3.zserg.net:9200")
           res = es.index(index="notes", doc_type='note',  body=note)
           if res['created']:
              return HttpResponseRedirect('/notes')
           else:
              return HttpResponseRedirect('/failed')
 
       return render(request, self.template_name, {'form': form})



