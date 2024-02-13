{
   "date": "2024-02-11T12:03:10-05:00",
   "draft": false,
   "title": "Hello World",
   "tags" : [
      "website"
   ]
}

This is the first ever post for the third iteration of my personal website that now features blogging thanks to the excellent [Hugo](https://gohugo.io/) static site generator. In this post I want to explain my thoughts about what should go on the site, touch on some of the technologies used to build the site, and briefly discuss my thoughts on the look of the site.

## What should go on the website?

The software engineer/developer portfolio websites I have seen usually look similar to a resume, with sections such as "work experience", "education", "skills", etc. To me these types of websites violate the principle of DRY. If all of this information is in a resume, why repeat it on a website? Now the same text in two locations needs to be updated whenever something changes. Three locations if your Linkedin page functions as another copy of your resume. 

An argument might be made that the "work experience" section on a website adds value with extra details that can't fit on a resume. However, if it is true that recruiters barely read resumes as they are, I feel that reading the same information only wordier is not something that any recruiter will engage in. Which then raises the question, who are the extra details for? Maybe yourself if you like to keep a detailed work history to look back at and feel good about, but is the self-satisfaction of this detailed work history worth the time spent writing and maintaining it? I believe that there is value in being able to concisely highlight only the important points of a work experience on the limited space of a resume. I also think that the lack of details for an entry leaves room to elaborate in an interview, and that by omitting information, I can more easily direct the flow of converstaion and come up with answers to common questions related to that missing information.

I feel the same DRY argument is true for the "about" section often included in websites. Both Linkedin and Github include a location for this information, why duplicate it for a third time? 

Sections titled "skills" often have a proficiency progress bar. The progress bar section to me seems at worst confusing and at best uneccessary. What is the percentage based on? If someone lists that they are 80% skilled in Python, does that mean they know 80% of all there is to know of Python? In [Cracking the Coding Interview](https://www.crackingthecodinginterview.com/), Gayle Laakmann McDowell recommends that skill proficieny metrics, should be kept to simple categories such as 'Proficient' or 'Experienced'. However, once you scale down the proficiency categories to something simple, they can fit on a resume, and then the same DRY argument applies.

So if I want to eschew the traditional portfolio site as a resume extension, what should I put on my personal website? I decided to define some goals before starting, and came up with two:

1. Develop my own little corner of the web to store things that I find interesting for later use or reference.
2. Create a platform that I can use to refine my views on different technologies, develop my writing skills, and record events of significance in my career.

Goal number one is based on the concept of a [Digital Garden](https://www.technologyreview.com/2020/09/03/1007716/digital-gardens-let-you-cultivate-your-own-little-bit-of-the-internet/), as well as this [Hacker News post](https://www.marginalia.nu/log/19-website-discoverability-crisis/). The concept of a digital garden is not new, the idea is to eschew social media in favor of your own hand-curated blob of the internet. The Hacker news post discusses a small website discoverability crisis. The writer argues that the best way to shine a light on smaller websites is to keep a bookmark of hyperlinks to places that one finds interesting.

Goal number two is more self-explanatory. It is often said that teaching is the best way to learn. If I can write a post about a difficult problem I have solved, a new tech stack that I learned to use, or simply just something I learned on a given day, maybe I will better internalize that information for the future. Additionally, I have heard that by expressing goals outwardly, a person is more likely to follow through to the completion of their goals. I've mostly heard this in reference to fitness, but I imagine it applies to projects as well. If I start a long project, now I have a place to document regular updates on the status of the project.

Using these goals, I have developed this website with three different components. The first component is the home page with my name and position. This should give visitors a feel for what is present on the rest of the site. The home page also contains links underneath my name and position. My goal is for these links to act as a centralized repository for any of my other accounts I deem relevant. The current links are my Github, my Linkedin, and my Leetcode. The second component is what I am calling the directory. The directory is a collection of any sites I have found interesting, and a brief description of what they are, all organized by category. The third component is this blog. Each blog post can be associated with one or more tags, and by clicking on a tag in the post, a user can see all posts with that tag.

## How should the website be built?

Portfolio websites I have seen will often be built in React or some other JS framework/library if the developer specializes in frontend technologies. Although I consider myself more of an Embedded Systems and Backend developer, I thought it might be fun to learn a frontend framework. As a fan of Google technologies and Typescript, I originally considered using [Angular](https://angular.io/) as the framework to build this site on, integrated with some free CMS for blogging. After completing the Angular tutorial, I realized that Angular might be a bit overkill for what I needed, but I did walk away impressed by how easy an intuitive it felt to use a declarative framework.

After the Angular tutorial I took a step back and thought about what I really needed, how I could get from point A to point B in the least amount of time, with the least amount of effort, and finish with a product that required little maintenance and just worked. I didn't really need anything with fancy Javascript, my experience with basic HTML would work fine. I also didn't really want to use a fancy CMS with a seperate web page and login for blog posts, markdown would be plenty good.

I decided the first question I had to answer was cost. I didn't want to pay to host the site. I had previously used Github pages to host a free personal website, so I decided to use them again. Github pages uses the [Jekyll](https://jekyllrb.com/) static site generator as a default solution for generating static contenct and blog posts, which at first seemed like perfect solution to what I needed. After some more digging, I decided that I didn't really want to learn Ruby, and didn't really want to use a canned Jekyll theme. Jekyll led me to a list of static site generators, where I discovered Hugo. As a big fan of Golang, and having some previous experience with Golang HTML templates, I decided I would use Hugo.

Hugo offers themes just like Jekyll, but after digging around a bit I couldn't find anything that I fit with what I had in mind. I wanted to use [Tailwind CSS](https://tailwindcss.com/) after seeing some other portfolio sites designed with it, so I found [this excellent blog post](https://dev.to/divrhino/how-to-add-tailwindcss-to-your-hugo-site-5290) on how to integrate Tailwind CSS into Hugo and started laying things out. I used the Hugo [smol theme](https://github.com/colorchestra/smol) and the Hugo docs to get a handle on how to structure my templates and content in my Hugo site. Skip ahead a few hours of building templates and adding content, and add in a custom domain and [Github Actions pipeline](https://gohugo.io/hosting-and-deployment/hosting-on-github/), and ross.grattafiori.dev was up and running!

I did run into a small problem with the Hugo markdown rendering and Tailwind CSS, which I may make another post about. This was eventually remedied by a combination of [Hugo shortcodes](https://gohugo.io/content-management/shortcodes/) and customizing base elements with Tailwind CSS.

## What should the site look like?

In its current state, this site is minimalist. I went with white text on a black background as the default, mostly because I often find myself enabling the Dark Reader extension on my browser for websites with too much white background. At one point I tried to add a nice minimalistic nature photo to the home page, but this proved to be much more difficult than I had anticipated, and I decided that the photo did not add enough value to continue pursuing its implementation.

I tried to forgo text wherever possible in favor of icons to cut down on clutter and give the site a cleaner look. There is plenty of space in the navbar to add more icons should I want to add more pages.

That's pretty much it. The site is very basic and not much to look at. There is no fancy CSS or javascript, no in-browser game engines or hidden easter eggs, not even an RSS feed yet. As I mentioned in the second section above, my goal was to get a site up and running as quickly and painlessly as possible, which I feel I achieved albeit some slight hiccups. In the future I may add fanciness or not, but right now my theory is the content of the site is more important that the style of the site. In that vein, I intend to focus on improving the quality of my blog posts over the look and feel of the my site design.

## Closing notes

That's the end of my first blog post! I'm pretty excited that I now have a place to post my tech-related thoughts. Here's to hoping that this isn't also my last blog post.