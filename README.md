
![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

# Family Shopper WIP
A bespoke shopping list management app developed using django and a variety of other technologies especially for the Hyland family.

Code Institute - Fourth Milestone Project: Build a Full-Stack site based on the business logic used to control a centrally-owned dataset (in this case, the data used by the Hyland family to organise their household grocery shopping). Set up an authentication mechanism (for one superuser, an "adult" and a "child" role) and provide appropriate access to the site's data, allowing each role to do activities appropriate to that role, based on the dataset.

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [The user story](#the-user-story)
- [System design](#system-design)
   * [The database structure](#the-database-structure)
- [The website's workflow:](#the-websites-workflow)
   * [Logging in](#logging-in)
   * [Cancelling list items](#cancelling-list-items)
   * [Buying list items](#buying-list-items)
   * [App database updates for checkbox changes](#app-database-updates-for-checkbox-changes)
- [Setup and preparation of the development and deployment environments](#setup-and-preparation-of-the-development-and-deployment-environments)
- [Design and coding philosophy and practice](#design-and-coding-philosophy-and-practice)
   * [App robustness](#app-robustness)
- [Bug fixes, linting, testing and UX](#bug-fixes-linting-testing-and-ux)
   * [Linting](#linting)
   * [Bugs and debugging](#bugs-and-debugging)
   * [Features testing](#features-testing)
   * [Browser and device compatibility](#browser-and-device-compatibility)
   * [UX](#ux)
   * [Final testing and validation before submission](#final-testing-and-validation-before-submission)
- [Lessons learnt](#lessons-learnt)
   * [Time management](#time-management)
- [Unresolved technical issues](#unresolved-technical-issues)
- [Other design questions](#other-design-questions)
   * [Help functions](#help-functions)
   * [Text resources for i10n and l10n](#text-resources-for-i10n-and-l10n)
- [Credits and sources](#credits-and-sources)
   * [Code resources](#code-resources)
   * [External technical and learning resources](#external-technical-and-learning-resources)
   * [Other credits](#other-credits)

<!-- TOC end -->

<!-- TOC --><a name="the-user-story"></a>
## The user story

The Hyland family is a four-headed monster that consumes a shocking lot of groceries (especially chocolate) every week. The main shopper in the family (the father of the household ... me) does his best but often finds it difficult to keep track of what's in stock and what's not.  The other three family members (the mother of the household, let's call her Jannett, and the two children, Lillian and Séamus) often tell him what from their point of view is missing and what new purchases might be appreciated.  They also occasionally(more than occasionally in Jannet's case) do a bit of shopping!

Since I'm currently learning full-stack programming with Code Institute and am required by my course to complete a Full-Stack Web application for my fourth portfolio project, I thought this requirement would provide a good opportunity to develop a basic prototype (or minimally viable product - MVP) of a shopping list app designed specifically for our family needs, for further development at a later date. The objective of this project is therefore to create just such a MVP. I recognise that I haven't even managed to get to that stage of development of the project, but hope to do so in a second round.

We decided that the MVP should include the following features:
- All users, upon logging in, should see a list of the products entered into the system as needing buying, but have not yet been marked as bought (the shopping list).
- All users should be able to mark individual items on the shopping list as bought or cancelled.
- The adults (i.e. Annett and myself) should be able to govern which products should be included in shopping lists and which sources (shops, supermarkets, etc.) should be allowed.
- The children should be able to suggest new products and sources to include in the system, subject to the approval of us two adults. (not yet implemented)
- It should be possible to add a description to each suggested and/or approved product. (only implemented for admin users in the admin pages)
- The children should be able to add a description only to a suggested product and should be unable to edit an approved product. (not yet implemented)
- It should be possible to add only approved products to the shopping list. (not yet implemented)
- Products should be divided into categories and default sources (e.g. shops and supermarkets) and the shopping list should be filterable using those categories and defaults. (not yet implemented)
- The children should not be able to cancel items from the shopping list but should be able to mark items as bought. The adults should be able to do both. (not yet implemented)
- There should be some mechanism to control which edits should take priority when more than one person at a time is editing the data. I have experimented (so far unsuccessfully) with Django.channels and WebSockets to implement a listening system that notifies users when another user has updated a field in any records they currently have loaded onto their UI. (not yet implemented)
- There should be no mechanism for outsiders to register to use the app. The superuser should the only person(s) able to add or delete a user from the app.
- Anyone not logged in or stumbling on the site accidentally (or maliciously!!) should see a page asking them to log in. If they can't log in, then the simply don't get to see the shopping list.

<!-- TOC --><a name="system-design"></a>
## System design
Some flow charts portraying a selection of important Hyland family shopping list workflows are yet to be provided.

I prepared a series of outline flow charts in consultation with Jannett on the basis of our family needs and habits. Once we'd agreed the basic processes, I began thinking about how to actually program the various functionalities the family needs in the short term.

My reasons for choosing a django-based system on a Postgresql database at the back end, with some important appearances from Bootstrap on the front end, were basically twofold:
- Django offers a seamless way of creating a simple full-stack website quickly and corresponding to the family's needs and habits.
- The most obvious way of satisfying the requirements of my fourth portfolio project on my Code Institute Full-Stack Programming course was to use Django along with Bootstrap, among other technologies.

### Authentication
I decided that, since the authentication needs of the app are fairly standard, I would use Django-Allauth to handle authentication, with a number of small adjustments.

Chief among the adjustments I made to the standard Django-Allauth process is that I removed any registration process managed by prospective users themselves. Since the App is (for the moment at least) for the exclusive use of the Hyland family (and honorary members of the Hyland family), I decided that the App Boss (me) would handle any registration process manually using the Django Admin structure.

For the same reason, I do not use any references to e-mails for the moment.

Of course, if the App were further developed for use by other families for their own needs, I would clearly need to add a user-managed registration system again, and would almost certainly use a pretty much standard AllAuth process.

Even if the App never moves beyond the Hyland family circle, I may yet add in e-mail address data in the future that allows users to report issues and request changes from the App Boss. My partner and kids can always talk to me, but they might like to send me a note immediately while the issue is in their head.

For the moment, though, I've parked that issue.


#### Project assessment/Outside users
For anyone outside the family who needs or wishes to enter the App as a user (as part of their assessment of this project, for example), I will create an extra user for each user status that that person may need. I will then inform that person of the user name and password for each of the identities that they may wish or need to use to access the App's functionalities.

I'll then ask them to change their password on first logging in as each user.

I'm happy enough to use the original allauth change_password template for this purpose, except that I don't like the way the standard Django-allauth functionality appears to leave the user stranded on the password_change_done page when that user has changed their password. However, that's another issue I've parked for the moment due to lack of time.


<!-- TOC --><a name="the-database-structure"></a>
### The database structure

I decided that the most convenient and forward-looking way to implement the above requirements (and possible future requirement) at the back end was to base the system on two main tables:
- a Product table, listing all the articles approved for inclusion in the shopping list
- a ListItem table (the actual shopping list), in which a new record is created every time a new item is added to the shopping list by picking a product to be bought

The other two tables (Category and Shop - see below) are designed exclusively (for the moment) to group the records in the Product and ListItem table to make it easier for the user to create the shopping list and to read and update the shopping list while out shopping.

This simple structure should allow the user to pick products out from a pre-existing product list and add them to the shopping list, change the quantity of the item required, add notes for shoppers, etc.. Some users (the adults) should be able to add, remove and modify product records on the product list, thus managing the sorts of thing that can end up on the shopping list.

When a shopping list item is either bought or cancelled, it will stop appearing on the shopping list (for details, see below), but it will not be removed from the database. This is so that the Shopping List App will always contain a record of a purchase or cancellation, along with any notes a user enters into a shopping list record. This might allow the App manager to see how many, say, blocks of white cheddar were bought in the previous month, for example. In the future too, such details as purchase price might be added as new fields to the model and can be used as a permanent record of purchases, with all the information one might require to assess costs and other details of the family's purchasing patterns.

It may even provide a first step to integrating electronic receipts into the list.

So, there is only one ongoing and ever-changing shopping list, that has products added to it and removed from it as they are bought or cancelled. Removal from the shopping list, however, does not mean deletion from the ListItem table; a list item being marked as bought or cancelled merely changes the value in the appropriate boolean field, with the effect that the item will disappear from the list (for details, see below).

It should be noted (and this applies to all models in the App Database) that even if a record is actually 'deleted' from the App, it is not ordinarily completely deleted from the database. What happens is that it loses its currency: that is to say, the flag 'current' in the database record, which is set by default to True is changed to False. All records whose boolean value 'current' is False are completely ignored by the App. Where they need to be restored for some reason or another, only the Superuser can do so using Django's Admin feature.

It is also possible for Superusers to delete records, but they shouldn't do so except in cases where there is absolutely no alternative.

#### Grouping and filtering products and shopping list items
The other bespoke tables of the database are as follows:
- Shop
- Category

For the moment, the purpose of both these tables is simply to allow the user to appropriately filter results for the Product and List Item tables, depending on where they are and what category of shopping they want to buy.

They also have the potential to expand to provide more information to the family members in future iterations of the App, with new fields added.

![The basic design of the DB](/assets/documentation/shopping_list_database_schema.webp)

*The basic design of the bespoke tables in the database (some fields have been added to each table/model since this drawing was made) *

#### Users and user group permissions
There are also two tables generic to Django:
- User
- Group

The purpose of the first of these from our point of view is to manage users and maintain security (so that nobody but family members can access the website), the second (again, from our point of view) is simply to maintain the functional distinction between an adult user and a child.  Adult users, even if they're not Superusers, are allowed to add products to and remove them from the product list, as well as being able to add and remove shops and product categories.

Child users are allowed only to add products to the shopping list and to buy and cancel items already on the shopping list. In a future iteration it might be a good idea to allow children to request that products to the product list and of shops and categories from their respective tables.


<!-- TOC --><a name="the-websites-workflow"></a>
## The website's workflow:

<!-- TOC --><a name="logging-in"></a>
### Authentication
The first thing a user sees on navigating to the website is an login page. Nobody can get any further without logging in. Users can set the App to remember them (i.e. not to require a new log-in when a new instance of the App is started up on the same device). Once logged in, any user in either group should be able to see the full current shopping list in order of entry (oldest first).

<!-- TOC --><a name="cancelling-list-items"></a>
### Cancelling list items
Each item on the shopping list will have two checkboxes; one on the left and the other on the right. The left-hand one will have the effect of cancelling the item from the list after the user clicks a confirmation message. This will be visually marked by displaying the item in a paler colour and disabling the "bought" checkbox. The cancellation can be undone by clicking or tapping the same checkbox again.

The database is updated as soon as the user confirms the change via the confimation message (a modular webpage). Undoing the cancellation will update the database again.

When the user reloads the page, the page's the cancelled item will disappear.

<!-- TOC --><a name="buying-list-items"></a>
### Marking list items as bought
The right-hand checkbox marks the corresponding list item as having been bought. In this case, to facilitate the user's shopping efficiency, no confirmation message is required. The item text is displayed as bought by striking it through with a semi-transparent line, as if it had been marked off using a blunt pencil. If the checkbox is checked by accident, it can be unchecked again in the usual way. I am considering adding a modal message in a later iteration that briefly appears to show the user that their purchase has been registered as bought in the database.

<!-- TOC --><a name="app-database-updates-for-checkbox-changes"></a>
### App database updates for checkbox changes
Changes to the checkboxes are written directly to the database. I am still considering completing a notification system using Django Channels and WebSockets to ensure that users are informed when someone else has updated data currently on their screen, to minimise the risk of data becoming inconsistent due to parallel usage of the app.  I may, however, decide that a simple routine using extra boolean fields in the relevant models as flags informing users of which user is looking at what data would be enough.


They should also see several buttons:
- a button inviting the user to add an item to the shopping list
- a button inviting the user to filter/or group shopping list items either by category or by shop
- a button inviting the user refresh the view, so that newly cancelled 

Unfortunately none of these buttons have yet been given any functionality.

There should be two checkboxes attached to each item on the shopping, though only one of them should be enabled for children:
- a *Cancel item* checkbox on the left, which should only be enabled for adults (this distinction has not yet been implemented)
- an *Item bought* checkbox on the right, which everyone should be able to check

When an adult checks the *Cancel item* checkbox, the text for the item is shown in a paler grey and the *Item bought* checkbox is disabled.
When anyone checks the *Item bought* checkbox, the text for the item is shown in strikethrough font (with the strikethrough line shown in dark gray; a bit like a blunt pencil) and the *Cancel item* checkbox is disabled. 

Clicking on any item text will bring the user to an *Item details* screen, where they can see further details on that Item. Adults can edit these details. (The distinction between Adults and Children has not yet been implemented.)

<!-- TOC --><a name="setup-and-preparation-of-the-development-and-deployment-environments"></a>
## Setup and preparation of the development and deployment environments

A later iteration of this project will include a detailed explanation of how I set up and configured both my development and deployment environments.

<!-- TOC --><a name="design-and-coding-philosophy-and-practice"></a>
## Design and coding philosophy and practice

<!-- TOC --><a name="app-robustness"></a>
### App robustness
Aside from the usual error handling in the code; using *try, except, [finally]* structures, for example, perhaps the main protection against unhandled errors is the practice of strictly circumscribing what the user is allowed to do by the App. The vast majority of functions are limited to choices from a closed list or choosing boolean values via checkboxes, etc.. The main defence against any possibble malicious use of the App is simply not allowing anyone but close family members (A further reassurance is that none of the family members are currently capable of mounting code injection attacks, or any other potential malicious attack on the App or its underlying database).

<!-- TOC --><a name="bug-fixes-linting-testing-and-ux"></a>
## Bug fixes, linting, testing and UX

<!-- TOC --><a name="linting"></a>
### Linting
Due to pressure of time (as a result of what was in hindsight an overambitious attempt to implement a notification system for multiple users through the use of Django.channels and WebSockets), I was unable to implement a linting solution for my html, css, javascript or python code. I intend in the next iteration to implement a system similar to the one explained in the Code Institute's walkthrough projects that form part of my learning materials.

<!-- TOC --><a name="bugs-and-debugging"></a>
### Bugs and debugging
Bugs were fixed as they arose function-by-function during development as they arrived. A systematic iterative search for bugs followed by rounds of bugfixing activity has not been implemented. For this, as for all the other incomplete elements in this project, I can only apologise.

#### Database debugging
While developing this app, I intermittently had to make updates to the database models and migrate them to the database. I didn't encounter any serious difficulties making such changes during this project.

<!-- TOC --><a name="features-testing"></a>
### Features testing
Of course I did ongoing testing of the limited features I have implemented in both the development and deployment environment as I went through each ticket on my Kanban board (which can be found at https://github.com/users/JaimeHyland/projects/3/views/1). The App is not yet mature enough for it to make sense to subject it to a final round of features testing.

<!-- TOC --><a name="browser-and-device-compatibility"></a>
### Browser and device compatibility
During ongoing development, I tested my work on the latest versions of Chrome and Edge, using developer tools in "inspect" mode at various resolutions (running a **smoke test** on before every commit at the very least) and intermittently running the App on the following physical devices:
- Samsung Galaxy A8 (360 x 740px effective size, running on the latest version of Chrome)
- ipod (768px x 1024px viewport size, running on the latest version of Safari)
- HP laptop (1920 x 1080px) and Dell second screen (1920 x 1200px) both running on latest versions of Chrome, Microsoft Edge and Firefox 

I have done no testing, nor do I plan to do any testing, on older Browser versions, nor on any other physical devices. 
So far, this App has proved responsive enough for use on all the  Android and Apple mobile devices we possess in the family.

Owing to lack of time and resources, I was unable to do any testing on any legacy versions of these or on any other browsers or physical machines. Nor do I plan to make any such test in the future.

<!-- TOC --><a name="ux"></a>
### UX
The App is not yet mature enough for it to require user experience feedback from its four potential users (one of which being yours truly). It'll receive lots of informal UX feedback (whether I like it or not!) once it achieves Beta status.

<!-- TOC --><a name="final-testing-and-validation-before-submission"></a>
### Final testing and validation before submission

All all console.log and print statements designed to facilitate the ongoing debugging process were carefully removed from the site's root directory and all child directories.

The following will be done before submission of a later iteration of this project:
- All internal and external links will be smoke-checked systematically.
- A systematic test on each of the machines and at each of the effective resolutions listed above (in portrait and landscape mode where appropriate) for:
    - Obvious visual issues in relation to accessibility, responsiveness and functionality.
    - The correct functioning of the above-listed functions.
    - The relevant _Code Institute_ assessment criteria for pass, merit and distinction (where not already covered in tests already completed).
- A final smoke-test after deployment running the above tests on each of the above-described devices and resolutions.
- All html pages and bespoke css code will be validate (see below).

<!-- TOC --><a name="lessons-learnt"></a>
## Lessons learnt

<!-- TOC --><a name="time-management"></a>
### Time management
When faced with the inevitable coding challenges of an inexperienced coder, I could sometimes have managed my time a little better. I often spent too long on bugs without looking for help. In addition, some of my decisions on pages and features to be included were over-ambitious.

### Technical tools and technical issues resolved 

Among many lessons I managed through blood, sweat and tears to learn from were the following:
- The use of the django shell (*'python3 manage.py shell'*) to run queries without altering the core code. 
- The use of pre-saved queries in a management/command/[command_file_name].py file (along with various issues attached to using it, which took me quite some time to sort out!)
- the use of websockets via django's channels and daphne packages was one of the biggest challenges I faced in developing this app. I depended heavily on a [tutorial](https://channels.readthedocs.io/en/stable/tutorial/index.html) on how to make a simple messaging app using the two packages that I found in the django documentation.

<!-- TOC --><a name="unresolved-technical-issues"></a>
## Unresolved technical issues
The major unresolved technical issue is my failure to create an effective notification system for multiple users using Django.channels and WebSockets. The result of this issue is that the deployed version of the App prints a number of WebSocket errors to the console. However, these errors do not affect the limited functionality that I have implemented in my App.

<!-- TOC --><a name="other-design-questions"></a>
## Other design questions

<!-- TOC --><a name="help-functions"></a>
### Help functions
I have not, and do not intend to implement any particular systematic Help infrastructure behind the App in addition to Django's generic help functionality.  I will concentrate on ensuring that all UIs in the App are as intuitive and simple as humanly possible. In any rare cases where it seems that some explanation may be necessary, I may provide the user with information via discreet modal displays.

<!-- TOC --><a name="text-resources-for-i10n-and-l10n"></a>
### Text resources for i10n and l10n
I do not anticipate any need to internationalise an App essentially designed for a single family. If I should decide in the future that such action is needed, I will leverage Django's built-in i18n and l10n capabilities in a later iteration of the App. 

<!-- TOC --><a name="credits-and-sources"></a>
## Credits and sources

<!-- TOC --><a name="code-resources"></a>
### Code resources
All the code is my own, though some of it is adapted from, or at least inspired by, some of the educational sites listed below. I have made extensive use of the code provided in the Code Institute's learning resources and of the Django documentation. Future iterations of this project will be making even more use of these two sources.

<!-- TOC --><a name="external-technical-and-learning-resources"></a>
### External technical and learning resources
Naturally enough, have researched widely to find out how to implement a variety of features not explicitly included in Code Institute's learning materials, including several visits to the following sites:
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

I used some code I found at [https://github.com/derlin/](https://derlin.github.io/bitdowntoc/) to generate this readme file's table of contents.

<!-- TOC --><a name="other-credits"></a>
### Other credits
While the current state of this project suggests that any credits for the work done would be premature. However, I would still like to thank my fellow students for their helpful suggestions and support, and in particular to my Student Welfare person, for their inspiration, encouragement and help in combatting impostor syndrome! But mainly for their patience.

Code Institute's excellent tutoring team also deserve a mention for their help so far, and for the help they'll surely be giving me in at least one future iteration of this project that I'm assuming will be necessary. Aside from my personal student care, I also have to thank the entire student care team for their flexibility ... and patience.

I also feel the need to thank you, the project assessor, also for your patience.
