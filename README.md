# Rise & Reflect

![]()

[Click here to view the live web application](LIVE LINK HERE)

### Hello and Welcome!

This is the documentation for our mental health website: Rise & Reflect, which forms part of the Hays & Super Connect 2023 annual Hackathon competition! Rise & Reflect is a revolutionary morning and evening routine website designed to enhance your mental wellbeing and awareness! With its user-friendly interface, Rise & Reflect guides you through personalized routines and tasks crafted by our team. While many may think that working on your morning routine first will kickstart your day, we believe that your evening routine is even more important. A calming, productive evening routine not only eases off a stressful day, it also influences how you start your morning the next day, which in turn affects the rest of the day. 

Use our app to create your ideal evening and morning routine, track your progress and most importantly, improve your overall mental wellbeing and productivity. Embrace a happier and healthier lifestyle as you nurture your mind and unlock your full potential. Start your journey to Rise & Reflect today!

Please use the table of contents below to navigate through all of the planning, features, deployment, testing and more!

## Table of Contents

1. [Project Development and Planning](#project-development-and-planning)
    - [Project Goals](#project-goals)
        - [Project Purpose](#project-purpose)
        - [Target Audience](#target-audience)
    - [Research](#research)
        - [Market Review](#market-review)
        - [Key Takeaways](#key-takeaways-from-market-review)
    - [User Stories](#user-stories)
    - [Design, Layout and Structure](#design-layout-and-structure)
        - [Wireframes](#wireframes)
        - [Structure and Layout](#structure-and-layout)
        - [Design and Colour](#design-and-colour)
        - [Font](#font)
2. [Technologies Used](#technologies-used)
    - [Languages](#languages)
    - [Frameworks](#frameworks)
    - [Tools](#tools)
3. [Features](#features)
    - [Whole Site](#whole-site)
        - [Favicon](#favicon)
        - [Footer](#footer)
    - [Welcome Section](#welcome-section)
    - [Quiz Section](#quiz-section)
        - [Progress Bar](#progress-bar)
        - [Questions and Options](#questions-and-options)
    - [Results Section](#results-section)
        - [Supervillian Personality Reveal](#supervillain-personality-reveal)
        - [Retake Quiz Button](#retake-quiz-button)
        - [Return Home Button](#return-home-button)
    - [Other Pages](#other-pages)
        - [404 page](#404-page)
    - [Future Features](#future-features)
4. [Testing](#testing)
    - [Automated Testing](#automated-testing)
        - [HTML Validator Testing](#html-validator-testing)
        - [CSS Validator Testing](#css-validator-testing)
        - [JS Validator Testing](#js-validator-testing)
        - [Accessibility](#accessibility)
        - [Performance](#performance)
    - [Manual Testing](#manual-testing)
        - [Responsiveness / Device Testing](#responsiveness-/-device-testing)
        - [Browser Compatibility](#browser-compatibility)
        - [Solved Bugs](#solved-bugs)
        - [Testing User Stories](#testing-user-stories)
5. [Deployment](#deployment)
6. [Credits](#credits)

## Project Development and Planning 

### Project Goals 

#### Project Purpose

Rise & Reflect was planned and developed using principles of User Experience (UX) design, which include the five planes of Strategy, Scope, Structure, Skeleton, and Surface. Using these principles, the aim was to create a fun, easy-to-use, responsive, and engaging website that allows users to create a productive, calming evening and morning routine to suit their mental health needs.

#### Target Audience

Despite this being built for a hackathon competition, Rise & Reflect was still treated as a real-world application for potential clients interested in improving their overall mental wellbeing, and creating a structured routine to improve other skills, like time management. 

Therefore, this website is designed for users of any background or age, but will most likely gain more interest from users interested in creating a routine or seeking to improve their mental health. The simplicity of the website makes it easy for adults, teenagers and even children to take, and retake, the quiz as many times as they want, and access the results each time. 

### Research 

#### Market Review 

Before designing the website, our team reviewed other mental health websites (see below), in order to get a feel of how they presented themselves, which content and features they offered, and the design choices they made in terms of colour palette. We also reviewed what appeared to work well for the user and what needed improvements (see Key Takeaways). 

[BetterHelp](https://www.betterhelp.com) | [Calm](https://www.calm.com) | [Headspace](https://www.headspace.com) | [The Mighty](https://themighty.com) | [Truity Big Five Personality Test](https://www.truity.com/test/big-five-personality-test)

#### Key Takeaways

- The website should be have lighter colors to create a calming environment for the user
- The Website should be clean, simple, and easy to navigate
- The sign up and login should be simple and easy
- The welcome page should not be too busy, as this will create the opposite effect on the user

### User Stories

As a first-time user, I would like to:
- Sign up quickly and easily
- Add and edit tasks for my evening and morning routine quickly and easily
- Navigate easily through the site

As a returning user, I would like to:
- Login quickly and easily
- View and edit my current evening or morning routine
- View my progress on the Profile page
- Navigate easily through the site
- Access an affordable platform that can help me deal with mental health stressors

These user stories gave our team a clear scope for the website and enabled us to stay on track with the project, preventing issues like scope creep at a later stage after the coding process. 

### Design, Layout and Structure 

#### Wireframes

We used [Balsamiq](https://balsamiq.com/) in the initial design phase, before the coding process. This enabled us to develop the website's structure, skeleton, layout and overall look and style. Our team created designs for desktop, tablet and mobile screens to ensure that responsiveness was at the forefront of the application from the beginning.

<details><summary>Screenshots</summary>

<img src="WEBSITE/rise_and_reflect/static/images/desktop_wireframes.png">

_Desktop Wireframes_

<img src="WEBSITE/rise_and_reflect/static/images/mobile_wireframes.png">

_Phone Wireframes_

</details>

#### Structure and Layout

The structure of this website was informed by the scope, principles of interactive design (IXD), as well as the user goals of the website. Keeping these important concepts in mind ensured that the website conformed to the user's expectations and needs. 

The main site is a simple, multi-page website with content displayed and hidden at different points in the quiz using Django. There are three main sections within the page which appear and disappear depending on where you are in the site. These are:

- Welcome, Sign Up and Sign In Area: 
    - A brief introduction to the site, which allows the user to sign up or login if they are a returning user.
- Routine Area: 
    - The main routine area, which allows users to Create, Read, Update and Delete tasks, using the CRUD functionality.
- Profile Page: 
    - The user can see a summary of their routines, as well as review their progress
    - The user can access their login information, and reset their password if necessary

#### Design and Colour

This site was designed for all screen sizes, and after conducting some research (using sites like [Adobe](https://xd.adobe.com/ideas/process/ui-design/what-is-mobile-first-design/)), it appears that most users use their mobile devices over desktop or iPad screens. 

- The design was influenced by calming colours like light purples, blues and greens which create a calming effect for the user. 
- The welcome page has images of people engaging in morning and evening routines.
- The same colours were used for all buttons and headings, to maintain consistency throughout the site. 

<details><summary>Screenshots</summary>

<img src="WEBSITE/rise_and_reflect/static/images/color_palette.png">

_Colour Palette for entire website_

</details>

#### Font

Our choice of font was Comfortaa. The light font style was used for all paragraphs and and the bold font was used for all headings and buttons. This font choice was imported from [Google Fonts](https://fonts.google.com/) and had a backup font of Cursive. We chose this font for my website because the cursive style contributed to the calming theme, whilst also providing a professional, legible finish.

## Technologies Used 

This website was developed using the frameworks of Django and Bootstrap 4, as well as some web tools for the initial planning. A list of those included in the project can be seen as follows: 

### Frameworks
- [Django](https://en.wikipedia.org/wiki/Django)
- [Bootstrap](https://en.wikipedia.org/wiki/Bootstrap)

### Languages 
- [HTML5](https://en.wikipedia.org/wiki/HTML5)
- [CSS3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
- [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
- [Python](https://en.wikipedia.org/wiki/Python)

### Tools 
- [Git](https://git-scm.com/)
    - Git was used for version control via GitPod, by using the terminal to Git and Push to GitHub.
- [GitHub](https://github.com/)
    - GitHub was used to store the project code after being created in GitPod/Git.
- [Gitpod](https://www.gitpod.io/)
    - Gitpod was used to create, edit and preview the project's code.
- [Balsamiq](https://balsamiq.com/)
     - Balsamiq was used to create wireframes during the initial design process.
- [Google Fonts](https://fonts.google.com/)
    - Google Fonts was used to select and import the fonts to the project (Libre Baskerville and Libre Baskerville Bold).
- [Font Awesome](https://fontawesome.com/)
    - Font Awesome was used to add icons to the site to help with UX and to add more character to the project visually.
- [Tiny PNG](https://tinypng.com/)
    - Used to further optimise the images for the site and reduce file size.
- [Adobe Illustrator](https://www.adobe.com/uk/products/illustrator.html) and [Adobe Color] (https://color.adobe.com/create/color-wheel)
    - These were used to create the colour pallette as well as ideas for the initial design.
- [Favicon.io](https://favicon.io/favicon-converter/)
    - Used to create and add the favicon to the browser tab.

## Features

### Whole Site

#### Favicon

We included a Favicon for the site using the an R&R graphic which had the same colours as the site's design. This helped to build the brand and continue the site design in the user's browser tab.

<details><summary>Screenshots</summary>

<img src="WEBSITE/rise_and_reflect/static/favicon/favicon-32x32.png">

_Favicon_

</details>

#### Footer 

- The footer contains links to relevant social media sites.
- The footer social icons have aria labels to improve accessibility.
- The footer social icons have a hover effect with a smooth colour transition.
- The footer is responsive on all screen sizes.

<details><summary>Screenshots</summary>

<img src="">

_Footer on Desktop_

<img src="">

_Footer on iPad_

<img src="">

_Footer on Phone_

<img src="">

_Hover effect on social links_

</details>

### Welcome Section

This section contains the following features:

- A brief introduction and information about the site, how it works and some persuasion for the user to sign up.
- A carousel with images pertaining to the mental wellness and routines.
- The layout is responsive on all devices, with margins widening on larger devices.
- Sign Up and Sign In button

<details><summary>Screenshots</summary>

<img src="">

_Welcome section on Desktop_

<img src="">

_Welcome section on iPad_

<img src="">

_Welcome section on Phone_

</details>

### User Log In Account and Sign Up Page

This gives the user the ability to create a secure account and log in so that they can re-access their data.

## Future Features 

We would like to add additional features to expand the site. This unfortunately fell out of the scope of this project, but would be useful to users in the future. 

### Mental Health Resources

We would like to add actual resources, such as meditation audios and videos, journal prompts and other things for the users to actually have access to on the site, after they have created their routine. 

## Testing

### Automated Testing

#### HTML Validator Testing 

We ran my HTML code for each page through the [W3C HTML Validator](https://validator.w3.org/). Thankfully, no errors were displayed. There were some minor warnings, due to the use of multiple h1 elements, but once this was resolved, the results came back clean. 

<details><summary>Screenshots</summary>

<img src="">

_HTML Validator Warnings_

<img src="">

_HTML Validator Result_

</details>

#### CSS Validator Testing

We ran the CSS code through the [W3C CSS Validator](https://jigsaw.w3.org/css-validator/). No errors were displayed.

#### JavaScript Validator Testing

We ran the JavaScript code through [Jshint validator](https://jshint.com/).

#### Accessibility

We tested accessibility of the website using Google Chrome Dev Tools Lighthouse, and the scores came out clean. We also ran the site through the [Wave Web Accessibility Evaulation Tool](https://wave.webaim.org/). No warnings or errors were shown. 

#### Performance

We tested the site's performance through Google Chrome Dev Tools Lighthouse. Thankfully, the performance, accessibility, SEO and best practices all produced good scores.

### Manual Testing

#### Browser Compatibility

The site was tested on the following browsers, with no browser-specific bugs detected. 

- Google Chrome
- Mozilla Firefox
- Apple Safari

#### Responsiveness/Device Testing

The website was tested on the following devices:
- HP Display 27-inch External Monitor
- Apple Macbook Pro 13-inch
- Galaxy S9+
- Apple iPhone 12 Pro
- Apple iPhone SE
- Apple iPad mini
- Apple iPad
- Galaxy Tablet
- Google Chrome Developer Tools - using responsive testing for all screen sizes

The website functioned as expected on all devices.

### Solved Bugs

## Deployment

### GitHub Pages

The site was deployed to GitHub pages. The steps to deploy are as follows: 
1. In the GitHub repository, navigate to the Settings tab.
2. From the left hand menu select 'Pages'.
3. From the source select Branch: main.
4. Click 'Save'.
5. A live link will be displayed when published successfully. 

The live link can be found here: [The Ultimate Supervillain Personality Quiz](https://pecheylauren02.github.io/mp2-supervillain-personality-quiz/)

### Forking the GitHub Repository

You can fork the repository by following these steps:
1. Go to the GitHub repository.
1. Click on Fork button in upper right hand corner.

### Cloning the GitHub Repository

You can clone the repository to use locally by following these steps:
1. Navigate to the GitHub Repository you want to clone.
2. Click on the code drop down button.
3. Click on HTTPS.
4. Copy the repository link to the clipboard.
5. Open your IDE of choice (git must be installed for the next steps).
6. Type git clone copied-git-url into the IDE terminal.

The project will now be cloned locally for you to use.

## Credits

### Design and Planning

- [Adobe Color](https://color.adobe.com/create/color-wheel) helped in developing the colour palette for the initial design phase of the website.

### Code

- [W3C Schools](https://www.w3schools.com/jsref/dom_obj_event.asp) helped in providing a list to all DOM elements and how to manipulate them.
- [StackOverflow](https://stackoverflow.com/) helped with offering solutions on how to debug css and javascript code for certain functions.
- [W3C Schools](https://www.w3schools.com/w3css/w3css_progressbar.asp) helped in initial structure and styling of progress bar.
- [JS Docs](https://jsdoc.app/about-getting-started.html) helped in naming the variables correctly in the javascript files.

### Images

All of the sites images were taken from [Pexels](https://www.pexels.com).

### Acknowledgements

#### Our Team members
- Sean Meade
- Paul Clarke
- Lauren Pechey
- Tomislav Dukez

