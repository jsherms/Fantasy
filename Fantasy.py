import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Read the CSV files
espn = pd.read_csv('ESPN_ranks.csv')
cbs = pd.read_csv('CBS_Ranks.csv')
nbc = pd.read_csv('NBC_Ranks.csv')

# Rename the columns
espn = espn.rename(columns={'Rank': 'Rank_ESPN'})
cbs = cbs.rename(columns={'Rank': 'Rank_CBS'})
nbc = nbc.rename(columns={'Rank': 'Rank_NBC'})

# Merge the dataframes
two = pd.merge(espn, cbs, on=['Player', 'Position'])
merged = pd.merge(two, nbc, on=['Player', 'Position'])

# Calculate the average rank
merged['Average_Rank'] = merged[['Rank_ESPN', 'Rank_CBS', 'Rank_NBC']].mean(axis=1).round(2)
merged = merged.drop(columns=['Team_x'])
merged = merged[['Average_Rank', 'Player', 'Position', 'Team_y', 'Rank_ESPN', 'Rank_CBS', 'Rank_NBC']]
merged = merged.rename(columns={'Team_y': 'Team'})
merged = merged.sort_values(by='Average_Rank')


@app.route('/', methods=['GET', 'POST'])
def index():
    position = 'ALL'
    if request.method == 'POST':
        position = request.form.get('position')
        if position == 'ALL':
            data = merged
        elif position == 'FLEX':
             data = merged[merged['Position'].isin(['RB', 'WR', 'TE'])]
        else:
            data = merged[merged['Position'] == position]
    else:
        data = merged
    
    return render_template('index.html', data=data.to_dict(orient='records'), position=position)


if __name__ == "__main__":
    app.run(debug=True)