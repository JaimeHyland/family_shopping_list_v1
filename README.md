![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

# Family Shopper
A bespoke shopping list management app developed especially for the Hyland family using Django and a variety of other technologies.

Code Institute - Fourth Milestone Project: Build a Full-Stack site based on the business logic used to control a centrally-owned dataset (in this case, the data used by the Hyland family to organise their household grocery shopping). Set up an authentication mechanism (for a superuser, an "adult" and a "child" role) and provide appropriate access to the site's data, and to alter that data, allowing each role to undertake activities appropriate to that role, based on the already existing dataset.

![The App as seen on a mobile screen](/assets/documentation/shopping_list_homepage.png)

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [The user story](#the-user-story)
- [System design](#system-design)
   * [Authentication](#authentication)
   * [Django apps](#django-apps)
      + [Project assessors/Outside users](#project-assessorsoutside-users)
   * [The database structure](#the-database-structure)
      + [Grouping and filtering products and shopping list items](#grouping-and-filtering-products-and-shopping-list-items)
      + [Users and user group permissions](#users-and-user-group-permissions)
- [The website's workflow:](#the-websites-workflow)
   * [Authentication](#authentication-1)
   * [Cancelling list items](#cancelling-list-items)
   * [Marking list items as bought](#marking-list-items-as-bought)
   * [App database updates for checkbox changes](#app-database-updates-for-checkbox-changes)
- [Design and coding philosophy and practice](#design-and-coding-philosophy-and-practice)
   * [Development, implementation and deployment environment](#development-implementation-and-deployment-environment)
   * [App robustness in code](#app-robustness-in-code)
- [Deployment to Heroku](#deployment-to-heroku)
   * [Initial registration](#initial-registration)
   * [Activating Code Institute's Heroku Student Pack](#activating-code-institutes-heroku-student-pack)
   * [Setting up my App in the Heroku environment](#setting-up-my-app-in-the-heroku-environment)
   * [Setting up Heroku for Daphne](#setting-up-heroku-for-daphne)
   * [Static file management](#static-file-management)
- [Running the app in the development environment](#running-the-app-in-the-development-environment)
- [Bug fixes, linting, testing and UX feedback](#bug-fixes-linting-testing-and-ux-feedback)
   * [Linting the Python](#linting-the-python)
   * [Linting the HTML, CSS and JavaScript](#linting-the-html-css-and-javascript)
   * [Linting config files.](#linting-config-files)
   * [Bugs and debugging](#bugs-and-debugging)
      + [Database debugging](#database-debugging)
      + [Debugging App logic](#debugging-app-logic)
   * [Features testing](#features-testing)
   * [Browser and device compatibility](#browser-and-device-compatibility)
   * [UX](#ux)
   * [Final testing and validation before submission](#final-testing-and-validation-before-submission)
- [Lessons learnt](#lessons-learnt)
   * [Time management](#time-management)
   * [Technical tools and technical issues resolved ](#technical-tools-and-technical-issues-resolved)
- [Unresolved technical issues](#unresolved-technical-issues)
   * [Issue with Chrome Developer Tools](#issue-with-chrome-developer-tools)
   * [The elephant in the room](#the-elephant-in-the-room)
- [Other design questions](#other-design-questions)
   * [Hard-coded data](#hard-coded-data)
   * [Help functions](#help-functions)
   * [Text resources for i10n and l10n](#text-resources-for-i10n-and-l10n)
- [Credits and sources](#credits-and-sources)
   * [Code resources](#code-resources)
   * [External technical and learning resources](#external-technical-and-learning-resources)
   * [Other credits](#other-credits)

<!-- TOC end -->

<!-- TOC --><a name="the-user-story"></a>
## The user story

The Hyland family is a four-headed monster that consumes a shocking lot of groceries (especially chocolate) every week. The main shopper in the family (the father of the household ... me) does his best but often finds it difficult to keep track of what's in stock and what's not.  The other three family members (the mother of the household, let's call her Jannett, and the two children, Lillian and Séamus) often tell him what from their point of view is missing and what new purchases might be appreciated.  They also occasionally (more than occasionally in Jannet's case) do a bit of shopping!

Since I'm currently learning full-stack programming with Code Institute and am required by my course to complete a Full-Stack Web application for my fourth portfolio project, I thought this requirement would provide a good opportunity to develop a basic prototype (or minimally viable product - MVP) of a shopping list app designed specifically for our family needs, for further development at a later date. The objective of this project is therefore to create just such a MVP.

We initially decided that the MVP should include the following features:
- All users, upon logging in, should see a list of the products currently entered into the system as needing buying, but have not yet been marked as bought (the shopping list).
- All users should be able to mark individual items on the shopping list as bought or cancelled.
- The adults (i.e. Jannett and myself) should be able to govern which products should be included in shopping lists and which sources (shops, supermarkets, etc.) should be included in the shopping management system.
- The children should eventually be able to suggest new products and sources to include in the system, subject to the approval of us two adults. (not yet implemented)
- It should be possible to add a description to each suggested and/or approved product. (only implemented in basic form)
- The children should eventually be able to add a description only to a suggested product and should be unable to edit an approved product. (not yet implemented)
- It should be possible to add only products already recorded in the Products model/table to the shopping list.
- Products should be divided into categories and default sources (e.g. shops) and the shopping list should eventually be filterable using those categories and defaults. (not yet fully implemented)
- Both adults and children should be able to cancel items from the shopping list amd to mark items as bought.
- There should be some mechanism to control which edits should take priority when more than one person at a time is editing the data. I have experimented (so far unsuccessfully) with Django.channels and WebSockets to implement a listening system that notifies users when another user has updated a field in any records they currently have loaded onto their UI. (this functionality is therefore also not yet implemented)
- There should be no mechanism for outsiders to register to use the app. The superuser should be the only person(s) able to add or delete a user from the app. This situation might change in the future, if other families become interested in using the app, but for the moment the MVP works fine with users being added and managed manually by the superuser.
- Anyone not logged in or stumbling on the site accidentally (or maliciously!!) should see a page asking them to log in. If they can't log in, then the simply don't get to see the shopping list (unless they can convince or blackmail the superuser &mdash; me).

<!-- TOC --><a name="system-design"></a>
## System design

Once we'd agreed the basic processes (see above), I began thinking about how to actually program the various functionalities the family needs in the short term.

My reasons for choosing a Django-based system on a Postgresql database at the back end, with some important appearances from Bootstrap on the front end, were basically twofold:
- Django offers a seamless way of creating a simple full-stack website quickly and corresponding to the family's needs and habits.
- The most obvious way of satisfying the requirements of my fourth portfolio project on my Code Institute Full-Stack Programming course was to use Django along with Bootstrap, among other technologies.
- With the time available to me I have made very limited use of bootstrap, and have hardly even begun to explore the possibilities of crispy forms and summernote.

<!-- TOC --><a name="authentication"></a>
### Authentication
I decided that, since the authentication needs of the app are fairly standard (though they do not include a user-managed registration system &ndash; see below), I would use Django-Allauth to handle authentication, with a number of small adjustments.

Chief among the adjustments I made to the standard Django-Allauth process is that I removed any registration process managed by prospective users themselves. Since the App is (for the moment at least) for the exclusive use of the Hyland family (and honorary members of the Hyland family), I decided that the App Boss (me) would handle any registration process manually using the Django Admin structure.

For the same reason, I do not use any references to e-mails for the moment.

Of course, if the App were further developed for use by other families for their own needs, I would clearly need to add a user-managed registration system again, and would almost certainly use a pretty much standard AllAuth process.

Even if the App never moves beyond the Hyland family circle, I may yet add in e-mail address data in the future that allows users to report issues and request changes from the App Boss. My partner and kids can always talk to me, but they might like to send me a note immediately while the issue is in their head. For the moment, though, I've parked that issue too.

<!-- TOC --><a name="django-apps"></a>
### Django apps
The family_shopping_list project contains only a single Django app: shopping_list, which effectively contains all the custom models and templates in the project. In hindsight, it may have been a better idea, and the code may have been easier to follow (including for me), if its various components had been divided into separate sub-apps.  This may be considered an opportunity for refactoring in future versions of the family shopping list!


<!-- TOC --><a name="project-assessorsoutside-users"></a>
#### Project assessors/Outside users
For anyone outside the family who needs or wishes to enter the App as a user (as part of their assessment of this project, for example), I will create an extra user for each user status that that person may need. I will then inform that person of the user name and password for each of the identities that they may wish or need to use to access the App's functionalities.

I'll ask them to change their password on first logging in as each user. In a future iteration I'll route new users automatically through the change password process upon first logging in!

I'm happy enough to use the original allauth change_password template for this purpose, except that I don't like the way the standard Django-allauth functionality appears to leave the user stranded on the password_change_done page when that user has changed their password. However, that's another issue I've parked for the moment due to lack of time.


<!-- TOC --><a name="the-database-structure"></a>
### The database structure

I decided that the most convenient and forward-looking way to implement the above requirements (and possible future requirements) at the back end was to base the system on essentially two main tables:
- a Product table, listing all the articles approved for inclusion in the shopping list;
- a ListItem table (the actual shopping list), in which a new record is created every time a new item is added to the shopping list by picking a product to be bought from the curated product table.

The other two tables (Category and Shop - see below) are (for the moment) designed exclusively to group the records in the Product and ListItem table to make it easier for the user to create the shopping list and to read and update the shopping list while out shopping.

This simple structure should allow the user to pick products out from a pre-existing product list and add them to the shopping list, change the quantity of the item required, add notes for shoppers, etc.. Some users (the adults) should be able to add, remove and modify product records on the product list, thus managing the sorts of thing that can end up on the shopping list. The process for ordinary users to remove product records is not yet fully implemented.

When a shopping list item is either bought or cancelled, it will stop appearing on the shopping list (for details, see below), but it will not be removed from the database. This is so that the Shopping List App will always contain a record of a purchase or cancellation, along with any notes a user enters into a shopping list record. This might in the future allow the App manager to see how many, say, blocks of white cheddar were bought in the previous month, for example. In the future too, such details as purchase price might be added as new fields to the model and can be used as a permanent record of purchases, with all the information one might require to assess costs and other details of the family's purchasing patterns.

It may even provide a logical basis upon which the first steps towards integrating electronic receipts into the App in a useful way.

So, what we have is one and only one ongoing and ever-changing shopping list, which has products added to and removed from it as they are bought or cancelled. It's worth repeating, however, that removal from the shopping list does not mean deletion from the ListItem table; a list item being marked as bought or cancelled merely changes the value in the appropriate boolean field, with the effect that the item will disappear from the list, but may still be accessed in future in other ways by users for a variety of purposes in the present or in the future (for details, see below).

It should be noted (and this applies to all models in the App's database) that even if a record is actually 'deleted' from the App, it is not ordinarily completely deleted from the database. What happens is that it loses its currency: that is to say, the flag 'current' in the database record, which is set by default to True is changed to False. All records whose boolean value 'current' is False are completely ignored by the App. Where they need to be restored for any reason, only the Superuser can do so using Django's Admin feature.

It is also possible for Superusers to delete records, but they shouldn't do so except in cases where there is absolutely no alternative.

<!-- TOC --><a name="grouping-and-filtering-products-and-shopping-list-items"></a>
#### Grouping and filtering products and shopping list items
The two other bespoke tables of the database are as follows:
- Shop
- Category

For the moment, the purpose of both these tables is simply to allow the user to appropriately filter results for the Product and List Item tables, depending on where they are and what category of shopping they want to buy.

They also have the potential to expand to provide more information to the family members in future iterations of the App, with new fields added.

![The basic design of the DB](/assets/documentation/shopping_list_database_schema.webp)

*The basic design of the bespoke tables in the database (some fields have been added to each table/model since this drawing was made) *

It should be noted that one or two changes have been made to the tables since this image was created, but the basic principle should remain pretty clear.

<!-- TOC --><a name="users-and-user-group-permissions"></a>
#### Users and user group permissions
There are also two important tables generic to Django:
- User
- Group

The purpose of the first of these from our point of view is to manage users and maintain security (so that nobody but family members can access the website), the second (again, from our point of view) is simply to maintain the functional distinction between an adult user and a child.  Adult users, even if they're not Superusers, are allowed to add products to and remove them from the product list, as well as being able to add and remove shops and product categories.

Child users are allowed only to add products to the shopping list and to buy and cancel items already on the shopping list. In a future iteration it might be a good idea to allow children to request that products to the product list and of shops and categories from their respective tables.

While child users can't access many of the pages of the site via the menus, and while some pages display differently depending on the user group of the current user, with some buttons enabled or disabled as appropriate and with some data made read-only or editable as appropriate, in some cases, children can use the browser's url bar to access some of the pages not accessible from the menus or buttons. This is an issue for resolution in a future iteration.


<!-- TOC --><a name="the-websites-workflow"></a>
## The website's workflow:

<!-- TOC --><a name="authentication-1"></a>
### Authentication
The first thing a new user sees on navigating to the website is a login page. Nobody can get any further without logging in. Users can set the App to remember them (i.e. not to require a new log-in when a new instance of the App is started up on the same device). Once logged in, any user in either group should be able to see the full current shopping list in order of entry (oldest first). If they're using a modern browser, they should be able to adjust the settings to log them in automatically on second and subsequent visits.

<!-- TOC --><a name="cancelling-list-items"></a>
### Cancelling list items
Each item on the shopping list will have two checkboxes; one on the left and the other on the right. The left-hand one will have the effect of cancelling the item from the list after the user clicks a confirmation message. This will be visually marked by displaying the item in a paler colour (removing the bold style of the text) and disabling the "bought" checkbox. The cancellation can be undone by clicking or tapping the same checkbox once more and confirming your change of mind.

The database is updated as soon as the user confirms the change via the confimation message (in the form of a modular webpage). Undoing the cancellation will update the database again.

When the user reloads the page or presses the __Refresh shopping list button__ at the bottom of the list the page's the cancelled item will disappear from the list.

<!-- TOC --><a name="marking-list-items-as-bought"></a>
### Marking list items as bought
The right-hand checkbox marks its associated list item as having been bought. In this case, to facilitate the user's shopping efficiency, no confirmation message is required. The item text is displayed as bought by striking it through with a semi-transparent grey line, as if it had been marked off using a blunt pencil. If the checkbox is checked by accident, it can be unchecked again by tapping on the checkbox again. I am considering adding a modal message in a later iteration that briefly appears to show the user that their purchase has been registered as bought in the database (not yet implemented).

<!-- TOC --><a name="app-database-updates-for-checkbox-changes"></a>
### App database updates for checkbox changes
Changes to the checkboxes are written directly and immediately to the database. I intend to complete a notification system using Django Channels and WebSockets to ensure that users are informed when someone else has updated data currently on their screen, to minimise the risk of data becoming inconsistent due to parallel usage of the app.
They should also see several buttons:
- a button inviting the user to add an item to the shopping list
- a button inviting the user to filter/or group shopping list items either by category or by shop (not yet implemented)
- a button inviting the user refresh the view, so that newly cancelled and bought items no longer appear in any form on the list (refreshing the page using the browser will have the same effect). 

When a user checks the *Cancel item* checkbox, the text for the item is shown in a paler grey and the *Item bought* checkbox is disabled.
When anyone checks the *Item bought* checkbox, the text for the item is shown in strikethrough font (with the strikethrough line shown in a semi-transparent dark gray) and the *Cancel item* checkbox is disabled. 

Clicking on any item text will bring the user to an *Item details* screen, where they can see further details on that Item. Adults should be able to edit these details. (This has not yet been correctly implemented.)


<!-- TOC --><a name="design-and-coding-philosophy-and-practice"></a>
## Design and coding philosophy and practice

<!-- TOC --><a name="development-implementation-and-deployment-environment"></a>
### Development, implementation and deployment environment
All the code created during this project was written using gitpod.io as my IDE, with version control using Git, storing (almost!) all code on a Github repository.

The resulting App was deployed to a Heroku environment following an early deploy approach (the App was deployed at an early stage of development in order to see progress early in the development cycle and to avoid last-minute deployment surprises). After initial deployment, the app code was pushed to the Heroku production environment on every commit, with all testing done on the development environment for that commit repeated on the production environment.

It was very early in the in the development process whein I moved my Apps very primitive initial data from an initial SQLite database to the PostgreSQL database that the App is now using. The database used by the development environment and in deployment are identical, and have been since almost the very beginning of the project. I did not have to make any data dump from SQLite to PostgreSQL.

The Debug setting was not hard set to No, but was instead handled by an environment variable (set to 'True' in the development environment via an env.py file and 'False' in production via a Heroku Config Var).  However, on the advice of my mentor, I have hardcoded the DEBUG value to False in version frozen for assessment.

<!-- TOC --><a name="app-robustness-in-code"></a>
### App robustness in code
Aside from the usual error handling in the code; using *try, except, [finally]* structures, for example, perhaps the main protection against unhandled errors is the practice of strictly circumscribing what the user is allowed to do by the App. The vast majority of functions are limited to choices from a closed list or choosing boolean values via checkboxes, etc.. The main defence against any possible malicious use of the App is simply not allowing anyone but close family members (A further reassurance is that none of the family members are currently capable of mounting code injection attacks, or any other potential malicious attack on the App or its underlying database).


<!-- TOC --><a name="deployment-to-heroku"></a>
## Deployment to Heroku

<!-- TOC --><a name="initial-registration"></a>
### Initial registration

My first step to facilitate deploying my App on the Heroku Python environment was to add my app's dependencies into my requirements.txt file (which the Heroku environment refers to when installing the necessary features on creation). I do this by running `` pip3 freeze > requirements.txt``, which collects all necessary installations on the Gitpod workspace and writes them into the requirements.txt file.

A also had to add the Heroku host url to my list of allowed hosts in my settings.py file.

```
ALLOWED_HOSTS = [
    ...
    'localhost',
    '8000-jaimehyland-familyshopp-qmoq4b3wyki.ws.codeinstitute-ide.net', # host in the development environment
    'family-shopping-list-v1-bafe564ca613.herokuapp.com',                # host in the deployed environment
    ...
]
```

The next step for someone completely new to Heroku would have been to create an account with Heroku at heroku.com, clicking on "Sign up for free" and filling out the sign-up form (using a genuine email address and with Role as Student and country as the country in which I currently live), and then clicking "Create free account". One would then need to confirm via the validation email sent by Heroku, set a password and log in, accepting Heroku's terms of service.  Heroku requires a real 16-digit credit or debit card for all its accounts and requires users to implement a minimum two-step validation process to use its hosting services. One then has to choose a form of validation. I originally chose a process in which a code number is sent to my smartphone every time I log in log-in via Salesforce's Authenticator app.

<!-- TOC --><a name="activating-code-institutes-heroku-student-pack"></a>
### Activating Code Institute's Heroku Student Pack

Once one's Heroku account is successfully set up, Code Institute students would need to navigate to www.heroku.com/github-students, click on the "Get the student offer" option, verify their status as a Github student and then click "Authorize heroku". One would then have to verify the previoiusly entered billing information, confirm the credit card details and then enter one's first and last names, setting "Code Institute" as the school name, and pressing "Send". On the dialog that would then open, one needs to indicate agreement with the Heroku Terms and Conditions by pressing "Agree". With that, registration as a Code Institute student would be complete and after a short interval, the sum of credits agreed between Code Institute and Heroku for Full-Stack Programming students will be added to one's Platform credits.

To get the hours of server time I need from Heroku, I needed to activate Eco dynos to allow all my apps to work. To set up the service, I went into the billing tab of on my dashboard and clicked on "Subscribe to Eco". After browsing through the information on the page, I clicked on Subscribe and confirmed that my subscription was now in existence- I then exited Heroku.

Rather nicely, these Eco Dynos are designed go to sleep after a period of inactivity, so that I don't have to pay for server time that I'm not using.


<!-- TOC --><a name="setting-up-my-app-in-the-heroku-environment"></a>
### Setting up my App in the Heroku environment

As this was not the first time I have used Heroku using the Student offer organised by Code Institute, I didn't have to go through the above complex rigmarole again. I simply logged into my personal Heroku dashboard using the above-described two-factor authentication process and created a new Heroku project using the "New" button on that dashboard, gave it the app name "family-shopping-list-v1", chose "Europe" as its region and then pressed "Create App". I then clicked on the "Settings" tab on the app page and clicked on "Reveal Config Vars". From there I created five configuration variables (Config Vars):
- CLOUDINARY_URL: the URL of the cloudinary environment from where Heroku will obtain the static files used by the deployed app, if there are any
- DATABASE_URL: where my postgres database makes its home
- DEBUG: set at 0 to prevent public access to detailed debugging information, which might allow hackers to reverse engineer my code for nefarious purposes. This functionality is buggy and is not used in the final project
- SECRET_KEY: this key is required in order to protect a number of security-critical Django processes, including, but not limited to the generation of CSRF tokens
- DISABLE_COLLECTSTATIC: initially set to 1, later changed to 0

For the purposes of the assessment project, the DEBUG value may be considered irrelevant, as the Django DEBUG value is hard-coded False. However, the ongoing project will use the Heroku DEBUG config var in future development. The detailed reasons for this approach are given below.

Three of these configuration variables have an equivalent in the env.py file in my development environment: 
- DATABASE_URL
- DEBUG 
- SECRET_KEY

The values of DATABASE_URL and SECRET_KEY in the env.py file are identical to their equivalents in the Heroku config vars. However, the DEBUG variable is set to 'True' in env.py so that I as the developer can see a detailed description of errors in my code while working. For reasons of security, the file is excluded from Git version management, and therefore does not get written to the deployed environment, as it is designed for use only in development. A simply piece of code in the settings.py file  should ensure that the deployed app searches Heroko's Config Vars rather than looking for the absent env.py file:
```
if os.path.isfile('env.py'):
    import env
[...]
DEBUG = os.environ.get('DEBUG')
```

This approach should prevent me from having to remember to manually change True to False in my code every time I commit and deploy a new version of my app to Heroku, and thus obviates the danger of hackers using detailed error messages to analyse my code for nefarious purposes.

However, the code is not reading the Heroku config var correctly (an issue that I discovered very late in development due to a late and unexpected bug that crept into my code during linting), so to be sure that I'm conforming to the standards expected of us programmers by the project assessment criteria, I have replaced:

```
DEBUG = os.environ.get('DEBUG')
```

with

```
DEBUG = False
```

I hope to reinstate the conditional DEBUG logic in a later iteration of the project.

<!-- TOC --><a name="setting-up-heroku-for-daphne"></a>
### Setting up Heroku for Daphne

Instead of using gunicorn in the command to use the webserver, I have opted to use Django's Daphne toolset, which allows my program to run asynchronously using channel layers via the Channels add-on, also available within the Django toolset. Both packages are added to the list of INSTALLED_APPS in the settings file, and are naturally also listed in the requirements.txt file with the appropriate version numbers to ensure that they're installed correctly by Heroku in the deployed environment.

The instruction for Heroku deployment that I wrote in my Procfile (which tells the Heroku deployment process where to start) was the following:
```
web: daphne -b 0.0.0.0 -p $PORT family_shopping_list.asgi:application
```

I did not need to add any buildpacks for this project.

Once all the above-described steps were completed, I switched to the Deploy tab in the Heroku family-shopping-list-v1 app page, selected Github as the environment I wanted to deploy from (under "Deployment method") and pressed "Connect to Github". I then searched for and selected the family-shopping-list-v1 repository.

I chose the manual "Deploy branch" option and waited until the deployment was complete. When that was done, I clicked on the "Open app" button, which opened the family-shopping-list App in a new tab on the same browser. I could then run a smoke test to ensure that everything was working in the deployed environment in a similar way to my last committed version of the App in development.

I then chose to enable automatic deploy from the main branch of my repository. This causes the deployment steps that I have defined as described above to run automatically every time I push the changes committed in Git to Github, ensuring (unless a deployment error occurs) that the deployed environment always contains the latest version of my App.

<!-- TOC --><a name="static-file-management"></a>
### Static file management
All static files are stored in the deployment environment on cloudinary.

The cloudinary url is defined in CLOUDINARY_URL in the setting file.

Cloudinary also gets a mention in INSTALLED_APPS
```
INSTALLED_APPS = [
    ...
    'cloudinary',
    ...
    'cloudinary_storage',
    ...
]
```

Aside from these details, it was also necessary to make the following settings so that cloudinary delivers its files effectively:

```
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# For deployed project only
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Explicit reference to whitenoise recommended for Daphne-based apps.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MIMETYPES = {'.webmanifest': 'application/manifest', }

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

To ensure that static files are served efficiently in the deployed app from a single, well-defined subdirectory, I ran the following command to collect all static files into that directory:

```
python manage.py collectstatic
```

A variety of other settings needed to be made to make Daphne run in deployment. Please look at the settings.py file to see the details.

<!-- TOC --><a name="running-the-app-in-the-development-environment"></a>
## Running the app in the development environment

Using the more usual ``runserver``-based command (``python manage.py runserver``) that we were taught can lead to issues in the development version of the app.

It makes more sense to run the app appealing explicitly to Daphne on the development server:
```
daphne family_shopping_list.asgi:application
```

However, one issue that should be noted with this method of running the app is that it doesn't seem to check whether all migrations have been applied on startup, while the runserver-based command would give you a warning if you hadn't completed your migrations! For this reason, when using Daphne, it's particularly important to remember to migrate any changes in your models (or in Django's standard models) before deploying!


<!-- TOC --><a name="bug-fixes-linting-testing-and-ux-feedback"></a>
## Bug fixes, linting, testing and UX feedback

<!-- TOC --><a name="linting-the-python"></a>
### Linting the Python
All python code (aside from standard and/or boiler-plate code provided by Django and similar) has been linted and corrected using flake8. For development purposes, I altered flake8's ini settings (in the ``.flake8`` file in the project's root directory) to allow lines of up to 119 characters during development. For the purposes of this project, however, I temporarily set the maximum line length to 79, as required by the guidelines, and as advised by my mentor.

I saw fit to comment out several issues using the ``# noqa`` notation, mostly to do with lines slightly longer than 79 characters whose readability would have clearly disimproved rather than improved by the addition of a line break (these cases were mostly in the models.py and urls.py files), but also once for an unused import at the top of my stub tests.py file, which was not used in this iteration of the App's development cycle.

While I strongly believe that the limit of 79 characters per line is excessively restrictive for python code readability in these days of larger, higher-resolution screens that often make much longer lines perfectly readable, I would be happy to reduce the standard number of characters per line to 79 if a client requires, especially if payment for my coding were being calculated according to the number of lines coded!

<!-- TOC --><a name="linting-the-html-css-and-javascript"></a>
### Linting the HTML, CSS and JavaScript
I did the linting in my HTML code (and only my HTML code &ndash;not the code provided by Django, even if slightly altered by me&ndash as that could be checked visually) using djlint, which was very useful in finding orphan closing nodes, etc.. The small bit of configuration that I did can be seen in the .djlint file on the root directory.

I did no linting on my fairly modestly sized css files, as it was easy enough to check their formatting and layout manually.

Linting my JavaScript was a little more involved. I used ESLint, which required a good deal more configuration (and, among other complications, an update of GitPod's standard version of Node.js) to set up.

You can see the configuration file on the project's root directory: ``.eslint.config.mjs``. You can see how I configured it by taking a look at the contents of that file. I enforced a 79-character line length here too, and formatting based on a four-character tab (I can't decide whether that or the equally standard two-char tab is preferable).

I discovered a bug in the ESLint's default configuration: in one piece of code (``fetch .then .catch`` structure) the linter demanded one tab more than is appropriate on each line from the ``.then`` keyword until the end of the structure. I dealt with this issue with a baseball bat: I simply marked each affected line of code with an instruction for the linter to ignore them (``// eslint-disable-line``) &ndash;an ugly but exceptional solution.

<!-- TOC --><a name="linting-config-files"></a>
### Linting config files.
The only reason I had to include the lint configuration files in my github repo was to facilitate the assessors of this project. I would normally simply keep such files locally on my personal coding notes and exclude them from the commit process by naming them in the .gitignore file. Given the choice, I would also allow lines much longer than the standard 79-80. I consider 119-character lines perfectly readable on modern screens.


<!-- TOC --><a name="bugs-and-debugging"></a>
### Bugs and debugging
Bugs were fixed as they arose function-by-function during development as they arrived. A systematic iterative search for bugs followed by rounds of bugfixing activity has not been implemented. For this, as for all the other incomplete elements in this project, I can only apologise.

<!-- TOC --><a name="database-debugging"></a>
#### Database debugging
While developing this app, I intermittently had to make updates to the database models and migrate them to the database. I didn't encounter any serious difficulties in making such changes during this project, though I did once have to make some slightly more intricate adjustments to the already existing data in the ListItem model when adding a unique slug record for each ListItem record. The model update history can be seen in the github site within the ./shopping_list/migrations directory. The issue involving the unique slug on the ListItem model can be traced there in migrations #016, #019 and #020.

<!-- TOC --><a name="debugging-app-logic"></a>
#### Debugging App logic
There remains a  list of issues with the App that I have not had the time to deal with. Some of these issues relate to the App's integration with cached data, and a few may be simply holes relating to duplicate data, etc., though I have spent considerable time and effort removing the most obvious of these. I have tried to reflect as many of the remaining issues as possible in the Use Cases on my Kanban project for resolution in future iterations of the App.

<!-- TOC --><a name="features-testing"></a>
### Features testing
Of course I did ongoing testing of the still fairly limited features I have implemented in both the development and deployment environment as I went through each ticket on my Kanban board (which can be found at [github.com/users/JaimeHyland/projects/6](https://github.com/users/JaimeHyland/projects/6/views/1)). The App is not quite yet mature enough for it to make sense to subject it to a systematic final round of features testing.  It is very much approaching that stage, though.

<!-- TOC --><a name="browser-and-device-compatibility"></a>
### Browser and device compatibility
During ongoing development, I tested my work on the latest versions of Chrome and Edge, using developer tools in "inspect" mode at various resolutions (running a **smoke test** on before every commit at the very least) and intermittently running the App on the following physical devices:
- Samsung Galaxy A8 (360 x 740px effective size, running on the latest version of Chrome)
- ipod (768px x 1024px viewport size, running on the latest version of Safari)
- HP laptop (1920 x 1080px) and Dell second screen (1920 x 1200px) both running on latest versions of Chrome, Microsoft Edge and Firefox 

I have done no testing, nor do I plan to do any testing, on older Browser versions, nor on any other physical devices. 
So far, this App has proved responsive enough for use on all the Android and Apple mobile devices we possess in the family.

Owing to lack of time and resources, I was unable to do any testing on any legacy versions of these or on any other browsers or physical machines. Nor do I plan to make any such test in the future.

The main pages of the App are, and will continue to be, optimised for use via a mobile device (either a tablet or even more usually smartphone). UsI anticipate that only the Superuser will use the thing on a laptop or PC, and even then mostly for administrative tasks. 

<!-- TOC --><a name="ux"></a>
### UX
The App is now close to being mature enough for it to profit from user experience feedback from its four potential users (one of which being yours truly). It'll no doubt receive lots of informal UX feedback (whether I like it or not!) over the coming weeks and months.

While the detailed information available on each product and shopping list item suits the UX needs of the Hyland family, as the Superuser is highly motivated to maintain the system assiduously, if the App should ever be converted into App generally usable by other individuals and families, the presence of such an assiduous superuser can't be guaranteed. As a result it may be necessary to "re-inject more simplicity" into the App logic, perhaps giving people the choice of using it as a simple smartphone-based shared list, perhaps containing nothing more than a list of the items that need buying, with few background details other than one- or two-word product entries.

Injecting such simplicity as an option would require a good deal of thought, consultation, coding and testing.

There are also a number of issue in terms of UX that still need to be dealt with: for example, the workflow for changing one's password leaves the user in a cul de sac without obvious way of getting back to the home page without either browsing backwards using the browser back arrow or directly editing the change_password_done template's url. The change_password_done template clearly needs some customisation. This constitutes yet another opportunity for refactoring in the future.

Another issue with the UX is that users who like to use their browser's back and forward arrows will note that pages often do not change for two, three or sometimes even more clicks or taps, as product, shop and category pages all have functions that cause the page to reload, with each reload counting as a different instance of the page. This isn't a critical issue, but it might be worth keeping in mind for repair in the future.

The very central role of the app &ndash;its facility to add products to the list and mark them off as they are bought&ndash; still has one deceptively complex issue: it allows more than one instance of each object to be added to the list. The user are likely to interpret this as meaning that more than one standard unit of that product needsbuying, but it would be far clearer to users if there was only one item on the list with an instruction to buy two of them. This is something that sadly yet again has to be left to another iteration of development.

For the moment I'm going to assume that the facility for the shopper to be able to simply tick stuff off the list as it is bought is more important than an ability to count precisely how many units are needed. If I'm wrong, no doubt user feedback at the beta stage will put me back on the right track.

There is a lot of room to improve the UX. Among the chief areas to improve are the following:
-- Positioning the buttons more appropriately and uniformly
-- Allowing filtering and ordering of the shopping list depending on the shop the user is in or the category of purchase they are considering making
-- Making data entry easier and more consistent, especially through the use of modal dialogs
-- Improving the graphic signals to the user on the shopping list page
-- Giving the user a choice of display palettes, or even "skins"

<!-- TOC --><a name="final-testing-and-validation-before-submission"></a>
### Final testing and validation before submission

This iteration
- All all console.log and print statements designed to facilitate the ongoing debugging process were carefully removed from the site's root directory and all child directories (I have a strict policy of marking all such statements with the word 'DEBUG' in block capitals to make it easier to search and destroy at the end of each iteration).
- All internal links (from menus, buttons and the various list items) have been smoke-checked systematically.

See the text above for details of features and links that have not been fully implemented, especially features whose foundations can be seen in the current code.

The following will be done before submission of a later iteration of this project:
- The two steps taken in the present iteration will be repeated.
- Any external links that may be added will be tested (none were added in this iteration).
- A systematic test on each of the machines and at each of the effective resolutions listed above (in portrait and landscape mode where appropriate) for:
    - Obvious visual issues in relation to accessibility, responsiveness and functionality.
    - The correct functioning of the above-listed functions.
- A final smoke-test after deployment running the above tests on each of the above-described devices and resolutions.


<!-- TOC --><a name="lessons-learnt"></a>
## Lessons learnt

<!-- TOC --><a name="time-management"></a>
### Time management
When faced with the inevitable coding challenges presented to a fairly inexperienced coder, I could sometimes have managed my time a little better. I often spent too long on bugs without looking for human help. In addition, some of my decisions on pages and features to be included were over-ambitious.

<!-- TOC --><a name="technical-tools-and-technical-issues-resolved"></a>
### Technical tools and technical issues resolved 
Among many lessons I managed through blood, sweat and tears to learn from were the following:
- The use of the django shell (*'python3 manage.py shell'*) to run queries without altering the core code. 
- The use of pre-saved queries in a management/command/[command_file_name].py file (along with various issues attached to using such files, which took me quite some time to sort out!)
- The use of websockets via django's channels and daphne packages was one of the biggest challenges I faced in developing this app. I depended heavily on a [tutorial](https://channels.readthedocs.io/en/stable/tutorial/index.html) on how to make a simple messaging app using the two packages that I found in the django documentation. While I learnt a lot in working here, I have not yet managed to achieve what I wished with these asynchronous technologies in the current App. See next section.


<!-- TOC --><a name="unresolved-technical-issues"></a>
## Unresolved technical issues

<!-- TOC --><a name="issue-with-chrome-developer-tools"></a>
### Issue with Chrome Developer Tools
A strange error appeared for a period on the console in Chrome when Developer Tools is open. It only occurred on the deployed environment (in Heroku). Chrome appeared to cut the App off from the Internet when I do anything on the web page that involves any POST to the database. The relevant errors were as follows:
```
POST https://family-shopping-list-v1-bafe564ca613.herokuapp.com/ net::ERR_INTERNET_DISCONNECTED
```

```
Form submission error TypeError: Failed to fetch
    at submitForm ((index):536:5)
    at updateDatabase ((index):524:5)
    at toggleCancelUncancel ((index):501:13)
    at HTMLInputElement.onchange ((index):131:64)
```

When the error occurred, the App instance ceased to work, acting as if the device had suddenly lost its Internet connection. All other tabs on the affected Chrome instance continued working as normal. However, restarting using the Heroku _Open App_ button produced a new instance without problems.

The strangest thing of all about this error is that it only occurred when Chrome's Developer Tools window was open: it didn't occur when using Chrome with the Developer Tools window closed. Nor did it occur in Edge, with or without its developer tools window open!

It took significant time to realise that the root of the problem lay with the Chrome Develop Tools functionality. One lesson I learnt from this is not to assume immediately the issue is necessarily caused by a problem in my code, settings or configurations.

In any case the issue has since disappeared (I suspect the most recent Chrome update sorted it out).

<!-- TOC --><a name="the-elephant-in-the-room"></a>
### The elephant in the room
Aside from this, the major unresolved technical issue is my failure to create an effective notification system for multiple users using Django.channels and WebSockets. The result of this issue is that the deployed version of the App fails to update the shopping list page of other users working on the App in real time when a list item is bought, unbought, cancelled or uncancelled. It was for this functionality that I decided (overambitiously) to use websockets via Daphne and Channels. AS A RESULT OF THIS CONTINUING ISSUE, CLASHES IN DATA STATES MAY OCCUR WHEN TWO INSTANCES OF THE APP ARE USED AT THE SAME TIME. 

I will be working on achieving the goal of achieving onscreen realtime multi-user data updates on an ongoing basis.


<!-- TOC --><a name="other-design-questions"></a>
## Other design questions

<!-- TOC --><a name="hard-coded-data"></a>
### Hard-coded data
Some of the data used by the app is for reasons of simplicity hard-coded at the development stage. One example of such data is the list of shop types (TYPES_OF_SHOP) used by the program, which is hard-coded into the Models.py file. This list (and any other hard-coded data) may be integrated into an appropriate data table in a future iteration, depending on early user feedback.

<!-- TOC --><a name="help-functions"></a>
### Help functions
I have not, and do not intend in any scheduled future, to implement any particular systematic user Help functionality behind the App in addition to Django's generic help features. I will concentrate on ensuring that the UX is as seamless as possible and that all UIs in the App are as intuitive and simple as humanly possible. In any rare cases where it seems that some explanation may be necessary, I may provide the user with information via discreet modal displays. Apart from immediate aesthetic considerations, I'll have to give further thought to the positioning of buttons, the greater use of modal windows, etc. (see above).

<!-- TOC --><a name="text-resources-for-i10n-and-l10n"></a>
### Text resources for i10n and l10n
I do not anticipate any need to internationalise an App essentially designed for a single family. However, as I live in Germany, and many potential testers of my app will be far more comfortable using the German language, any practicable beta version will need to be localized for such users. When the time comes to take that step, I will leverage Django's built-in i18n and l10n capabilities in a later iteration of the App.

<!-- TOC --><a name="credits-and-sources"></a>
## Credits and sources

<!-- TOC --><a name="code-resources"></a>
### Code resources
All the code is my own, though some of it is adapted from, or at least inspired by, some of the educational and industry sites listed below. I have made extensive use of the code provided in the Code Institute's learning resources and of the Django, Bootstrap and other documentation. Future iterations of this project will be making even more use of such sources.

<!-- TOC --><a name="external-technical-and-learning-resources"></a>
### External technical and learning resources
Naturally enough, I have researched widely to find out how to implement a variety of features not explicitly included in Code Institute's learning materials, including several visits to the following sites:
- [w3schools.com](https://w3schools.com/)
- [stackoverflow.com](https://stackoverflow.com/)
- [freecodecamp.org](https://www.freecodecamp.org/)
- [codecademy.com](https://www.codecademy.com/)
- [w3docs.com](https://www.w3docs.com/)
- [discuss.python.org](https://discuss.python.org/)
- [digitalocean.com](https://www.digitalocean.com/)
- [programiz.com](https://www.programiz.com/python-programming)
- [digitalocean.com](https://www.digitalocean.com/community/tutorials/)
- [geeksforgeeks.org](https://www.geeksforgeeks.org/)
- [medium.com](https://medium.com/)
- [django channels](https://channels.readthedocs.io/en/latest/)
- [Python Software Foundation](https://pypi.org/)
- [djLint](https://www.djlint.com/)
- [ESLint](https://eslint.org/)

I used some code I found at [https://github.com/derlin/](https://derlin.github.io/bitdowntoc/) to generate this readme file's table of contents.

<!-- TOC --><a name="other-credits"></a>
### Other credits
I would still like to thank my fellow students for their helpful suggestions and support, and in particular to my Student Care facilitator, for their inspiration, encouragement and help in combatting my recurring impostor syndrome! But mainly for their patience.

My mentor, Oluwafemi Medale, deserves special praise and gratitude for jumping in at the last moment at very short notice to check over my project for obvious flaws.

Code Institute's excellent tutoring team also deserve a special mention for their help, which they have consistently given in an open, friendly, encouraging, knowledgeable and professional manner.

I also feel the need to thank you, my third (and final) project assessor, for your patience and understanding of both the complexity, overambition and imperfections of this project. And for your sheer effort in putting yourself through this project, and especially its over-long readme file.
