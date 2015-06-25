import pytz
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase

from .models import Competition, CompetitionStage, CompetitionGenre, CompetitionCountry,\
                    CompetitionPrize, CompetitionTerms, CompetitionVisual,\
                    CompetitionStageRequirement, CompetitionEntry,\
                    CompetitionEntryAudio, CompetitionChart, CompetitionJudge,\
                    CompetitionEntryRating, CompetitionEntryLike
from media.models import Genre, Audio
# Create your tests here.

"""
Testing competition

Competitions have a lot of functionality to ensure they are valid to be displayed on the front end

Has a unique Slug
Has at least one Competition Stage - that has a final stage
Has a Competition Genre
Has at least one Competition Country
Has at least one Competition Prize
Has Competition Terms
Has Competition Visuals

"""
class CompetitionTestCase(TestCase):
    """Check competition validation functionality works"""
    def setUp(self):
        user = User(**{
            "email": "admin@jbcole.co.uk",
            "username": "fame_admin",
            "password": "gjfkgjfk"
            })
        user.save()
        self.user = user

        competition = Competition(**{
                "name": "Test Competition",
                "slug": "test",
                "date_start": datetime(2015, 06, 25, 8, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 07, 31, 12, 0, 0, 0, pytz.UTC),
                "creator": user
            })
        competition.save()
        self.competition = competition

        genre = Genre(**{
                "name": "Country"
            })
        genre.save()

    def test_unique_slug(self):
        """Test for unique slug"""
        # based on datetime(2015, 06, 25, 8, 0, 0, 0, pytz.UTC)
        
        # valid
        competition = Competition(**{
                "name": "Test Competition",
                "slug": "test",
                "date_start": datetime(2015, 06, 25, 8, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 07, 31, 12, 0, 0, 0, pytz.UTC),
                "creator": self.user
            })
        try:
            competition.save()
            self.assertFalse(True)
        except:
            self.assertTrue(True)

    def test_has_valid_competition_stage(self):
        """Test for unique slug"""
        # based on datetime(2015, 06, 25, 8, 0, 0, 0, pytz.UTC)
        
        # invalid
        self.assertFalse(self.competition.has_valid_competition_stage())

        competition_stage = CompetitionStage(**{
                "competition": self.competition,
                "name": "Final Round",
                "description": "You must complete the round of destiny",
                "date_start": datetime(2015, 06, 25, 8, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 07, 31, 12, 0, 0, 0, pytz.UTC),
                "ordering": 1,
                "final_stage":True
            })
        competition_stage.save()
        
        # valid
        self.assertTrue(self.competition.has_valid_competition_stage())

    def test_has_competition_genre(self):
        """Test for Competition genre"""
        self.assertFalse(self.competition.has_valid_competition_genre())

        competition_genre = CompetitionGenre(**{
                "competition":self.competition,
                "genre":Genre.objects.get(name="Country")
            })
        competition_genre.save()

        self.assertTrue(self.competition.has_valid_competition_genre())

    def test_has_valid_competition_country(self):
        """Test has valid competition country"""
        self.assertFalse(self.competition.has_valid_competition_country())

        competition_country = CompetitionCountry(**{
                "competition": self.competition,
                "country": "GB"
            })
        competition_country.save()

        self.assertTrue(self.competition.has_valid_competition_country())

    def test_has_valid_competition_prize(self):
        self.assertFalse(self.competition.has_valid_competition_prize())

        competition_prize = CompetitionPrize(**{
                "competition": self.competition,
                "prize":"First place!",
                "description":"This is the prize",
                "image":"",
                "ordering":1
            })
        competition_prize.save()

        self.assertTrue(self.competition.has_valid_competition_prize())

    def test_has_valid_competition_terms(self):
        self.assertFalse(self.competition.has_valid_competition_terms())

        competition_terms = CompetitionTerms(**{
                "competition": self.competition,
                "terms":"Please do this"
            })
        competition_terms.save()

        self.assertTrue(self.competition.has_valid_competition_terms())

    def test_has_valid_competition_visuals(self):
        self.assertFalse(self.competition.has_valid_competition_visuals())

        competition_visual = CompetitionVisual(**{
                "competition": self.competition
            })
        competition_visual.save()
        self.assertFalse(self.competition.has_valid_competition_visuals())

        competition_visual.landing_page_content = "Hi there"
        competition_visual.landing_page_image = "image.png"
        competition_visual.save()
        self.assertFalse(self.competition.has_valid_competition_visuals())

        competition_visual.entry_instructions = "Why don't you go here?"
        competition_visual.save()
        self.assertTrue(self.competition.has_valid_competition_visuals())

    def test_is_valid_competition(self):
        self.assertFalse(self.competition.is_valid_competition())

        competition_stage = CompetitionStage(**{
                "competition": self.competition,
                "name": "Final Round",
                "description": "You must complete the round of destiny",
                "date_start": datetime(2015, 06, 25, 8, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 07, 31, 12, 0, 0, 0, pytz.UTC),
                "ordering": 1,
                "final_stage":True,
                "new_entries_open": True
            })
        competition_stage.save()
        competition_genre = CompetitionGenre(**{
                "competition":self.competition,
                "genre":Genre.objects.get(name="Country")
            })
        competition_genre.save()
        competition_country = CompetitionCountry(**{
                "competition": self.competition,
                "country": "GB"
            })
        competition_country.save()
        competition_prize = CompetitionPrize(**{
                "competition": self.competition,
                "prize":"First place!",
                "description":"This is the prize",
                "image":"",
                "ordering":1
            })
        competition_prize.save()
        competition_terms = CompetitionTerms(**{
                "competition": self.competition,
                "terms":"Please do this"
            })
        competition_terms.save()
        competition_visual = CompetitionVisual(**{
                "competition": self.competition
            })
        competition_visual.landing_page_content = "Hi there"
        competition_visual.landing_page_image = "image.png"
        competition_visual.entry_instructions = "Go here"
        competition_visual.save()

        competition_stage_requirement = CompetitionStageRequirement(**{"competition_stage":competition_stage,"name":"Audio requirement","description":"Upload your first track!","media_type":"audio","total_required":1,"ordering":1,"primary":True})
        competition_stage_requirement.save()

        self.assertTrue(self.competition.is_valid_competition())

    def test_has_number_entries(self):
        """Check number of entries"""
        competition_stage = CompetitionStage(**{"competition": self.competition,"name": "Final Round","description": "You must complete the round of destiny","date_start": datetime(2015, 06, 25, 8, 0, 0, 0, pytz.UTC),"date_end": datetime(2015, 07, 31, 12, 0, 0, 0, pytz.UTC),"ordering": 1,"final_stage":False,"new_entries_open": True})
        competition_stage.save()

        competition_stage_requirement = CompetitionStageRequirement(**{"competition_stage":competition_stage,"name":"Audio requirement","description":"Upload your first track!","media_type":"audio","total_required":1,"ordering":1,"primary":True})
        competition_stage_requirement.save()

        self.assertTrue(self.competition.has_number_entries() < 1)
        competition_entry = CompetitionEntry(**{
                "competition":self.competition,
                "user":self.user,
                "name":"Competition Entry",
                "final_position":0,
                "final_points":0
            })
        competition_entry.save()
        self.assertTrue(self.competition.has_number_entries() == 1)

    def test_get_competition_status(self):
        """Check competition status"""
        self.competition.date_start = datetime.now(tz=pytz.UTC) + timedelta(days=1)
        self.competition.date_end = datetime.now(tz=pytz.UTC) + timedelta(days=2)
        self.assertTrue(self.competition.get_competition_status() == "not_started")

        self.competition.date_start = datetime.now(tz=pytz.UTC) - timedelta(days=2)
        self.competition.date_end = datetime.now(tz=pytz.UTC) - timedelta(days=1)
        self.assertTrue(self.competition.get_competition_status() == "ended")

        self.competition.date_start = datetime.now(tz=pytz.UTC) - timedelta(days=2)
        self.competition.date_end = datetime.now(tz=pytz.UTC) + timedelta(days=2)
        self.assertTrue(self.competition.get_competition_status() == "invalid")

        competition_stage = CompetitionStage(**{
                "competition": self.competition,
                "name": "Final Round",
                "description": "You must complete the round of destiny",
                "date_start": datetime(2015, 06, 25, 8, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 07, 31, 12, 0, 0, 0, pytz.UTC),
                "ordering": 1,
                "final_stage":True,
                "new_entries_open": True
            })
        competition_stage.save()
        competition_genre = CompetitionGenre(**{
                "competition":self.competition,
                "genre":Genre.objects.get(name="Country")
            })
        competition_genre.save()
        competition_country = CompetitionCountry(**{
                "competition": self.competition,
                "country": "GB"
            })
        competition_country.save()
        competition_prize = CompetitionPrize(**{
                "competition": self.competition,
                "prize":"First place!",
                "description":"This is the prize",
                "image":"",
                "ordering":1
            })
        competition_prize.save()
        competition_terms = CompetitionTerms(**{
                "competition": self.competition,
                "terms":"Please do this"
            })
        competition_terms.save()
        competition_visual = CompetitionVisual(**{
                "competition": self.competition
            })
        competition_visual.landing_page_content = "Hi there"
        competition_visual.landing_page_image = "image.png"
        competition_visual.entry_instructions = "Go here"
        competition_visual.save()

        competition_stage_requirement = CompetitionStageRequirement(**{"competition_stage":competition_stage,"name":"Audio requirement","description":"Upload your first track!","media_type":"audio","total_required":1,"ordering":1,"primary":True})
        competition_stage_requirement.save()

        self.assertTrue(self.competition.get_competition_status() == "valid")

    def test_get_time_remaining(self):
        """Check time remaining for competition"""
        self.assertTrue(self.competition.get_time_remaining())

    def test_has_primary_competition_stage_requirement(self):
        self.assertFalse(self.competition.has_primary_competition_stage_requirement())

        competition_stage = CompetitionStage(**{
                "competition": self.competition,
                "name": "Final Round",
                "description": "You must complete the round of destiny",
                "date_start": datetime(2015, 06, 25, 8, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 07, 31, 12, 0, 0, 0, pytz.UTC),
                "ordering": 1,
                "final_stage":False,
                "new_entries_open": True
            })
        competition_stage.save()

        competition_stage_requirement = CompetitionStageRequirement(**{
            "competition_stage":competition_stage,
            "name":"Audio requirement",
            "description":"Upload your first track!",
            "media_type":"audio",
            "total_required":2,
            "ordering":1,
            "primary":True
            })
        competition_stage_requirement.save()

        self.assertTrue(self.competition.has_primary_competition_stage_requirement())


