from django.db import models


class YearlyStats(models.Model):
    year = models.IntegerField(blank=True, null=True)  # Year of the stats
    rating = models.IntegerField(blank=True, null=True)  # Player's rating for that year
    games_played = models.IntegerField(blank=True, null=True)  # Number of games played
    snaps_played = models.IntegerField(blank=True, null=True)  # Number of snaps played

    player = models.ForeignKey('Player', related_name='yearly_stats', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.year} - Rating: {self.rating}"

class PositionChange(models.Model):
    old_position = models.CharField(max_length=10, blank=True, null=True)  # Position before the change
    new_position = models.CharField(max_length=10, blank=True, null=True)  # Position after the change
    rating_before = models.IntegerField(blank=True, null=True)  # Rating before the position change
    rating_after = models.IntegerField(blank=True, null=True)  # Rating after the position change
    year_of_change = models.IntegerField(blank=True, null=True)  # Year when the position change occurred

    player = models.ForeignKey('Player', related_name='position_changes', on_delete=models.CASCADE)

    def __str__(self):
        return f"From {self.old_position} to {self.new_position} in {self.year_of_change}"

class Award(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)  # Name of the award
    year_won = models.IntegerField(blank=True, null=True)  # Year the award was won

    player = models.ForeignKey('Player', related_name='awards', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.year_won}"

class Player(models.Model):
    POSITION_CHOICES = [
        ('QB', 'Quarterback'),
        ('HB', 'Halfback'),
        ('FB', 'Fullback'),
        ('WR', 'Wide Receiver'),
        ('TE', 'Tight End'),
        ('LT', 'Left Tackle'),
        ('LG', 'Left Guard'),
        ('C', 'Center'),
        ('RG', 'Right Guard'),
        ('RT', 'Right Tackle'),
        ('LE', 'Left End'),
        ('RE', 'Right End'),
        ('DT', 'Defensive Tackle'),
        ('LOLB', 'Left Outside Linebacker'),
        ('MLB', 'Middle Linebacker'),
        ('ROLB', 'Right Outside Linebacker'),
        ('CB', 'Cornerback'),
        ('FS', 'Free Safety'),
        ('SS', 'Strong Safety'),
        ('K', 'Kicker'),
        ('P', 'Punter')
    ]

    GEM_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Bust', 'Bust'),
        ('N/A', 'Not Available')
    ]

    name = models.CharField(max_length=100)  # Required field
    position = models.CharField(max_length=5, choices=POSITION_CHOICES, blank=True, null=True)
    redshirt_status = models.CharField(max_length=20, choices=[
        ('Eligible', 'Eligible'),
        ('Redshirted', 'Redshirted'),
        ('Not Eligible', 'Not Eligible')
    ], blank=True, null=True)
    current_year = models.CharField(max_length=10, choices=[
        ('Recruit', 'Recruit'),
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('RS FR', 'Redshirt Freshman'),
        ('RS SO', 'Redshirt Sophomore'),
        ('RS JR', 'Redshirt Junior'),
        ('RS SR', 'Redshirt Senior')
    ], blank=True, null=True)
    initial_rating = models.IntegerField(blank=True, null=True)
    current_rating = models.IntegerField(blank=True, null=True)
    archetype = models.CharField(max_length=50, blank=True, null=True)
    career_result = models.CharField(
        max_length=50, 
        choices=[
            ('Drafted Round 1', 'Drafted Round 1'),
            ('Drafted Round 2', 'Drafted Round 2'),
            ('Drafted Round 3', 'Drafted Round 3'),
            ('Drafted Round 4', 'Drafted Round 4'),
            ('Drafted Round 5', 'Drafted Round 5'),
            ('Drafted Round 6', 'Drafted Round 6'),
            ('Drafted Round 7', 'Drafted Round 7'),
            ('Undrafted', 'Undrafted'),
            ('Cut', 'Cut'),
            ('Transferred Out', 'Transferred Out')
        ],
        blank=True,
        null=True
    )

    # New fields for recruits
    hs_star_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)  # 1-5 star rating
    gem_status = models.CharField(max_length=10, choices=GEM_CHOICES, blank=True, null=True)
    national_rank = models.IntegerField(blank=True, null=True)  # National ranking
    position_rank = models.IntegerField(blank=True, null=True)  # Positional ranking
    recruit_class_year = models.IntegerField(blank=True, null=True)  # Recruiting class year

    @property
    def rating_difference(self):
        """Calculate the overall rating difference automatically."""
        return self.current_rating - self.initial_rating if self.current_rating and self.initial_rating else None

    def save(self, *args, **kwargs):
        # Save the Player instance first to ensure it has a primary key
        super().save(*args, **kwargs)
        
        # Now it's safe to access related objects
        if self.yearly_stats.exists():
            self.current_rating = self.yearly_stats.order_by('-year').first().rating
        
        # Save again to update the current_rating if needed
        super().save(*args, **kwargs)

    def add_award(self, award_name, year_won):
        """Add an award if the player's position is eligible for it."""
        # Award eligibility logic can go here
        Award.objects.create(player=self, name=award_name, year_won=year_won)

    def __str__(self):
        return self.name
