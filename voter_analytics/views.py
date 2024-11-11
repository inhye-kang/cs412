from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView
from .models import Voter
from django.db.models import Count
import plotly
import plotly.graph_objs as go
import pandas as pd

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_listing.html'
    context_object_name = 'voters'
    paginate_by = 100
    ordering = ['last_name', 'first_name']

    def get_queryset(self):
        queryset = Voter.objects.all().order_by('last_name', 'first_name')
        
        party_affiliation = self.request.GET.get('party_affiliation')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        voter_score = self.request.GET.get('voter_score')
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']

        if party_affiliation:
            queryset = queryset.filter(party=party_affiliation)
        
        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=min_year)
        
        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=max_year)
        
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        for election in elections:
            if self.request.GET.get(election) == 'on':
                queryset = queryset.filter(**{election: True})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['voter_score_range'] = range(6)  
        context['election_fields'] = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town'] 
        context['years_range'] = range(1920, 2024)
        context['parties'] = Voter.objects.values_list('party', flat=True).distinct()
        context['street_num'] = self.request.GET.get('street_num')
        context['current_time'] = timezone.now()
        print(context)
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/show_voter.html'
    context_object_name = 'voter'

class VoterGraphView(TemplateView):
    template_name = 'voter_analytics/graphs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        queryset = Voter.objects.all()
        party_affiliation = self.request.GET.get('party_affiliation')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        voter_score = self.request.GET.get('voter_score')
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']

        if party_affiliation:
            queryset = queryset.filter(party=party_affiliation)

        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=min_year)

        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=max_year)

        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        for election in elections:
            if self.request.GET.get(election) == 'on':
                queryset = queryset.filter(**{election: True})

        birth_years = queryset.values_list('date_of_birth', flat=True)
        birth_years = [date.year for date in birth_years if date] 
        birth_year_series = pd.Series(birth_years)

        year_counts = birth_year_series.value_counts().sort_index()
        year_fig = go.Figure(data=[go.Bar(x=year_counts.index, y=year_counts.values)])
        year_fig.update_layout(title="Voter Distribution by Year of Birth",
                               xaxis_title="Year of Birth",
                               yaxis_title="Number of Voters")
        year_div = plot(year_fig, output_type='div')

        party_counts = queryset.values('party').annotate(count=Count('party'))
        parties = [item['party'] for item in party_counts]
        counts = [item['count'] for item in party_counts]

        party_fig = go.Figure(data=[go.Pie(labels=parties, values=counts, hole=0.3)])
        party_fig.update_layout(title="Voter Distribution by Party Affiliation")
        party_div = plot(party_fig, output_type='div')

        election_counts = [queryset.filter(**{field: True}).count() for field in elections]

        election_fig = go.Figure(data=[go.Bar(x=elections, y=election_counts)])
        election_fig.update_layout(title="Vote Count by Election",
                                   xaxis_title="Election",
                                   yaxis_title="Number of Voters")
        election_div = plot(election_fig, output_type='div')

        context['year_div'] = year_div
        context['party_div'] = party_div
        context['election_div'] = election_div
        context['voter_score_range'] = range(6)
        context['election_fields'] = elections
        context['years_range'] = range(1920, 2024)
        
        return context