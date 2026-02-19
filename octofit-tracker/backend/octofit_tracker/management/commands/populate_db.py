from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.WARNING('Deleting old data...'))
            Activity.objects.all().delete()
            Workout.objects.all().delete()
            Leaderboard.objects.all().delete()
            User.objects.all().delete()
            Team.objects.all().delete()

            self.stdout.write(self.style.SUCCESS('Creating teams...'))
            marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
            dc = Team.objects.create(name='DC', description='DC superheroes')

            self.stdout.write(self.style.SUCCESS('Creating users...'))
            users = [
                User.objects.create(email='tony@stark.com', username='IronMan', team=marvel),
                User.objects.create(email='steve@rogers.com', username='CaptainAmerica', team=marvel),
                User.objects.create(email='bruce@wayne.com', username='Batman', team=dc),
                User.objects.create(email='clark@kent.com', username='Superman', team=dc),
            ]

            self.stdout.write(self.style.SUCCESS('Creating activities...'))
            Activity.objects.create(user=users[0], type='Running', duration=30, date='2024-01-01')
            Activity.objects.create(user=users[1], type='Cycling', duration=45, date='2024-01-02')
            Activity.objects.create(user=users[2], type='Swimming', duration=60, date='2024-01-03')
            Activity.objects.create(user=users[3], type='Yoga', duration=20, date='2024-01-04')

            self.stdout.write(self.style.SUCCESS('Creating workouts...'))
            w1 = Workout.objects.create(name='Full Body', description='Full body workout')
            w2 = Workout.objects.create(name='Cardio Blast', description='Cardio workout')
            w1.suggested_for.set(users[:2])
            w2.suggested_for.set(users[2:])

            self.stdout.write(self.style.SUCCESS('Creating leaderboard...'))
            Leaderboard.objects.create(team=marvel, score=100)
            Leaderboard.objects.create(team=dc, score=90)

            self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
