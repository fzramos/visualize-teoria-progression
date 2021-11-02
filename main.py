from scrape_training_results import training_scraper
from visualize_training_results import run_viz_app
from update_historical_stats import update_historical_stats

# Scrape Recent Excercise Statistics
new_stats_df = training_scraper()

# Combine recent stats with historical stats
update_historical_stats(new_stats_df)

# Visualize
run_viz_app()