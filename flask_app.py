
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
#from processing import HN
from google.cloud import bigquery
import pandas as pd
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/SunValidus/mysite/My First Project-922625eb09a6.json"

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/",methods=["GET", "POST"])
#@app.route("/HackerNewsQuery",methods=["GET", "POST"])


def query_page():
        errors = ""
        if request.method == "POST":
            keyword = None


            keyword = request.form["keyword"]
            keyword= "%"+keyword+"%"


            if keyword is not None:
                result,result_table = HN(keyword)
                return '''
                    <html>
                        <body>
                            <p>The result is: </p>
                            <p>{result}</p>
                            <p>{result_table}</p>
                            <p><a href="/">Click here to search again</a>
                        </body>
                    </html>
                    '''.format(result=result,result_table=result_table)

        return '''
        <html>
            <body>
                <p>Enter your keyword:
                <form method="post" action=".">
                    <p><input name="keyword" /></p>
                    <p><input type="submit" value="To search" /></p>
                </form>
            </body>
        </html>
    '''


def HN(keyword):
    import os
    from google.cloud import bigquery
    import pandas as pd
    import json
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/SunValidus/mysite/My First Project-922625eb09a6.json"
    client = bigquery.Client()
    query = """
    SELECT
        title,url,text,DATE(timestamp) AS date
    FROM `bigquery-public-data.hacker_news.full`
    WHERE title LIKE @keyword
    ORDER BY title DESC
     ;

                         """

    params=[
        bigquery.ScalarQueryParameter('keyword', 'STRING', keyword)

    ]
    job_config=bigquery.QueryJobConfig()
    job_config.query_parameters=params
    query_job=client.query(query,job_config=job_config)
    results = query_job.result()
    articles=pd.DataFrame(columns=['title','URL','text','date'])
    for row in results:
        articles.loc[len(articles)]=row
    articles['date']=articles['date'].astype(str)
    Response=articles.to_json(orient='records')

    Response_table=articles.to_html() #display html table
    #Response = json.dumps(Response)
    #print(articles)
    return Response,Response_table

