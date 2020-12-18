import copy

LOOK_UP_TABLE = {}

COLUMN_INPUTS = ['region', 'season', 'target_group', 'vertical']

LOOK_UP_TABLE['region'] = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']

LOOK_UP_TABLE['season'] = ['Winter', 'Spring', 'Summer', 'Autumn']

LOOK_UP_TABLE['vertical'] = ['Arts & Entertainment & Books & Literature', 'Autos', 'Beauty', 'Fitness & Health', 'Business & Finance', 'Computers & Technology', 'Education', 'Fashion', 'Food & Drinks', 'Games',
                                 'Home & Garden', 'Parenting & Family', 'Pets & Animals', 'Real Estate', 'Uncategorized', 'Shopping', 'Sports', 'Travel', 'Law & Government Local News', 'People', 'Society & Online Communities', 'Energy']

LOOK_UP_TABLE['campaign_objective'] = ['engagement_rate', 'click_through_rate']

COLUMN_OUTPUTS = ['campaign_objective']
