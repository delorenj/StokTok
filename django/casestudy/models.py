"""
Django models for the casestudy service.

We have added the initial Security model for you with common fields for a
stock market security. Add any additional fields you need to this model to
complete the case study.

Once you have added a new field to the Security model or created any new
models you can run 'make migrations' to create the new Django migration files
and apply them to the database.

https://docs.djangoproject.com/en/4.2/topics/db/models/
"""

from django.contrib.auth.models import User
from django.db import models


class Security(models.Model):
    """
    Represents a Stock or ETF trading in the US stock market, i.e. Apple,
    Google, SPDR S&P 500 ETF Trust, etc.
    """

    # The security's name (e.g. Netflix Inc)
    name = models.CharField(max_length=255, null=False, blank=False)

    # The security's ticker (e.g. NFLX)
    ticker = models.CharField(max_length=20, null=False, blank=False, unique=True)

    # This field is used to store the last price of a security
    last_price = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=11,
    )

    currency = models.CharField(max_length=3, default='USD')
    exchange = models.CharField(max_length=50, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['ticker']),
        ]

"""
Represents a watchlist for a user.

Indexing decisions:
1. We create a unique constraint on 'user' and 'name' to ensure each user
   can only have one watchlist with a given name.
2. We add an index on the 'user' field to optimize queries that filter
   or join on the user, which is likely to be a common operation when
   retrieving a user's watchlists.
3. We don't index 'name' separately as it's already part of the unique
   constraint with 'user', which can be used as an index.
4. We don't index 'created_at' or 'updated_at' as they are less likely
   to be used in filtering or sorting operations frequently.
"""    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlists')
    name = models.CharField(max_length=100, default='Default')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ['user', 'name']
        indexes = [
            models.Index(fields=['user']),
        ]

"""
Represents an item in a watchlist.

Indexing decisions:
1. We create a unique constraint on 'watchlist' and 'security' to ensure
   each watchlist can only have one item for a given security.
2. We add an index on the 'watchlist' field to optimize queries that filter
   or join on the watchlist, which is likely to be a common operation when
   retrieving a watchlist's items.
3. We add an index on the 'security' field to optimize queries that filter
   or join on the security, which is likely to be a common operation when
   retrieving a watchlist's items.
"""
class WatchlistItem(models.Model):
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name='items')
    security = models.ForeignKey(Security, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['watchlist', 'security']
        indexes = [
            models.Index(fields=['watchlist']),
            models.Index(fields=['security']),
        ]