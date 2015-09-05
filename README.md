#Ma3ana Kam

Ma3ana kam is a side project that I thought to implement to solve one of my own
problems and practive Django more.

##Idea
The idea behind this application is estimate the expense you'll expend in
certain period (week, 2 weeks, month, etc.) and add what you really expend during
this period. Application will give you simple report about your period at glance
specially period that match current date.
Ma3ana kam is your spending journal but with extra features:
    - List of periods: wher you can create multiple journals, for example:
            - Home Shopping Journal.
            - My Expense Journal.
            - Home Expense Jorunal.
    - Estimate period, this wil help you to get what is stiuation between
    estimated expenses against the real expenses.
    - Entries: this is the real spending, you'll have complete list with date
    and which period this expense belong to.

##Installation
Create your virtualenv and install the required packages.
####For MySQL
`pip install -r requirements_mysql.txt`
####For PostgreSQL
`pip install -r requirements_postres.txt`

##Run
1- Activate your virtualenv.
2- Go to project folder.
3- Run `python manage.py runserver
