from django.contrib import admin

from .models import (
	Editor,
	Author,
	Keyword,
	Document,
	Copy,
	Book,
	Journal,
	JournalArticle,
	Media,
	Issue,
	) 

admin.site.register([Editor,
	Author,
	Keyword,
	Document,
	Copy,
	Book,
	Journal,
	JournalArticle,
	Media,
	Issue
	])