class CompetitionStageTestCase(TestCase):
    """Check competition stage functionality works"""
    def setUp(self):
        user = User(**{
            "email": "admin@jbcole.co.uk",
            "username": "fame_admin",
            "password": "gjfkgjfk"
            })
        user.save()

        competition = Competition(**{
                "name": "Test Competition",
                "slug": "test",
                "date_start": datetime(2015, 06, 25, 8, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 07, 31, 12, 0, 0, 0, pytz.UTC),
                "creator": user
            })
        competition.save()
        self.competition = competition

        self.competition_stage = CompetitionStage(**{
                "competition": competition,
                "name": "First Round",
                "description": "You must complete the round of destiny",
                "date_start": datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 06, 26, 9, 0, 0, 0, pytz.UTC),
                "ordering": 1,
                "new_entries_open": True
            })

    def test_date_is_bigger(self):
        """Test for most basic function date_is_bigger"""
        # based on datetime(2015, 06, 25, 8, 0, 0, 0, pytz.UTC)
        
        # valid
        self.competition_stage.date_start = datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC) # set initially, repeating
        self.assertTrue(self.competition_stage.date_is_bigger(self.competition_stage.date_start, self.competition_stage.competition.date_start))
        self.assertFalse(self.competition_stage.date_is_bigger(self.competition_stage.competition.date_start, self.competition_stage.date_start))

        # check if equals overlapping counts
        self.competition_stage.date_start = datetime(2015, 06, 25, 8, 0, 0, 0, pytz.UTC) # set initially, repeating
        self.assertTrue(self.competition_stage.date_is_bigger(self.competition_stage.date_start, self.competition_stage.competition.date_start))
        self.assertFalse(self.competition_stage.date_is_bigger(self.competition_stage.date_start, self.competition_stage.competition.date_start, True))

    def test_is_date_within_competition(self):
        """Test for function is_date_within_competition"""
        self.competition_stage.date_start = datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC) # set initially, repeating
        
        # valid
        response = self.competition_stage.is_date_within_competition()
        self.assertFalse(response['error'])

        # invalid - start date too early
        self.competition_stage.date_start = datetime(2015, 05, 25, 9, 0, 0, 0, pytz.UTC)
        response = self.competition_stage.is_date_within_competition()
        self.assertTrue(response['error'])
        self.assertTrue(response['field'] == "date_start")

        # invalid - end date too late
        self.competition_stage.date_start = datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC)
        self.competition_stage.date_end = datetime(2015, 8, 25, 9, 0, 0, 0, pytz.UTC)
        response = self.competition_stage.is_date_within_competition()
        self.assertTrue(response['error'])
        self.assertTrue(response['field'] == "date_end")

        # invalid - start date before end date
        self.competition_stage.date_end = datetime(2015, 06, 26, 9, 0, 0, 0, pytz.UTC) # reset end date
        self.competition_stage.date_start = datetime(2015, 07, 25, 9, 0, 0, 0, pytz.UTC)
        response = self.competition_stage.is_date_within_competition()
        self.assertTrue(response['error'])
        self.assertTrue(response['field'] == "date_start")


    def test_date_overlap(self):
        """Test for function date_overlap"""
        self.competition_stage.date_start = datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC) # set initially, repeating

        # check standard overlap
        response = self.competition_stage.is_date_overlap(datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC), datetime(2015, 06, 24, 9, 0, 0, 0, pytz.UTC), datetime(2015, 06, 26, 9, 0, 0, 0, pytz.UTC))
        self.assertTrue(response) # overlap

        # check standard overlap - same start times
        response = self.competition_stage.is_date_overlap(datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC), datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC), datetime(2015, 06, 26, 9, 0, 0, 0, pytz.UTC))
        self.assertFalse(response) # overlap
        response = self.competition_stage.is_date_overlap(datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC), datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC), datetime(2015, 06, 26, 9, 0, 0, 0, pytz.UTC), "start")
        self.assertTrue(response)

        # check standard overlap - same end times
        response = self.competition_stage.is_date_overlap(datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC), datetime(2015, 06, 24, 9, 0, 0, 0, pytz.UTC), datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC))
        self.assertFalse(response)
        response = self.competition_stage.is_date_overlap(datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC), datetime(2015, 06, 24, 9, 0, 0, 0, pytz.UTC), datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC), "end")
        self.assertTrue(response)


    def test_is_no_date_overlap(self):
        """Test for function is_no_date_overlap"""

        self.competition_stage.date_start = datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC)
        self.competition_stage.date_end = datetime(2015, 06, 26, 9, 0, 0, 0, pytz.UTC) # reset end date

        self.competition_stage.competition_stages_to_check = []

        response = self.competition_stage.is_no_date_overlap()
        self.assertFalse(response["error"])

        competition_stage = CompetitionStage(**{
                "competition": self.competition,
                "name": "First Round",
                "description": "You must complete the round of destiny",
                "date_start": datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 06, 26, 9, 0, 0, 0, pytz.UTC),
                "ordering": 1
            })
        competition_stage.save()

        competition_stage = CompetitionStage(**{
                "competition": self.competition,
                "name": "First Round",
                "description": "You must complete the round of destiny",
                "date_start": datetime(2015, 06, 27, 9, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 06, 28, 9, 0, 0, 0, pytz.UTC),
                "ordering": 1
            })
        competition_stage.save()
        
        # overlapping
        self.competition_stage.competition_stages_to_check = CompetitionStage.objects.filter(competition=self.competition)
        
        response = self.competition_stage.is_no_date_overlap()
        self.assertTrue(response["error"])

        # covering
        self.competition_stage.date_start = datetime(2015, 06, 22, 9, 0, 0, 0, pytz.UTC)
        self.competition_stage.date_end = datetime(2015, 06, 29, 9, 0, 0, 0, pytz.UTC) # reset end date

        response = self.competition_stage.is_no_date_overlap()
        self.assertTrue(response["error"])

        # no overlap
        self.competition_stage.date_start = datetime(2015, 06, 28, 10, 0, 0, 0, pytz.UTC)
        self.competition_stage.date_end = datetime(2015, 06, 29, 9, 0, 0, 0, pytz.UTC) # reset end date

        response = self.competition_stage.is_no_date_overlap()
        self.assertFalse(response["error"])



    def test_is_valid_date_range(self):
        """Test for function is_valid_date_range"""
        competition_stage = CompetitionStage(**{
                "competition": self.competition,
                "name": "First Round",
                "description": "You must complete the round of destiny",
                "date_start": datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 06, 26, 9, 0, 0, 0, pytz.UTC),
                "ordering": 1
            })
        competition_stage.save()

        competition_stage = CompetitionStage(**{
                "competition": self.competition,
                "name": "First Round",
                "description": "You must complete the round of destiny",
                "date_start": datetime(2015, 06, 27, 9, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 06, 28, 9, 0, 0, 0, pytz.UTC),
                "ordering": 1
            })
        competition_stage.save()
        
        # no overlapping
        self.competition_stage.date_start = datetime(2015, 06, 28, 10, 0, 0, 0, pytz.UTC)
        self.competition_stage.date_end = datetime(2015, 06, 29, 9, 0, 0, 0, pytz.UTC) # reset end date

        self.competition.date_start = datetime(2015, 06, 25, 8, 0, 0, 0, pytz.UTC)
        self.competition.date_end = datetime(2015, 07, 31, 12, 0, 0, 0, pytz.UTC)

        self.competition_stage.competition_stages_to_check = CompetitionStage.objects.filter(competition=self.competition)

        response = self.competition_stage.is_valid_date_range()
        self.assertFalse(response["error"])

    def test_confirm_valid_knockout_stage(self):
        # valid knockout stage
        self.assertTrue(self.competition_stage.confirm_valid_knockout_stage(True, 10))
        self.assertTrue(self.competition_stage.confirm_valid_knockout_stage(False, 10))
        self.assertTrue(self.competition_stage.confirm_valid_knockout_stage(False, 0))
        
        self.assertFalse(self.competition_stage.confirm_valid_knockout_stage(True, 0))

    def test_confirm_valid_final_stage(self):
        # valid final stage
        self.competition_stage.date_end = datetime(2015, 07, 31, 12, 0, 0, 0, pytz.UTC) # reset end date
        self.competition.date_end = datetime(2015, 07, 31, 12, 0, 0, 0, pytz.UTC)

        self.assertTrue(self.competition_stage.confirm_valid_final_stage(False, self.competition_stage.date_end, self.competition.date_end))
        self.assertTrue(self.competition_stage.confirm_valid_final_stage(True, self.competition_stage.date_end, self.competition.date_end))
        
        self.competition_stage.date_end = datetime(2015, 07, 28, 12, 0, 0, 0, pytz.UTC) # reset end date
        self.assertFalse(self.competition_stage.confirm_valid_final_stage(True, self.competition_stage.date_end, self.competition.date_end))

    def test_is_valid_entries_access(self):
        self.competition_stage.save()

        second_competition_stage = CompetitionStage(**{
                "competition": self.competition,
                "name": "Second Round",
                "description": "You must complete the round of destiny",
                "date_start": datetime(2015, 06, 26, 9, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 06, 27, 9, 0, 0, 0, pytz.UTC),
                "ordering": 1,
                "new_entries_open": False
            })

        third_competition_stage = CompetitionStage(**{
                "competition": self.competition,
                "name": "Third Round",
                "description": "You must complete the round of destiny",
                "date_start": datetime(2015, 06, 27, 9, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 06, 28, 9, 0, 0, 0, pytz.UTC),
                "ordering": 1,
                "new_entries_open": True
            })

        # second stage is fine
        error_to_check = second_competition_stage.is_valid_entries_access(second_competition_stage.new_entries_open)
        self.assertFalse(error_to_check["error"])
        second_competition_stage.save()

        # third stage is not fine
        error_to_check = third_competition_stage.is_valid_entries_access(third_competition_stage.new_entries_open)
        self.assertTrue(error_to_check["error"])

        # third stage is not fine as knockout stage
        third_competition_stage.knockout_stage = True
        error_to_check = third_competition_stage.is_valid_entries_access(third_competition_stage.new_entries_open)
        self.assertTrue(error_to_check["error"])

        # third stage is now fine
        third_competition_stage.new_entries_open = False
        error_to_check = third_competition_stage.is_valid_entries_access(third_competition_stage.new_entries_open)
        self.assertFalse(error_to_check["error"])
        third_competition_stage.save()



