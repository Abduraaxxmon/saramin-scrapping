import pandas as pd
import os
from Translation import translate_list
from Load_to_csv import *


def collect_into_dataframe(name_companies, job_titles, location_jobs, post_dates, skills, country, job):
    # Translate only the relevant lists
    print(len(name_companies), len(job_titles),len(skills), len(location_jobs))
    skills = skills[len(skills)-len(name_companies):]

    name_companies = translate_list(name_companies)
    job_titles = translate_list(job_titles)
    skills = translate_list(skills)
    location_jobs = translate_list(location_jobs)

    country_list = [country] * len(name_companies)
    job_title_from_list = [job] * len(name_companies)
    source = ["saramin.co.kr"] * len(name_companies)
    salary = ["N/A"] * len(name_companies)
    logo_urls = ["company Logo"] * len(name_companies)
    job_title_from_list = translate_list(job_title_from_list)

    print(len(name_companies), len(job_titles),len(skills), len(location_jobs))
    data = {
        "Posted_date": post_dates,
        "Job Title from List": job_title_from_list,
        "Job Title": job_titles,
        "Company": name_companies,
        "Company Logo URL": logo_urls,
        "Country": country_list,
        "Location": location_jobs,  # No translation needed for location
        "Skills": skills,  # Skills will be translated
        "Salary Info" : salary,
        "Source": source  # No translation needed for sources
    }

    df = pd.DataFrame(data)

    df['Job Title'] = df['Job Title'].apply(lambda x: x.replace(',', '') if isinstance(x, str) else x)


    create_skills_cross_join_csv(jobs_df=df) 

    list_of_Jobs_to_csv(df)



def create_skills_cross_join_csv(jobs_df):

    try:
        expanded_rows = []

        # Iterate over each job row
        for _, row in jobs_df.iterrows():
            skills_list = row['Skills'].split(', ')  # Split skills string into a list
            for skill in skills_list:
                expanded_row = {
                    "Posted_date": row["Posted_date"],
                    "Job Title": row["Job Title from List"],
                    "Country": row["Country"],
                    "Company": row["Company"],
                    "Skill": skill
                }
                expanded_rows.append(expanded_row)
        # print(expanded_rows)

        # Convert the expanded rows into a DataFrame
        expanded_df = pd.DataFrame(expanded_rows)
        expanded_skills_to_csv(expanded_df)
    except Exception as e:
        print(f"An error occurred during the skills cross-join process: {e}")