class CompetitionStageRequirementTestCase(TestCase):
    """Confirm Competition Stage Requirements are valid"""
    def setUp(self):
        user = User(**{
            "email": "admin@jbcole.co.uk",
            "username": "fame_admin",
            "password": "gjfkgjfk"
            })
        user.save()
        self.user = user

        competition = Competition(**{
                "name": "Test Competition",
                "slug": "test",
                "date_start": datetime(2015, 06, 25, 8, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 07, 31, 12, 0, 0, 0, pytz.UTC),
                "creator": user
            })
        competition.save()
        self.competition = competition

        self.competition = competition

        self.competition_stage = CompetitionStage(**{
                "competition": competition,
                "name": "First Round",
                "description": "You must complete the round of destiny",
                "date_start": datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 06, 26, 9, 0, 0, 0, pytz.UTC),
                "ordering": 1
            })
        self.competition_stage.save()

        self.competition_stage_requirement = CompetitionStageRequirement(**{
            "competition_stage":self.competition_stage,
            "name":"Audio requirement",
            "description":"Upload your first track!",
            "media_type":"audio",
            "total_required":2,
            "ordering":1,
            })
        self.competition_stage_requirement.save()

    def test_is_valid_media_type(self):
        self.assertTrue(self.competition_stage_requirement.is_valid_media_type())

        competition_stage_requirement = CompetitionStageRequirement(**{
            "competition_stage":self.competition_stage,
            "name":"Audio requirement",
            "description":"Upload your second track!",
            "media_type":"audio",
            "total_required":1,
            "ordering":2,
            })
        
        self.assertFalse(competition_stage_requirement.is_valid_media_type())

        try:
            competition_stage_requirement.clean()
            self.assertFalse(True)
        except:
            self.assertTrue(True)

    def test_is_valid_competition_stage_requirement(self):
        """Is valid confirmation stage requirement"""
        # is valid CSR - not primary
        self.assertTrue(self.competition_stage_requirement.is_valid_competition_stage_requirement())

        # is not valid CSR - primary, 2 entries
        self.competition_stage_requirement.primary = True
        self.assertFalse(self.competition_stage_requirement.is_valid_competition_stage_requirement())
        # is valid CSR - primary, 1 entry
        self.competition_stage_requirement.total_required = 1
        self.assertTrue(self.competition_stage_requirement.is_valid_competition_stage_requirement())
        self.competition_stage_requirement.save()

        # is not valid CSR - 2 primaries
        competition_stage_requirement = CompetitionStageRequirement(**{
            "competition_stage":self.competition_stage,
            "name":"Audio requirement",
            "description":"Upload your second track!",
            "media_type":"audio",
            "total_required":1,
            "ordering":2,
            "primary":True
            })
        self.assertFalse(competition_stage_requirement.is_valid_competition_stage_requirement())

    def test_is_unique_primary_requirement(self):
        """Check if unique primary"""
        # is not a unique primary 
        self.assertFalse(self.competition_stage_requirement.is_unique_primary_requirement())

        # is a unique primary 
        self.competition_stage_requirement.primary = True
        self.assertTrue(self.competition_stage_requirement.is_unique_primary_requirement())
        self.competition_stage_requirement.save()

        # is not a unique primary
        competition_stage_requirement = CompetitionStageRequirement(**{
            "competition_stage":self.competition_stage,
            "name":"Audio requirement",
            "description":"Upload your second track!",
            "media_type":"audio",
            "total_required":1,
            "ordering":2,
            "primary":True
            })
        self.assertFalse(competition_stage_requirement.is_unique_primary_requirement())

    def test_has_unique_entry(self):
        """Check if only one entry"""
        # total required = 2
        self.assertFalse(self.competition_stage_requirement.has_unique_entry())

        # total required = 0
        self.competition_stage_requirement.total_required = 0
        self.assertFalse(self.competition_stage_requirement.has_unique_entry())

        # total required = 1
        self.competition_stage_requirement.total_required = 1
        self.assertTrue(self.competition_stage_requirement.has_unique_entry())


class CompetitionEntryTestCase(TestCase):
    """Return Competition Entry"""

    def setUp(self):
        user = User(**{
            "email": "admin@jbcole.co.uk",
            "username": "fame_admin",
            "password": "gjfkgjfk"
            })
        user.save()
        self.user = user

        competition = Competition(**{
                "name": "Test Competition",
                "slug": "test",
                "date_start": datetime(2015, 06, 25, 8, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 07, 31, 12, 0, 0, 0, pytz.UTC),
                "creator": user
            })
        competition.save()
        self.competition = competition

        self.competition_stage = CompetitionStage(**{
                "competition": competition,
                "name": "First Round",
                "description": "You must complete the round of destiny",
                "date_start": datetime(2015, 06, 25, 9, 0, 0, 0, pytz.UTC),
                "date_end": datetime(2015, 06, 26, 9, 0, 0, 0, pytz.UTC),
                "ordering": 1
            })
        self.competition_stage.save()
        self.competition_entry = CompetitionEntry(**{
                "competition":self.competition,
                "user":user,
                "name":"Competition Entry",
                "final_position":0,
                "final_points":0
            })

    def test_is_competition_creator(self):
        """Check is competition creator"""
        self.assertTrue(self.competition_entry.is_competition_creator())

        user = User(**{
            "email": "admin2@jbcole.co.uk",
            "username": "fame_admin_2",
            "password": "gjfkgjfk"
            })
        user.save()

        self.competition_entry.user = user
        self.assertFalse(self.competition_entry.is_competition_creator())

    def test_is_unique_entry(self):
        """Check is unique entry"""
        self.assertTrue(self.competition_entry.is_unique_entry())

        self.competition_entry.save()

        competition_entry = CompetitionEntry(**{
                "competition":self.competition,
                "user":self.user,
                "name":"Competition Entry",
                "final_position":0,
                "final_points":0
            })

        self.assertFalse(competition_entry.is_unique_entry())

        try:
            competition_entry.save()
            self.assertFalse(True)
        except:
            self.assertTrue(True)

    def test_can_create_entry(self):
        self.assertFalse(self.competition_entry.can_create_entry())

        self.competition_stage.date_start=timezone.now() - timedelta(days=1)
        self.competition_stage.date_end = timezone.now() + timedelta(days=1)
        self.assertFalse(self.competition_entry.can_create_entry())

        self.competition_stage.new_entries_open = True
        self.competition_stage.save()
        self.assertTrue(self.competition_entry.can_create_entry())

"""
Testing Competition Chart

Competition Chart is a dynamic function.

It stores all the relevant competition entries and helps keep their current scores up to date

It also handles knocking out competition entries and assigning them their final score
"""
class CompetitionChartTestCase(TestCase):
    def setUp(self):
        """Set up for chart requires:
            Users (5)
            Competition
            Competition Stages (1 start, 1 knockout and final)
            Competition Stage Requirements
            Competition Judges (2)
            Competition Entries (4)
            Competition Entry Likes (5)
            Competition Judge Ratings (2)
        """
        user1 = User(**{"email": "admin@jbcole.co.uk","username": "fame_admin1","password": "gjfkgjfk"})
        user1.save()
        user2 = User(**{"email": "admin@jbcole.co.uk","username": "fame_admin2","password": "gjfkgjfk"})
        user2.save()
        user3 = User(**{"email": "admin@jbcole.co.uk","username": "fame_admin3","password": "gjfkgjfk"})
        user3.save()
        user4 = User(**{"email": "admin@jbcole.co.uk","username": "fame_admin4","password": "gjfkgjfk"})
        user4.save()
        user5 = User(**{"email": "admin@jbcole.co.uk","username": "fame_admin5","password": "gjfkgjfk"})
        user5.save()
        user6 = User(**{"email": "admin@jbcole.co.uk","username": "fame_admin6","password": "gjfkgjfk"})
        user6.save()
        user7 = User(**{"email": "admin@jbcole.co.uk","username": "fame_admin7","password": "gjfkgjfk"})
        user7.save()
        self.user_list = [user1, user2, user3, user4, user5, user6, user7]

        current_date = timezone.now()
        competition = Competition(**{"name": "Test Competition","slug": "test","date_start": (current_date-timedelta(days=1)),"date_end": (current_date+timedelta(days=1)),"creator":user1})
        competition.save()
        self.competition = competition

        competition_stage1 = CompetitionStage(**{"competition": competition,"name": "First Round","description": "You must complete the round of destiny","date_start": (current_date-timedelta(days=1)),"date_end": (current_date+timedelta(minutes=1)),"ordering": 1})
        competition_stage1.save()
        competition_stage2 = CompetitionStage(**{"competition": competition,"name": "First Round","description": "You must complete the round of destiny","date_start": (current_date-timedelta(minutes=1)),"date_end": (current_date+timedelta(days=1)),"ordering": 1,"knockout_stage":True,"knockout_stage_limit":2,"final_stage":True})
        competition_stage2.save()
        self.competition_stages = [competition_stage1,competition_stage2]

        competition_stage_requirement = CompetitionStageRequirement(**{"competition_stage":competition_stage1,"name":"Audio requirement","description":"Upload your first track!","media_type":"audio","total_required":1,"ordering":1,"primary":True})
        competition_stage_requirement.save()
        self.competition_stage_requirements = [competition_stage_requirement]

        audio2 = Audio(**{"name":"This is track 1","user":user2})
        audio2.save()
        audio3 = Audio(**{"name":"This is track 1","user":user3})
        audio3.save()
        audio4 = Audio(**{"name":"This is track 1","user":user4})
        audio4.save()

        competition_entry2 = CompetitionEntry(**{"competition":self.competition,"user":user2,"name":"Competition Entry","final_position":0,"final_points":0,"active":True})
        competition_entry2.save()
        competition_entry3 = CompetitionEntry(**{"competition":self.competition,"user":user3,"name":"Competition Entry","final_position":0,"final_points":0,"active":True})
        competition_entry3.save()
        competition_entry4 = CompetitionEntry(**{"competition":self.competition,"user":user4,"name":"Competition Entry","final_position":0,"final_points":0,"active":True})
        competition_entry4.save()
        self.competition_entries = [competition_entry2,competition_entry3,competition_entry4]

        competition_entry_audio2 = CompetitionEntryAudio(**{"competition_entry":competition_entry2,"competition_stage_requirement":competition_stage_requirement,"entry":audio2})
        competition_entry_audio2.save()
        competition_entry_audio3 = CompetitionEntryAudio(**{"competition_entry":competition_entry3,"competition_stage_requirement":competition_stage_requirement,"entry":audio3})
        competition_entry_audio3.save()
        competition_entry_audio4 = CompetitionEntryAudio(**{"competition_entry":competition_entry4,"competition_stage_requirement":competition_stage_requirement,"entry":audio4})
        competition_entry_audio4.save()

        competition_judge1 = CompetitionJudge(**{"competition":competition,"judge":user6,"description":"Description","thumbnail_image":"","carousel_image":"","ordering":1})
        competition_judge1.save()
        competition_judge2 = CompetitionJudge(**{"competition":competition,"judge":user7,"description":"Description","thumbnail_image":"","carousel_image":"","ordering":2})
        competition_judge2.save()

        self.competition_judges = [competition_judge1, competition_judge2]

        self.competition_chart = CompetitionChart()

        self.assertTrue(self.competition_chart.create_chart(self.competition))

    def test_create_chart(self):
        self.assertTrue(self.competition_chart.create_chart(self.competition))

    def test_update_chart(self):
        competition_entry5 = CompetitionEntry(**{"competition":self.competition,"user":self.user_list[4],"name":"Competition Entry","final_position":0,"final_points":0,"active":True})
        competition_entry5.save()
        audio5 = Audio(**{"name":"This is track 1","user":self.user_list[4]})
        audio5.save()
        competition_entry_audio5 = CompetitionEntryAudio(**{"competition_entry":competition_entry5,"competition_stage_requirement":self.competition_stage_requirements[0],"entry":audio5})
        competition_entry_audio5.save()
        self.assertTrue(self.competition_chart.update_chart(self.competition))

    def test_knockout_entry(self):
        competition_chart_entry = CompetitionChart.objects.get(entry=self.competition_entries[0])
        self.assertTrue(self.competition_chart.knockout_entry(competition_chart_entry,4))

    def test_create_entry(self):
        competition_entry5 = CompetitionEntry(**{"competition":self.competition,"user":self.user_list[4],"name":"Competition Entry","final_position":0,"final_points":0,"active":True})
        competition_entry5.save()
        self.assertTrue(self.competition_chart.create_entry(competition_entry5))
        self.assertFalse(self.competition_chart.create_entry(self.competition_entries[0]))

    def test_update_entry(self):
        self.assertTrue(self.competition_chart.update_entry(CompetitionChart.objects.get(id=self.competition_entries[0].id)))

    def test_calculate_score(self):
        self.assertTrue(self.competition_chart.calculate_score(self.competition_entries[0]) < 1)

        rating = CompetitionEntryRating(**{"competition_entry":self.competition_entries[0],"judge":self.competition_judges[0],"rating":5})
        rating.save()

        self.assertEquals(self.competition_chart.calculate_score(self.competition_entries[0]), 2500)

        like = CompetitionEntryLike(**{"competition_entry":self.competition_entries[0],"fan":self.user_list[4]})
        like.save()

        self.assertEquals(self.competition_chart.calculate_score(self.competition_entries[0]), 2501)

    def test_display_ranking(self):
        self.assertTrue(len(self.competition_chart.display_ranking(self.competition)) == 3)

    def test_display_plays(self):
        self.assertTrue(len(self.competition_chart.display_plays(self.competition)) == 3)

    def test_display_most_recent(self):
        self.assertTrue(len(self.competition_chart.display_plays(self.competition)) == 3)

    def test_return_judges_score(self):
        self.assertTrue(self.competition_chart.return_judges_score(5,10) == 50)
        self.assertTrue(self.competition_chart.return_judges_score(5,500) == 2500)

    def test_knockout_entries(self):
        self.assertTrue(self.competition_chart.knockout_entries(self.competition,1))
        self.assertFalse(self.competition_chart.knockout_entries(self.competition,1))

    def test_close_competition(self):
        self.assertTrue(self.competition_chart.close_competition(self.competition))